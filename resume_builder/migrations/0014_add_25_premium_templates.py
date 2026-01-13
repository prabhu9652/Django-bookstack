# Generated migration for 25 new premium ATS-compliant templates
from django.db import migrations


def add_premium_templates(apps, schema_editor):
    ResumeTemplate = apps.get_model('resume_builder', 'ResumeTemplate')
    
    templates = [
        # Category: Executive/Leadership (5 templates)
        {
            'name': 'Monarch',
            'slug': 'monarch',
            'category': 'executive',
            'description': 'Commanding presence with bold header, ideal for C-suite and directors',
            'primary_color': '#1e3a5f',
            'display_order': 27,
            'is_active': True,
        },
        {
            'name': 'Summit',
            'slug': 'summit',
            'category': 'executive',
            'description': 'Peak professional design with elegant hierarchy for senior leaders',
            'primary_color': '#2d3748',
            'display_order': 28,
            'is_active': True,
        },
        {
            'name': 'Regent',
            'slug': 'regent',
            'category': 'executive',
            'description': 'Refined serif typography with classic executive appeal',
            'primary_color': '#4a5568',
            'display_order': 29,
            'is_active': True,
        },
        {
            'name': 'Pinnacle',
            'slug': 'pinnacle',
            'category': 'executive',
            'description': 'Top-tier layout with commanding name treatment',
            'primary_color': '#1a365d',
            'display_order': 30,
            'is_active': True,
        },
        {
            'name': 'Dynasty',
            'slug': 'dynasty',
            'category': 'executive',
            'description': 'Prestigious design with refined spacing for executives',
            'primary_color': '#2c5282',
            'display_order': 31,
            'is_active': True,
        },
        
        # Category: Technical/Engineering (5 templates)
        {
            'name': 'Circuit',
            'slug': 'circuit',
            'category': 'technical',
            'description': 'Clean technical layout with monospace accents for engineers',
            'primary_color': '#2b6cb0',
            'display_order': 32,
            'is_active': True,
        },
        {
            'name': 'Matrix',
            'slug': 'matrix',
            'category': 'technical',
            'description': 'Grid-based structure optimized for technical roles',
            'primary_color': '#276749',
            'display_order': 33,
            'is_active': True,
        },
        {
            'name': 'Quantum',
            'slug': 'quantum',
            'category': 'technical',
            'description': 'Modern tech aesthetic with skills-first layout',
            'primary_color': '#5a67d8',
            'display_order': 34,
            'is_active': True,
        },
        {
            'name': 'Binary',
            'slug': 'binary',
            'category': 'technical',
            'description': 'Minimalist developer-focused design with code aesthetics',
            'primary_color': '#319795',
            'display_order': 35,
            'is_active': True,
        },
        {
            'name': 'Stack',
            'slug': 'stack',
            'category': 'technical',
            'description': 'Full-stack friendly layout with prominent tech skills',
            'primary_color': '#3182ce',
            'display_order': 36,
            'is_active': True,
        },
        
        # Category: Modern/Contemporary (5 templates)
        {
            'name': 'Prism',
            'slug': 'prism',
            'category': 'modern',
            'description': 'Light and airy design with subtle color accents',
            'primary_color': '#667eea',
            'display_order': 37,
            'is_active': True,
        },
        {
            'name': 'Nova',
            'slug': 'nova',
            'category': 'modern',
            'description': 'Fresh contemporary style with dynamic spacing',
            'primary_color': '#ed8936',
            'display_order': 38,
            'is_active': True,
        },
        {
            'name': 'Pulse',
            'slug': 'pulse',
            'category': 'modern',
            'description': 'Energetic layout with modern typography',
            'primary_color': '#e53e3e',
            'display_order': 39,
            'is_active': True,
        },
        {
            'name': 'Flux',
            'slug': 'flux',
            'category': 'modern',
            'description': 'Flowing design with seamless section transitions',
            'primary_color': '#38b2ac',
            'display_order': 40,
            'is_active': True,
        },
        {
            'name': 'Vertex',
            'slug': 'vertex',
            'category': 'modern',
            'description': 'Sharp, angular design with bold section headers',
            'primary_color': '#805ad5',
            'display_order': 41,
            'is_active': True,
        },
        
        # Category: Minimal/Clean (5 templates)
        {
            'name': 'Zen',
            'slug': 'zen',
            'category': 'minimal',
            'description': 'Maximum whitespace with peaceful, focused layout',
            'primary_color': '#718096',
            'display_order': 42,
            'is_active': True,
        },
        {
            'name': 'Pure',
            'slug': 'pure',
            'category': 'minimal',
            'description': 'Ultra-clean single column with perfect typography',
            'primary_color': '#4a5568',
            'display_order': 43,
            'is_active': True,
        },
        {
            'name': 'Essence',
            'slug': 'essence',
            'category': 'minimal',
            'description': 'Distilled design focusing on content clarity',
            'primary_color': '#2d3748',
            'display_order': 44,
            'is_active': True,
        },
        {
            'name': 'Canvas',
            'slug': 'canvas',
            'category': 'minimal',
            'description': 'Blank slate aesthetic with subtle structure',
            'primary_color': '#1a202c',
            'display_order': 45,
            'is_active': True,
        },
        {
            'name': 'Whisper',
            'slug': 'whisper',
            'category': 'minimal',
            'description': 'Soft, understated elegance with light typography',
            'primary_color': '#a0aec0',
            'display_order': 46,
            'is_active': True,
        },
        
        # Category: Professional/Corporate (5 templates)
        {
            'name': 'Sterling',
            'slug': 'sterling',
            'category': 'professional',
            'description': 'Premium corporate design with refined details',
            'primary_color': '#2d3748',
            'display_order': 47,
            'is_active': True,
        },
        {
            'name': 'Anchor',
            'slug': 'anchor',
            'category': 'professional',
            'description': 'Solid, dependable layout for established professionals',
            'primary_color': '#1a365d',
            'display_order': 48,
            'is_active': True,
        },
        {
            'name': 'Merit',
            'slug': 'merit',
            'category': 'professional',
            'description': 'Achievement-focused design highlighting accomplishments',
            'primary_color': '#285e61',
            'display_order': 49,
            'is_active': True,
        },
        {
            'name': 'Beacon',
            'slug': 'beacon',
            'category': 'professional',
            'description': 'Guiding light design with clear visual hierarchy',
            'primary_color': '#2c5282',
            'display_order': 50,
            'is_active': True,
        },
        {
            'name': 'Keystone',
            'slug': 'keystone',
            'category': 'professional',
            'description': 'Foundational design with strong structural elements',
            'primary_color': '#744210',
            'display_order': 51,
            'is_active': True,
        },
    ]
    
    for template_data in templates:
        ResumeTemplate.objects.create(**template_data)


def remove_premium_templates(apps, schema_editor):
    ResumeTemplate = apps.get_model('resume_builder', 'ResumeTemplate')
    slugs = [
        'monarch', 'summit', 'regent', 'pinnacle', 'dynasty',
        'circuit', 'matrix', 'quantum', 'binary', 'stack',
        'prism', 'nova', 'pulse', 'flux', 'vertex',
        'zen', 'pure', 'essence', 'canvas', 'whisper',
        'sterling', 'anchor', 'merit', 'beacon', 'keystone'
    ]
    ResumeTemplate.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('resume_builder', '0013_add_premium_templates'),
    ]

    operations = [
        migrations.RunPython(add_premium_templates, remove_premium_templates),
    ]
