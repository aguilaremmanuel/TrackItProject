from django.contrib import admin
from django.urls import path
from . import views
from .views import generate_qr_code

urlpatterns = [
    path('login/',views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('signup/',views.user_signup, name='user_signup'),

    path('admin-login/',views.system_admin_login, name='system_admin_login'),
    path('admin-dashboard/',views.system_admin_dashboard, name='system_admin_dashboard'),

    path('system-admin-dashboard/', views.system_admin_dashboard, name='system_admin_dashboard'),
    path('system-admin-user-management/<str:office>/', views.system_admin_user_management, name='system_admin_user_management'),
    path('system-admin-update-user-display/<str:office>/', views.update_user_display, name='update_user_display'),
    path('update-user-status/<str:user_id>/<str:action>/<str:office>/<str:user_type>', views.update_user_status, name='update_user_status'),
    path('system-admin-doc-management/',views.system_admin_doc_management, name='system_admin_doc_management'),
    path('edit-document-type/', views.edit_document_type, name='edit_document_type'),
    path('delete-document-type/<int:document_no>/', views.delete_document_type, name='delete_document_type'),
    path('system-admin-new-record/',views.system_admin_new_record, name='system_admin_new_record'),
    
    path('document-update-status/<str:action>/<int:document_no>/', views.document_update_status, name='document_update_status'),

    path('director-login/',views.director_login, name='director_login'),
    path('director-user-management/<str:office>/', views.director_user_management, name='director_user_management'),
    path('director-doc-management/',views.director_doc_management, name='director_doc_management'),
    path('director-dashboard/',views.director_dashboard, name='director_dashboard'),
    path('director-all-records/',views.director_all_records, name='director_all_records'),
    path('director-needs-action/<str:scanned_document_no>/',views.director_needs_action, name='director_needs_action'),
    path('director-activity-logs/', views.director_activity_logs, name='director_activity_logs'),
    path('director-update-needs-action-display', views.director_update_needs_action_display, name='director_update_needs_action_display'),

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
    path('admin-officer-activity-logs/',views.admin_officer_activity_logs, name='admin_officer_activity_logs'),

    path('sro-dashboard/',views.dashboard_sro, name='dashboard_sro'),
    path('sro-records/<str:panel>/<str:scanned_document_no>/',views.sro_records, name='sro_records'),
    path('sro-update-records-display/<str:panel>/', views.sro_update_records_display, name='sro_update_records_display'),
    path('sro-unacted-records/',views.sro_unacted_records, name='sro_unacted_records'),
    path('sro-activity-logs/',views.sro_activity_logs, name='sro_activity_logs'),
    
    path('action-officer-dashboard/',views.dashboard_action_officer, name='dashboard_action_officer'),
    path('action-officer-records/<str:scanned_document_no>/',views.action_officer_records, name='action_officer_records'),
    path('action-officer-update-records-display', views.action_officer_update_records_display, name='action_officer_update_records_display'),
    path('action-officer-unacted-records/',views.action_officer_unacted_records, name='action_officer_unacted_records'),
    path('action-officer-activity-logs/',views.action_officer_activity_logs, name='action_officer_activity_logs'),

    path('forgot-password/',views.forgot_password, name='forgot_password'),
    path('new-password/<uidb64>/<token>/', views.new_password, name='new_password'),

    path('scanned-qr-code/<int:document_no>/', views.scanning_qr_code, name='scanning_qr_code'),
]
