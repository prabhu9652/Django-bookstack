from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.template import Template, Context
from django.db import transaction
import json
import logging

from .models import Resume, CoverLetter, ResumeTemplate, CoverLetterTemplate

logger = logging.getLogger(__name__)


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
    
    # Get role from query parameter or default
    role = request.GET.get('role', 'devops_sre')
    
    # Get role-specific cover letter content
    cover_letter_content = get_default_cover_letter_content(role)
    
    # Create the cover letter with role-specific defaults
    cover_letter = CoverLetter.objects.create(
        user=request.user,
        template=template,
        title='My Cover Letter',
        full_name=f'{request.user.first_name} {request.user.last_name}'.strip() or request.user.username,
        email=request.user.email or '',
        phone='',
        address='',
        company_name='Company Name',
        position_title=cover_letter_content['position_title'],
        hiring_manager='',
        opening_paragraph=cover_letter_content['opening_paragraph'],
        body_paragraph=cover_letter_content['body_paragraph'],
        closing_paragraph=cover_letter_content['closing_paragraph'],
    )
    
    messages.success(request, 'Cover letter created! Start editing below.')
    return redirect('resume_builder:edit_cover_letter', cover_letter_id=cover_letter.id)


def get_default_cover_letter_content(role):
    """Get industry-standard cover letter content based on role."""
    
    if role == 'devops_sre':
        return {
            'position_title': 'DevOps / SRE Engineer',
            'opening_paragraph': 'I am writing to express my strong interest in the DevOps/SRE Engineer position at your organization. With over 5 years of hands-on experience in cloud infrastructure, CI/CD automation, and site reliability engineering, I am confident in my ability to drive operational excellence and enable your engineering teams to deliver software faster and more reliably.',
            'body_paragraph': '''Throughout my career, I have developed deep expertise in designing and implementing scalable, resilient infrastructure solutions. My key accomplishments include:

• Architected and deployed multi-region Kubernetes clusters on AWS EKS, achieving 99.99% uptime while supporting 500+ microservices in production

• Designed and implemented GitOps-based CI/CD pipelines using GitHub Actions, ArgoCD, and Terraform, reducing deployment time from 2 hours to under 15 minutes

• Built comprehensive observability solutions using Prometheus, Grafana, and ELK stack, reducing Mean Time to Resolution (MTTR) by 60%

• Implemented Infrastructure as Code practices using Terraform and Terragrunt, managing 200+ AWS resources across multiple environments

• Led security hardening initiatives including IAM policies, WAF configurations, and secrets management with HashiCorp Vault

I am passionate about automation, reliability engineering, and building systems that scale. I thrive in collaborative environments where I can work closely with development teams to improve deployment velocity and system reliability.''',
            'closing_paragraph': 'I am excited about the opportunity to bring my technical expertise and passion for DevOps practices to your team. I would welcome the chance to discuss how my experience in cloud infrastructure, automation, and reliability engineering can contribute to your organization\'s success.\n\nThank you for considering my application. I look forward to the opportunity to speak with you.'
        }
    
    elif role == 'software_engineer':
        return {
            'position_title': 'Software Engineer',
            'opening_paragraph': 'I am writing to express my enthusiasm for the Software Engineer position at your organization. With over 5 years of experience in full-stack development, system design, and building scalable applications, I am eager to contribute my technical skills and problem-solving abilities to your engineering team.',
            'body_paragraph': '''Throughout my career, I have consistently delivered high-quality software solutions that drive business value. My key accomplishments include:

• Designed and implemented RESTful APIs serving 10M+ daily requests with 99.9% availability, using Python, Django, and PostgreSQL

• Led the migration from monolithic architecture to microservices, improving system scalability and reducing deployment complexity

• Optimized database queries and implemented caching strategies using Redis, reducing API response times by 40%

• Built responsive, accessible front-end applications using React and TypeScript, following modern best practices and design patterns

• Implemented comprehensive test coverage achieving 85%+ code coverage, significantly reducing production bugs

• Mentored junior developers through code reviews, pair programming, and technical documentation

I am passionate about writing clean, maintainable code and building systems that solve real-world problems. I thrive in agile environments where collaboration and continuous improvement are valued.''',
            'closing_paragraph': 'I am excited about the opportunity to contribute to your team and help build innovative software solutions. I would welcome the chance to discuss how my experience in software development and system design can add value to your organization.\n\nThank you for considering my application. I look forward to the opportunity to speak with you.'
        }
    
    elif role == 'ds_ml':
        return {
            'position_title': 'Data Scientist / ML Engineer',
            'opening_paragraph': 'I am writing to express my strong interest in the Data Scientist / ML Engineer position at your organization. With over 5 years of experience in machine learning, statistical analysis, and building production ML systems, I am excited about the opportunity to leverage data-driven insights to solve complex business problems.',
            'body_paragraph': '''Throughout my career, I have developed and deployed machine learning solutions that deliver measurable business impact. My key accomplishments include:

• Developed and deployed production ML models serving 5M+ predictions daily with 99.5% uptime, using Python, TensorFlow, and AWS SageMaker

• Built end-to-end ML pipelines using Airflow and MLflow, reducing model deployment time by 70% and enabling rapid experimentation

• Implemented recommendation systems that increased user engagement by 25% and drove significant revenue growth

• Optimized model inference latency from 200ms to 50ms through model quantization, pruning, and efficient serving infrastructure

• Designed A/B testing frameworks for ML models, enabling data-driven model selection and continuous improvement

• Collaborated with product and engineering teams to translate business requirements into ML solutions, ensuring alignment with organizational goals

I am passionate about applying machine learning to solve real-world problems and building scalable ML systems. I stay current with the latest research and best practices in the rapidly evolving field of AI/ML.''',
            'closing_paragraph': 'I am excited about the opportunity to bring my expertise in machine learning and data science to your team. I would welcome the chance to discuss how my experience in building production ML systems can contribute to your organization\'s data-driven initiatives.\n\nThank you for considering my application. I look forward to the opportunity to speak with you.'
        }
    
    # Default fallback
    return {
        'position_title': 'Position Title',
        'opening_paragraph': 'I am writing to express my strong interest in the position at your organization. With my extensive experience and proven track record of success, I am confident in my ability to contribute significantly to your team.',
        'body_paragraph': '''Throughout my career, I have consistently delivered results and demonstrated my commitment to excellence. My key accomplishments include:

• Successfully led and delivered multiple high-impact projects on time and within budget

• Collaborated effectively with cross-functional teams to achieve organizational goals

• Continuously improved processes and implemented best practices

• Mentored team members and contributed to a positive team culture

I am passionate about my work and committed to continuous learning and professional growth.''',
        'closing_paragraph': 'I am excited about the opportunity to bring my skills and experience to your organization. I would welcome the chance to discuss how I can contribute to your team\'s success.\n\nThank you for considering my application. I look forward to the opportunity to speak with you.'
    }


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
    """Download resume as high-quality PDF using WeasyPrint."""
    from .pdf_generator import generate_resume_pdf
    
    try:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        
        # Generate PDF
        pdf_bytes = generate_resume_pdf(resume, request)
        
        # Return PDF response
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        safe_name = resume.full_name.replace(' ', '_').replace('/', '_')
        response['Content-Disposition'] = f'attachment; filename="{safe_name}_Resume.pdf"'
        return response
        
    except Exception as e:
        logger.error(f"PDF generation failed for resume {resume_id}: {str(e)}")
        return HttpResponse(f"PDF generation failed: {str(e)}", content_type='text/plain', status=500)


@login_required
def create_cover_letter(request, template_id):
    """Create a new cover letter with role-based default content"""
    template = get_object_or_404(CoverLetterTemplate, id=template_id, is_active=True)
    
    if request.method == 'POST':
        try:
            # Get role from form or default
            role = request.POST.get('role', 'devops_sre')
            cover_letter_content = get_default_cover_letter_content(role)
            
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
                    position_title=request.POST.get('position_title', cover_letter_content['position_title']),
                    hiring_manager=request.POST.get('hiring_manager', ''),
                    opening_paragraph=cover_letter_content['opening_paragraph'],
                    body_paragraph=cover_letter_content['body_paragraph'],
                    closing_paragraph=cover_letter_content['closing_paragraph'],
                )
                messages.success(request, 'Cover letter created successfully!')
                return redirect('resume_builder:edit_cover_letter', cover_letter_id=cover_letter.id)
        except Exception as e:
            messages.error(request, 'Error creating cover letter. Please try again.')
    
    # GET request - show role selection
    role = request.GET.get('role', 'devops_sre')
    
    # Role options for selection
    role_options = [
        {
            'id': 'devops_sre',
            'name': 'DevOps / SRE Engineer',
            'icon': 'fas fa-server',
            'description': 'Cloud infrastructure, CI/CD, Kubernetes, observability'
        },
        {
            'id': 'software_engineer',
            'name': 'Software Engineer',
            'icon': 'fas fa-code',
            'description': 'Full-stack development, APIs, system design'
        },
        {
            'id': 'ds_ml',
            'name': 'DS / ML Engineer',
            'icon': 'fas fa-brain',
            'description': 'Machine learning, data pipelines, MLOps'
        },
    ]
    
    context = {
        'title': f'Create Cover Letter - {template.name}',
        'template': template,
        'role': role,
        'role_options': role_options,
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
    """Download cover letter as high-quality PDF using WeasyPrint."""
    from .pdf_generator import generate_cover_letter_pdf
    
    try:
        cover_letter = get_object_or_404(CoverLetter, id=cover_letter_id, user=request.user)
        
        # Generate PDF
        pdf_bytes = generate_cover_letter_pdf(cover_letter)
        
        # Return PDF response
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        safe_name = cover_letter.full_name.replace(' ', '_').replace('/', '_')
        safe_company = cover_letter.company_name.replace(' ', '_').replace('/', '_')
        response['Content-Disposition'] = f'attachment; filename="{safe_name}_Cover_Letter_{safe_company}.pdf"'
        return response
        
    except Exception as e:
        logger.error(f"PDF generation failed for cover letter {cover_letter_id}: {str(e)}")
        return HttpResponse(f"PDF generation failed: {str(e)}", content_type='text/plain', status=500)


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

