from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
import uuid


class JobPosting(models.Model):
    """Job posting model for careers portal"""
    
    LOCATION_TYPES = [
        ('remote', 'Remote'),
        ('onsite', 'On-site'),
        ('hybrid', 'Hybrid'),
    ]
    
    EMPLOYMENT_TYPES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    
    # Core fields
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPES, default='remote')
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES, default='full_time')
    
    # Rich text content
    description = models.TextField(help_text="Full job description")
    responsibilities = models.TextField(help_text="One responsibility per line")
    requirements = models.TextField(help_text="One requirement per line")
    nice_to_have = models.TextField(blank=True, help_text="Optional skills, one per line")
    benefits = models.TextField(blank=True, help_text="What we offer, one benefit per line")
    tech_stack = models.JSONField(default=list, blank=True, help_text="List of technologies")
    
    # Experience level
    experience_range = models.CharField(max_length=50, blank=True, help_text="e.g., 3-5 years")
    
    # Optional fields
    salary_range = models.CharField(max_length=100, blank=True)
    
    # Status and dates
    is_active = models.BooleanField(default=True)
    closes_at = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job Posting'
        verbose_name_plural = 'Job Postings'
    
    def __str__(self):
        return f"{self.title} - {self.department}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            # Handle duplicates by appending unique suffix
            counter = 1
            while JobPosting.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
                counter += 1
                if counter > 10:  # Safety limit
                    self.slug = f"{base_slug}-{uuid.uuid4().hex[:12]}"
                    break
        super().save(*args, **kwargs)
    
    def is_open(self):
        """Check if job is accepting applications"""
        if not self.is_active:
            return False
        if self.closes_at and self.closes_at < timezone.now():
            return False
        return True
    
    def get_responsibilities_list(self):
        """Return responsibilities as a list"""
        return [r.strip() for r in self.responsibilities.split('\n') if r.strip()]
    
    def get_requirements_list(self):
        """Return requirements as a list"""
        return [r.strip() for r in self.requirements.split('\n') if r.strip()]
    
    def get_nice_to_have_list(self):
        """Return nice-to-have skills as a list"""
        if not self.nice_to_have:
            return []
        return [n.strip() for n in self.nice_to_have.split('\n') if n.strip()]
    
    def get_benefits_list(self):
        """Return benefits as a list"""
        if not self.benefits:
            return []
        return [b.strip() for b in self.benefits.split('\n') if b.strip()]
    
    def get_application_count(self):
        """Return count of applications for this job"""
        return self.applications.count()



def application_resume_path(instance, filename):
    """Generate upload path for application resumes"""
    return f'applications/{instance.user.id}/resumes/{filename}'


def application_cover_letter_path(instance, filename):
    """Generate upload path for application cover letters"""
    return f'applications/{instance.user.id}/cover_letters/{filename}'


class Application(models.Model):
    """Job application model linking candidates to jobs"""
    
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    
    # Relationships
    job = models.ForeignKey(
        JobPosting, 
        on_delete=models.CASCADE, 
        related_name='applications'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='job_applications'
    )
    
    # Option 1: Link to existing Resume Builder documents
    resume = models.ForeignKey(
        'resume_builder.Resume', 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='job_applications'
    )
    cover_letter = models.ForeignKey(
        'resume_builder.CoverLetter', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='job_applications'
    )
    
    # Option 2: Direct file uploads (PDF only)
    uploaded_resume = models.FileField(
        upload_to=application_resume_path,
        null=True,
        blank=True,
        help_text="Upload resume as PDF (max 5MB)"
    )
    uploaded_resume_name = models.CharField(max_length=255, blank=True)
    
    uploaded_cover_letter = models.FileField(
        upload_to=application_cover_letter_path,
        null=True,
        blank=True,
        help_text="Upload cover letter as PDF (max 5MB)"
    )
    uploaded_cover_letter_name = models.CharField(max_length=255, blank=True)
    
    # Snapshot of user data at application time (data integrity)
    applicant_name = models.CharField(max_length=200)
    applicant_email = models.EmailField()
    
    # Optional links
    portfolio_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # Application content
    additional_notes = models.TextField(blank=True)
    
    # Status tracking
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='applied'
    )
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-applied_at']
        unique_together = ['job', 'user']  # Prevent duplicate applications
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
    
    def __str__(self):
        return f"{self.applicant_name} - {self.job.title}"
    
    def save(self, *args, **kwargs):
        # Snapshot user data on first save
        if not self.pk:
            full_name = f"{self.user.first_name} {self.user.last_name}".strip()
            self.applicant_name = full_name or self.user.username
            self.applicant_email = self.user.email
        super().save(*args, **kwargs)
    
    def get_status_color(self):
        """Return CSS color class for status badge"""
        colors = {
            'applied': 'blue',
            'under_review': 'yellow',
            'interview': 'purple',
            'rejected': 'red',
            'hired': 'green',
        }
        return colors.get(self.status, 'gray')
    
    def has_resume(self):
        """Check if application has any resume (linked or uploaded)"""
        return self.resume is not None or bool(self.uploaded_resume)
    
    def has_cover_letter(self):
        """Check if application has any cover letter (linked or uploaded)"""
        return self.cover_letter is not None or bool(self.uploaded_cover_letter)
    
    def get_resume_display_name(self):
        """Get display name for resume"""
        if self.resume:
            return self.resume.title
        elif self.uploaded_resume_name:
            return self.uploaded_resume_name
        elif self.uploaded_resume:
            return self.uploaded_resume.name.split('/')[-1]
        return None
    
    def get_cover_letter_display_name(self):
        """Get display name for cover letter"""
        if self.cover_letter:
            return self.cover_letter.title
        elif self.uploaded_cover_letter_name:
            return self.uploaded_cover_letter_name
        elif self.uploaded_cover_letter:
            return self.uploaded_cover_letter.name.split('/')[-1]
        return None



class ApplicationNote(models.Model):
    """Internal notes for applications (admin use only)"""
    
    application = models.ForeignKey(
        Application, 
        on_delete=models.CASCADE, 
        related_name='notes'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='application_notes'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Application Note'
        verbose_name_plural = 'Application Notes'
    
    def __str__(self):
        return f"Note by {self.author.username} on {self.application}"
