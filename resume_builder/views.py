from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.template import Template, Context
from django.db import transaction
import json

from .models import Resume, CoverLetter, ResumeTemplate, CoverLetterTemplate


def home(request):
    """Resume Builder landing page"""
    context = {
        'title': 'Professional Resume & Cover Letter Builder',
        'resume_count': ResumeTemplate.objects.filter(is_active=True).count(),
        'cover_letter_count': CoverLetterTemplate.objects.filter(is_active=True).count(),
    }
    
    if request.user.is_authenticated:
        context.update({
            'user_resumes': Resume.objects.filter(user=request.user).count(),
            'user_cover_letters': CoverLetter.objects.filter(user=request.user).count(),
        })
    
    return render(request, 'resume_builder/home.html', context)


@login_required
def dashboard(request):
    """User dashboard showing all documents"""
    resumes = Resume.objects.filter(user=request.user)[:10]
    cover_letters = CoverLetter.objects.filter(user=request.user)[:10]
    
    context = {
        'title': 'My Documents',
        'resumes': resumes,
        'cover_letters': cover_letters,
    }
    
    return render(request, 'resume_builder/dashboard.html', context)


def resume_templates(request):
    """Display available resume templates"""
    templates = ResumeTemplate.objects.filter(is_active=True)
    
    context = {
        'title': 'Choose Resume Template',
        'templates': templates,
    }
    
    return render(request, 'resume_builder/resume_templates.html', context)


def cover_letter_templates(request):
    """Display available cover letter templates"""
    templates = CoverLetterTemplate.objects.filter(is_active=True)
    
    context = {
        'title': 'Choose Cover Letter Template',
        'templates': templates,
    }
    
    return render(request, 'resume_builder/cover_letter_templates.html', context)


@login_required
def create_resume(request, template_id):
    """Create a new resume"""
    template = get_object_or_404(ResumeTemplate, id=template_id, is_active=True)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                resume = Resume.objects.create(
                    user=request.user,
                    template=template,
                    title=request.POST.get('title', f'My {template.name} Resume'),
                    full_name=request.POST.get('full_name', f'{request.user.first_name} {request.user.last_name}'.strip() or request.user.username),
                    email=request.POST.get('email', request.user.email),
                    phone=request.POST.get('phone', ''),
                    location=request.POST.get('location', ''),
                    website=request.POST.get('website', ''),
                    linkedin=request.POST.get('linkedin', ''),
                    summary=request.POST.get('summary', 'Professional summary goes here...'),
                    experience=[{
                        'title': 'Job Title',
                        'company': 'Company Name',
                        'location': 'City, State',
                        'start_date': '2023',
                        'end_date': 'Present',
                        'description': 'Job description and achievements...'
                    }],
                    education=[{
                        'degree': 'Degree Name',
                        'school': 'University Name',
                        'location': 'City, State',
                        'graduation_date': '2023'
                    }],
                    skills=['Skill 1', 'Skill 2', 'Skill 3']
                )
                messages.success(request, 'Resume created successfully!')
                return redirect('resume_builder:edit_resume', resume_id=resume.id)
        except Exception as e:
            messages.error(request, 'Error creating resume. Please try again.')
    
    context = {
        'title': f'Create Resume - {template.name}',
        'template': template,
    }
    
    return render(request, 'resume_builder/create_resume.html', context)


@login_required
def edit_resume(request, resume_id):
    """Edit an existing resume"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == 'POST':
        try:
            # Update resume fields
            resume.title = request.POST.get('title', resume.title)
            resume.full_name = request.POST.get('full_name', resume.full_name)
            resume.email = request.POST.get('email', resume.email)
            resume.phone = request.POST.get('phone', resume.phone)
            resume.location = request.POST.get('location', resume.location)
            resume.website = request.POST.get('website', resume.website)
            resume.linkedin = request.POST.get('linkedin', resume.linkedin)
            resume.summary = request.POST.get('summary', resume.summary)
            
            # Handle JSON fields
            if 'experience' in request.POST:
                resume.experience = json.loads(request.POST.get('experience', '[]'))
            if 'education' in request.POST:
                resume.education = json.loads(request.POST.get('education', '[]'))
            if 'skills' in request.POST:
                resume.skills = json.loads(request.POST.get('skills', '[]'))
            
            resume.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Resume saved successfully!'})
            else:
                messages.success(request, 'Resume updated successfully!')
                return redirect('resume_builder:edit_resume', resume_id=resume.id)
                
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
            else:
                messages.error(request, 'Error updating resume. Please try again.')
    
    context = {
        'title': f'Edit Resume - {resume.title}',
        'resume': resume,
    }
    
    return render(request, 'resume_builder/edit_resume.html', context)


@login_required
def preview_resume(request, resume_id):
    """Preview resume"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    context = {
        'title': f'Preview - {resume.title}',
        'resume': resume,
    }
    
    return render(request, 'resume_builder/preview_resume.html', context)


@login_required
def download_resume(request, resume_id):
    """Download resume as HTML"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    # Render the resume using the template
    template = Template(resume.template.html_template)
    context = Context({
        'resume': resume,
        'css_styles': resume.template.css_styles,
    })
    rendered_html = template.render(context)
    
    # Create response
    response = HttpResponse(rendered_html, content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="{resume.title}.html"'
    
    return response


@login_required
def create_cover_letter(request, template_id):
    """Create a new cover letter"""
    template = get_object_or_404(CoverLetterTemplate, id=template_id, is_active=True)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                cover_letter = CoverLetter.objects.create(
                    user=request.user,
                    template=template,
                    title=request.POST.get('title', f'My {template.name} Cover Letter'),
                    full_name=request.POST.get('full_name', f'{request.user.first_name} {request.user.last_name}'.strip() or request.user.username),
                    email=request.POST.get('email', request.user.email),
                    phone=request.POST.get('phone', ''),
                    location=request.POST.get('location', ''),
                    company_name=request.POST.get('company_name', 'Company Name'),
                    position_title=request.POST.get('position_title', 'Position Title'),
                    hiring_manager=request.POST.get('hiring_manager', ''),
                    content=request.POST.get('content', 'Dear Hiring Manager,\n\nI am writing to express my interest in the position...\n\nSincerely,\n[Your Name]')
                )
                messages.success(request, 'Cover letter created successfully!')
                return redirect('resume_builder:edit_cover_letter', cover_letter_id=cover_letter.id)
        except Exception as e:
            messages.error(request, 'Error creating cover letter. Please try again.')
    
    context = {
        'title': f'Create Cover Letter - {template.name}',
        'template': template,
    }
    
    return render(request, 'resume_builder/create_cover_letter.html', context)


@login_required
def edit_cover_letter(request, cover_letter_id):
    """Edit an existing cover letter"""
    cover_letter = get_object_or_404(CoverLetter, id=cover_letter_id, user=request.user)
    
    context = {
        'title': f'Edit Cover Letter - {cover_letter.title}',
        'cover_letter': cover_letter,
    }
    
    return render(request, 'resume_builder/edit_cover_letter.html', context)


@login_required
def preview_cover_letter(request, cover_letter_id):
    """Preview cover letter"""
    cover_letter = get_object_or_404(CoverLetter, id=cover_letter_id, user=request.user)
    
    context = {
        'title': f'Preview - {cover_letter.title}',
        'cover_letter': cover_letter,
    }
    
    return render(request, 'resume_builder/preview_cover_letter.html', context)


@login_required
def download_cover_letter(request, cover_letter_id):
    """Download cover letter as HTML"""
    cover_letter = get_object_or_404(CoverLetter, id=cover_letter_id, user=request.user)
    
    # Render the cover letter using the template
    template = Template(cover_letter.template.html_template)
    context = Context({
        'cover_letter': cover_letter,
        'css_styles': cover_letter.template.css_styles,
    })
    rendered_html = template.render(context)
    
    # Create response
    response = HttpResponse(rendered_html, content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="{cover_letter.title}.html"'
    
    return response


@login_required
@require_POST
def delete_resume(request, resume_id):
    """Delete a resume"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    title = resume.title
    resume.delete()
    messages.success(request, f'Resume "{title}" deleted successfully.')
    return redirect('resume_builder:dashboard')


@login_required
@require_POST
def delete_cover_letter(request, cover_letter_id):
    """Delete a cover letter"""
    cover_letter = get_object_or_404(CoverLetter, id=cover_letter_id, user=request.user)
    title = cover_letter.title
    cover_letter.delete()
    messages.success(request, f'Cover letter "{title}" deleted successfully.')
    return redirect('resume_builder:dashboard')

@login_required
@require_POST
def api_save_resume(request, resume_id):
    """API endpoint for saving resume data"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    try:
        data = json.loads(request.body)
        
        # Update resume fields
        resume.full_name = data.get('full_name', resume.full_name)
        resume.email = data.get('email', resume.email)
        resume.phone = data.get('phone', resume.phone)
        resume.location = data.get('location', resume.location)
        resume.website = data.get('website', resume.website)
        resume.linkedin = data.get('linkedin', resume.linkedin)
        resume.summary = data.get('summary', resume.summary)
        
        # Update JSON fields
        resume.skills = data.get('skills', resume.skills)
        resume.experience = data.get('experience', resume.experience)
        resume.education = data.get('education', resume.education)
        
        resume.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Resume saved successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
@require_POST
def api_save_cover_letter(request, cover_letter_id):
    """API endpoint for saving cover letter data"""
    cover_letter = get_object_or_404(CoverLetter, id=cover_letter_id, user=request.user)
    
    try:
        data = json.loads(request.body)
        
        # Update cover letter fields
        cover_letter.full_name = data.get('full_name', cover_letter.full_name)
        cover_letter.email = data.get('email', cover_letter.email)
        cover_letter.phone = data.get('phone', cover_letter.phone)
        cover_letter.location = data.get('location', cover_letter.location)
        cover_letter.company_name = data.get('company_name', cover_letter.company_name)
        cover_letter.position_title = data.get('position_title', cover_letter.position_title)
        cover_letter.hiring_manager = data.get('hiring_manager', cover_letter.hiring_manager)
        cover_letter.content = data.get('content', cover_letter.content)
        
        cover_letter.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cover letter saved successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

