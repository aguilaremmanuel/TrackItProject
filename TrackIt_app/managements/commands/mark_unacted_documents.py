from django.core.management.base import BaseCommand
from django.utils import timezone
from TrackIt_app.models import Document, ActivityLogs
from django.contrib.auth.models import User  # Replace with your actual user model if different

class Command(BaseCommand):
    help = 'Mark documents as unacted and log them in activity logs'

    def handle(self, *args, **kwargs):
        now = timezone.now().date()  # Get the current date

        # Fetch all documents that are not 'For Archiving' and are past the deadline
        documents = Document.objects.filter(
            status__in=['For DIR Approval', 'For Routing', 'For SRO Receiving', 'For ACT Receiving', 'For Resolving'],
            ongoing_deadline__lt=now,
            recent_update__lt=now
        )

        # Loop through the documents and check if they are unacted
        for document in documents:
            # Log the unacted document in ActivityLogs if not already logged
            activity_log = ActivityLogs.objects.filter(
                document_id=document.id,
                activity="unacted document"
            ).exists()

            if not activity_log:

                if document.status == 'For DIR Approval':
                    user

                # Assuming the user who last handled the document can be fetched
                user = User.objects.get(pk=document.act_receiver)  # Replace with actual logic if necessary

                # Create the new activity log
                ActivityLogs.objects.create(
                    time_stamp=document.ongoing_deadline,  # When the document became "unacted"
                    activity="unacted document",
                    document_id=document,
                    user_id=user,
                    remarks=None
                )

        self.stdout.write(self.style.SUCCESS('Successfully marked unacted documents.'))
