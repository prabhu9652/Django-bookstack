"""
Management command to upload template preview images.

Usage:
    python manage.py upload_template_previews professional /path/to/professional.png
    python manage.py upload_template_previews modern /path/to/modern.png
    python manage.py upload_template_previews executive /path/to/executive.png
"""
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from resume_builder.models import ResumeTemplate
import os


class Command(BaseCommand):
    help = 'Upload a preview image for a resume template'

    def add_arguments(self, parser):
        parser.add_argument('template_slug', type=str, help='Template slug (professional, modern, executive)')
        parser.add_argument('image_path', type=str, help='Path to the preview image file')

    def handle(self, *args, **options):
        template_slug = options['template_slug']
        image_path = options['image_path']
        
        # Validate image path
        if not os.path.exists(image_path):
            raise CommandError(f'Image file not found: {image_path}')
        
        # Get the template
        try:
            template = ResumeTemplate.objects.get(slug=template_slug)
        except ResumeTemplate.DoesNotExist:
            raise CommandError(f'Template not found: {template_slug}')
        
        # Upload the image
        with open(image_path, 'rb') as f:
            filename = os.path.basename(image_path)
            template.preview_image.save(filename, File(f), save=True)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully uploaded preview image for "{template.name}" template')
        )
        self.stdout.write(f'  Image URL: {template.preview_image.url}')
