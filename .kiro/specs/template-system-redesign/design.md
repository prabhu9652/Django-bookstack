# Design Document: Template System Redesign

## Overview

This design document outlines the architecture for redesigning and expanding the resume and cover letter template system. The system will provide a premium, scalable template library with pixel-perfect PDF generation, consistent with industry leaders like Canva, Resume.io, and Zety.

The design leverages the existing Playwright-based PDF generation pipeline and extends the current template architecture to support additional templates without code duplication.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Template System                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  Database   │  │  Template   │  │    PDF Generator        │ │
│  │  Models     │  │  Themes     │  │    (Playwright)         │ │
│  │             │  │             │  │                         │ │
│  │ - Resume    │  │ - Palettes  │  │ - build_resume_html()   │ │
│  │   Template  │  │ - Role Recs │  │ - build_cover_letter_   │ │
│  │ - Cover     │  │ - Color     │  │   html()                │ │
│  │   Letter    │  │   Utils     │  │ - _generate_pdf_with_   │ │
│  │   Template  │  │             │  │   playwright()          │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│         │                │                      │               │
│         └────────────────┼──────────────────────┘               │
│                          │                                      │
│  ┌───────────────────────▼───────────────────────────────────┐ │
│  │                  Template Renderer                         │ │
│  │                                                            │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │ │
│  │  │ Base Styles  │  │  Template    │  │  HTML Builder    │ │ │
│  │  │ (shared CSS) │  │  Styles      │  │  Functions       │ │ │
│  │  │              │  │  (per-tmpl)  │  │                  │ │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Template Rendering Flow

```
User Selects Template
        │
        ▼
┌───────────────────┐
│ Load Template     │
│ from Database     │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Get Color Palette │
│ from Themes       │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐     ┌───────────────────┐
│ Build HTML        │────▶│ Live Preview      │
│ (template-specific│     │ (Browser Render)  │
│  + base styles)   │     └───────────────────┘
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐     ┌───────────────────┐
│ Playwright        │────▶│ PDF Output        │
│ PDF Generation    │     │ (Pixel-Perfect)   │
└───────────────────┘     └───────────────────┘
```

## Components and Interfaces

### 1. Template Model Extensions

```python
# resume_builder/models.py

class ResumeTemplate(models.Model):
    CATEGORIES = [
        ('professional', 'Professional'),
        ('modern', 'Modern'),
        ('executive', 'Executive'),
        ('minimal', 'Minimal'),
        ('creative', 'Creative'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.TextField()
    
    # Template rendering
    html_template = models.TextField()  # Legacy - kept for compatibility
    css_styles = models.TextField()     # Legacy - kept for compatibility
    
    # Visual customization
    primary_color = models.CharField(max_length=7, default='#4a9d9a')
    preview_image = models.ImageField(upload_to='template_previews/', blank=True)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    is_ats_safe = models.BooleanField(default=True)
    recommended_roles = models.JSONField(default=list)  # ['devops_sre', 'software_engineer']
    
    # Ordering
    display_order = models.IntegerField(default=0)


class CoverLetterTemplate(models.Model):
    TONES = [
        ('formal', 'Formal'),
        ('professional', 'Professional'),
        ('modern', 'Modern'),
        ('creative', 'Creative'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    tone = models.CharField(max_length=20, choices=TONES)
    description = models.TextField()
    
    # Visual customization
    primary_color = models.CharField(max_length=7, default='#1a1a1a')
    preview_image = models.ImageField(upload_to='cl_template_previews/', blank=True)
    
    # Pairing with resume templates
    paired_resume_template = models.ForeignKey(
        ResumeTemplate, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text='Recommended resume template to pair with'
    )
    
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
```

### 2. Template Registry

```python
# resume_builder/template_registry.py

from typing import Dict, Callable, List
from dataclasses import dataclass

@dataclass
class TemplateDefinition:
    """Definition for a template's rendering functions"""
    slug: str
    name: str
    category: str
    build_html: Callable  # Function to build template HTML
    get_styles: Callable  # Function to get template CSS
    default_color: str
    is_ats_safe: bool = True
    recommended_roles: List[str] = None

class TemplateRegistry:
    """Central registry for all template definitions"""
    
    _resume_templates: Dict[str, TemplateDefinition] = {}
    _cover_letter_templates: Dict[str, TemplateDefinition] = {}
    
    @classmethod
    def register_resume_template(cls, definition: TemplateDefinition):
        cls._resume_templates[definition.slug] = definition
    
    @classmethod
    def register_cover_letter_template(cls, definition: TemplateDefinition):
        cls._cover_letter_templates[definition.slug] = definition
    
    @classmethod
    def get_resume_template(cls, slug: str) -> TemplateDefinition:
        return cls._resume_templates.get(slug)
    
    @classmethod
    def get_cover_letter_template(cls, slug: str) -> TemplateDefinition:
        return cls._cover_letter_templates.get(slug)
    
    @classmethod
    def list_resume_templates(cls) -> List[TemplateDefinition]:
        return list(cls._resume_templates.values())
```

### 3. New Resume Templates

#### 3.1 Minimal Clean Template

```python
def _build_minimal_template(resume, primary_color: str) -> str:
    """
    Minimal Clean Template
    - Single column layout
    - Maximum whitespace
    - Subtle accent colors
    - Clean typography
    """
    # Contact line
    contact_parts = []
    if resume.email:
        contact_parts.append(_escape(resume.email))
    if resume.phone:
        contact_parts.append(_escape(resume.phone))
    if resume.location:
        contact_parts.append(_escape(resume.location))
    if resume.linkedin:
        contact_parts.append(_escape(resume.linkedin))
    
    contact_html = ' • '.join(contact_parts)
    
    # Summary
    summary_html = ''
    if resume.summary:
        summary_html = f'''
        <section class="section">
            <p class="summary-text">{_escape(resume.summary)}</p>
        </section>'''
    
    # Experience
    experience_html = _build_minimal_experience(resume.experience)
    
    # Education
    education_html = _build_minimal_education(resume.education)
    
    # Skills (inline)
    skills_html = ''
    if resume.skills:
        skills_html = f'''
        <section class="section">
            <h2 class="section-title">Skills</h2>
            <p class="skills-inline">{' • '.join([_escape(s) for s in resume.skills])}</p>
        </section>'''
    
    return f'''
    <header class="header">
        <h1 class="name">{_escape(resume.full_name)}</h1>
        <p class="role">{_escape(resume.role_title or '')}</p>
        <p class="contact">{contact_html}</p>
    </header>
    
    <main class="content">
        {summary_html}
        {experience_html}
        {education_html}
        {skills_html}
    </main>'''
```

#### 3.2 Creative Bold Template

```python
def _build_creative_template(resume, primary_color: str) -> str:
    """
    Creative Bold Template
    - Asymmetric two-column layout
    - Bold typography with large name
    - Color blocks for visual interest
    - Skills with visual indicators
    """
    # Left column: Name, contact, skills
    # Right column: Summary, experience, education
    
    contact_items = []
    if resume.email:
        contact_items.append(f'<div class="contact-item">{_escape(resume.email)}</div>')
    if resume.phone:
        contact_items.append(f'<div class="contact-item">{_escape(resume.phone)}</div>')
    if resume.location:
        contact_items.append(f'<div class="contact-item">{_escape(resume.location)}</div>')
    if resume.linkedin:
        contact_items.append(f'<div class="contact-item">{_escape(resume.linkedin)}</div>')
    if resume.github:
        contact_items.append(f'<div class="contact-item">{_escape(resume.github)}</div>')
    
    # Skills with bars
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li><span class="skill-dot"></span>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''
        <div class="sidebar-section">
            <h3 class="sidebar-heading">EXPERTISE</h3>
            <ul class="skill-list">{items}</ul>
        </div>'''
    
    # Languages
    languages_html = ''
    if resume.languages:
        items = ''.join([f'<li>{_escape(l)}</li>' for l in resume.languages])
        languages_html = f'''
        <div class="sidebar-section">
            <h3 class="sidebar-heading">LANGUAGES</h3>
            <ul class="lang-list">{items}</ul>
        </div>'''
    
    return f'''
    <div class="creative-layout">
        <aside class="left-column">
            <div class="name-block">
                <h1 class="name">{_escape(resume.full_name)}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
            </div>
            
            <div class="contact-block">
                {''.join(contact_items)}
            </div>
            
            {skills_html}
            {languages_html}
        </aside>
        
        <main class="right-column">
            {_build_creative_summary(resume.summary)}
            {_build_creative_experience(resume.experience, primary_color)}
            {_build_creative_education(resume.education)}
        </main>
    </div>'''
```

#### 3.3 Technical Template

```python
def _build_technical_template(resume, primary_color: str) -> str:
    """
    Technical Template
    - Optimized for engineering roles
    - Skills prominently displayed with categories
    - Projects section emphasized
    - Clean, scannable layout
    """
    # Header with name and contact
    contact_parts = []
    if resume.email:
        contact_parts.append(f'<span>✉ {_escape(resume.email)}</span>')
    if resume.phone:
        contact_parts.append(f'<span>☎ {_escape(resume.phone)}</span>')
    if resume.github:
        contact_parts.append(f'<span>⌘ {_escape(resume.github)}</span>')
    if resume.linkedin:
        contact_parts.append(f'<span>in {_escape(resume.linkedin)}</span>')
    
    # Technical skills with categories
    skills_html = _build_technical_skills(resume.skills, primary_color)
    
    # Projects (prominent for technical roles)
    projects_html = _build_technical_projects(resume.projects, primary_color)
    
    return f'''
    <header class="header">
        <div class="header-main">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
        </div>
        <div class="header-contact">
            {''.join(contact_parts)}
        </div>
    </header>
    
    <div class="body-container">
        <main class="main-content">
            {_build_technical_summary(resume.summary)}
            {_build_technical_experience(resume.experience)}
            {projects_html}
        </main>
        
        <aside class="sidebar">
            {skills_html}
            {_build_technical_education(resume.education)}
            {_build_technical_certifications(resume.certifications)}
        </aside>
    </div>'''
```

### 4. Color Utility Functions

```python
# resume_builder/color_utils.py

import colorsys
from typing import Tuple

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB to hex color"""
    return f'#{r:02x}{g:02x}{b:02x}'

def calculate_luminance(hex_color: str) -> float:
    """Calculate relative luminance for WCAG contrast"""
    r, g, b = hex_to_rgb(hex_color)
    
    def adjust(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    
    return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)

def calculate_contrast_ratio(color1: str, color2: str) -> float:
    """Calculate WCAG contrast ratio between two colors"""
    l1 = calculate_luminance(color1)
    l2 = calculate_luminance(color2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)

def is_wcag_aa_compliant(foreground: str, background: str, large_text: bool = False) -> bool:
    """Check if color combination meets WCAG AA standards"""
    ratio = calculate_contrast_ratio(foreground, background)
    threshold = 3.0 if large_text else 4.5
    return ratio >= threshold

def generate_complementary_colors(primary: str) -> dict:
    """Generate complementary colors from a primary color"""
    r, g, b = hex_to_rgb(primary)
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    
    # Darker variant (secondary)
    secondary_l = max(0, l - 0.15)
    sr, sg, sb = colorsys.hls_to_rgb(h, secondary_l, s)
    secondary = rgb_to_hex(int(sr*255), int(sg*255), int(sb*255))
    
    # Lighter variant (accent)
    accent_l = min(1, l + 0.15)
    ar, ag, ab = colorsys.hls_to_rgb(h, accent_l, s)
    accent = rgb_to_hex(int(ar*255), int(ag*255), int(ab*255))
    
    # Determine text color based on luminance
    text_on_primary = '#ffffff' if calculate_luminance(primary) < 0.5 else '#1a1a1a'
    
    return {
        'primary': primary,
        'secondary': secondary,
        'accent': accent,
        'text_on_primary': text_on_primary,
        'text_primary': '#1a1a1a',
        'text_secondary': '#555555',
    }
```

### 5. Cover Letter Template Pairing

```python
# resume_builder/template_pairing.py

TEMPLATE_PAIRS = {
    # Resume template slug -> Cover letter template slug
    'professional': 'classic',
    'modern': 'modern',
    'executive': 'creative',
    'minimal': 'classic',
    'creative': 'creative',
    'technical': 'modern',
}

def get_paired_cover_letter_template(resume_template_slug: str) -> str:
    """Get the recommended cover letter template for a resume template"""
    return TEMPLATE_PAIRS.get(resume_template_slug, 'classic')

def apply_resume_branding_to_cover_letter(cover_letter, resume):
    """Apply resume's color palette to cover letter"""
    if resume and resume.primary_color:
        cover_letter.primary_color = resume.primary_color
    return cover_letter
```

## Data Models

### Template Data Structure

```python
# Resume template data stored in database
{
    "name": "Professional",
    "slug": "professional",
    "category": "professional",
    "description": "Classic professional layout with photo and left sidebar",
    "primary_color": "#4a9d9a",
    "is_active": True,
    "is_ats_safe": True,
    "recommended_roles": ["devops_sre", "software_engineer"],
    "display_order": 1
}

# Color palette structure
{
    "name": "Teal Classic",
    "primary": "#4a9d9a",
    "secondary": "#3d8584",
    "accent": "#5fb3b0",
    "text_primary": "#1a1a1a",
    "text_secondary": "#555555",
    "background": "#ffffff",
    "sidebar_bg": "#f7f7f7",
    "description": "Classic teal - professional and trustworthy",
    "recommended_roles": ["devops_sre", "software_engineer"]
}
```

### Template Selector Data

```python
# Data passed to template selector UI
{
    "templates": [
        {
            "id": 1,
            "name": "Professional",
            "slug": "professional",
            "category": "professional",
            "category_display": "Professional",
            "description": "Classic professional layout",
            "preview_image_url": "/media/template_previews/professional.png",
            "primary_color": "#4a9d9a",
            "is_recommended": True,  # Based on user's role
        },
        # ... more templates
    ],
    "categories": ["professional", "modern", "executive", "minimal", "creative"],
    "user_role": "software_engineer",
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Template Inventory Completeness

*For any* template category (Professional, Modern, Executive, Minimal, Creative), the Template_System SHALL provide at least one active template, and the total number of active resume templates SHALL be at least 6.

**Validates: Requirements 1.1, 1.5, 2.5**

### Property 2: WCAG Color Contrast Compliance

*For any* color palette in the Template_System, the contrast ratio between text_primary and background colors SHALL be at least 4.5:1 (WCAG AA standard), and the contrast ratio between text on primary color and the primary color SHALL be at least 4.5:1.

**Validates: Requirements 2.4, 8.5**

### Property 3: Font Stack Consistency

*For any* generated resume or cover letter HTML, the font-family CSS property SHALL include at least one of the approved font stacks: ['Segoe UI', 'Roboto', 'Arial'] for sans-serif templates or ['Georgia', 'Times New Roman'] for serif templates.

**Validates: Requirements 2.2**

### Property 4: Role-Based Template Recommendations

*For any* valid role (devops_sre, software_engineer, ds_ml), the get_role_recommendations function SHALL return a dictionary containing 'recommended_template' with a valid template slug that exists in the database.

**Validates: Requirements 3.3**

### Property 5: Cover Letter Template Count

*For any* query of active cover letter templates, the Template_System SHALL return at least 4 distinct templates with valid tone values (formal, professional, modern, creative).

**Validates: Requirements 5.1, 5.3**

### Property 6: Resume-Cover Letter Color Consistency

*For any* resume with a primary_color set, when apply_resume_branding_to_cover_letter is called, the resulting cover letter's primary_color SHALL equal the resume's primary_color.

**Validates: Requirements 5.2, 6.1, 6.3**

### Property 7: Cover Letter Structure Completeness

*For any* cover letter HTML generated by build_cover_letter_html, the output SHALL contain all required business letter sections: header (with sender name), date element, recipient section, salutation, content paragraphs, and closing with signature.

**Validates: Requirements 5.6**

### Property 8: Color Palette Generation

*For any* valid hex color input to generate_complementary_colors, the function SHALL return a dictionary containing keys: 'primary', 'secondary', 'accent', 'text_on_primary', 'text_primary', 'text_secondary', where all color values are valid 7-character hex codes.

**Validates: Requirements 8.3, 8.4**

### Property 9: PDF Generation Consistency

*For any* resume or cover letter, the PDF generated on any device (mobile or desktop) SHALL be byte-identical when given the same input data and template, since PDF generation is server-side via Playwright.

**Validates: Requirements 10.4**

## Error Handling

### Template Loading Errors

```python
class TemplateNotFoundError(Exception):
    """Raised when a requested template doesn't exist"""
    pass

class TemplateRenderError(Exception):
    """Raised when template rendering fails"""
    pass

def get_template_or_default(slug: str, default_slug: str = 'professional'):
    """Get template by slug, falling back to default if not found"""
    try:
        return ResumeTemplate.objects.get(slug=slug, is_active=True)
    except ResumeTemplate.DoesNotExist:
        logger.warning(f"Template '{slug}' not found, using default")
        return ResumeTemplate.objects.get(slug=default_slug)
```

### Color Validation Errors

```python
def validate_hex_color(color: str) -> bool:
    """Validate hex color format"""
    import re
    return bool(re.match(r'^#[0-9A-Fa-f]{6}$', color))

def safe_color_or_default(color: str, default: str = '#4a9d9a') -> str:
    """Return color if valid, otherwise return default"""
    return color if validate_hex_color(color) else default
```

### Preview Image Fallback

```python
def get_template_preview_url(template) -> str:
    """Get preview image URL with fallback"""
    if template.preview_image:
        return template.preview_image.url
    return f'/static/images/template_fallbacks/{template.slug}.svg'
```

## Testing Strategy

### Unit Tests

Unit tests verify specific examples and edge cases:

1. **Template Model Tests**
   - Test template creation with all required fields
   - Test slug auto-generation
   - Test category choices validation

2. **Color Utility Tests**
   - Test hex_to_rgb conversion with known values
   - Test contrast ratio calculation with known pairs
   - Test complementary color generation

3. **Template Pairing Tests**
   - Test all resume templates have a paired cover letter
   - Test branding application copies color correctly

### Property-Based Tests

Property-based tests verify universal properties across all inputs using Hypothesis:

1. **Property 1: Template Inventory** - Verify template counts per category
2. **Property 2: WCAG Compliance** - Verify all palettes meet contrast requirements
3. **Property 3: Font Stacks** - Verify generated HTML contains approved fonts
4. **Property 4: Role Recommendations** - Verify recommendations return valid templates
5. **Property 5: Cover Letter Count** - Verify minimum template count
6. **Property 6: Color Consistency** - Verify branding application
7. **Property 7: Letter Structure** - Verify HTML contains required sections
8. **Property 8: Color Generation** - Verify complementary color output format
9. **Property 9: PDF Consistency** - Verify deterministic PDF output

### Test Configuration

```python
# conftest.py
import pytest
from hypothesis import settings

# Configure Hypothesis for property-based tests
settings.register_profile("ci", max_examples=100)
settings.register_profile("dev", max_examples=20)
settings.load_profile("dev")

@pytest.fixture
def sample_resume():
    """Create a sample resume for testing"""
    return Resume(
        full_name="John Doe",
        email="john@example.com",
        role_title="Software Engineer",
        skills=["Python", "Django", "AWS"],
        # ... other fields
    )
```

## Migration Plan

1. **Phase 1: Database Updates**
   - Add new fields to ResumeTemplate model (display_order, is_ats_safe, recommended_roles)
   - Add paired_resume_template to CoverLetterTemplate
   - Run migrations

2. **Phase 2: New Templates**
   - Implement Minimal, Creative, Technical template HTML builders
   - Add corresponding CSS styles
   - Create database entries for new templates

3. **Phase 3: Color System**
   - Implement color_utils.py
   - Update template_themes.py with new palettes
   - Add WCAG validation to color picker

4. **Phase 4: UI Updates**
   - Update template selector with new grid layout
   - Add category filtering
   - Implement lazy loading for preview images

5. **Phase 5: Testing**
   - Write property-based tests
   - Run visual regression tests
   - Verify PDF output matches preview
