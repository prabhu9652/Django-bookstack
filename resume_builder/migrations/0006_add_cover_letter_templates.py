from django.db import migrations


def create_cover_letter_templates(apps, schema_editor):
    """Create the 3 industry-standard cover letter templates."""
    CoverLetterTemplate = apps.get_model('resume_builder', 'CoverLetterTemplate')
    
    # Template 1: Classic Professional
    CoverLetterTemplate.objects.get_or_create(
        slug='classic',
        defaults={
            'name': 'Classic Professional',
            'tone': 'formal',
            'description': 'Traditional serif typography with minimal styling. Ideal for corporate roles, finance, consulting, and government positions.',
            'html_template': '',
            'css_styles': '',
            'is_active': True,
            'primary_color': '#1a1a1a',
        }
    )
    
    # Template 2: Modern Professional
    CoverLetterTemplate.objects.get_or_create(
        slug='modern',
        defaults={
            'name': 'Modern Professional',
            'tone': 'professional',
            'description': 'Clean sans-serif design with balanced spacing and subtle dividers. Perfect for tech roles, startups, and product positions.',
            'html_template': '',
            'css_styles': '',
            'is_active': True,
            'primary_color': '#2d3748',
        }
    )
    
    # Template 3: Creative Professional
    CoverLetterTemplate.objects.get_or_create(
        slug='creative',
        defaults={
            'name': 'Creative Professional',
            'tone': 'modern',
            'description': 'Bold header with color accent and contemporary design. Great for design, marketing, and media roles while remaining ATS-friendly.',
            'html_template': '',
            'css_styles': '',
            'is_active': True,
            'primary_color': '#4a9d9a',
        }
    )


def remove_cover_letter_templates(apps, schema_editor):
    """Remove the cover letter templates."""
    CoverLetterTemplate = apps.get_model('resume_builder', 'CoverLetterTemplate')
    CoverLetterTemplate.objects.filter(slug__in=['classic', 'modern', 'creative']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('resume_builder', '0005_add_preview_image_to_resumetemplate'),
    ]

    operations = [
        migrations.RunPython(create_cover_letter_templates, remove_cover_letter_templates),
    ]
