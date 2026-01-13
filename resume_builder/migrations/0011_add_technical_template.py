# Generated migration for Technical template

from django.db import migrations


def add_technical_template(apps, schema_editor):
    """Add Technical resume template to database."""
    ResumeTemplate = apps.get_model('resume_builder', 'ResumeTemplate')
    
    # Check if template already exists
    if not ResumeTemplate.objects.filter(slug='technical').exists():
        ResumeTemplate.objects.create(
            name='Technical',
            slug='technical',
            description='Clean, scannable layout with prominent skills sidebar and monospace accents. Optimized for software engineers, DevOps, and SRE roles.',
            category='modern',
            primary_color='#2ecc71',
            is_active=True,
            display_order=5,
            is_ats_safe=True,
            recommended_roles=['software_engineer', 'devops_sre', 'data_scientist', 'backend_developer', 'full_stack_developer']
        )


def remove_technical_template(apps, schema_editor):
    """Remove Technical template."""
    ResumeTemplate = apps.get_model('resume_builder', 'ResumeTemplate')
    ResumeTemplate.objects.filter(slug='technical').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('resume_builder', '0010_add_creative_template'),
    ]

    operations = [
        migrations.RunPython(add_technical_template, remove_technical_template),
    ]
