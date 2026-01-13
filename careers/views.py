from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from django.db import IntegrityError
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import json
import logging

from .models import JobPosting, Application, ApplicationNote
from .decorators import superuser_required
from resume_builder.models import Resume, CoverLetter

logger = logging.getLogger(__name__)


# ============================================
# PUBLIC VIEWS
# ============================================

def careers_home(request):
    """Careers landing page with job listings"""
    # Get filter parameters
    department = request.GET.get('department', '')
    location_type = request.GET.get('location_type', '')
    employment_type = request.GET.get('employment_type', '')
    search = request.GET.get('search', '')
    
    # Base queryset - only active and open jobs
    jobs = JobPosting.objects.filter(is_active=True)
    
    # Filter out jobs past their close date
    jobs = jobs.filter(
        Q(closes_at__isnull=True) | Q(closes_at__gt=timezone.now())
    )
    
    # Apply filters
    if department:
        jobs = jobs.filter(department__iexact=department)
    if location_type:
        jobs = jobs.filter(location_type=location_type)
    if employment_type:
        jobs = jobs.filter(employment_type=employment_type)
    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    
    # Get unique departments for filter dropdown
    departments = JobPosting.objects.filter(is_active=True).values_list(
        'department', flat=True
    ).distinct().order_by('department')
    
    context = {
        'title': 'Careers',
        'jobs': jobs,
        'job_count': jobs.count(),
        'departments': departments,
        'location_types': JobPosting.LOCATION_TYPES,
        'employment_types': JobPosting.EMPLOYMENT_TYPES,
        'current_filters': {
            'department': department,
            'location_type': location_type,
            'employment_type': employment_type,
            'search': search,
        },
    }
    
    return render(request, 'careers/careers_home.html', context)


def job_detail(request, slug):
    """Job details page"""
    job = get_object_or_404(JobPosting, slug=slug)
    
    # Increment view count
    job.view_count += 1
    job.save(update_fields=['view_count'])
    
    # Check if user has already applied
    has_applied = False
    if request.user.is_authenticated:
        has_applied = Application.objects.filter(
            job=job, user=request.user
        ).exists()
    
    context = {
        'title': job.title,
        'job': job,
        'has_applied': has_applied,
        'is_open': job.is_open(),
    }
    
    return render(request, 'careers/job_detail.html', context)


# ============================================
# CANDIDATE VIEWS
# ============================================

@login_required
def apply_job(request, slug):
    """Application form for a job"""
    job = get_object_or_404(JobPosting, slug=slug)
    
    # Check if job is open
    if not job.is_open():
        messages.error(request, 'This position is no longer accepting applications.')
        return redirect('careers:job_detail', slug=slug)
    
    # Check if already applied
    if Application.objects.filter(job=job, user=request.user).exists():
        messages.info(request, 'You have already applied to this position.')
        return redirect('careers:job_detail', slug=slug)
    
    # Get user's resumes and cover letters
    resumes = Resume.objects.filter(user=request.user).order_by('-updated_at')
    cover_letters = CoverLetter.objects.filter(user=request.user).order_by('-updated_at')
    
    context = {
        'title': f'Apply - {job.title}',
        'job': job,
        'resumes': resumes,
        'cover_letters': cover_letters,
        'user_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
        'user_email': request.user.email,
    }
    
    return render(request, 'careers/apply_job.html', context)


@login_required
def my_applications(request):
    """User's applications dashboard"""
    status_filter = request.GET.get('status', '')
    
    applications = Application.objects.filter(user=request.user)
    
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    context = {
        'title': 'My Applications',
        'applications': applications,
        'status_choices': Application.STATUS_CHOICES,
        'current_status': status_filter,
    }
    
    return render(request, 'careers/my_applications.html', context)


@login_required
def application_detail(request, application_id):
    """View application details (candidate view)"""
    application = get_object_or_404(
        Application, id=application_id, user=request.user
    )
    
    context = {
        'title': f'Application - {application.job.title}',
        'application': application,
    }
    
    return render(request, 'careers/application_detail.html', context)


# ============================================
# ADMIN VIEWS
# ============================================

@superuser_required
def admin_jobs_dashboard(request):
    """Admin job management dashboard"""
    status_filter = request.GET.get('status', '')
    department_filter = request.GET.get('department', '')
    
    jobs = JobPosting.objects.annotate(
        application_count=Count('applications')
    ).order_by('-created_at')
    
    if status_filter == 'active':
        jobs = jobs.filter(is_active=True)
    elif status_filter == 'closed':
        jobs = jobs.filter(is_active=False)
    
    if department_filter:
        jobs = jobs.filter(department__iexact=department_filter)
    
    departments = JobPosting.objects.values_list(
        'department', flat=True
    ).distinct().order_by('department')
    
    context = {
        'title': 'Manage Jobs',
        'jobs': jobs,
        'departments': departments,
        'current_filters': {
            'status': status_filter,
            'department': department_filter,
        },
    }
    
    return render(request, 'careers/admin/jobs_dashboard.html', context)


@superuser_required
def admin_create_job(request):
    """Create new job posting"""
    if request.method == 'POST':
        try:
            # Parse tech_stack from comma-separated string
            tech_stack_str = request.POST.get('tech_stack', '')
            tech_stack = [t.strip() for t in tech_stack_str.split(',') if t.strip()]
            
            # Parse closes_at date
            closes_at = request.POST.get('closes_at')
            if closes_at:
                closes_at = timezone.datetime.fromisoformat(closes_at)
            else:
                closes_at = None
            
            job = JobPosting.objects.create(
                title=request.POST.get('title'),
                department=request.POST.get('department'),
                location=request.POST.get('location'),
                location_type=request.POST.get('location_type'),
                employment_type=request.POST.get('employment_type'),
                description=request.POST.get('description'),
                responsibilities=request.POST.get('responsibilities'),
                requirements=request.POST.get('requirements'),
                nice_to_have=request.POST.get('nice_to_have', ''),
                benefits=request.POST.get('benefits', ''),
                tech_stack=tech_stack,
                experience_range=request.POST.get('experience_range', ''),
                salary_range=request.POST.get('salary_range', ''),
                is_active=request.POST.get('is_active') == 'on',
                closes_at=closes_at,
            )
            
            messages.success(request, f'Job "{job.title}" created successfully!')
            return redirect('careers:admin_jobs_dashboard')
            
        except Exception as e:
            logger.error(f"Error creating job: {str(e)}")
            messages.error(request, f'Error creating job: {str(e)}')
    
    context = {
        'title': 'Create Job Posting',
        'location_types': JobPosting.LOCATION_TYPES,
        'employment_types': JobPosting.EMPLOYMENT_TYPES,
    }
    
    return render(request, 'careers/admin/job_form.html', context)


@superuser_required
def admin_edit_job(request, job_id):
    """Edit existing job posting"""
    job = get_object_or_404(JobPosting, id=job_id)
    
    if request.method == 'POST':
        try:
            # Parse tech_stack from comma-separated string
            tech_stack_str = request.POST.get('tech_stack', '')
            tech_stack = [t.strip() for t in tech_stack_str.split(',') if t.strip()]
            
            # Parse closes_at date
            closes_at = request.POST.get('closes_at')
            if closes_at:
                closes_at = timezone.datetime.fromisoformat(closes_at)
            else:
                closes_at = None
            
            job.title = request.POST.get('title')
            job.department = request.POST.get('department')
            job.location = request.POST.get('location')
            job.location_type = request.POST.get('location_type')
            job.employment_type = request.POST.get('employment_type')
            job.description = request.POST.get('description')
            job.responsibilities = request.POST.get('responsibilities')
            job.requirements = request.POST.get('requirements')
            job.nice_to_have = request.POST.get('nice_to_have', '')
            job.benefits = request.POST.get('benefits', '')
            job.tech_stack = tech_stack
            job.experience_range = request.POST.get('experience_range', '')
            job.salary_range = request.POST.get('salary_range', '')
            job.is_active = request.POST.get('is_active') == 'on'
            job.closes_at = closes_at
            job.save()
            
            messages.success(request, f'Job "{job.title}" updated successfully!')
            return redirect('careers:admin_jobs_dashboard')
            
        except Exception as e:
            logger.error(f"Error updating job: {str(e)}")
            messages.error(request, f'Error updating job: {str(e)}')
    
    context = {
        'title': f'Edit Job - {job.title}',
        'job': job,
        'location_types': JobPosting.LOCATION_TYPES,
        'employment_types': JobPosting.EMPLOYMENT_TYPES,
    }
    
    return render(request, 'careers/admin/job_form.html', context)


@superuser_required
def admin_applications_dashboard(request):
    """Admin applications dashboard"""
    job_filter = request.GET.get('job', '')
    status_filter = request.GET.get('status', '')
    search = request.GET.get('search', '')
    
    applications = Application.objects.select_related('job', 'user', 'resume')
    
    if job_filter:
        applications = applications.filter(job_id=job_filter)
    if status_filter:
        applications = applications.filter(status=status_filter)
    if search:
        applications = applications.filter(
            Q(applicant_name__icontains=search) | 
            Q(applicant_email__icontains=search)
        )
    
    jobs = JobPosting.objects.all().order_by('title')
    
    context = {
        'title': 'Applications',
        'applications': applications,
        'jobs': jobs,
        'status_choices': Application.STATUS_CHOICES,
        'current_filters': {
            'job': job_filter,
            'status': status_filter,
            'search': search,
        },
    }
    
    return render(request, 'careers/admin/applications_dashboard.html', context)


@superuser_required
def admin_application_detail(request, application_id):
    """Admin view of application details"""
    application = get_object_or_404(
        Application.objects.select_related('job', 'user', 'resume', 'cover_letter'),
        id=application_id
    )
    
    notes = application.notes.select_related('author').all()
    
    context = {
        'title': f'Application - {application.applicant_name}',
        'application': application,
        'notes': notes,
        'status_choices': Application.STATUS_CHOICES,
    }
    
    return render(request, 'careers/admin/application_detail.html', context)


# ============================================
# API ENDPOINTS
# ============================================

@login_required
@require_POST
def api_submit_application(request):
    """API endpoint to submit job application"""
    try:
        # Check if it's a multipart form (file upload) or JSON
        content_type = request.content_type
        
        if 'multipart/form-data' in content_type:
            # Handle file upload submission
            job_id = request.POST.get('job_id')
            resume_id = request.POST.get('resume_id')
            cover_letter_id = request.POST.get('cover_letter_id')
            portfolio_url = request.POST.get('portfolio_url', '')
            linkedin_url = request.POST.get('linkedin_url', '')
            github_url = request.POST.get('github_url', '')
            additional_notes = request.POST.get('additional_notes', '')
            
            # Get uploaded files
            uploaded_resume = request.FILES.get('uploaded_resume')
            uploaded_cover_letter = request.FILES.get('uploaded_cover_letter')
        else:
            # Handle JSON submission
            data = json.loads(request.body)
            job_id = data.get('job_id')
            resume_id = data.get('resume_id')
            cover_letter_id = data.get('cover_letter_id')
            portfolio_url = data.get('portfolio_url', '')
            linkedin_url = data.get('linkedin_url', '')
            github_url = data.get('github_url', '')
            additional_notes = data.get('additional_notes', '')
            uploaded_resume = None
            uploaded_cover_letter = None
        
        # Validate job exists and is open
        job = get_object_or_404(JobPosting, id=job_id)
        if not job.is_open():
            return JsonResponse({
                'success': False,
                'error': 'This position is no longer accepting applications.'
            }, status=400)
        
        # Validate resume - either selected or uploaded
        resume = None
        if resume_id:
            resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        
        if not resume and not uploaded_resume:
            return JsonResponse({
                'success': False,
                'error': 'Please select or upload a resume to continue.'
            }, status=400)
        
        # Validate uploaded resume file
        if uploaded_resume:
            # Check file size (max 5MB)
            if uploaded_resume.size > 5 * 1024 * 1024:
                return JsonResponse({
                    'success': False,
                    'error': 'Resume file size must be less than 5MB.'
                }, status=400)
            
            # Check file type (PDF only)
            if not uploaded_resume.name.lower().endswith('.pdf'):
                return JsonResponse({
                    'success': False,
                    'error': 'Resume must be a PDF file.'
                }, status=400)
        
        # Get cover letter if provided
        cover_letter = None
        if cover_letter_id:
            cover_letter = get_object_or_404(
                CoverLetter, id=cover_letter_id, user=request.user
            )
        
        # Validate uploaded cover letter file
        if uploaded_cover_letter:
            if uploaded_cover_letter.size > 5 * 1024 * 1024:
                return JsonResponse({
                    'success': False,
                    'error': 'Cover letter file size must be less than 5MB.'
                }, status=400)
            
            if not uploaded_cover_letter.name.lower().endswith('.pdf'):
                return JsonResponse({
                    'success': False,
                    'error': 'Cover letter must be a PDF file.'
                }, status=400)
        
        # Validate URLs
        url_validator = URLValidator()
        for url_field, url_value in [
            ('portfolio_url', portfolio_url),
            ('linkedin_url', linkedin_url),
            ('github_url', github_url),
        ]:
            if url_value:
                try:
                    url_validator(url_value)
                except ValidationError:
                    return JsonResponse({
                        'success': False,
                        'error': f'Please enter a valid URL for {url_field.replace("_", " ")}.'
                    }, status=400)
        
        # Create application
        try:
            application = Application(
                job=job,
                user=request.user,
                resume=resume,
                cover_letter=cover_letter,
                portfolio_url=portfolio_url,
                linkedin_url=linkedin_url,
                github_url=github_url,
                additional_notes=additional_notes,
            )
            
            # Handle file uploads
            if uploaded_resume:
                application.uploaded_resume = uploaded_resume
                application.uploaded_resume_name = uploaded_resume.name
            
            if uploaded_cover_letter:
                application.uploaded_cover_letter = uploaded_cover_letter
                application.uploaded_cover_letter_name = uploaded_cover_letter.name
            
            application.save()
            
        except IntegrityError:
            return JsonResponse({
                'success': False,
                'error': 'You have already applied to this position.'
            }, status=400)
        
        return JsonResponse({
            'success': True,
            'message': 'Your application has been submitted!',
            'job_title': job.title,
            'applied_at': application.applied_at.strftime('%B %d, %Y'),
            'redirect_url': f'/careers/my-applications/{application.id}/',
        })
        
    except Exception as e:
        logger.error(f"Error submitting application: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@superuser_required
@require_POST
def api_update_application_status(request, application_id):
    """API endpoint to update application status"""
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        
        # Validate status
        valid_statuses = [s[0] for s in Application.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return JsonResponse({
                'success': False,
                'error': 'Invalid status value.'
            }, status=400)
        
        application = get_object_or_404(Application, id=application_id)
        application.status = new_status
        application.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Status updated to {application.get_status_display()}',
            'status': new_status,
            'status_display': application.get_status_display(),
        })
        
    except Exception as e:
        logger.error(f"Error updating application status: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@superuser_required
@require_POST
def api_add_application_note(request, application_id):
    """API endpoint to add internal note to application"""
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        if not content:
            return JsonResponse({
                'success': False,
                'error': 'Note content is required.'
            }, status=400)
        
        application = get_object_or_404(Application, id=application_id)
        
        note = ApplicationNote.objects.create(
            application=application,
            author=request.user,
            content=content,
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Note added successfully.',
            'note': {
                'id': note.id,
                'content': note.content,
                'author': note.author.username,
                'created_at': note.created_at.strftime('%B %d, %Y %H:%M'),
            }
        })
        
    except Exception as e:
        logger.error(f"Error adding application note: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@superuser_required
@require_POST
def api_toggle_job_status(request, job_id):
    """API endpoint to toggle job active status"""
    try:
        job = get_object_or_404(JobPosting, id=job_id)
        job.is_active = not job.is_active
        job.save()
        
        status_text = 'activated' if job.is_active else 'deactivated'
        
        return JsonResponse({
            'success': True,
            'message': f'Job "{job.title}" has been {status_text}.',
            'is_active': job.is_active,
        })
        
    except Exception as e:
        logger.error(f"Error toggling job status: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


# ============================================
# FILE DOWNLOAD VIEWS (Admin Only)
# ============================================

@superuser_required
def download_uploaded_resume(request, application_id):
    """Download uploaded resume file (admin only)"""
    application = get_object_or_404(Application, id=application_id)
    
    if not application.uploaded_resume:
        messages.error(request, 'No uploaded resume found for this application.')
        return redirect('careers:admin_application_detail', application_id=application_id)
    
    file_path = application.uploaded_resume.path
    filename = application.uploaded_resume_name or f'resume_{application.applicant_name}.pdf'
    
    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    except FileNotFoundError:
        messages.error(request, 'Resume file not found.')
        return redirect('careers:admin_application_detail', application_id=application_id)


@superuser_required
def download_uploaded_cover_letter(request, application_id):
    """Download uploaded cover letter file (admin only)"""
    application = get_object_or_404(Application, id=application_id)
    
    if not application.uploaded_cover_letter:
        messages.error(request, 'No uploaded cover letter found for this application.')
        return redirect('careers:admin_application_detail', application_id=application_id)
    
    file_path = application.uploaded_cover_letter.path
    filename = application.uploaded_cover_letter_name or f'cover_letter_{application.applicant_name}.pdf'
    
    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    except FileNotFoundError:
        messages.error(request, 'Cover letter file not found.')
        return redirect('careers:admin_application_detail', application_id=application_id)



@superuser_required
@require_POST
def api_delete_application(request, application_id):
    """API endpoint to delete an application (admin only)"""
    try:
        application = get_object_or_404(Application, id=application_id)
        
        applicant_name = application.applicant_name
        job_title = application.job.title
        
        # Delete uploaded files if they exist
        if application.uploaded_resume:
            try:
                application.uploaded_resume.delete(save=False)
            except Exception as e:
                logger.warning(f"Could not delete uploaded resume: {e}")
        
        if application.uploaded_cover_letter:
            try:
                application.uploaded_cover_letter.delete(save=False)
            except Exception as e:
                logger.warning(f"Could not delete uploaded cover letter: {e}")
        
        # Delete the application
        application.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Application from {applicant_name} for {job_title} has been deleted.',
        })
        
    except Exception as e:
        logger.error(f"Error deleting application: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
