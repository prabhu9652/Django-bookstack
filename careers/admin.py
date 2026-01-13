from django.contrib import admin
from .models import JobPosting, Application, ApplicationNote


class ApplicationNoteInline(admin.TabularInline):
    model = ApplicationNote
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('author', 'content', 'created_at')


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'location', 'location_type', 'employment_type', 'experience_range', 'is_active', 'application_count', 'created_at')
    list_filter = ('is_active', 'department', 'location_type', 'employment_type', 'created_at')
    search_fields = ('title', 'description', 'department', 'location')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('view_count', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'department', 'location', 'location_type', 'employment_type', 'experience_range')
        }),
        ('Job Details', {
            'fields': ('description', 'responsibilities', 'requirements', 'nice_to_have', 'tech_stack', 'salary_range')
        }),
        ('Benefits', {
            'fields': ('benefits',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'closes_at')
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def application_count(self, obj):
        return obj.applications.count()
    application_count.short_description = 'Applications'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant_name', 'job', 'status', 'has_resume_display', 'has_cover_letter_display', 'applied_at', 'updated_at')
    list_filter = ('status', 'job', 'applied_at')
    search_fields = ('applicant_name', 'applicant_email', 'job__title')
    readonly_fields = ('applied_at', 'updated_at', 'applicant_name', 'applicant_email')
    ordering = ('-applied_at',)
    inlines = [ApplicationNoteInline]
    
    fieldsets = (
        ('Applicant Info', {
            'fields': ('user', 'applicant_name', 'applicant_email')
        }),
        ('Job & Documents (Resume Builder)', {
            'fields': ('job', 'resume', 'cover_letter')
        }),
        ('Uploaded Documents', {
            'fields': ('uploaded_resume', 'uploaded_resume_name', 'uploaded_cover_letter', 'uploaded_cover_letter_name'),
            'classes': ('collapse',)
        }),
        ('Links', {
            'fields': ('portfolio_url', 'linkedin_url', 'github_url'),
            'classes': ('collapse',)
        }),
        ('Additional Info', {
            'fields': ('additional_notes',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'applied_at', 'updated_at')
        }),
    )
    
    def has_resume_display(self, obj):
        if obj.resume:
            return '✓ Builder'
        elif obj.uploaded_resume:
            return '✓ Uploaded'
        return '✗'
    has_resume_display.short_description = 'Resume'
    
    def has_cover_letter_display(self, obj):
        if obj.cover_letter:
            return '✓ Builder'
        elif obj.uploaded_cover_letter:
            return '✓ Uploaded'
        return '—'
    has_cover_letter_display.short_description = 'Cover Letter'


@admin.register(ApplicationNote)
class ApplicationNoteAdmin(admin.ModelAdmin):
    list_display = ('application', 'author', 'short_content', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'application__applicant_name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'
