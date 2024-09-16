from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.user_login, name='user_login'),
    path('signup/',views.user_signup, name='user_signup'),

    path('admin-login/',views.system_admin_login, name='system_admin_login'),
    path('admin-dashboard/',views.system_admin_dashboard, name='system_admin_dashboard'),

    path('system-admin-user-management/<str:office>/', views.system_admin_user_management, name='system_admin_user_management'),
    path('update-user-status/<str:user_id>/<str:action>/', views.update_user_status, name='update_user_status'),
    path('update-user-status/<str:user_id>/<str:action>/<str:office>', views.update_user_status, name='update_user_status'),

    path('system-admin-doc-management/',views.system_admin_doc_management, name='system_admin_doc_management'),
    path('edit-document-type/', views.edit_document_type, name='edit_document_type'),
    path('delete-document-type/<int:document_no>/', views.delete_document_type, name='delete_document_type'),

    path('director-login/',views.director_login, name='director_login'),

    path('director-dashboard/',views.dashboard_director, name='dashboard_director'),
    path('admin-officer-dashboard/',views.dashboard_admin_officer, name='dashboard_admin_officer'),
    path('admin-officer-new-record/',views.new_record_admin_officer, name='new_record_admin_officer'),
    path('admin-officer-all-records/',views.all_records_admin_officer, name='all_records_admin_officer'),
    path('admin-officer-needs-action/',views.needs_action_admin_officer, name='needs_action_admin_officer'),
    path('admin-officer-overdue/',views.overdue_admin_officer, name='overdue_admin_officer'),
    path('admin-officer-archive/',views.archive_admin_officer, name='archive_admin_officer'),
    path('admin-officer-activity-logs/',views.activity_logs_admin_officer, name='activity_logs_admin_officer'),

    path('sro-dashboard/',views.dashboard_sro, name='dashboard_sro'),
    path('sro-all-records/',views.all_records_sro, name='all_records_sro'),
    path('sro-unacted-documents/',views.unacted_documents_sro, name='unacted_documents_sro'),
    path('sro-activity-logs/',views.activity_logs_sro, name='activity_logs_sro'),
    
    path('action-officer-dashboard/',views.dashboard_action_officer, name='dashboard_action_officer'),
    path('action-officer-all-records/',views.all_records_action_officer, name='all_records_action_officer'),
    path('action-officer-unacted-documents/',views.unacted_documents_action_officer, name='unacted_documents_action_officer'),
    path('action-officer-activity-logs/',views.activity_logs_action_officer, name='activity_logs_action_officer'),

    path('forgot-password/',views.forgot_password, name='forgot_password'),
    path('new-password/',views.new_password, name='new_password'),
]
