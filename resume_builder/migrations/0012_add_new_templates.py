# Generated migration for 10 new resume templates

from django.db import migrations


def add_new_templates(apps, schema_editor):
    """Add 10 new resume templates to database."""
    ResumeTemplate = apps.get_model('resume_builder', 'ResumeTemplate')
    
    new_templates = [
        {
            'name': 'Compact',
            'slug': 'compact',
            'description': 'Dense, information-rich single column layout. Perfect for experienced professionals with extensive content.',
            'category': 'modern',
            'primary_color': '#3b82f6',
            'display_order': 7,
            'is_ats_safe': True,
            'recommended_roles': ['software_engineer', 'devops_sre', 'backend_developer', 'full_stack_developer']
        },
        {
            'name': 'Elegant',
            'slug': 'elegant',
            'description': 'Refined serif typography with classic feel. Sophisticated design for senior professionals.',
            'category': 'classic',
            'primary_color': '#d4af37',
            'display_order': 8,
            'is_ats_safe': True,
            'recommended_roles': ['product_manager', 'software_engineer', 'data_scientist']
        },
        {
            'name': 'Bold',
            'slug': 'bold',
            'description': 'Strong visual hierarchy with impactful headers. Makes a powerful first impression.',
            'category': 'modern',
            'primary_color': '#ef4444',
            'display_order': 9,
            'is_ats_safe': True,
            'recommended_roles': ['devops_sre', 'software_engineer', 'full_stack_developer']
        },
        {
            'name': 'Classic',
            'slug': 'classic',
            'description': 'Traditional, timeless resume design. Clean and professional for any industry.',
            'category': 'classic',
            'primary_color': '#1a1a1a',
            'display_order': 10,
            'is_ats_safe': True,
            'recommended_roles': ['software_engineer', 'product_manager', 'data_scientist']
        },
        {
            'name': 'Timeline',
            'slug': 'timeline',
            'description': 'Visual timeline layout for experience. Great for showing career progression.',
            'category': 'modern',
            'primary_color': '#8b5cf6',
            'display_order': 11,
            'is_ats_safe': True,
            'recommended_roles': ['software_engineer', 'devops_sre', 'product_manager']
        },
        {
            'name': 'Infographic',
            'slug': 'infographic',
            'description': 'Data visualization style with skill bars. Eye-catching sidebar design.',
            'category': 'creative',
            'primary_color': '#06b6d4',
            'display_order': 12,
            'is_ats_safe': True,
            'recommended_roles': ['data_scientist', 'frontend_developer', 'full_stack_developer']
        },
        {
            'name': 'Corporate',
            'slug': 'corporate',
            'description': 'Professional enterprise style. Ideal for Fortune 500 and large company applications.',
            'category': 'professional',
            'primary_color': '#0f766e',
            'display_order': 13,
            'is_ats_safe': True,
            'recommended_roles': ['software_engineer', 'product_manager', 'devops_sre']
        },
        {
            'name': 'Startup',
            'slug': 'startup',
            'description': 'Modern, dynamic tech startup style. Gradient accents and contemporary design.',
            'category': 'modern',
            'primary_color': '#667eea',
            'display_order': 14,
            'is_ats_safe': True,
            'recommended_roles': ['software_engineer', 'devops_sre', 'full_stack_developer', 'frontend_developer']
        },
        {
            'name': 'Academic',
            'slug': 'academic',
            'description': 'Research and academic focused. Serif typography for scholarly applications.',
            'category': 'classic',
            'primary_color': '#1e3a5f',
            'display_order': 15,
            'is_ats_safe': True,
            'recommended_roles': ['data_scientist', 'software_engineer', 'backend_developer']
        },
        {
            'name': 'Swiss',
            'slug': 'swiss',
            'description': 'Clean Swiss/International typographic style. Minimalist grid-based design.',
            'category': 'minimal',
            'primary_color': '#374151',
            'display_order': 16,
            'is_ats_safe': True,
            'recommended_roles': ['software_engineer', 'frontend_developer', 'product_manager']
        },
    ]
    
    for template_data in new_templates:
        if not ResumeTemplate.objects.filter(slug=template_data['slug']).exists():
            ResumeTemplate.objects.create(
                name=template_data['name'],
                slug=template_data['slug'],
                description=template_data['description'],
                category=template_data['category'],
                primary_color=template_data['primary_color'],
                is_active=True,
                display_order=template_data['display_order'],
                is_ats_safe=template_data['is_ats_safe'],
                recommended_roles=template_data['recommended_roles']
            )


def remove_new_templates(apps, schema_editor):
    """Remove the new templates."""
    ResumeTemplate = apps.get_model('resume_builder', 'ResumeTemplate')
    slugs = ['compact', 'elegant', 'bold', 'classic', 'timeline', 
             'infographic', 'corporate', 'startup', 'academic', 'swiss']
    ResumeTemplate.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('resume_builder', '0011_add_technical_template'),
    ]

    operations = [
        migrations.RunPython(add_new_templates, remove_new_templates),
    ]
