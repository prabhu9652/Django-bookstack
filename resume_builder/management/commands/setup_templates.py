from django.core.management.base import BaseCommand
from resume_builder.models import ResumeTemplate, CoverLetterTemplate


class Command(BaseCommand):
    help = 'Set up initial resume and cover letter templates'

    def handle(self, *args, **options):
        self.stdout.write('Setting up Resume Builder templates...')
        
        # Create Resume Templates
        resume_templates = [
            {
                'name': 'Professional',
                'category': 'professional',
                'description': 'Clean and professional design perfect for corporate environments',
                'html_template': '''
                <div style="max-width: 800px; margin: 0 auto; font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="text-align: center; margin-bottom: 30px; border-bottom: 2px solid #333; padding-bottom: 20px;">
                        <h1 style="font-size: 28px; font-weight: bold; margin-bottom: 10px;">{{ resume.full_name }}</h1>
                        <div style="font-size: 14px; color: #666;">
                            {{ resume.email }}{% if resume.phone %} • {{ resume.phone }}{% endif %}{% if resume.location %} • {{ resume.location }}{% endif %}
                        </div>
                    </div>
                    {% if resume.summary %}
                    <div style="margin-bottom: 25px;">
                        <h2 style="font-size: 18px; font-weight: bold; border-bottom: 1px solid #ccc; padding-bottom: 5px;">Professional Summary</h2>
                        <p>{{ resume.summary }}</p>
                    </div>
                    {% endif %}
                    {% if resume.experience %}
                    <div style="margin-bottom: 25px;">
                        <h2 style="font-size: 18px; font-weight: bold; border-bottom: 1px solid #ccc; padding-bottom: 5px;">Experience</h2>
                        {% for exp in resume.experience %}
                        <div style="margin-bottom: 15px;">
                            <h3 style="font-size: 16px; font-weight: bold;">{{ exp.title }} - {{ exp.company }}</h3>
                            <div style="font-size: 14px; color: #666;">{{ exp.start_date }} - {{ exp.end_date }}</div>
                            <p style="font-size: 14px;">{{ exp.description }}</p>
                        </div>
                        {% endfor %}
                    </div>
                    {% endif %}
                    {% if resume.education %}
                    <div style="margin-bottom: 25px;">
                        <h2 style="font-size: 18px; font-weight: bold; border-bottom: 1px solid #ccc; padding-bottom: 5px;">Education</h2>
                        {% for edu in resume.education %}
                        <div style="margin-bottom: 10px;">
                            <h3 style="font-size: 16px; font-weight: bold;">{{ edu.degree }} - {{ edu.school }}</h3>
                            <div style="font-size: 14px; color: #666;">{{ edu.graduation_date }}</div>
                        </div>
                        {% endfor %}
                    </div>
                    {% endif %}
                    {% if resume.skills %}
                    <div>
                        <h2 style="font-size: 18px; font-weight: bold; border-bottom: 1px solid #ccc; padding-bottom: 5px;">Skills</h2>
                        <p>{% for skill in resume.skills %}{{ skill }}{% if not forloop.last %}, {% endif %}{% endfor %}</p>
                    </div>
                    {% endif %}
                </div>
                ''',
                'css_styles': 'body { font-family: Arial, sans-serif; }'
            },
            {
                'name': 'Modern',
                'category': 'modern',
                'description': 'Contemporary design with clean lines and modern typography',
                'html_template': '''
                <div style="max-width: 800px; margin: 0 auto; font-family: 'Helvetica Neue', sans-serif; line-height: 1.6; color: #2c3e50;">
                    <div style="background: #3498db; color: white; padding: 30px; text-align: center; margin-bottom: 30px;">
                        <h1 style="font-size: 32px; font-weight: 300; margin-bottom: 10px;">{{ resume.full_name }}</h1>
                        <div style="font-size: 16px;">
                            {{ resume.email }}{% if resume.phone %} • {{ resume.phone }}{% endif %}{% if resume.location %} • {{ resume.location }}{% endif %}
                        </div>
                    </div>
                    {% if resume.summary %}
                    <div style="margin-bottom: 30px;">
                        <h2 style="font-size: 20px; font-weight: 600; color: #3498db; margin-bottom: 15px;">About Me</h2>
                        <p style="font-size: 16px; line-height: 1.7;">{{ resume.summary }}</p>
                    </div>
                    {% endif %}
                    {% if resume.experience %}
                    <div style="margin-bottom: 30px;">
                        <h2 style="font-size: 20px; font-weight: 600; color: #3498db; margin-bottom: 15px;">Experience</h2>
                        {% for exp in resume.experience %}
                        <div style="margin-bottom: 20px; padding-left: 20px; border-left: 3px solid #3498db;">
                            <h3 style="font-size: 18px; font-weight: 600; margin-bottom: 5px;">{{ exp.title }}</h3>
                            <div style="font-size: 16px; color: #7f8c8d; margin-bottom: 5px;">{{ exp.company }} • {{ exp.start_date }} - {{ exp.end_date }}</div>
                            <p style="font-size: 15px;">{{ exp.description }}</p>
                        </div>
                        {% endfor %}
                    </div>
                    {% endif %}
                    {% if resume.education %}
                    <div style="margin-bottom: 30px;">
                        <h2 style="font-size: 20px; font-weight: 600; color: #3498db; margin-bottom: 15px;">Education</h2>
                        {% for edu in resume.education %}
                        <div style="margin-bottom: 15px;">
                            <h3 style="font-size: 18px; font-weight: 600;">{{ edu.degree }}</h3>
                            <div style="font-size: 16px; color: #7f8c8d;">{{ edu.school }} • {{ edu.graduation_date }}</div>
                        </div>
                        {% endfor %}
                    </div>
                    {% endif %}
                    {% if resume.skills %}
                    <div>
                        <h2 style="font-size: 20px; font-weight: 600; color: #3498db; margin-bottom: 15px;">Skills</h2>
                        <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                            {% for skill in resume.skills %}
                            <span style="background: #ecf0f1; padding: 8px 15px; border-radius: 20px; font-size: 14px;">{{ skill }}</span>
                            {% endfor %}
                        </div>
                    </div>
                    {% endif %}
                </div>
                ''',
                'css_styles': 'body { font-family: "Helvetica Neue", sans-serif; }'
            },
            {
                'name': 'Minimal',
                'category': 'minimal',
                'description': 'Simple and clean design focusing on content',
                'html_template': '''
                <div style="max-width: 700px; margin: 0 auto; font-family: 'Georgia', serif; line-height: 1.8; color: #333;">
                    <div style="margin-bottom: 40px;">
                        <h1 style="font-size: 36px; font-weight: normal; margin-bottom: 10px; letter-spacing: -1px;">{{ resume.full_name }}</h1>
                        <div style="font-size: 16px; color: #666; font-style: italic;">
                            {{ resume.email }}{% if resume.phone %} • {{ resume.phone }}{% endif %}{% if resume.location %} • {{ resume.location }}{% endif %}
                        </div>
                    </div>
                    {% if resume.summary %}
                    <div style="margin-bottom: 35px;">
                        <p style="font-size: 18px; line-height: 1.6; font-style: italic; color: #555;">{{ resume.summary }}</p>
                    </div>
                    {% endif %}
                    {% if resume.experience %}
                    <div style="margin-bottom: 35px;">
                        <h2 style="font-size: 22px; font-weight: normal; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px;">Experience</h2>
                        {% for exp in resume.experience %}
                        <div style="margin-bottom: 25px;">
                            <h3 style="font-size: 18px; font-weight: bold; margin-bottom: 5px;">{{ exp.title }}</h3>
                            <div style="font-size: 16px; color: #666; margin-bottom: 8px;">{{ exp.company }} • {{ exp.start_date }} - {{ exp.end_date }}</div>
                            <p style="font-size: 16px;">{{ exp.description }}</p>
                        </div>
                        {% endfor %}
                    </div>
                    {% endif %}
                    {% if resume.education %}
                    <div style="margin-bottom: 35px;">
                        <h2 style="font-size: 22px; font-weight: normal; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px;">Education</h2>
                        {% for edu in resume.education %}
                        <div style="margin-bottom: 15px;">
                            <h3 style="font-size: 18px; font-weight: bold;">{{ edu.degree }}</h3>
                            <div style="font-size: 16px; color: #666;">{{ edu.school }} • {{ edu.graduation_date }}</div>
                        </div>
                        {% endfor %}
                    </div>
                    {% endif %}
                    {% if resume.skills %}
                    <div>
                        <h2 style="font-size: 22px; font-weight: normal; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px;">Skills</h2>
                        <p style="font-size: 16px;">{% for skill in resume.skills %}{{ skill }}{% if not forloop.last %} • {% endif %}{% endfor %}</p>
                    </div>
                    {% endif %}
                </div>
                ''',
                'css_styles': 'body { font-family: Georgia, serif; }'
            }
        ]
        
        for template_data in resume_templates:
            template, created = ResumeTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                self.stdout.write(f'Created resume template: {template.name}')
            else:
                self.stdout.write(f'Resume template already exists: {template.name}')
        
        # Create Cover Letter Templates
        cover_letter_templates = [
            {
                'name': 'Professional',
                'tone': 'professional',
                'description': 'Professional and formal tone suitable for corporate positions',
                'html_template': '''
                <div style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="text-align: right; margin-bottom: 30px;">
                        <div style="font-weight: bold;">{{ cover_letter.full_name }}</div>
                        <div>{{ cover_letter.email }}</div>
                        {% if cover_letter.phone %}<div>{{ cover_letter.phone }}</div>{% endif %}
                        {% if cover_letter.location %}<div>{{ cover_letter.location }}</div>{% endif %}
                    </div>
                    
                    <div style="margin-bottom: 30px;">
                        <div>{{ "now"|date:"F d, Y" }}</div>
                    </div>
                    
                    <div style="margin-bottom: 30px;">
                        {% if cover_letter.hiring_manager %}
                        <div>{{ cover_letter.hiring_manager }}</div>
                        {% endif %}
                        <div>{{ cover_letter.company_name }}</div>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <strong>Re: {{ cover_letter.position_title }}</strong>
                    </div>
                    
                    <div style="white-space: pre-line; margin-bottom: 30px;">{{ cover_letter.content }}</div>
                    
                    <div>
                        <div>Sincerely,</div>
                        <div style="margin-top: 20px;">{{ cover_letter.full_name }}</div>
                    </div>
                </div>
                ''',
                'css_styles': 'body { font-family: Arial, sans-serif; }'
            },
            {
                'name': 'Modern',
                'tone': 'modern',
                'description': 'Contemporary and engaging tone for creative industries',
                'html_template': '''
                <div style="max-width: 600px; margin: 0 auto; font-family: 'Helvetica Neue', sans-serif; line-height: 1.7; color: #2c3e50;">
                    <div style="background: #3498db; color: white; padding: 20px; margin-bottom: 30px;">
                        <h1 style="font-size: 24px; font-weight: 300; margin: 0;">{{ cover_letter.full_name }}</h1>
                        <div style="font-size: 14px; margin-top: 10px;">
                            {{ cover_letter.email }}{% if cover_letter.phone %} • {{ cover_letter.phone }}{% endif %}
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 25px;">
                        <div style="font-size: 14px; color: #7f8c8d;">{{ "now"|date:"F d, Y" }}</div>
                    </div>
                    
                    <div style="margin-bottom: 25px;">
                        <div style="font-size: 18px; font-weight: 600; color: #3498db;">{{ cover_letter.company_name }}</div>
                        <div style="font-size: 16px; color: #7f8c8d;">{{ cover_letter.position_title }}</div>
                    </div>
                    
                    <div style="white-space: pre-line; font-size: 16px; margin-bottom: 30px;">{{ cover_letter.content }}</div>
                    
                    <div style="font-size: 16px;">
                        <div>Best regards,</div>
                        <div style="margin-top: 15px; font-weight: 600;">{{ cover_letter.full_name }}</div>
                    </div>
                </div>
                ''',
                'css_styles': 'body { font-family: "Helvetica Neue", sans-serif; }'
            }
        ]
        
        for template_data in cover_letter_templates:
            template, created = CoverLetterTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                self.stdout.write(f'Created cover letter template: {template.name}')
            else:
                self.stdout.write(f'Cover letter template already exists: {template.name}')
        
        self.stdout.write(self.style.SUCCESS('Successfully set up Resume Builder templates!'))