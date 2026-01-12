from django.urls import path
from . import views

app_name = 'resume_builder'

urlpatterns = [
    # Home and Dashboard
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Resume URLs - Template selection
    path('resume-templates/', views.resume_templates, name='resume_templates'),
    
    # Draft Editor (NEW - No auto-save)
    path('draft-resume/<int:template_id>/', views.draft_resume_editor, name='draft_resume_editor'),
    path('draft-cover-letter/<int:template_id>/', views.draft_cover_letter_editor, name='draft_cover_letter_editor'),
    
    # Legacy direct creation (kept for backward compatibility)
    path('create-resume/', views.create_resume_direct, name='create_resume_direct'),
    path('create-resume/<int:template_id>/', views.create_resume, name='create_resume'),
    
    # Existing resume editing (for saved documents)
    path('edit-resume/<int:resume_id>/', views.edit_resume, name='edit_resume'),
    path('preview-resume/<int:resume_id>/', views.preview_resume, name='preview_resume'),
    path('download-resume/<int:resume_id>/', views.download_resume, name='download_resume'),
    path('delete-resume/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    
    # Cover Letter URLs - Template selection
    path('cover-letter-templates/', views.cover_letter_templates, name='cover_letter_templates'),
    
    # Legacy direct creation (kept for backward compatibility)
    path('create-cover-letter/', views.create_cover_letter_direct, name='create_cover_letter_direct'),
    path('create-cover-letter/<int:template_id>/', views.create_cover_letter, name='create_cover_letter'),
    
    # Existing cover letter editing (for saved documents)
    path('edit-cover-letter/<int:cover_letter_id>/', views.edit_cover_letter, name='edit_cover_letter'),
    path('preview-cover-letter/<int:cover_letter_id>/', views.preview_cover_letter, name='preview_cover_letter'),
    path('download-cover-letter/<int:cover_letter_id>/', views.download_cover_letter, name='download_cover_letter'),
    path('delete-cover-letter/<int:cover_letter_id>/', views.delete_cover_letter, name='delete_cover_letter'),
    
    # API Endpoints - Existing
    path('api/save-resume/<int:resume_id>/', views.api_save_resume, name='api_save_resume'),
    path('api/upload-photo/<int:resume_id>/', views.api_upload_photo, name='api_upload_photo'),
    path('api/save-cover-letter/<int:cover_letter_id>/', views.api_save_cover_letter, name='api_save_cover_letter'),
    
    # API Endpoints - Draft Save (NEW)
    path('api/save-draft-resume/', views.api_save_draft_resume, name='api_save_draft_resume'),
    path('api/save-draft-cover-letter/', views.api_save_draft_cover_letter, name='api_save_draft_cover_letter'),
    
    # API Endpoints - Rename
    path('api/rename-resume/<int:resume_id>/', views.api_rename_resume, name='api_rename_resume'),
    path('api/rename-cover-letter/<int:cover_letter_id>/', views.api_rename_cover_letter, name='api_rename_cover_letter'),
]