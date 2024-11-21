from django.core.management.base import BaseCommand
from django.utils import timezone
from TrackIt_app.models import Document, UnactedLogs, User, ActivityLogs
from datetime import timedelta, date, datetime

class Command(BaseCommand):
    help = 'Mark documents as unacted and log them in activity logs'

    def handle(self, *args, **kwargs):
        now = timezone.localtime().date()  # Get the current date

        # Fetch all documents that are not 'For Archiving' and are past the deadline
        documents = Document.objects.filter(
            status__in=['For DIR Approval', 'For Routing', 'For SRO Receiving', 'For ACT Receiving', 'For Resolving'],
            ongoing_deadline__lt=now
        )

        if not documents:
            print('No documents found')
            return

        # Loop through the documents and check if they are unacted
        for document in documents:

            ongoing_deadline = document.ongoing_deadline
            # get the owner of the document
            if document.status == 'For DIR Approval':
                user = User.objects.get(role='Director')
                if not user:
                    print('No user found')
                    return
            elif document.status == 'For Routing':
                user = User.objects.get(role='ADO', status='active')
                if not user:
                    print('No user found')
                    return
            elif document.status == 'For SRO Receiving':
                receiving_office = document.next_route
                user = User.objects.get(office_id_id=receiving_office, role='SRO', status='active')
                if not user:
                    print('No user found')
                    return
            elif document.status == 'For ACT Receiving':
                user = User.objects.get(user_id=document.act_receiver, status='active')
                if not user:
                    print('No user found')
                    return
                pass_unacted_document(document, user)
            elif document.status == 'For Resolving':
                receiving_office = document.next_route
                user = User.objects.get(office_id_id=receiving_office, role='SRO', status='active')
                if not user:
                    print('No user found')
                    return
            
            unacted_log = UnactedLogs.objects.filter(
                user_id = user,
                status = document.status,
                document_id = document
            ).exists()

            if not unacted_log:
                UnactedLogs.objects.create(
                    time_stamp = timezone.now(), 
                    document_id = document,
                    user_id = user,
                    status = document.status
                )

        self.stdout.write(self.style.SUCCESS('Successfully marked unacted documents.'))

def pass_unacted_document(document, user):

    officers = User.objects.filter(office_id=user.office_id, role='ACT', status='active').exclude(user_id=user.user_id)

    if not officers:
        print("There's no other officers found")
        return
    
    officers = officers.filter(max_load_per_day__gt=0)

    if not officers:
        # Reset max_load_per_day to 5 for each officer
        for officer in officers:
            officer.max_load_per_day = 5
            officer.save()

    if officers.count() == 1:
        document.act_receiver = officers.first().user_id
        days_deadline = document.document_type.priority_level.deadline
        document.ongoing_deadline = date.today() + timedelta(days=days_deadline)
        document.save()

        ActivityLogs.objects.create(
            time_stamp = timezone.now(), 
            activity = 'Document Reassigned Due to Inaction',
            document_id = document,
            user_id = user,
            receiver_id_id = document.act_receiver
        )

    else:
        officers_performance_levels = {}
        for officer in officers:
            fifteen_days_ago = timezone.now() - timedelta(days=15)
            received_document_count = ActivityLogs.objects.filter(activity='Document Forwarded to Action Officer', receiver_id=officer, time_stamp__gte=fifteen_days_ago).count()
            acted_documents = ActivityLogs.objects.filter(activity='Document Endorsed by Action Officer', receiver_id=officer, time_stamp__gte=fifteen_days_ago)
           
            if received_document_count > 0:
                average_acted_document = (acted_documents.count() / received_document_count) * 100
            else:
                average_acted_document = 0 

            average_response_time = calculate_average_response_time(acted_documents, officer)

            officers_performance_levels[officer.user_id] = (average_acted_document + average_response_time) * 2

        sorted_officers = sorted(officers_performance_levels, key=officers_performance_levels.get, reverse=True)

        highest_performance_officer = None

        for officer_id in sorted_officers:
            get_available_officer = User.objects.get(user_id=officer_id)  # Assuming 'id' is the primary key
            max_load = get_available_officer.max_load_per_day
            if max_load > 0:
                highest_performance_officer = officer_id
                get_available_officer.max_load_per_day -= 1
                get_available_officer.save()
                break
        
        document.act_receiver = highest_performance_officer
        days_deadline = document.document_type.priority_level.deadline
        document.ongoing_deadline = date.today() + timedelta(days=days_deadline)
        document.save()

        ActivityLogs.objects.create(
            time_stamp = timezone.now(), 
            activity = 'Document Reassigned Due to Inaction',
            document_id = document,
            user_id = user,
            receiver_id_id = document.act_receiver
        )

def calculate_average_response_time(acted_documents, officer):

    officer_average_response_time = []

    for document in acted_documents:

        time_acted = document.time_stamp
        log = ActivityLogs.objects.get(activity='Document Forwarded to Action Officer', document_id=document.document_id, receiver_id=officer)
        time_received = log.time_stamp

        time_taken = (time_acted - time_received).days
        time_alloted = document.document_id.document_type.priority_level.deadline

        document_average_response_time = ((time_alloted - time_taken) / time_alloted) * 100
        officer_average_response_time.append(document_average_response_time)

    if officer_average_response_time:
        overall_average = sum(officer_average_response_time) / len(officer_average_response_time)
        return overall_average
    else:
        return 0

