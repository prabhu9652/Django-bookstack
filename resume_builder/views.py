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
    """Display available resume templates with role selection"""
    templates = ResumeTemplate.objects.filter(is_active=True)
    
    # Role options for the user to select
    role_options = [
        {
            'id': 'devops_sre',
            'name': 'DevOps / SRE Engineer',
            'icon': 'fas fa-server',
            'description': 'Infrastructure automation, CI/CD, cloud platforms, Kubernetes, monitoring & observability',
            'skills_preview': ['AWS', 'Terraform', 'Kubernetes', 'Docker', 'GitHub Actions', 'Prometheus']
        },
        {
            'id': 'software_engineer',
            'name': 'Software Engineer',
            'icon': 'fas fa-code',
            'description': 'Backend/frontend development, APIs, databases, system design, clean architecture',
            'skills_preview': ['Python', 'JavaScript', 'React', 'Node.js', 'PostgreSQL', 'REST APIs']
        },
        {
            'id': 'ds_ml',
            'name': 'DS / ML Engineer',
            'icon': 'fas fa-brain',
            'description': 'Machine learning, data pipelines, model training, deployment, analytics',
            'skills_preview': ['Python', 'TensorFlow', 'PyTorch', 'Pandas', 'Scikit-learn', 'MLflow']
        },
    ]
    
    context = {
        'title': 'Choose Resume Template',
        'templates': templates,
        'role_options': role_options,
    }
    
    return render(request, 'resume_builder/resume_templates.html', context)


@login_required
def create_resume_direct(request):
    """Create a new resume directly without template selection - goes straight to editor"""
    # Get or create a default template
    template = ResumeTemplate.objects.filter(is_active=True).first()
    if not template:
        # Create a default template if none exists
        template = ResumeTemplate.objects.create(
            name='Professional',
            slug='professional',
            category='professional',
            description='Clean, professional resume template',
            html_template='',
            css_styles='',
            is_active=True
        )
    
    # Default role
    role = request.GET.get('role', 'devops_sre')
    
    # Create the resume with defaults
    resume = Resume.objects.create(
        user=request.user,
        template=template,
        title='My Resume',
        role=role,
        full_name=f'{request.user.first_name} {request.user.last_name}'.strip() or request.user.username,
        role_title=get_default_role_title(role),
        email=request.user.email or '',
        phone='',
        address='',
        linkedin='',
        github='',
        summary=get_default_summary_for_role(role),
        skills=get_default_skills_for_role(role),
        experience=[get_default_experience_for_role(role)],
        education=[{
            'degree': 'Bachelor of Technology',
            'field': 'Computer Science',
            'school': 'University Name',
            'graduation_date': '2020'
        }],
        languages=['English'],
    )
    
    messages.success(request, 'Resume created! Start editing below.')
    return redirect('resume_builder:edit_resume', resume_id=resume.id)


@login_required
def create_cover_letter_direct(request):
    """Create a new cover letter directly without template selection - goes straight to editor"""
    # Get or create a default template
    template = CoverLetterTemplate.objects.filter(is_active=True).first()
    if not template:
        # Create a default template if none exists
        template = CoverLetterTemplate.objects.create(
            name='Professional',
            slug='professional',
            tone='professional',
            description='Clean, professional cover letter template',
            html_template='',
            css_styles='',
            is_active=True
        )
    
    # Create the cover letter with defaults
    cover_letter = CoverLetter.objects.create(
        user=request.user,
        template=template,
        title='My Cover Letter',
        full_name=f'{request.user.first_name} {request.user.last_name}'.strip() or request.user.username,
        email=request.user.email or '',
        phone='',
        address='',
        company_name='Company Name',
        position_title='Position Title',
        hiring_manager='',
        opening_paragraph='I am writing to express my strong interest in the [Position] role at [Company]. With my extensive experience in cloud infrastructure, DevOps practices, and site reliability engineering, I am confident in my ability to contribute significantly to your team.',
        body_paragraph='In my current role, I have successfully:\n\n• Architected and implemented scalable cloud infrastructure on AWS\n• Designed CI/CD pipelines reducing deployment time by 70%\n• Led initiatives improving system reliability to 99.9% uptime\n• Mentored team members on DevOps best practices',
        closing_paragraph='I am excited about the opportunity to bring my skills and experience to your organization. I would welcome the chance to discuss how I can contribute to your team\'s success.\n\nThank you for considering my application.',
    )
    
    messages.success(request, 'Cover letter created! Start editing below.')
    return redirect('resume_builder:edit_cover_letter', cover_letter_id=cover_letter.id)


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
    """Create a new resume with role selection"""
    template = get_object_or_404(ResumeTemplate, id=template_id, is_active=True)
    
    if request.method == 'POST':
        try:
            role = request.POST.get('role', 'software_engineer')
            
            # Get default skills structure based on role
            default_skills = get_default_skills_for_role(role)
            
            with transaction.atomic():
                resume = Resume.objects.create(
                    user=request.user,
                    template=template,
                    title=request.POST.get('title', f'My {template.name} Resume'),
                    role=role,
                    full_name=request.POST.get('full_name', f'{request.user.first_name} {request.user.last_name}'.strip() or request.user.username),
                    role_title=get_default_role_title(role),
                    email=request.POST.get('email', request.user.email),
                    phone=request.POST.get('phone', ''),
                    location=request.POST.get('location', ''),
                    linkedin=request.POST.get('linkedin', ''),
                    github=request.POST.get('github', ''),
                    website=request.POST.get('website', ''),
                    summary=get_default_summary_for_role(role),
                    skills=default_skills,
                    experience=[get_default_experience_for_role(role)],
                    education=[{
                        'degree': 'Bachelor of Technology',
                        'field': 'Computer Science',
                        'school': 'University Name',
                        'location': 'City, Country',
                        'graduation_date': '2020'
                    }],
                    projects=[],
                    languages=['English'],
                    certifications=[]
                )
                messages.success(request, 'Resume created successfully!')
                return redirect('resume_builder:edit_resume', resume_id=resume.id)
        except Exception as e:
            messages.error(request, f'Error creating resume: {str(e)}')
    
    context = {
        'title': f'Create Resume - {template.name}',
        'template': template,
        'role': request.GET.get('role', 'software_engineer'),
    }
    
    return render(request, 'resume_builder/create_resume.html', context)


def get_default_role_title(role):
    """Get default role title based on selected role"""
    titles = {
        'devops_sre': 'Senior DevOps / SRE Engineer',
        'software_engineer': 'Senior Software Engineer',
        'ds_ml': 'Senior Data Scientist / ML Engineer',
    }
    return titles.get(role, 'Software Professional')


def get_default_skills_for_role(role):
    """Get default skills list based on role"""
    if role == 'devops_sre':
        return [
            'AWS', 'Azure', 'GCP', 'DigitalOcean',
            'AWS Migration', 'Terraform', 'Terragrunt',
            'Shell scripting', 'Docker',
            'Kubernetes (K8s, EKS, AKS, GKE)',
            'Jenkins', 'Ansible', 'Puppet', 'Packer',
            'Python', 'GIT', 'Github', 'Bitbucket',
            'GitLab', 'Bamboo', 'GitLab CI/CD', 'GitHub Actions'
        ]
    elif role == 'software_engineer':
        return [
            'Python', 'JavaScript', 'TypeScript', 'Java', 'Go',
            'React', 'Vue.js', 'Node.js', 'Django', 'FastAPI',
            'PostgreSQL', 'MySQL', 'MongoDB', 'Redis',
            'REST APIs', 'GraphQL', 'Docker', 'Kubernetes',
            'Git', 'CI/CD', 'AWS', 'System Design'
        ]
    elif role == 'ds_ml':
        return [
            'Python', 'R', 'SQL', 'Scala',
            'TensorFlow', 'PyTorch', 'Scikit-learn', 'Keras',
            'Pandas', 'NumPy', 'Spark', 'Airflow',
            'AWS SageMaker', 'MLflow', 'Docker',
            'Matplotlib', 'Seaborn', 'Tableau',
            'PostgreSQL', 'MongoDB', 'BigQuery'
        ]
    return []


def get_default_summary_for_role(role):
    """Get default professional summary based on role"""
    if role == 'devops_sre':
        return """Results-driven DevOps/SRE Engineer with 5+ years of experience designing and implementing scalable cloud infrastructure, CI/CD pipelines, and observability solutions. Expert in AWS, Kubernetes, Terraform, and GitOps practices. Proven track record of reducing deployment times by 70%, achieving 99.9% uptime SLAs, and implementing infrastructure-as-code across multi-cloud environments. Passionate about automation, reliability engineering, and enabling development teams to ship faster with confidence."""
    elif role == 'software_engineer':
        return """Senior Software Engineer with 5+ years of experience building scalable, high-performance applications. Proficient in full-stack development with expertise in Python, JavaScript, and cloud-native architectures. Strong background in system design, API development, and microservices. Committed to writing clean, maintainable code and implementing best practices in software development lifecycle."""
    elif role == 'ds_ml':
        return """Data Scientist / ML Engineer with 5+ years of experience developing and deploying machine learning models at scale. Expert in Python, TensorFlow, and PyTorch with a strong foundation in statistical analysis and data engineering. Proven ability to translate business requirements into ML solutions, achieving significant improvements in prediction accuracy and operational efficiency. Experienced in MLOps practices and end-to-end ML pipeline development."""
    return "Professional summary goes here..."


def get_default_experience_for_role(role):
    """Get default experience entry based on role"""
    if role == 'devops_sre':
        return {
            'company': 'Tech Company',
            'role': 'Senior DevOps Engineer',
            'location': 'City, Country',
            'start_date': '2022',
            'end_date': 'Present',
            'bullets': [
                'Architected and implemented multi-region Kubernetes clusters on AWS EKS, achieving 99.99% uptime and supporting 500+ microservices',
                'Designed and deployed GitOps-based CI/CD pipelines using GitHub Actions and ArgoCD, reducing deployment time from 2 hours to 15 minutes',
                'Implemented Infrastructure as Code using Terraform and Terragrunt, managing 200+ AWS resources across 5 environments',
                'Built comprehensive observability stack with Prometheus, Grafana, and ELK, reducing MTTR by 60%',
                'Led security hardening initiatives including IAM policies, WAF rules, and secrets management with HashiCorp Vault',
                'Automated disaster recovery procedures achieving RPO of 1 hour and RTO of 30 minutes'
            ]
        }
    elif role == 'software_engineer':
        return {
            'company': 'Tech Company',
            'role': 'Senior Software Engineer',
            'location': 'City, Country',
            'start_date': '2022',
            'end_date': 'Present',
            'bullets': [
                'Designed and implemented RESTful APIs serving 10M+ daily requests with 99.9% availability',
                'Led migration from monolithic architecture to microservices, improving scalability and deployment frequency',
                'Optimized database queries and implemented caching strategies, reducing API response times by 40%',
                'Mentored junior developers and conducted code reviews to maintain high code quality standards',
                'Implemented comprehensive test coverage achieving 85%+ code coverage across all services'
            ]
        }
    elif role == 'ds_ml':
        return {
            'company': 'Tech Company',
            'role': 'Senior ML Engineer',
            'location': 'City, Country',
            'start_date': '2022',
            'end_date': 'Present',
            'bullets': [
                'Developed and deployed production ML models serving 5M+ predictions daily with 99.5% uptime',
                'Built end-to-end ML pipelines using Airflow and MLflow, reducing model deployment time by 70%',
                'Implemented A/B testing framework for ML models, enabling data-driven model selection',
                'Optimized model inference latency from 200ms to 50ms through model quantization and optimization',
                'Collaborated with product teams to translate business requirements into ML solutions'
            ]
        }
    return {
        'company': 'Company Name',
        'role': 'Job Title',
        'location': 'City, Country',
        'start_date': '2022',
        'end_date': 'Present',
        'bullets': ['Achievement 1', 'Achievement 2', 'Achievement 3']
    }


@login_required
def edit_resume(request, resume_id):
    """Edit an existing resume with role-aware sections"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == 'POST':
        try:
            # Handle file upload
            if 'profile_photo' in request.FILES:
                resume.profile_photo = request.FILES['profile_photo']
            
            # Update resume fields
            resume.title = request.POST.get('title', resume.title)
            resume.role = request.POST.get('role', resume.role)
            resume.primary_color = request.POST.get('primary_color', resume.primary_color)
            resume.full_name = request.POST.get('full_name', resume.full_name)
            resume.role_title = request.POST.get('role_title', resume.role_title)
            resume.email = request.POST.get('email', resume.email)
            resume.phone = request.POST.get('phone', resume.phone)
            resume.address = request.POST.get('address', resume.address)
            resume.location = request.POST.get('location', resume.location)
            resume.linkedin = request.POST.get('linkedin', resume.linkedin)
            resume.github = request.POST.get('github', resume.github)
            resume.website = request.POST.get('website', resume.website)
            resume.summary = request.POST.get('summary', resume.summary)
            
            # Handle JSON fields
            if 'experience' in request.POST:
                resume.experience = json.loads(request.POST.get('experience', '[]'))
            if 'education' in request.POST:
                resume.education = json.loads(request.POST.get('education', '[]'))
            if 'skills' in request.POST:
                resume.skills = json.loads(request.POST.get('skills', '[]'))
            if 'projects' in request.POST:
                resume.projects = json.loads(request.POST.get('projects', '[]'))
            if 'languages' in request.POST:
                resume.languages = json.loads(request.POST.get('languages', '[]'))
            if 'certifications' in request.POST:
                resume.certifications = json.loads(request.POST.get('certifications', '[]'))
            
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
                messages.error(request, f'Error updating resume: {str(e)}')
    
    # Color options for the theme picker
    color_options = [
        {'name': 'Teal', 'value': '#4a9d9a'},
        {'name': 'Navy', 'value': '#1e3a5f'},
        {'name': 'Forest', 'value': '#2d5a3d'},
        {'name': 'Burgundy', 'value': '#722f37'},
        {'name': 'Slate', 'value': '#475569'},
        {'name': 'Purple', 'value': '#5b21b6'},
    ]
    
    context = {
        'title': f'Edit Resume - {resume.title}',
        'resume': resume,
        'color_options': color_options,
        'role_options': [
            ('devops_sre', 'DevOps / SRE Engineer'),
            ('software_engineer', 'Software Engineer'),
            ('ds_ml', 'DS / ML Engineer'),
        ],
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
    """Download resume as HTML with professional styling matching the preview"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    # Generate professional HTML resume
    html_content = generate_resume_html(resume, request)
    
    # Create response
    response = HttpResponse(html_content, content_type='text/html')
    filename = f"{resume.full_name.replace(' ', '_')}_Resume.html"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


def generate_resume_html(resume, request=None):
    """Generate a professional HTML resume matching the preview design"""
    
    primary_color = resume.primary_color or '#4a9d9a'
    
    # Profile photo
    photo_html = ''
    if resume.profile_photo:
        if request:
            photo_url = request.build_absolute_uri(resume.profile_photo.url)
        else:
            photo_url = resume.profile_photo.url
        photo_html = f'<img src="{photo_url}" alt="{resume.full_name}">'
    else:
        photo_html = '<div class="photo-placeholder">👤</div>'
    
    # Contact info
    contact_html = ''
    if resume.email:
        contact_html += f'<div class="contact-item">✉ {resume.email}</div>'
    if resume.phone:
        contact_html += f'<div class="contact-item">📞 {resume.phone}</div>'
    if resume.address:
        contact_html += f'<div class="contact-item">🏠 {resume.address}</div>'
    if resume.linkedin:
        contact_html += f'<div class="contact-item">🔗 {resume.linkedin}</div>'
    if resume.github:
        contact_html += f'<div class="contact-item">💻 {resume.github}</div>'
    
    # Skills
    skills_html = ''
    if resume.skills:
        skills_html = ''.join([f'<li>{skill}</li>' for skill in resume.skills])
    
    # Languages
    languages_html = ''
    if resume.languages:
        languages_html = f'''
        <section class="sidebar-section">
            <h2 class="sidebar-heading">LANGUAGES</h2>
            <ul class="skills-list">{''.join([f"<li>{lang}</li>" for lang in resume.languages])}</ul>
        </section>'''
    
    # Education
    education_html = ''
    if resume.education:
        edu_items = ''
        for edu in resume.education:
            field = f'<div class="edu-field">{edu.get("field", "")}</div>' if edu.get('field') else ''
            edu_items += f'''
            <div class="edu-item">
                <div class="edu-degree">{edu.get('degree', '')}</div>
                {field}
                <div class="edu-school">{edu.get('school', '')}</div>
                <div class="edu-year">{edu.get('graduation_date', '')}</div>
            </div>'''
        education_html = f'''
        <section class="sidebar-section">
            <h2 class="sidebar-heading">EDUCATION</h2>
            {edu_items}
        </section>'''
    
    # Summary
    summary_html = ''
    if resume.summary:
        summary_html = f'''
        <section class="main-section">
            <h2 class="section-heading"><span class="heading-box">PROFILE</span></h2>
            <p class="profile-text">{resume.summary}</p>
        </section>'''
    
    # Experience
    experience_html = ''
    if resume.experience:
        exp_entries = ''
        for exp in resume.experience:
            bullets_html = ''
            if exp.get('bullets'):
                bullets = ''.join([f'<li>{b.replace("**", "<strong>").replace("**", "</strong>")}</li>' for b in exp['bullets']])
                bullets_html = f'<ul class="exp-bullets">{bullets}</ul>'
            
            exp_entries += f'''
            <div class="exp-entry">
                <div class="exp-header">
                    <div class="exp-role">{exp.get('role', '')}</div>
                    <div class="exp-date">{exp.get('start_date', '')} - {exp.get('end_date', '')}</div>
                </div>
                <div class="exp-company">{exp.get('company', '')}</div>
                {bullets_html}
            </div>'''
        
        experience_html = f'''
        <section class="main-section">
            <h2 class="section-heading"><span class="heading-box">EMPLOYMENT</span></h2>
            {exp_entries}
        </section>'''
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{resume.full_name} - Resume</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', 'Roboto', Arial, sans-serif; font-size: 10pt; line-height: 1.4; color: #1a1a1a; background: #f5f5f5; }}
        .resume {{ max-width: 210mm; margin: 0 auto; background: #fff; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        
        .header {{ background: {primary_color}; color: #fff; padding: 30px 40px; display: flex; align-items: center; gap: 30px; }}
        .header-photo {{ width: 120px; height: 120px; border-radius: 50%; overflow: hidden; border: 4px solid rgba(255,255,255,0.3); flex-shrink: 0; background: rgba(255,255,255,0.1); }}
        .header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
        .photo-placeholder {{ width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 48px; }}
        .header-info {{ flex: 1; }}
        .header-name {{ font-size: 32pt; font-weight: 700; margin: 0 0 4px 0; letter-spacing: 3px; }}
        .header-role {{ font-size: 14pt; font-weight: 500; margin: 0 0 16px 0; color: rgba(255,255,255,0.9); }}
        .contact-item {{ font-size: 9.5pt; margin-bottom: 6px; color: rgba(255,255,255,0.95); }}
        
        .body {{ display: flex; }}
        .sidebar {{ width: 200px; background: #f8f9fa; padding: 24px 20px; }}
        .sidebar-section {{ margin-bottom: 24px; }}
        .sidebar-heading {{ font-size: 11pt; font-weight: 700; color: #4a9d9a; margin: 0 0 12px 0; letter-spacing: 1px; }}
        .skills-list {{ list-style: none; }}
        .skills-list li {{ font-size: 9.5pt; color: #1a1a1a; padding: 3px 0; }}
        .edu-item {{ margin-bottom: 12px; }}
        .edu-degree {{ font-weight: 600; font-size: 9.5pt; }}
        .edu-field {{ font-size: 9pt; color: #555; }}
        .edu-school {{ font-size: 9pt; color: #666; }}
        .edu-year {{ font-size: 9pt; color: #888; }}
        
        .main {{ flex: 1; padding: 24px 30px; }}
        .main-section {{ margin-bottom: 24px; }}
        .section-heading {{ font-size: 11pt; font-weight: 700; margin: 0 0 12px 0; }}
        .heading-box {{ background: {primary_color}; color: #fff; padding: 4px 12px; letter-spacing: 1px; }}
        .profile-text {{ font-size: 10pt; color: #333; text-align: justify; line-height: 1.5; }}
        
        .exp-entry {{ margin-bottom: 20px; }}
        .exp-header {{ display: flex; justify-content: space-between; margin-bottom: 2px; }}
        .exp-role {{ font-weight: 700; font-size: 11pt; }}
        .exp-date {{ font-size: 9.5pt; color: #666; }}
        .exp-company {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
        .exp-bullets {{ margin: 0; padding-left: 16px; }}
        .exp-bullets li {{ font-size: 9.5pt; color: #333; margin-bottom: 6px; line-height: 1.45; text-align: justify; }}
        .exp-bullets li strong {{ font-weight: 700; color: #1a1a1a; }}
        
        @media print {{ body {{ background: white; }} .resume {{ box-shadow: none; }} }}
    </style>
</head>
<body>
    <div class="resume">
        <header class="header">
            <div class="header-photo">{photo_html}</div>
            <div class="header-info">
                <h1 class="header-name">{resume.full_name.upper()}</h1>
                <p class="header-role">{resume.role_title or resume.get_role_display()}</p>
                <div class="header-contact">{contact_html}</div>
            </div>
        </header>
        
        <div class="body">
            <aside class="sidebar">
                <section class="sidebar-section">
                    <h2 class="sidebar-heading">SKILLS</h2>
                    <ul class="skills-list">{skills_html}</ul>
                </section>
                {languages_html}
                {education_html}
            </aside>
            
            <main class="main">
                {summary_html}
                {experience_html}
            </main>
        </div>
    </div>
</body>
</html>'''
    
    return html


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
    
    # Color options for the theme picker
    color_options = [
        {'name': 'Teal', 'value': '#4a9d9a'},
        {'name': 'Navy', 'value': '#1e3a5f'},
        {'name': 'Forest', 'value': '#2d5a3d'},
        {'name': 'Burgundy', 'value': '#722f37'},
        {'name': 'Slate', 'value': '#475569'},
        {'name': 'Purple', 'value': '#5b21b6'},
    ]
    
    context = {
        'title': f'Edit Cover Letter - {cover_letter.title}',
        'cover_letter': cover_letter,
        'color_options': color_options,
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
    """Download cover letter as HTML with professional styling"""
    cover_letter = get_object_or_404(CoverLetter, id=cover_letter_id, user=request.user)
    
    html_content = generate_cover_letter_html(cover_letter)
    
    response = HttpResponse(html_content, content_type='text/html')
    filename = f"{cover_letter.full_name.replace(' ', '_')}_Cover_Letter_{cover_letter.company_name.replace(' ', '_')}.html"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


def generate_cover_letter_html(cover_letter):
    """Generate professional HTML cover letter"""
    from datetime import date
    
    primary_color = cover_letter.primary_color or '#4a9d9a'
    today = date.today().strftime("%B %d, %Y")
    
    # Contact info
    contact_parts = []
    if cover_letter.email: contact_parts.append(cover_letter.email)
    if cover_letter.phone: contact_parts.append(cover_letter.phone)
    if cover_letter.linkedin: contact_parts.append(cover_letter.linkedin)
    contact_html = ' | '.join(contact_parts)
    
    # Body content
    body_html = ''
    if cover_letter.opening_paragraph:
        body_html += f'<p>{cover_letter.opening_paragraph}</p>'
    if cover_letter.body_paragraph:
        body_html += f'<p>{cover_letter.body_paragraph.replace(chr(10), "</p><p>")}</p>'
    if cover_letter.closing_paragraph:
        body_html += f'<p>{cover_letter.closing_paragraph}</p>'
    if cover_letter.content and not cover_letter.opening_paragraph:
        body_html = f'<div style="white-space: pre-line;">{cover_letter.content}</div>'
    
    hiring_manager = cover_letter.hiring_manager or 'Hiring Manager'
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cover_letter.full_name} - Cover Letter</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Georgia, 'Times New Roman', serif; font-size: 11pt; line-height: 1.6; color: #1a1a1a; background: #f5f5f5; }}
        .letter {{ max-width: 210mm; margin: 0 auto; background: #fff; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        .header-bar {{ height: 8px; background: {primary_color}; }}
        .header-content {{ padding: 30px 50px 20px; border-bottom: 1px solid #e5e7eb; }}
        .sender-name {{ font-size: 24pt; font-weight: 700; color: {primary_color}; margin-bottom: 8px; font-family: 'Segoe UI', Arial, sans-serif; }}
        .sender-contact {{ font-size: 10pt; color: #555; font-family: 'Segoe UI', Arial, sans-serif; }}
        .sender-address {{ margin-top: 8px; font-size: 10pt; color: #666; font-family: 'Segoe UI', Arial, sans-serif; }}
        .date {{ padding: 30px 50px 0; font-size: 10.5pt; }}
        .recipient {{ padding: 20px 50px 0; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; }}
        .subject {{ padding: 24px 50px 0; font-size: 11pt; }}
        .salutation {{ padding: 24px 50px 0; font-size: 11pt; }}
        .body {{ padding: 20px 50px; }}
        .body p {{ margin: 0 0 16px 0; text-align: justify; }}
        .closing {{ padding: 24px 50px 50px; }}
        .signature {{ font-weight: 600; font-size: 12pt; color: {primary_color}; margin-top: 30px; font-family: 'Segoe UI', Arial, sans-serif; }}
        @media print {{ body {{ background: white; }} .letter {{ box-shadow: none; }} }}
    </style>
</head>
<body>
    <div class="letter">
        <div class="header-bar"></div>
        <div class="header-content">
            <div class="sender-name">{cover_letter.full_name}</div>
            <div class="sender-contact">{contact_html}</div>
            {"<div class='sender-address'>" + cover_letter.address + "</div>" if cover_letter.address else ""}
        </div>
        
        <div class="date">{today}</div>
        
        <div class="recipient">
            {"<div class='recipient-name'>" + cover_letter.hiring_manager + "</div>" if cover_letter.hiring_manager else ""}
            <div class="company-name">{cover_letter.company_name}</div>
            {"<div style='font-size: 10pt; color: #666; margin-top: 4px;'>" + cover_letter.company_address + "</div>" if cover_letter.company_address else ""}
        </div>
        
        <div class="subject"><strong>Re: Application for {cover_letter.position_title}</strong></div>
        
        <div class="salutation">Dear {hiring_manager},</div>
        
        <div class="body">{body_html}</div>
        
        <div class="closing">
            <p>Sincerely,</p>
            <div class="signature">{cover_letter.full_name}</div>
        </div>
    </div>
</body>
</html>'''
    
    return html


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
        resume.role = data.get('role', resume.role)
        resume.role_title = data.get('role_title', resume.role_title)
        resume.primary_color = data.get('primary_color', resume.primary_color)
        resume.email = data.get('email', resume.email)
        resume.phone = data.get('phone', resume.phone)
        resume.address = data.get('address', resume.address)
        resume.location = data.get('location', resume.location)
        resume.linkedin = data.get('linkedin', resume.linkedin)
        resume.github = data.get('github', resume.github)
        resume.website = data.get('website', resume.website)
        resume.summary = data.get('summary', resume.summary)
        
        # Update JSON fields
        if 'skills' in data:
            resume.skills = data.get('skills', resume.skills)
        if 'experience' in data:
            resume.experience = data.get('experience', resume.experience)
        if 'education' in data:
            resume.education = data.get('education', resume.education)
        if 'projects' in data:
            resume.projects = data.get('projects', resume.projects)
        if 'languages' in data:
            resume.languages = data.get('languages', resume.languages)
        if 'certifications' in data:
            resume.certifications = data.get('certifications', resume.certifications)
        
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
def api_upload_photo(request, resume_id):
    """API endpoint for uploading profile photo"""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    try:
        if 'profile_photo' in request.FILES:
            resume.profile_photo = request.FILES['profile_photo']
            resume.save()
            return JsonResponse({
                'success': True,
                'message': 'Photo uploaded successfully',
                'photo_url': resume.profile_photo.url if resume.profile_photo else None
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'No photo provided'
            }, status=400)
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
        cover_letter.address = data.get('address', cover_letter.address)
        cover_letter.location = data.get('location', cover_letter.location)
        cover_letter.linkedin = data.get('linkedin', cover_letter.linkedin)
        cover_letter.company_name = data.get('company_name', cover_letter.company_name)
        cover_letter.company_address = data.get('company_address', cover_letter.company_address)
        cover_letter.position_title = data.get('position_title', cover_letter.position_title)
        cover_letter.hiring_manager = data.get('hiring_manager', cover_letter.hiring_manager)
        cover_letter.opening_paragraph = data.get('opening_paragraph', cover_letter.opening_paragraph)
        cover_letter.body_paragraph = data.get('body_paragraph', cover_letter.body_paragraph)
        cover_letter.closing_paragraph = data.get('closing_paragraph', cover_letter.closing_paragraph)
        cover_letter.primary_color = data.get('primary_color', cover_letter.primary_color)
        
        # Legacy content field
        if 'content' in data:
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

