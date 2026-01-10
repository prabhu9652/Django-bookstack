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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    template = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="My Resume")
    
    # Personal Information
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    
    # Content
    summary = models.TextField(blank=True)
    experience = models.JSONField(default=list)
    education = models.JSONField(default=list)
    skills = models.JSONField(default=list)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class CoverLetter(models.Model):
    """User's cover letter documents"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cover_letters')
    template = models.ForeignKey(CoverLetterTemplate, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="My Cover Letter")
    
    # Personal Information
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    # Company Information
    company_name = models.CharField(max_length=100)
    position_title = models.CharField(max_length=100)
    hiring_manager = models.CharField(max_length=100, blank=True)
    
    # Content
    content = models.TextField()
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.title} - {self.company_name} - {self.user.username}"