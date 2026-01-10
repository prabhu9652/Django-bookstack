# Installation Guide - Resume Builder

## Quick Start

### 1. Install Python Dependencies

```bash
# Install core requirements
pip install -r requirements.txt

# For development (optional)
pip install -r requirements-dev.txt

# For full PDF export (optional)
pip install -r requirements-pdf.txt
```

### 2. System Dependencies for PDF Export (Optional)

The Resume Builder works without these, but for full PDF export functionality:

#### macOS
```bash
brew install pango
```

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

#### CentOS/RHEL/Fedora
```bash
sudo yum install pango harfbuzz
# or for newer versions:
sudo dnf install pango harfbuzz
```

### 3. Database Setup

```bash
# Run migrations
python manage.py migrate

# Set up resume templates
python manage.py setup_resume_templates

# Create superuser (optional)
python manage.py createsuperuser
```

### 4. Run the Application

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/resume-builder/` to access the Resume Builder.

## Package Details

### Core Requirements
- **Django 5.x**: Web framework
- **Pillow**: Image processing
- **gunicorn**: Production WSGI server
- **whitenoise**: Static file serving
- **psycopg2-binary**: PostgreSQL adapter

### Resume Builder Specific
- **weasyprint**: HTML to PDF conversion
- **cffi**: Foreign function interface
- **pydyf**: PDF generation library
- **cssselect2**: CSS selector implementation
- **tinycss2**: CSS parser
- **fonttools**: Font utilities
- **python-dateutil**: Date parsing utilities

### Development Tools (Optional)
- **pytest**: Testing framework
- **black**: Code formatter
- **flake8**: Code linter
- **django-debug-toolbar**: Debug information

## Troubleshooting

### PDF Export Issues
If PDF export fails, the application will gracefully fall back to HTML export. To fix PDF export:

1. Ensure system libraries are installed (see above)
2. Verify WeasyPrint installation: `python -c "import weasyprint; print('OK')"`
3. Check logs for specific error messages

### Common Issues

#### ImportError: No module named 'weasyprint'
```bash
pip install weasyprint
```

#### OSError: cannot load library 'libpango-1.0-0'
Install system dependencies (see above sections for your OS).

#### Permission denied errors
Ensure proper file permissions for media and static directories.

## Production Deployment

### Environment Variables
```bash
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com
```

### Static Files
```bash
python manage.py collectstatic
```

### Database
```bash
python manage.py migrate
python manage.py setup_resume_templates
```

## Features Included

✅ Professional resume templates (4 styles)
✅ Cover letter templates (3 styles)  
✅ Real-time preview
✅ Auto-save functionality
✅ PDF/HTML export
✅ Mobile responsive design
✅ User authentication
✅ Document management dashboard
✅ Template customization
✅ Professional styling