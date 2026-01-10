from django.contrib import admin
from .models import ResumeTemplate, CoverLetterTemplate, Resume, CoverLetter


@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(CoverLetterTemplate)
class CoverLetterTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'tone', 'is_active', 'created_at']
    list_filter = ['tone', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'template', 'created_at', 'updated_at']
    list_filter = ['template', 'created_at']
    search_fields = ['title', 'user__username', 'full_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CoverLetter)
class CoverLetterAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'company_name', 'position_title', 'created_at', 'updated_at']
    list_filter = ['template', 'created_at']
    search_fields = ['title', 'user__username', 'company_name', 'position_title']
    readonly_fields = ['created_at', 'updated_at']