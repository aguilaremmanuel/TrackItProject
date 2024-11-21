from django.contrib import admin
from django.urls import path
from . import views
from .views import generate_qr_code
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('signup/',views.user_signup, name='user_signup'),

    #path('admin-login/',views.system_admin_login, name='system_admin_login'),
    path('admin-dashboard/',views.system_admin_dashboard, name='system_admin_dashboard'),

    path('system-admin-dashboard/', views.system_admin_dashboard, name='system_admin_dashboard'),
    path('system-admin-user-management/<str:office>/', views.system_admin_user_management, name='system_admin_user_management'),
    path('system-admin-update-user-display/<str:office>/', views.update_user_display, name='update_user_display'),
    path('update-user-status/<str:user_id>/<str:action>/<str:office>/<str:user_type>', views.update_user_status, name='update_user_status'),
    path('system-admin-doc-management/',views.system_admin_doc_management, name='system_admin_doc_management'),
    path('edit-document-type/', views.edit_document_type, name='edit_document_type'),
    path('delete-document-type/<int:document_no>/', views.delete_document_type, name='delete_document_type'),
    path('system-admin-new-record/',views.system_admin_new_record, name='system_admin_new_record'),
    path('system-admin-all-records/', views.system_admin_all_records, name='system_admin_all_records'),
    path('system-admin-archive/', views.system_admin_archive, name='system_admin_archive'),
    path('system-admin-announcements/',views.system_admin_announcements, name='system_admin_announcements'),
    path('system-admin-generate-reports/<str:report_type>/',views.system_admin_generate_reports, name='system_admin_generate_reports'),
    
    path('document-update-status/<str:action>/<int:document_no>/', views.document_update_status, name='document_update_status'),

    # DOCUMENT TYPES:
    path('update-document-types-display/', views.update_document_types_display, name='update_document_types_display'),

    #path('director-login/',views.director_login, name='director_login'),
    path('director-user-management/<str:office>/', views.director_user_management, name='director_user_management'),
    path('director-doc-management/',views.director_doc_management, name='director_doc_management'),
    path('director-dashboard/',views.director_dashboard, name='director_dashboard'),
    path('director-all-records/',views.director_all_records, name='director_all_records'),
    path('director-needs-action/<str:scanned_document_no>/',views.director_needs_action, name='director_needs_action'),
    path('director-unacted-records/', views.director_unacted_records, name='director_unacted_records'),
    path('system-admin-director-activity-logs/<str:activity_type>/', views.sys_dir_activity_logs, name='sys_dir_activity_logs'),
    path('update-archive-display/<str:user>', views.update_archive_display, name='update_archive_display'),
    path('director-update-needs-action-display', views.director_update_needs_action_display, name='director_update_needs_action_display'),
    path('director-announcements/',views.director_announcements, name='director_announcements'),
    path('director-archive/', views.director_archive, name='director_archive'),
    path('director-generate-reports/<str:report_type>/',views.director_generate_reports, name='director_generate_reports'),

    path('admin-officer-dashboard/',views.admin_officer_dashboard, name='admin_officer_dashboard'),
    path('admin-officer-new-record/',views.admin_officer_new_record, name='admin_officer_new_record'),
    path('add-record/', views.add_record, name='add_record'),
    path('load-document-types/', views.load_document_types, name='load_document_types'),
    path('generate-qrcode/<int:document_no>/', views.generate_qr_code, name='generate_qr_code'),

    path('admin-officer-all-records/',views.admin_officer_all_records, name='admin_officer_all_records'),
    path('admin-officer-all-records-display/<str:user>', views.update_all_records_display, name='update_all_records_display'),
    path('fetch-document-details/<int:document_no>/', views.fetch_document_details, name='fetch_document_details'),
    path('add-remarks/<int:document_no>/<int:remarks_no>/', views.add_remarks, name='add_remarks'),
    path('delete-empty-remarks/', views.delete_empty_remarks, name='delete_empty_remarks'),
    path('get-routes/<int:document_no>/', views.get_routes, name='get_routes'),
    path('admin-officer-needs-action/<str:panel>/<str:scanned_document_no>/',views.admin_officer_needs_action, name='admin_officer_needs_action'),
    path('admin-officer-update-needs-action-display/<str:panel>/', views.admin_officer_update_needs_action_display, name='admin_officer_update_needs_action_display'),
    path('admin-officer-unacted-records/',views.admin_officer_unacted_records, name='admin_officer_unacted_records'),
    path('admin-officer-archive/',views.admin_officer_archive, name='admin_officer_archive'),
    path('admin-officer-activity-logs/<str:activity_type>/',views.admin_officer_activity_logs, name='admin_officer_activity_logs'),

    path('sro-dashboard/',views.sro_dashboard, name='sro_dashboard'),
    path('sro-records/<str:panel>/<str:scanned_document_no>/',views.sro_records, name='sro_records'),
    path('sro-update-records-display/<str:panel>/', views.sro_update_records_display, name='sro_update_records_display'),
    path('sro-unacted-records/',views.sro_unacted_records, name='sro_unacted_records'),
    path('sro-activity-logs/<str:activity_type>/',views.sro_activity_logs, name='sro_activity_logs'),
    
    path('action-officer-dashboard/',views.action_officer_dashboard, name='action_officer_dashboard'),
    path('action-officer-records/<str:scanned_document_no>/',views.action_officer_records, name='action_officer_records'),
    path('action-officer-update-records-display', views.action_officer_update_records_display, name='action_officer_update_records_display'),
    path('action-officer-unacted-records/',views.action_officer_unacted_records, name='action_officer_unacted_records'),
    path('action-officer-activity-logs/<str:activity_type>/',views.action_officer_activity_logs, name='action_officer_activity_logs'),

    path('forgot-password/',views.forgot_password, name='forgot_password'),
    path('new-password/<uidb64>/<token>/', views.new_password, name='new_password'),

    path('scanned-qr-code/<int:document_no>/', views.scanning_qr_code, name='scanning_qr_code'),

    path('update-unacted-records-display/', views.update_unacted_records_display, name='update_unacted_records_display'),

    path('generate-document-report/<int:document_no>/', views.generate_document_report, name='generate_document_report'),
    path('new-employee-report/', views.new_employee_report, name='new_employee_report'),
    path('load-target-employees/', views.load_target_employees, name='load_target_employees'),
    path('new-office-report/', views.new_office_report, name='new_office_report'),
    path('update-reports/<str:report_type>', views.update_reports_display, name='update_reports_display'),
    path('delete-report/<int:report_no>/', views.delete_report, name='delete_report'),
    path('download-performance-report/<int:report_no>/', views.download_performance_report, name='download_performance_report'),

    path('check-remarks/<int:document_no>/<int:activity_log_no>/', views.check_remarks, name='check_remarks'),
    path('change-priority-level/<int:document_no>/<int:activity_log_no>/', views.change_priority_level, name='change_priority_level'),

    path('generate-upload-file-qrcode/<int:activity_log_no>/', views.generate_upload_file_qrcode, name='generate_upload_file_qrcode'),
    path('upload-file-page/<int:activity_log_no>/', views.upload_file_page, name='upload_file_page'),
    path('upload-file-with-phone/<int:activity_log_no>', views.upload_file_with_phone, name='upload_file_with_phone'),

    path('fetch-phone-upload-file/<int:activity_log_no>/', views.fetch_phone_upload_file, name='fetch_phone_upload_file'),
    path('delete-phone-upload-file/<int:activity_log_no>/', views.delete_phone_upload_file, name='delete_phone_upload_file'),

    path('edit-profile/',views.edit_profile, name='edit_profile'),

    path('update-announcement/<int:id>/', views.update_announcement, name='update_announcement'),
    path('delete-announcement/<int:id>/', views.delete_announcement, name='delete_announcement'),
    path('announcement/<int:announcement_id>/attachment/', views.view_attachment, name='view_attachment'),

    path('director-total-records/<str:time_span>/', views.director_total_records, name='director_total_records'),
    path('director-document-status/<str:time_span>/<str:document_status>/', views.director_document_status, name='director_document_status'),
    path('director-office-performance/<str:time_span>/<str:target_office>/', views.director_office_performance, name='director_office_performance'),
    path('director-employee-performance/<str:time_span>/<str:target_report_type>/<str:target_office>/', views.director_employee_performance, name='director_employee_performance'),
    path('generate-document-status-report/<str:time_span>/<str:document_status>/', views.generate_document_status_report, name='generate_document_status_report'),

    path('fetch-new-notifications/', views.fetch_new_notifications, name='fetch_new_notifications'),
    path('fetch-earlier-notifications/', views.fetch_earlier_notifications, name='fetch_earlier_notifications'),
    path('fetch-unread-notifications/', views.fetch_unread_notifications, name='fetch_unread_notifications'),
    path('click-notification/<str:notification_type>/<int:no>/', views.click_notification, name='click_notification'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
