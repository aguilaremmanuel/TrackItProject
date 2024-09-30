from django.db import models

# Create your models here.
class Office(models.Model):
    office_id = models.CharField(max_length=3 ,primary_key = True)
    office_name = models.CharField(max_length=45)
    class Meta:
        db_table = 'tbl_office'

class SystemAdmin(models.Model):
    sa_user_id = models.CharField(max_length=8, primary_key=True)
    sa_user_lastname = models.CharField(max_length=45)
    sa_user_firstname = models.CharField(max_length=45)
    sa_user_middlename = models.CharField(max_length=45, null = True)
    password = models.CharField(max_length=45)  

class User(models.Model):
    user_id = models.CharField(max_length=8, primary_key=True)
    lastname = models.CharField(max_length=45)
    firstname = models.CharField(max_length=45)
    middlename = models.CharField(max_length=45, null = True)
    email = models.EmailField(max_length=45)
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
    class Meta:
        db_table = 'tbl_document'

class Remarks(models.Model):
    no = models.BigAutoField(primary_key=True)
    remarks = models.CharField(max_length=300, null=True, blank=True)
    class Meta:
        db_table = 'tbl_remarks'

class ActivityLogs(models.Model):
    no = models.BigAutoField(primary_key=True)
    time_stamp = models.DateTimeField(blank=True)
    activity = models.CharField(max_length=50)
    document_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.ForeignKey(Remarks, on_delete=models.SET_NULL, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        db_table = 'tbl_activity_logs'

