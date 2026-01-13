# Generated migration for 37 new cover letter templates
from django.db import migrations


def add_cover_letter_templates(apps, schema_editor):
    CoverLetterTemplate = apps.get_model('resume_builder', 'CoverLetterTemplate')
    
    templates = [
        # FORMAL TEMPLATES (7)
        {'name': 'Executive', 'slug': 'executive', 'tone': 'formal', 'description': 'Commanding executive presence with refined typography', 'primary_color': '#1e3a5f', 'display_order': 4},
        {'name': 'Diplomat', 'slug': 'diplomat', 'tone': 'formal', 'description': 'Elegant formal style for senior positions', 'primary_color': '#2d3748', 'display_order': 5},
        {'name': 'Chancellor', 'slug': 'chancellor', 'tone': 'formal', 'description': 'Traditional serif typography with classic appeal', 'primary_color': '#4a5568', 'display_order': 6},
        {'name': 'Statesman', 'slug': 'statesman', 'tone': 'formal', 'description': 'Distinguished formal layout for leadership roles', 'primary_color': '#1a365d', 'display_order': 7},
        {'name': 'Regent', 'slug': 'cl_regent', 'tone': 'formal', 'description': 'Regal formal design with refined spacing', 'primary_color': '#2c5282', 'display_order': 8},
        {'name': 'Sovereign', 'slug': 'sovereign', 'tone': 'formal', 'description': 'Premium formal template with bold header', 'primary_color': '#1a202c', 'display_order': 9},
        {'name': 'Ambassador', 'slug': 'ambassador', 'tone': 'formal', 'description': 'Diplomatic formal style with elegant borders', 'primary_color': '#2d3748', 'display_order': 10},
        
        # PROFESSIONAL TEMPLATES (10)
        {'name': 'Corporate', 'slug': 'corporate', 'tone': 'professional', 'description': 'Clean corporate style for business professionals', 'primary_color': '#2b6cb0', 'display_order': 11},
        {'name': 'Enterprise', 'slug': 'enterprise', 'tone': 'professional', 'description': 'Enterprise-grade professional design', 'primary_color': '#276749', 'display_order': 12},
        {'name': 'Sterling', 'slug': 'cl_sterling', 'tone': 'professional', 'description': 'Premium professional with refined details', 'primary_color': '#2d3748', 'display_order': 13},
        {'name': 'Pinnacle', 'slug': 'cl_pinnacle', 'tone': 'professional', 'description': 'Top-tier professional layout', 'primary_color': '#1a365d', 'display_order': 14},
        {'name': 'Summit', 'slug': 'cl_summit', 'tone': 'professional', 'description': 'Peak professional design', 'primary_color': '#2d3748', 'display_order': 15},
        {'name': 'Keystone', 'slug': 'cl_keystone', 'tone': 'professional', 'description': 'Foundational professional structure', 'primary_color': '#744210', 'display_order': 16},
        {'name': 'Anchor', 'slug': 'cl_anchor', 'tone': 'professional', 'description': 'Solid dependable professional layout', 'primary_color': '#1a365d', 'display_order': 17},

        # MODERN TEMPLATES (10)
        {'name': 'Streamline', 'slug': 'cl_streamline', 'tone': 'modern', 'description': 'Flowing modern layout with smooth transitions', 'primary_color': '#0891b2', 'display_order': 18},
        {'name': 'Metro', 'slug': 'cl_metro', 'tone': 'modern', 'description': 'Urban modern style with accent sidebar', 'primary_color': '#0f766e', 'display_order': 19},
        {'name': 'Nordic', 'slug': 'cl_nordic', 'tone': 'modern', 'description': 'Scandinavian minimalism with generous whitespace', 'primary_color': '#64748b', 'display_order': 20},
        {'name': 'Slate', 'slug': 'cl_slate', 'tone': 'modern', 'description': 'Dark header with sophisticated typography', 'primary_color': '#334155', 'display_order': 21},
        {'name': 'Prism', 'slug': 'prism', 'tone': 'modern', 'description': 'Light and airy with subtle color accents', 'primary_color': '#667eea', 'display_order': 22},
        {'name': 'Nova', 'slug': 'nova', 'tone': 'modern', 'description': 'Fresh contemporary with dynamic spacing', 'primary_color': '#ed8936', 'display_order': 23},
        {'name': 'Pulse', 'slug': 'pulse', 'tone': 'modern', 'description': 'Energetic modern with gradient accent', 'primary_color': '#e53e3e', 'display_order': 24},
        {'name': 'Flux', 'slug': 'flux', 'tone': 'modern', 'description': 'Flowing design with rounded corners', 'primary_color': '#38b2ac', 'display_order': 25},
        {'name': 'Vertex', 'slug': 'vertex', 'tone': 'modern', 'description': 'Sharp angular modern design', 'primary_color': '#805ad5', 'display_order': 26},
        {'name': 'Circuit', 'slug': 'circuit', 'tone': 'modern', 'description': 'Tech-inspired modern with monospace accents', 'primary_color': '#2b6cb0', 'display_order': 27},
        
        # CREATIVE TEMPLATES (10)
        {'name': 'Artisan', 'slug': 'artisan', 'tone': 'creative', 'description': 'Crafted creative design with unique header', 'primary_color': '#9f7aea', 'display_order': 28},
        {'name': 'Canvas', 'slug': 'cl_canvas', 'tone': 'creative', 'description': 'Blank slate creative aesthetic', 'primary_color': '#1a202c', 'display_order': 29},
        {'name': 'Palette', 'slug': 'palette', 'tone': 'creative', 'description': 'Colorful creative with bold accents', 'primary_color': '#dd6b20', 'display_order': 30},
        {'name': 'Studio', 'slug': 'studio', 'tone': 'creative', 'description': 'Designer studio creative style', 'primary_color': '#d53f8c', 'display_order': 31},
        {'name': 'Gallery', 'slug': 'gallery', 'tone': 'creative', 'description': 'Gallery-inspired creative layout', 'primary_color': '#805ad5', 'display_order': 32},
        {'name': 'Spectrum', 'slug': 'spectrum', 'tone': 'creative', 'description': 'Full spectrum creative style', 'primary_color': '#667eea', 'display_order': 33},
        {'name': 'Spark', 'slug': 'spark', 'tone': 'creative', 'description': 'Energetic creative with spark', 'primary_color': '#f6ad55', 'display_order': 34},
        {'name': 'Bloom', 'slug': 'bloom', 'tone': 'creative', 'description': 'Fresh blooming creative style', 'primary_color': '#68d391', 'display_order': 35},
        {'name': 'Aurora', 'slug': 'aurora', 'tone': 'creative', 'description': 'Northern lights inspired creative', 'primary_color': '#4fd1c5', 'display_order': 36},
        {'name': 'Zen', 'slug': 'cl_zen', 'tone': 'creative', 'description': 'Peaceful zen creative minimalism', 'primary_color': '#718096', 'display_order': 37},
    ]
    
    # Default HTML template and CSS for all new templates
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
    slugs = [
        'executive', 'diplomat', 'chancellor', 'statesman', 'cl_regent', 'sovereign', 'ambassador',
        'corporate', 'enterprise', 'cl_sterling', 'cl_pinnacle', 'cl_summit', 'cl_keystone', 'cl_anchor',
        'cl_streamline', 'cl_metro', 'cl_nordic', 'cl_slate', 'prism', 'nova', 'pulse', 'flux', 'vertex', 'circuit',
        'artisan', 'cl_canvas', 'palette', 'studio', 'gallery', 'spectrum', 'spark', 'bloom', 'aurora', 'cl_zen'
    ]
    CoverLetterTemplate.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('resume_builder', '0014_add_25_premium_templates'),
    ]

    operations = [
        migrations.RunPython(add_cover_letter_templates, remove_cover_letter_templates),
    ]
