from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class RoadmapPath(models.Model):
    """
    Represents a career roadmap path (DevOps/SRE, Full-Stack Development, DSML)
    """
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    subtitle = models.CharField(max_length=200)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, default='fas fa-route')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    estimated_duration = models.CharField(max_length=50)  # e.g., "12-18 months"
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Roadmap Path'
        verbose_name_plural = 'Roadmap Paths'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('roadmap:path_detail', kwargs={'slug': self.slug})


class RoadmapPhase(models.Model):
    """
    Represents a phase within a roadmap path (e.g., Foundation, Intermediate, Advanced)
    """
    roadmap_path = models.ForeignKey(RoadmapPath, on_delete=models.CASCADE, related_name='phases')
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=50)  # e.g., "3-4 months"
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['roadmap_path', 'order']
        unique_together = ['roadmap_path', 'order']
        verbose_name = 'Roadmap Phase'
        verbose_name_plural = 'Roadmap Phases'
    
    def __str__(self):
        return f"{self.roadmap_path.name} - {self.name}"


class RoadmapSkill(models.Model):
    """
    Represents individual skills within a roadmap phase
    """
    phase = models.ForeignKey(RoadmapPhase, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_core = models.BooleanField(default=True)  # Core vs optional skill
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['phase', 'order']
        unique_together = ['phase', 'order']
        verbose_name = 'Roadmap Skill'
        verbose_name_plural = 'Roadmap Skills'
    
    def __str__(self):
        return f"{self.phase.name} - {self.name}"


class UserProgress(models.Model):
    """
    Tracks user progress through roadmap paths and skills
    """
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roadmap_progress')
    roadmap_path = models.ForeignKey(RoadmapPath, on_delete=models.CASCADE)
    skill = models.ForeignKey(RoadmapSkill, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'roadmap_path', 'skill']
        verbose_name = 'User Progress'
        verbose_name_plural = 'User Progress'
    
    def __str__(self):
        skill_name = self.skill.name if self.skill else "Overall"
        return f"{self.user.username} - {self.roadmap_path.name} - {skill_name}"


class RoadmapHighlight(models.Model):
    """
    Key highlights/features for each roadmap path (displayed on cards)
    """
    roadmap_path = models.ForeignKey(RoadmapPath, on_delete=models.CASCADE, related_name='highlights')
    title = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=50, default='fas fa-check')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['roadmap_path', 'order']
        unique_together = ['roadmap_path', 'order']
        verbose_name = 'Roadmap Highlight'
        verbose_name_plural = 'Roadmap Highlights'
    
    def __str__(self):
        return f"{self.roadmap_path.name} - {self.title}"