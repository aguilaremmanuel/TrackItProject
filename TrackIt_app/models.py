from django.db import models

# Create your models here.
class Office(models.Model):
    office_id = models.CharField(max_length=3 ,primary_key = True)
    office_name = models.CharField(max_length=45)
    class Meta:
        db_table = 'tbl_office'

class User(models.Model):
    user_id = models.CharField(max_length=8, primary_key=True)
    lastname = models.CharField(max_length=45)
    firstname = models.CharField(max_length=45)
    middlename = models.CharField(max_length=45, null = True)
    email = models.EmailField(max_length=45, null = True)
    def get_email_field_name(self):
        return 'email' 
    contact_no = models.CharField(max_length=11)
    password = models.CharField(max_length=45)
    role = models.CharField(max_length=45)
    office_id = models.ForeignKey(Office, on_delete=models.CASCADE, null=True, blank=True)
    registered_date = models.DateTimeField(null=True, blank=True)
    verified_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(null=True, max_length=20, default = 'for verification')
    employee_id = models.CharField(max_length=12, blank = True)
    last_login = models.DateTimeField(null=True, blank=True)
    receive_recent = models.BooleanField(default=False)
    max_load_per_day = models.IntegerField(default=5)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True)
    class Meta:
        db_table = 'tbl_user'

class PriorityLevel(models.Model):
    no = models.BigAutoField(primary_key=True)
    priority_level = models.CharField(max_length=16)
    deadline = models.IntegerField()
    class Meta:
        db_table = 'tbl_priority_level'

class DocumentType(models.Model):
    document_no = models.BigAutoField(primary_key=True)
    document_type = models.CharField(max_length=45)
    category = models.CharField(max_length=7)
    priority_level = models.ForeignKey(PriorityLevel, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    used_count = models.IntegerField(default=0)
    last_update = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'tbl_document_type'

class DocumentRoute(models.Model):
    routing_no = models.BigAutoField(primary_key=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, null=True, blank=True)
    route = models.ForeignKey(Office, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        db_table = 'tbl_document_route'

class Document(models.Model):
    document_no = models.BigAutoField(primary_key=True)
    tracking_no = models.CharField(max_length=30)
    sender_name = models.CharField(max_length=45, null=True, blank=True)
    sender_department = models.CharField(max_length=45, null=True, blank=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, null=True, blank=True)
    next_route = models.CharField(max_length=45, null=True)
    subject = models.CharField(max_length=120)
    remarks = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=25)
    recent_update = models.DateTimeField(blank=True, null=True)
    act_receiver = models.CharField(max_length=10, blank=True, null=True)
    ongoing_deadline = models.DateField(null=True, blank=True)
    old_document_type = models.IntegerField(null=True, blank=True)
    is_rejected = models.BooleanField(default=False)
    class Meta:
        db_table = 'tbl_document'

class Remarks(models.Model):
    no = models.BigAutoField(primary_key=True)
    remarks = models.CharField(max_length=300, null=True, blank=True)
    class Meta:
        db_table = 'tbl_remarks'

def document_directory_path(instance, filename):
    return f'document/{instance.document_id.document_no}/{filename}'

class ActivityLogs(models.Model):
    no = models.BigAutoField(primary_key=True)
    time_stamp = models.DateTimeField(blank=True)
    activity = models.CharField(max_length=50)
    document_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.ForeignKey(Remarks, on_delete=models.SET_NULL, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='activity_logs_actor')
    receiver_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_logs_receiver')
    file_attachment = models.FileField(upload_to=document_directory_path, null=True, blank=True)
    class Meta:
        db_table = 'tbl_activity_logs'

class Reports(models.Model):
    report_no = models.BigAutoField(primary_key=True)
    report_name = models.CharField(max_length=50)
    report_type = models.CharField(max_length=20)
    employee_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    office_id = models.ForeignKey(Office, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    last_update = models.DateTimeField(blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'tbl_reports'

class UnactedLogs(models.Model):
    record_no = models.BigAutoField(primary_key=True)
    time_stamp = models.DateField(null=True, blank=True)
    document_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=25, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_acted = models.BooleanField(default=False)
    date_acted = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'tbl_unacted_logs'

class DocumentManagementLogs(models.Model):
    record_no = models.BigAutoField(primary_key=True)
    time_stamp = models.DateTimeField(blank=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, null=True, blank=True)
    activity = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        db_table = 'tbl_document_management_logs'

class ReportManagementLogs(models.Model):
    record_no = models.BigAutoField(primary_key=True)
    time_stamp = models.DateTimeField(blank=True)
    report = models.ForeignKey(Reports, on_delete=models.CASCADE, null=True, blank=True)
    activity = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        db_table = 'tbl_report_management_logs'

class UserManagementLogs(models.Model):
    record_no = models.BigAutoField(primary_key=True)
    time_stamp = models.DateTimeField(blank=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    activity = models.CharField(max_length=50)
    user = models.CharField(max_length=10, blank=True, null=True)
    class Meta:
        db_table = 'tbl_user_management_logs'

class Announcement(models.Model):
    title = models.TextField(max_length=100)
    description = models.TextField()
    attachment = models.FileField(upload_to='', blank=True, null=True, default='default_attachment.pdf')
    created_at = models.DateTimeField(auto_now_add=True)
    offices = models.CharField(max_length=255, null=True)
    all_offices = models.BooleanField(default=False)
    end_date = models.DateField(null=True, blank=True) #
    created_by = models.CharField(max_length=50)

    class Meta:
        db_table = 'tbl_announcement'



