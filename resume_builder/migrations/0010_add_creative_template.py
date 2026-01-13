# Generated migration for Creative Bold template

from django.db import migrations


def add_creative_template(apps, schema_editor):
    """Add Creative Bold resume template to database."""
    ResumeTemplate = apps.get_model('resume_builder', 'ResumeTemplate')
    
    # Check if template already exists
    if not ResumeTemplate.objects.filter(slug='creative').exists():
        ResumeTemplate.objects.create(
            name='Creative Bold',
            slug='creative',
            description='Eye-catching asymmetric design with bold name block and visual skill indicators. Perfect for creative professionals, designers, and marketing roles.',
            category='creative',
            primary_color='#e74c3c',
            is_active=True,
            display_order=4,
            is_ats_safe=False,  # Creative design may not be fully ATS-compatible
            recommended_roles=['designer', 'marketing', 'creative_director', 'ux_designer', 'brand_manager']
        )


def remove_creative_template(apps, schema_editor):
    """Remove Creative Bold template."""
    ResumeTemplate = apps.get_model('resume_builder', 'ResumeTemplate')
    ResumeTemplate.objects.filter(slug='creative').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('resume_builder', '0009_add_minimal_template'),
    ]

    operations = [
        migrations.RunPython(add_creative_template, remove_creative_template),
    ]
