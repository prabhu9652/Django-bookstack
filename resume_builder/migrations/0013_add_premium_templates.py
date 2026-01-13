# Generated migration for 10 new premium ATS-compliant templates
from django.db import migrations


def add_premium_templates(apps, schema_editor):
    ResumeTemplate = apps.get_model('resume_builder', 'ResumeTemplate')
    
    templates = [
        {
            'name': 'Slate',
            'slug': 'slate',
            'category': 'modern',
            'description': 'Dark header with clean body, sophisticated typography',
            'primary_color': '#334155',
            'display_order': 17,
            'is_active': True,
        },
        {
            'name': 'Metro',
            'slug': 'metro',
            'category': 'modern',
            'description': 'Clean lines, accent sidebar, urban professional feel',
            'primary_color': '#0f766e',
            'display_order': 18,
            'is_active': True,
        },
        {
            'name': 'Horizon',
            'slug': 'horizon',
            'category': 'executive',
            'description': 'Wide header band, balanced sections, executive presence',
            'primary_color': '#1e40af',
            'display_order': 19,
            'is_active': True,
        },
        {
            'name': 'Nordic',
            'slug': 'nordic',
            'category': 'minimal',
            'description': 'Scandinavian minimalism, generous whitespace, subtle accents',
            'primary_color': '#64748b',
            'display_order': 20,
            'is_active': True,
        },
        {
            'name': 'Apex',
            'slug': 'apex',
            'category': 'executive',
            'description': 'Bold name treatment, structured sections, leadership focus',
            'primary_color': '#0c4a6e',
            'display_order': 21,
            'is_active': True,
        },
        {
            'name': 'Clarity',
            'slug': 'clarity',
            'category': 'professional',
            'description': 'Crystal clear hierarchy, perfect readability, ATS optimized',
            'primary_color': '#059669',
            'display_order': 22,
            'is_active': True,
        },
        {
            'name': 'Prestige',
            'slug': 'prestige',
            'category': 'executive',
            'description': 'Premium feel, refined typography, senior-level positioning',
            'primary_color': '#7c3aed',
            'display_order': 23,
            'is_active': True,
        },
        {
            'name': 'Streamline',
            'slug': 'streamline',
            'category': 'modern',
            'description': 'Flowing layout, smooth transitions, contemporary design',
            'primary_color': '#0891b2',
            'display_order': 24,
            'is_active': True,
        },
        {
            'name': 'Foundation',
            'slug': 'foundation',
            'category': 'professional',
            'description': 'Solid structure, traditional excellence, timeless appeal',
            'primary_color': '#374151',
            'display_order': 25,
            'is_active': True,
        },
        {
            'name': 'Zenith',
            'slug': 'zenith',
            'category': 'executive',
            'description': 'Peak professional design, commanding presence, top-tier layout',
            'primary_color': '#1f2937',
            'display_order': 26,
            'is_active': True,
        },
    ]
    
    for template_data in templates:
        ResumeTemplate.objects.create(**template_data)


def remove_premium_templates(apps, schema_editor):
    ResumeTemplate = apps.get_model('resume_builder', 'ResumeTemplate')
    slugs = ['slate', 'metro', 'horizon', 'nordic', 'apex', 'clarity', 'prestige', 'streamline', 'foundation', 'zenith']
    ResumeTemplate.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('resume_builder', '0012_add_new_templates'),
    ]

    operations = [
        migrations.RunPython(add_premium_templates, remove_premium_templates),
    ]
