# Generated migration for 3 additional cover letter templates
from django.db import migrations


def add_cover_letter_templates(apps, schema_editor):
    CoverLetterTemplate = apps.get_model('resume_builder', 'CoverLetterTemplate')
    
    templates = [
        {'name': 'Pure', 'slug': 'cl_pure', 'tone': 'creative', 'description': 'Ultra-clean creative simplicity', 'primary_color': '#4a5568', 'display_order': 38},
        {'name': 'Essence', 'slug': 'cl_essence', 'tone': 'creative', 'description': 'Distilled creative clarity', 'primary_color': '#2d3748', 'display_order': 39},
        {'name': 'Ember', 'slug': 'ember', 'tone': 'creative', 'description': 'Warm ember creative design', 'primary_color': '#fc8181', 'display_order': 40},
    ]
    
    default_html = '''<div class="cover-letter">
    <header class="header">
        <h1 class="name">{{ full_name }}</h1>
        <div class="contact">{{ email }} | {{ phone }}</div>
    </header>
    <div class="body">
        <div class="date">{{ date }}</div>
        <div class="recipient">{{ company_name }}</div>
        <div class="content">{{ body }}</div>
        <div class="closing">Sincerely,<br>{{ full_name }}</div>
    </div>
</div>'''
    
    default_css = '''.cover-letter { font-family: Arial, sans-serif; }'''
    
    for template_data in templates:
        template_data['html_template'] = default_html
        template_data['css_styles'] = default_css
        template_data['is_active'] = True
        CoverLetterTemplate.objects.create(**template_data)


def remove_cover_letter_templates(apps, schema_editor):
    CoverLetterTemplate = apps.get_model('resume_builder', 'CoverLetterTemplate')
    slugs = ['cl_pure', 'cl_essence', 'ember']
    CoverLetterTemplate.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('resume_builder', '0015_add_37_cover_letter_templates'),
    ]

    operations = [
        migrations.RunPython(add_cover_letter_templates, remove_cover_letter_templates),
    ]
