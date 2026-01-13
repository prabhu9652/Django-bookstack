from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    # Public views
    path('', views.careers_home, name='careers_home'),
    path('job/<slug:slug>/', views.job_detail, name='job_detail'),
    
    # Candidate views (login required)
    path('job/<slug:slug>/apply/', views.apply_job, name='apply_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('my-applications/<int:application_id>/', views.application_detail, name='application_detail'),
    
    # Admin views (superuser required)
    path('admin/jobs/', views.admin_jobs_dashboard, name='admin_jobs_dashboard'),
    path('admin/jobs/create/', views.admin_create_job, name='admin_create_job'),
    path('admin/jobs/<int:job_id>/edit/', views.admin_edit_job, name='admin_edit_job'),
    path('admin/applications/', views.admin_applications_dashboard, name='admin_applications_dashboard'),
    path('admin/applications/<int:application_id>/', views.admin_application_detail, name='admin_application_detail'),
    
    # API endpoints
    path('api/apply/', views.api_submit_application, name='api_submit_application'),
    path('api/application/<int:application_id>/status/', views.api_update_application_status, name='api_update_application_status'),
    path('api/application/<int:application_id>/note/', views.api_add_application_note, name='api_add_application_note'),
    path('api/job/<int:job_id>/toggle/', views.api_toggle_job_status, name='api_toggle_job_status'),
    
    # File download endpoints (admin only)
    path('admin/applications/<int:application_id>/resume/download/', views.download_uploaded_resume, name='download_uploaded_resume'),
    path('admin/applications/<int:application_id>/cover-letter/download/', views.download_uploaded_cover_letter, name='download_uploaded_cover_letter'),
    path('api/application/<int:application_id>/delete/', views.api_delete_application, name='api_delete_application'),
]
