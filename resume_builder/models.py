from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import json


class ResumeTemplate(models.Model):
    """Resume templates with different styles"""
    CATEGORIES = [
        ('professional', 'Professional'),
        ('modern', 'Modern'),
        ('creative', 'Creative'),
        ('minimal', 'Minimal'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, default='professional')
    description = models.TextField()
    html_template = models.TextField()
    css_styles = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Color scheme
    primary_color = models.CharField(max_length=7, default='#4a9d9a', help_text='Primary color hex code')
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CoverLetterTemplate(models.Model):
    """Cover letter templates with different tones"""
    TONES = [
        ('formal', 'Formal'),
        ('professional', 'Professional'),
        ('friendly', 'Friendly'),
        ('modern', 'Modern'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    tone = models.CharField(max_length=20, choices=TONES, default='professional')
    description = models.TextField()
    html_template = models.TextField()
    css_styles = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Color scheme
    primary_color = models.CharField(max_length=7, default='#4a9d9a', help_text='Primary color hex code')
    
    class Meta:
        ordering = ['tone', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_tone_display()})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Resume(models.Model):
    """User's resume documents"""
    
    ROLE_CHOICES = [
        ('devops_sre', 'DevOps / SRE Engineer'),
        ('software_engineer', 'Software Engineer'),
        ('ds_ml', 'DS / ML Engineer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    template = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="My Resume")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='software_engineer')
    
    # Profile Photo
    profile_photo = models.ImageField(upload_to='resume_photos/', blank=True, null=True)
    
    # Color Theme
    primary_color = models.CharField(max_length=7, default='#4a9d9a', help_text='Header/accent color')
    
    # Personal Information (Header)
    full_name = models.CharField(max_length=100)
    role_title = models.CharField(max_length=100, blank=True, help_text="e.g., Senior DevOps Engineer")
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True, help_text="Full address")
    location = models.CharField(max_length=100, blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    website = models.URLField(blank=True)
    
    # Skills - Simple list for left sidebar
    skills = models.JSONField(default=list)
    
    # Profile/Summary (4-6 lines, role-specific)
    summary = models.TextField(blank=True)
    
    # Experience - Achievement-driven bullet points
    experience = models.JSONField(default=list)
    
    # Projects (Optional)
    projects = models.JSONField(default=list)
    
    # Education
    education = models.JSONField(default=list)
    
    # Languages
    languages = models.JSONField(default=list)
    
    # Certifications (Optional)
    certifications = models.JSONField(default=list)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def get_role_display_title(self):
        """Get the display title based on role"""
        role_titles = {
            'devops_sre': 'DevOps / SRE Engineer',
            'software_engineer': 'Software Engineer',
            'ds_ml': 'Data Science / ML Engineer',
        }
        return self.role_title or role_titles.get(self.role, 'Professional')


class CoverLetter(models.Model):
    """User's cover letter documents"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cover_letters')
    template = models.ForeignKey(CoverLetterTemplate, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="My Cover Letter")
    
    # Color Theme
    primary_color = models.CharField(max_length=7, default='#4a9d9a', help_text='Header/accent color')
    
    # Personal Information
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True, help_text="Full address")
    location = models.CharField(max_length=100, blank=True)
    linkedin = models.URLField(blank=True)
    
    # Company Information
    company_name = models.CharField(max_length=100)
    company_address = models.TextField(blank=True)
    position_title = models.CharField(max_length=100)
    hiring_manager = models.CharField(max_length=100, blank=True)
    
    # Content sections
    opening_paragraph = models.TextField(blank=True, help_text="Introduction and why you're applying")
    body_paragraph = models.TextField(blank=True, help_text="Your qualifications and achievements")
    closing_paragraph = models.TextField(blank=True, help_text="Call to action and closing")
    
    # Legacy content field
    content = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.title} - {self.company_name} - {self.user.username}"