from django.core.management.base import BaseCommand
from django.utils import timezone
from TrackIt_app.models import Document, DocumentDueLogs, User
from datetime import timedelta, date, datetime

class Command(BaseCommand):
    help = 'Push notification for document incoming dues'

    def handle(self, *args, **kwargs):

        now = timezone.localtime().date()
        tomorrow = now + timedelta(days=1)

        # Fetch all documents that are not 'For Archiving' and are past the deadline
        documents_due_today = Document.objects.filter(
            status__in=['For DIR Approval', 'For Routing', 'For SRO Receiving', 'For ACT Receiving', 'For Resolving'],
            ongoing_deadline=now
        )

        documents_due_tomorrow = Document.objects.filter(
            status__in=['For DIR Approval', 'For Routing', 'For SRO Receiving', 'For ACT Receiving', 'For Resolving'],
            ongoing_deadline=tomorrow
        )

        for document in documents_due_today:
            user = get_user(document)
            DocumentDueLogs.objects.create(
                due_type = 'today',
                time_stamp = timezone.now(), 
                document_id = document,
                user_id = user
            )

        for document in documents_due_tomorrow:
            user = get_user(document)
            DocumentDueLogs.objects.create(
                due_type = 'tomorrow',
                time_stamp = timezone.now(), 
                document_id = document,
                user_id = user
            )

        self.stdout.write(self.style.SUCCESS('Successfully pushed notification.'))

def get_user(document):

    roles = {
        'For DIR Approval': 'Director',
        'For Routing': 'ADO',
        'For SRO Receiving': 'SRO',
        'For Resolving': 'SRO'
    }

    if document.status in roles:

        role = roles[document.status]
        if document.status in ['For SRO Receiving', 'For Resolving']:
            receiving_office = document.next_route
            user = User.objects.filter(office_id_id=receiving_office, role=role, status='active').first()
        elif document.status == 'For ACT Receiving':
            user = User.objects.filter(user_id=document.act_receiver, status='active').first()
        else:
            user = User.objects.filter(role=role, status='active').first()

        return user

    print('No user found')
    return None

