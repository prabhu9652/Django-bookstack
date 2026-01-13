"""
Production-Grade PDF Generator using Browser-Based Rendering
============================================================

ARCHITECTURE:
- Uses Playwright (Chromium) for PDF generation
- Same rendering engine as browser preview = pixel-perfect match
- Single source of truth: the preview HTML/CSS

WHY THIS WORKS:
- Browser preview uses Chromium to render HTML/CSS
- Playwright uses the SAME Chromium engine
- Result: Preview = PDF (guaranteed)
"""

import io
import base64
import logging
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

# Check Playwright availability at import time
PLAYWRIGHT_AVAILABLE = False

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
    logger.info("Playwright available - using browser-based PDF generation")
except ImportError:
    logger.warning("Playwright not available - PDF generation will fail")


# =============================================================================
# MAIN PDF GENERATION API
# =============================================================================

def generate_resume_pdf(resume, request=None) -> bytes:
    """
    Generate pixel-perfect PDF from resume using Playwright (Chromium).
    """
    if not PLAYWRIGHT_AVAILABLE:
        raise RuntimeError(
            "Playwright not available.\n"
            "Install: pip install playwright && playwright install chromium"
        )
    
    html_content = build_resume_html(resume)
    return _generate_pdf_with_playwright(html_content)


def generate_cover_letter_pdf(cover_letter) -> bytes:
    """Generate pixel-perfect PDF from cover letter using Playwright."""
    if not PLAYWRIGHT_AVAILABLE:
        raise RuntimeError(
            "Playwright not available.\n"
            "Install: pip install playwright && playwright install chromium"
        )
    
    html_content = build_cover_letter_html(cover_letter)
    return _generate_pdf_with_playwright(html_content)


# =============================================================================
# PLAYWRIGHT PDF GENERATION (Primary - Pixel Perfect)
# =============================================================================

def _generate_pdf_with_playwright(html_content: str) -> bytes:
    """
    Generate PDF using Playwright's Chromium engine.
    
    This guarantees pixel-perfect output because:
    - Same engine as browser preview
    - Full CSS support (flexbox, grid, etc.)
    - Identical font rendering
    - Identical layout calculations
    """
    async def _async_generate():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Set viewport to A4 dimensions at 96 DPI
            await page.set_viewport_size({
                'width': 794,   # A4 width at 96 DPI
                'height': 1123  # A4 height at 96 DPI
            })
            
            # Load HTML content
            await page.set_content(html_content, wait_until='networkidle')
            
            # Generate PDF with A4 settings
            pdf_bytes = await page.pdf(
                format='A4',
                print_background=True,
                margin={
                    'top': '0mm',
                    'right': '0mm',
                    'bottom': '0mm',
                    'left': '0mm'
                }
            )
            
            await browser.close()
            return pdf_bytes
    
    # Run async function in sync context
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If already in async context, create new loop
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, _async_generate())
                return future.result()
        else:
            return loop.run_until_complete(_async_generate())
    except RuntimeError:
        return asyncio.run(_async_generate())


# =============================================================================
# HTML BUILDER - Single Source of Truth
# =============================================================================

def build_resume_html(resume) -> str:
    """
    Build complete HTML document for resume.
    
    This HTML is used for BOTH preview and PDF generation,
    ensuring pixel-perfect match.
    """
    template_slug = resume.template.slug if resume.template else 'professional'
    primary_color = resume.primary_color or (
        resume.template.primary_color if resume.template else '#4a9d9a'
    )
    
    # Get template-specific body content
    if template_slug == 'modern':
        body_html = _build_modern_template(resume, primary_color)
    elif template_slug == 'executive':
        body_html = _build_executive_template(resume, primary_color)
    elif template_slug == 'minimal':
        body_html = _build_minimal_template(resume, primary_color)
    elif template_slug == 'creative':
        body_html = _build_creative_template(resume, primary_color)
    elif template_slug == 'technical':
        body_html = _build_technical_template(resume, primary_color)
    else:
        body_html = _build_professional_template(resume, primary_color)
    
    # Build complete HTML document
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(resume.full_name)} - Resume</title>
    <style>
{_get_base_styles()}
{_get_template_styles(template_slug, primary_color)}
    </style>
</head>
<body>
    <div class="resume-page">
        {body_html}
    </div>
</body>
</html>'''


# =============================================================================
# BASE STYLES - Shared across all templates
# =============================================================================

def _get_base_styles() -> str:
    """Base CSS reset and typography."""
    return '''
/* A4 Page Setup */
@page {
    size: A4;
    margin: 0;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    width: 210mm;
    min-height: 297mm;
    font-family: 'Segoe UI', 'Roboto', -apple-system, BlinkMacSystemFont, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.4;
    color: #333;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.resume-page {
    width: 210mm;
    min-height: 297mm;
    background: #fff;
    overflow: hidden;
}

/* Typography */
h1, h2, h3 { margin: 0; }
p { margin: 0; }
ul { margin: 0; padding: 0; }
li { margin-bottom: 1.5mm; }
strong { font-weight: 600; }
'''


# =============================================================================
# MODERN TEMPLATE - Clean design, Main LEFT, Skills RIGHT
# =============================================================================

def _build_modern_template(resume, primary_color: str) -> str:
    """Build Modern template HTML."""
    
    # Header contact - include all contact info including LinkedIn and GitHub
    contact_parts = []
    if resume.email:
        contact_parts.append(f'<span>✉ {_escape(resume.email)}</span>')
    if resume.phone:
        contact_parts.append(f'<span>✆ {_escape(resume.phone)}</span>')
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_parts.append(f'<span>⌂ {_escape(loc)}</span>')
    if resume.linkedin:
        contact_parts.append(f'<span>in {_escape(resume.linkedin)}</span>')
    if resume.github:
        contact_parts.append(f'<span>⌘ {_escape(resume.github)}</span>')
    
    # Summary
    summary_html = ''
    if resume.summary:
        summary_html = f'''
        <section class="section">
            <h2 class="section-title">Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    # Education
    education_html = _build_education_html(resume.education, 'modern')
    
    # Employment
    employment_html = _build_employment_html(resume.experience, 'modern')
    
    # Sidebar - Skills
    skills_html = _build_skills_html(resume.skills, 'modern')
    
    # Sidebar - Languages
    languages_html = ''
    if resume.languages:
        languages_html = f'''
        <div class="sidebar-section">
            <h3 class="sidebar-title">Languages</h3>
            {_build_skills_html(resume.languages, 'modern')}
        </div>'''
    
    return f'''
    <header class="header">
        <h1 class="name">{_escape(resume.full_name)}</h1>
        <p class="role">{_escape(resume.role_title or '')}</p>
        <div class="contact">{''.join(contact_parts)}</div>
    </header>
    
    <div class="body-container">
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
        
        <aside class="sidebar">
            <div class="sidebar-section">
                <h3 class="sidebar-title">Skills</h3>
                {skills_html}
            </div>
            {languages_html}
        </aside>
    </div>'''


def _get_modern_styles(primary_color: str) -> str:
    """CSS for Modern template."""
    return f'''
/* Modern Header */
.header {{
    background: {primary_color};
    color: #fff;
    padding: 28px 36px;
}}

.header .name {{
    font-size: 26pt;
    font-weight: 400;
    margin-bottom: 4px;
}}

.header .role {{
    font-size: 12pt;
    font-weight: 300;
    color: rgba(255,255,255,0.85);
    margin-bottom: 12px;
}}

.header .contact {{
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    font-size: 9pt;
    color: rgba(255,255,255,0.8);
}}

/* Body - Flexbox Layout */
.body-container {{
    display: flex;
    min-height: calc(297mm - 100px);
}}

.main-content {{
    flex: 1;
    padding: 30px 28px 24px 28px;
    border-right: 1px solid #e5e7eb;
}}

.sidebar {{
    width: 180px;
    background: #f8f9fa;
    padding: 30px 18px 24px 18px;
}}

/* Sections */
.section {{
    margin-bottom: 24px;
}}

.section-title {{
    font-size: 14pt;
    font-weight: 400;
    color: #333;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}

.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.6;
    text-align: justify;
}}

/* Sidebar */
.sidebar-section {{
    margin-bottom: 20px;
}}

.sidebar-title {{
    font-size: 11pt;
    font-weight: 400;
    color: {primary_color};
    margin-bottom: 10px;
    padding-bottom: 4px;
    border-bottom: 1px solid #dee2e6;
}}

.sidebar-text {{
    font-size: 9pt;
    color: #666;
    word-break: break-all;
}}

.skills-list {{
    list-style: none;
}}

.skills-list li {{
    font-size: 9.5pt;
    color: #444;
    padding: 6px 0;
    border-bottom: 1px solid #e9ecef;
}}

.skills-list li:last-child {{
    border-bottom: none;
}}

/* Entries */
.entry {{
    margin-bottom: 18px;
}}

.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}}

.entry-title {{
    font-weight: 600;
    font-size: 10.5pt;
    color: #333;
}}

.entry-date {{
    font-size: 9pt;
    color: #666;
}}

.entry-subtitle {{
    font-size: 9.5pt;
    color: {primary_color};
    margin-bottom: 8px;
}}

.entry-bullets {{
    margin: 0;
    padding-left: 16px;
    list-style-type: disc;
}}

.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.5;
}}
'''


# =============================================================================
# EXECUTIVE TEMPLATE - Bold design, Skills LEFT with bars, Main RIGHT
# =============================================================================

def _build_executive_template(resume, primary_color: str) -> str:
    """Build Executive template HTML."""
    
    # Header contact
    contact_items = []
    if resume.email:
        contact_items.append(f'<div>✉ {_escape(resume.email)}</div>')
    if resume.phone:
        contact_items.append(f'<div>✆ {_escape(resume.phone)}</div>')
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_items.append(f'<div>⌂ {_escape(loc)}</div>')
    if resume.linkedin:
        contact_items.append(f'<div>in {_escape(resume.linkedin)}</div>')
    
    # Skills with colored bars
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li><span class="skill-bar"></span>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'<ul class="exec-skills">{items}</ul>'
    
    # Languages
    languages_html = ''
    if resume.languages:
        items = ''.join([f'<li><span class="skill-bar"></span>{_escape(l)}</li>' for l in resume.languages])
        languages_html = f'''
        <div class="sidebar-section">
            <h3 class="sidebar-heading">LANGUAGES</h3>
            <ul class="exec-skills">{items}</ul>
        </div>'''
    
    # Summary
    summary_html = ''
    if resume.summary:
        summary_html = f'''
        <section class="section">
            <h2 class="section-heading"><span class="badge">SUMMARY</span></h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    # Education & Employment
    education_html = _build_education_html(resume.education, 'executive')
    employment_html = _build_employment_html(resume.experience, 'executive')
    
    return f'''
    <header class="header">
        <h1 class="name">{_escape(resume.full_name).upper()}</h1>
        <p class="role">{_escape(resume.role_title or '')}</p>
        <div class="contact">{''.join(contact_items)}</div>
    </header>
    
    <div class="body-container">
        <aside class="sidebar">
            <div class="sidebar-section">
                <h3 class="sidebar-heading">SKILLS</h3>
                {skills_html}
            </div>
            {languages_html}
        </aside>
        
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
    </div>'''


def _get_executive_styles(primary_color: str) -> str:
    """CSS for Executive template."""
    return f'''
/* Executive Header */
.header {{
    background: {primary_color};
    color: #fff;
    padding: 28px 36px;
}}

.header .name {{
    font-size: 30pt;
    font-weight: 700;
    letter-spacing: 3px;
    margin-bottom: 4px;
}}

.header .role {{
    font-size: 12pt;
    font-weight: 400;
    margin-bottom: 14px;
}}

.header .contact {{
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 9pt;
    color: rgba(255,255,255,0.9);
}}

/* Body - Flexbox Layout */
.body-container {{
    display: flex;
    min-height: calc(297mm - 120px);
}}

.sidebar {{
    width: 180px;
    background: #f5f5f5;
    padding: 30px 18px 24px 18px;
}}

.main-content {{
    flex: 1;
    padding: 30px 28px 24px 28px;
}}

/* Sidebar */
.sidebar-section {{
    margin-bottom: 20px;
}}

.sidebar-heading {{
    font-size: 10pt;
    font-weight: 700;
    color: #333;
    letter-spacing: 1px;
    margin-bottom: 14px;
}}

.exec-skills {{
    list-style: none;
}}

.exec-skills li {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 9.5pt;
    color: #333;
    margin-bottom: 8px;
}}

.skill-bar {{
    width: 8px;
    height: 8px;
    background: {primary_color};
    flex-shrink: 0;
}}

/* Sections */
.section {{
    margin-bottom: 24px;
}}

.section-heading {{
    margin-bottom: 12px;
}}

.badge {{
    display: inline-block;
    background: {primary_color};
    color: #fff;
    font-size: 10pt;
    font-weight: 600;
    letter-spacing: 1px;
    padding: 4px 12px;
}}

.section-text {{
    font-size: 10pt;
    color: #333;
    line-height: 1.55;
    text-align: justify;
}}

/* Entries */
.entry {{
    margin-bottom: 18px;
}}

.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}}

.entry-title {{
    font-weight: 700;
    font-size: 10.5pt;
    color: #333;
}}

.entry-date {{
    font-size: 9pt;
    color: #555;
}}

.entry-subtitle {{
    font-size: 9.5pt;
    color: {primary_color};
    margin-bottom: 8px;
}}

.entry-bullets {{
    margin: 0;
    padding-left: 16px;
    list-style-type: disc;
}}

.entry-bullets li {{
    font-size: 9.5pt;
    color: #333;
    margin-bottom: 6px;
    line-height: 1.5;
    text-align: justify;
}}
'''


# =============================================================================
# PROFESSIONAL TEMPLATE - Photo header, Skills LEFT, Main RIGHT
# =============================================================================

def _build_professional_template(resume, primary_color: str) -> str:
    """Build Professional template HTML."""
    
    # Photo
    photo_html = _get_photo_html(resume)
    
    # Contact items
    contact_items = []
    if resume.email:
        contact_items.append(f'<div class="contact-item"><span class="icon">✉</span> {_escape(resume.email)}</div>')
    if resume.phone:
        contact_items.append(f'<div class="contact-item"><span class="icon">✆</span> {_escape(resume.phone)}</div>')
    if resume.address:
        contact_items.append(f'<div class="contact-item"><span class="icon">⌂</span> {_escape(resume.address)}</div>')
    if resume.linkedin:
        contact_items.append(f'<div class="contact-item"><span class="icon">in</span> {_escape(resume.linkedin)}</div>')
    if resume.github:
        contact_items.append(f'<div class="contact-item"><span class="icon">⌘</span> {_escape(resume.github)}</div>')
    
    # Skills
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''
        <div class="sidebar-section">
            <h2 class="sidebar-heading">SKILLS</h2>
            <ul class="simple-list">{items}</ul>
        </div>'''
    
    # Languages
    languages_html = ''
    if resume.languages:
        items = ''.join([f'<li>{_escape(l)}</li>' for l in resume.languages])
        languages_html = f'''
        <div class="sidebar-section">
            <h2 class="sidebar-heading">LANGUAGES</h2>
            <ul class="simple-list">{items}</ul>
        </div>'''
    
    # Education in sidebar
    education_sidebar = _build_education_sidebar(resume.education)
    
    # Profile
    profile_html = ''
    if resume.summary:
        profile_html = f'''
        <section class="section">
            <h2 class="section-heading"><span class="badge">PROFILE</span></h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    # Employment
    employment_html = _build_employment_html(resume.experience, 'professional')
    
    return f'''
    <header class="header">
        <div class="header-photo">
            {photo_html}
        </div>
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name).upper()}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{''.join(contact_items)}</div>
        </div>
    </header>
    
    <div class="body-container">
        <aside class="sidebar">
            {skills_html}
            {languages_html}
            {education_sidebar}
        </aside>
        
        <main class="main-content">
            {profile_html}
            {employment_html}
        </main>
    </div>'''


def _get_professional_styles(primary_color: str) -> str:
    """CSS for Professional template."""
    return f'''
/* Professional Header */
.header {{
    background: {primary_color};
    color: #fff;
    padding: 30px 40px;
    display: flex;
    align-items: center;
    gap: 30px;
}}

.header-photo {{
    width: 120px;
    height: 120px;
    border-radius: 50%;
    overflow: hidden;
    border: 4px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
    background: rgba(255,255,255,0.1);
    display: flex;
    align-items: center;
    justify-content: center;
}}

.header-photo img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

.photo-placeholder {{
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 48px;
    color: rgba(255,255,255,0.5);
}}

.header-info {{
    flex: 1;
}}

.header .name {{
    font-size: 32pt;
    font-weight: 700;
    letter-spacing: 3px;
    margin-bottom: 4px;
}}

.header .role {{
    font-size: 14pt;
    font-weight: 500;
    color: rgba(255,255,255,0.9);
    margin-bottom: 16px;
}}

.header .contact {{
    display: flex;
    flex-direction: column;
    gap: 6px;
}}

.contact-item {{
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 9.5pt;
    color: rgba(255,255,255,0.95);
}}

.contact-item .icon {{
    width: 14px;
}}

/* Body - Flexbox Layout */
.body-container {{
    display: flex;
    min-height: calc(297mm - 180px);
}}

.sidebar {{
    width: 200px;
    background: #f8f9fa;
    padding: 30px 20px 24px 20px;
    border-right: 1px solid #e5e7eb;
}}

.main-content {{
    flex: 1;
    padding: 30px 30px 24px 30px;
}}

/* Sidebar */
.sidebar-section {{
    margin-bottom: 24px;
}}

.sidebar-heading {{
    font-size: 11pt;
    font-weight: 700;
    color: {primary_color};
    letter-spacing: 1px;
    margin-bottom: 12px;
}}

.simple-list {{
    list-style: none;
}}

.simple-list li {{
    font-size: 9.5pt;
    color: #1a1a1a;
    padding: 3px 0;
}}

/* Education in Sidebar */
.edu-item {{
    margin-bottom: 12px;
}}

.edu-degree {{
    font-weight: 600;
    font-size: 9.5pt;
    color: #1a1a1a;
}}

.edu-field {{
    font-size: 9.5pt;
    color: #1a1a1a;
}}

.edu-school {{
    font-size: 9.5pt;
    color: #1a1a1a;
}}

.edu-year {{
    font-size: 9.5pt;
    color: #1a1a1a;
}}

/* Sections */
.section {{
    margin-bottom: 24px;
}}

.section-heading {{
    margin-bottom: 12px;
}}

.badge {{
    display: inline-block;
    background: {primary_color};
    color: #fff;
    font-size: 10pt;
    font-weight: 600;
    letter-spacing: 1px;
    padding: 4px 12px;
}}

.section-text {{
    font-size: 10pt;
    color: #333;
    line-height: 1.5;
    text-align: justify;
}}

/* Entries */
.entry {{
    margin-bottom: 20px;
}}

.entry-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 2px;
}}

.entry-title {{
    font-weight: 700;
    font-size: 11pt;
    color: #1a1a1a;
}}

.entry-date {{
    font-size: 9.5pt;
    color: #666;
}}

.entry-subtitle {{
    font-size: 10pt;
    color: {primary_color};
    margin-bottom: 8px;
}}

.entry-bullets {{
    margin: 0;
    padding-left: 16px;
    list-style-type: disc;
}}

.entry-bullets li {{
    font-size: 9.5pt;
    color: #333;
    margin-bottom: 6px;
    line-height: 1.45;
    text-align: justify;
}}

.entry-bullets li strong {{
    font-weight: 700;
    color: #1a1a1a;
}}
'''


# =============================================================================
# MINIMAL CLEAN TEMPLATE - Single column, maximum whitespace, subtle accents
# =============================================================================

def _build_minimal_template(resume, primary_color: str) -> str:
    """
    Build Minimal Clean template HTML.
    
    Features:
    - Single column layout
    - Maximum whitespace
    - Centered header
    - Inline skills with bullet separators
    - Clean typography hierarchy
    """
    # Contact line with bullet separators
    contact_parts = []
    if resume.email:
        contact_parts.append(_escape(resume.email))
    if resume.phone:
        contact_parts.append(_escape(resume.phone))
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_parts.append(_escape(loc))
    if resume.linkedin:
        contact_parts.append(_escape(resume.linkedin))
    if resume.github:
        contact_parts.append(_escape(resume.github))
    
    contact_html = ' <span class="separator">•</span> '.join(contact_parts)
    
    # Summary
    summary_html = ''
    if resume.summary:
        summary_html = f'''
        <section class="section">
            <p class="summary-text">{_escape(resume.summary)}</p>
        </section>'''
    
    # Experience
    experience_html = _build_minimal_experience(resume.experience, primary_color)
    
    # Education
    education_html = _build_minimal_education(resume.education, primary_color)
    
    # Skills (inline with bullet separators)
    skills_html = ''
    if resume.skills:
        skills_inline = ' <span class="separator">•</span> '.join([_escape(s) for s in resume.skills])
        skills_html = f'''
        <section class="section">
            <h2 class="section-title">Skills</h2>
            <p class="skills-inline">{skills_inline}</p>
        </section>'''
    
    # Languages (inline)
    languages_html = ''
    if resume.languages:
        langs_inline = ' <span class="separator">•</span> '.join([_escape(l) for l in resume.languages])
        languages_html = f'''
        <section class="section">
            <h2 class="section-title">Languages</h2>
            <p class="skills-inline">{langs_inline}</p>
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
        {languages_html}
    </main>'''


def _build_minimal_experience(experience: list, primary_color: str) -> str:
    """Build experience section for Minimal template."""
    if not experience:
        return ''
    
    entries = ''
    for exp in experience:
        role = _escape(exp.get('role', ''))
        company = _escape(exp.get('company', ''))
        start = _escape(exp.get('start_date', ''))
        end = _escape(exp.get('end_date', ''))
        date_str = f"{start} – {end}" if start else end
        
        bullets_html = ''
        if exp.get('bullets'):
            items = ''.join([f'<li>{_format_bullet(b)}</li>' for b in exp['bullets']])
            bullets_html = f'<ul class="entry-bullets">{items}</ul>'
        
        entries += f'''
        <div class="entry">
            <div class="entry-header">
                <div class="entry-left">
                    <span class="entry-title">{role}</span>
                    <span class="entry-company">{company}</span>
                </div>
                <span class="entry-date">{date_str}</span>
            </div>
            {bullets_html}
        </div>'''
    
    return f'''
    <section class="section">
        <h2 class="section-title">Experience</h2>
        {entries}
    </section>'''


def _build_minimal_education(education: list, primary_color: str) -> str:
    """Build education section for Minimal template."""
    if not education:
        return ''
    
    entries = ''
    for edu in education:
        degree = _escape(edu.get('degree', ''))
        field = _escape(edu.get('field', ''))
        school = _escape(edu.get('school', ''))
        year = _escape(edu.get('graduation_date', ''))
        
        title = f"{degree} in {field}" if field else degree
        
        entries += f'''
        <div class="entry">
            <div class="entry-header">
                <div class="entry-left">
                    <span class="entry-title">{title}</span>
                    <span class="entry-company">{school}</span>
                </div>
                <span class="entry-date">{year}</span>
            </div>
        </div>'''
    
    return f'''
    <section class="section">
        <h2 class="section-title">Education</h2>
        {entries}
    </section>'''


def _get_minimal_styles(primary_color: str) -> str:
    """CSS for Minimal Clean template."""
    return f'''
/* Minimal Header - Centered */
.header {{
    text-align: center;
    padding: 40px 50px 30px;
    border-bottom: 1px solid #e5e7eb;
}}

.header .name {{
    font-size: 28pt;
    font-weight: 300;
    color: #1a1a1a;
    letter-spacing: 2px;
    margin-bottom: 6px;
}}

.header .role {{
    font-size: 11pt;
    font-weight: 400;
    color: {primary_color};
    margin-bottom: 12px;
}}

.header .contact {{
    font-size: 9pt;
    color: #666;
    line-height: 1.6;
}}

.header .separator {{
    color: #ccc;
    margin: 0 2px;
}}

/* Content - Single Column */
.content {{
    padding: 30px 50px;
    max-width: 100%;
}}

/* Sections */
.section {{
    margin-bottom: 28px;
}}

.section-title {{
    font-size: 11pt;
    font-weight: 600;
    color: #1a1a1a;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid {primary_color};
}}

.summary-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
    text-align: justify;
}}

.skills-inline {{
    font-size: 10pt;
    color: #444;
    line-height: 1.8;
}}

.skills-inline .separator {{
    color: #ccc;
    margin: 0 4px;
}}

/* Entries */
.entry {{
    margin-bottom: 18px;
}}

.entry-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 6px;
}}

.entry-left {{
    display: flex;
    flex-direction: column;
}}

.entry-title {{
    font-weight: 600;
    font-size: 10.5pt;
    color: #1a1a1a;
}}

.entry-company {{
    font-size: 9.5pt;
    color: {primary_color};
    margin-top: 2px;
}}

.entry-date {{
    font-size: 9pt;
    color: #888;
    white-space: nowrap;
}}

.entry-bullets {{
    margin: 8px 0 0 0;
    padding-left: 18px;
    list-style-type: disc;
}}

.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 4px;
    line-height: 1.5;
}}

.entry-bullets li strong {{
    font-weight: 600;
    color: #1a1a1a;
}}
'''


# =============================================================================
# CREATIVE BOLD TEMPLATE - Asymmetric two-column, bold name block, visual skills
# =============================================================================

def _build_creative_template(resume, primary_color: str) -> str:
    """
    Build Creative Bold template HTML.
    
    Features:
    - Asymmetric two-column layout (narrow left sidebar, wide right main)
    - Bold name block with color background
    - Skills with visual dot indicators
    - Modern, eye-catching design for creative roles
    """
    # Contact info for sidebar
    contact_items = []
    if resume.email:
        contact_items.append(f'<div class="contact-item">{_escape(resume.email)}</div>')
    if resume.phone:
        contact_items.append(f'<div class="contact-item">{_escape(resume.phone)}</div>')
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_items.append(f'<div class="contact-item">{_escape(loc)}</div>')
    if resume.linkedin:
        contact_items.append(f'<div class="contact-item">{_escape(resume.linkedin)}</div>')
    if resume.github:
        contact_items.append(f'<div class="contact-item">{_escape(resume.github)}</div>')
    
    # Skills with dot indicators
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li><span class="skill-dot"></span>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''
        <div class="sidebar-section">
            <h3 class="sidebar-title">SKILLS</h3>
            <ul class="creative-skills">{items}</ul>
        </div>'''
    
    # Languages
    languages_html = ''
    if resume.languages:
        items = ''.join([f'<li><span class="skill-dot"></span>{_escape(l)}</li>' for l in resume.languages])
        languages_html = f'''
        <div class="sidebar-section">
            <h3 class="sidebar-title">LANGUAGES</h3>
            <ul class="creative-skills">{items}</ul>
        </div>'''
    
    # Summary
    summary_html = ''
    if resume.summary:
        summary_html = f'''
        <section class="section">
            <h2 class="section-title">About Me</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    # Experience
    experience_html = _build_creative_experience(resume.experience, primary_color)
    
    # Education
    education_html = _build_creative_education(resume.education, primary_color)
    
    return f'''
    <header class="header">
        <div class="name-block">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
        </div>
    </header>
    
    <div class="body-container">
        <aside class="sidebar">
            <div class="sidebar-section">
                <h3 class="sidebar-title">CONTACT</h3>
                {''.join(contact_items)}
            </div>
            {skills_html}
            {languages_html}
        </aside>
        
        <main class="main-content">
            {summary_html}
            {experience_html}
            {education_html}
        </main>
    </div>'''


def _build_creative_experience(experience: list, primary_color: str) -> str:
    """Build experience section for Creative template."""
    if not experience:
        return ''
    
    entries = ''
    for exp in experience:
        role = _escape(exp.get('role', ''))
        company = _escape(exp.get('company', ''))
        start = _escape(exp.get('start_date', ''))
        end = _escape(exp.get('end_date', ''))
        date_str = f"{start} – {end}" if start else end
        
        bullets_html = ''
        if exp.get('bullets'):
            items = ''.join([f'<li>{_format_bullet(b)}</li>' for b in exp['bullets']])
            bullets_html = f'<ul class="entry-bullets">{items}</ul>'
        
        entries += f'''
        <div class="entry">
            <div class="entry-header">
                <span class="entry-title">{role}</span>
                <span class="entry-date">{date_str}</span>
            </div>
            <div class="entry-subtitle">{company}</div>
            {bullets_html}
        </div>'''
    
    return f'''
    <section class="section">
        <h2 class="section-title">Experience</h2>
        {entries}
    </section>'''


def _build_creative_education(education: list, primary_color: str) -> str:
    """Build education section for Creative template."""
    if not education:
        return ''
    
    entries = ''
    for edu in education:
        degree = _escape(edu.get('degree', ''))
        field = _escape(edu.get('field', ''))
        school = _escape(edu.get('school', ''))
        year = _escape(edu.get('graduation_date', ''))
        
        title = f"{degree} in {field}" if field else degree
        
        entries += f'''
        <div class="entry">
            <div class="entry-header">
                <span class="entry-title">{title}</span>
                <span class="entry-date">{year}</span>
            </div>
            <div class="entry-subtitle">{school}</div>
        </div>'''
    
    return f'''
    <section class="section">
        <h2 class="section-title">Education</h2>
        {entries}
    </section>'''


def _get_creative_styles(primary_color: str) -> str:
    """CSS for Creative Bold template."""
    return f'''
/* Creative Header - Bold name block */
.header {{
    background: #fff;
    padding: 0;
}}

.name-block {{
    background: {primary_color};
    color: #fff;
    padding: 35px 40px;
    margin: 20px 20px 0 20px;
}}

.header .name {{
    font-size: 32pt;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 6px;
}}

.header .role {{
    font-size: 13pt;
    font-weight: 400;
    color: rgba(255,255,255,0.9);
}}

/* Body - Asymmetric two-column */
.body-container {{
    display: flex;
    min-height: calc(297mm - 140px);
    padding: 0 20px 20px 20px;
}}

.sidebar {{
    width: 160px;
    background: #f5f5f5;
    padding: 25px 18px;
    flex-shrink: 0;
}}

.main-content {{
    flex: 1;
    padding: 25px 28px;
}}

/* Sidebar */
.sidebar-section {{
    margin-bottom: 22px;
}}

.sidebar-title {{
    font-size: 9pt;
    font-weight: 700;
    color: {primary_color};
    letter-spacing: 1.5px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}

.contact-item {{
    font-size: 8.5pt;
    color: #333;
    margin-bottom: 8px;
    word-break: break-all;
    line-height: 1.4;
}}

.creative-skills {{
    list-style: none;
}}

.creative-skills li {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 9pt;
    color: #333;
    margin-bottom: 7px;
}}

.skill-dot {{
    width: 6px;
    height: 6px;
    background: {primary_color};
    border-radius: 50%;
    flex-shrink: 0;
}}

/* Sections */
.section {{
    margin-bottom: 22px;
}}

.section-title {{
    font-size: 12pt;
    font-weight: 700;
    color: {primary_color};
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid #e5e7eb;
}}

.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.6;
    text-align: justify;
}}

/* Entries */
.entry {{
    margin-bottom: 16px;
}}

.entry-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 2px;
}}

.entry-title {{
    font-weight: 700;
    font-size: 10.5pt;
    color: #1a1a1a;
}}

.entry-date {{
    font-size: 9pt;
    color: #666;
    white-space: nowrap;
}}

.entry-subtitle {{
    font-size: 9.5pt;
    color: {primary_color};
    margin-bottom: 8px;
}}

.entry-bullets {{
    margin: 6px 0 0 0;
    padding-left: 16px;
    list-style-type: disc;
}}

.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 4px;
    line-height: 1.5;
}}

.entry-bullets li strong {{
    font-weight: 600;
    color: #1a1a1a;
}}
'''


# =============================================================================
# TECHNICAL TEMPLATE - Skills sidebar, projects emphasis, GitHub/LinkedIn header
# =============================================================================

def _build_technical_template(resume, primary_color: str) -> str:
    """
    Build Technical template HTML.
    
    Features:
    - Skills prominently displayed in sidebar
    - Clean, scannable layout
    - GitHub/LinkedIn in header contact area
    - Monospace accents for technical feel
    - Optimized for software engineers, DevOps, SRE roles
    """
    # Header contact - include GitHub and LinkedIn prominently
    contact_parts = []
    if resume.email:
        contact_parts.append(f'<span class="contact-item">✉ {_escape(resume.email)}</span>')
    if resume.phone:
        contact_parts.append(f'<span class="contact-item">✆ {_escape(resume.phone)}</span>')
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_parts.append(f'<span class="contact-item">⌂ {_escape(loc)}</span>')
    if resume.github:
        contact_parts.append(f'<span class="contact-item github">⌘ {_escape(resume.github)}</span>')
    if resume.linkedin:
        contact_parts.append(f'<span class="contact-item linkedin">in {_escape(resume.linkedin)}</span>')
    
    # Skills in sidebar with categories
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''
        <div class="sidebar-section">
            <h3 class="sidebar-title">TECHNICAL SKILLS</h3>
            <ul class="tech-skills">{items}</ul>
        </div>'''
    
    # Languages
    languages_html = ''
    if resume.languages:
        items = ''.join([f'<li>{_escape(l)}</li>' for l in resume.languages])
        languages_html = f'''
        <div class="sidebar-section">
            <h3 class="sidebar-title">LANGUAGES</h3>
            <ul class="tech-skills">{items}</ul>
        </div>'''
    
    # Summary
    summary_html = ''
    if resume.summary:
        summary_html = f'''
        <section class="section">
            <h2 class="section-title">Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    # Experience
    experience_html = _build_technical_experience(resume.experience, primary_color)
    
    # Education
    education_html = _build_technical_education(resume.education, primary_color)
    
    return f'''
    <header class="header">
        <div class="header-main">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
        </div>
        <div class="header-contact">{''.join(contact_parts)}</div>
    </header>
    
    <div class="body-container">
        <aside class="sidebar">
            {skills_html}
            {languages_html}
        </aside>
        
        <main class="main-content">
            {summary_html}
            {experience_html}
            {education_html}
        </main>
    </div>'''


def _build_technical_experience(experience: list, primary_color: str) -> str:
    """Build experience section for Technical template."""
    if not experience:
        return ''
    
    entries = ''
    for exp in experience:
        role = _escape(exp.get('role', ''))
        company = _escape(exp.get('company', ''))
        start = _escape(exp.get('start_date', ''))
        end = _escape(exp.get('end_date', ''))
        date_str = f"{start} – {end}" if start else end
        
        bullets_html = ''
        if exp.get('bullets'):
            items = ''.join([f'<li>{_format_bullet(b)}</li>' for b in exp['bullets']])
            bullets_html = f'<ul class="entry-bullets">{items}</ul>'
        
        entries += f'''
        <div class="entry">
            <div class="entry-header">
                <div class="entry-left">
                    <span class="entry-title">{role}</span>
                    <span class="entry-company">{company}</span>
                </div>
                <span class="entry-date">{date_str}</span>
            </div>
            {bullets_html}
        </div>'''
    
    return f'''
    <section class="section">
        <h2 class="section-title">Experience</h2>
        {entries}
    </section>'''


def _build_technical_education(education: list, primary_color: str) -> str:
    """Build education section for Technical template."""
    if not education:
        return ''
    
    entries = ''
    for edu in education:
        degree = _escape(edu.get('degree', ''))
        field = _escape(edu.get('field', ''))
        school = _escape(edu.get('school', ''))
        year = _escape(edu.get('graduation_date', ''))
        
        title = f"{degree} in {field}" if field else degree
        
        entries += f'''
        <div class="entry">
            <div class="entry-header">
                <div class="entry-left">
                    <span class="entry-title">{title}</span>
                    <span class="entry-company">{school}</span>
                </div>
                <span class="entry-date">{year}</span>
            </div>
        </div>'''
    
    return f'''
    <section class="section">
        <h2 class="section-title">Education</h2>
        {entries}
    </section>'''


def _get_technical_styles(primary_color: str) -> str:
    """CSS for Technical template."""
    return f'''
/* Technical Header - Clean with prominent contact */
.header {{
    background: #1a1a1a;
    color: #fff;
    padding: 28px 36px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}}

.header-main {{
    flex: 1;
}}

.header .name {{
    font-size: 26pt;
    font-weight: 600;
    margin-bottom: 4px;
    font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
}}

.header .role {{
    font-size: 12pt;
    font-weight: 400;
    color: {primary_color};
}}

.header-contact {{
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 6px;
    font-size: 9pt;
    color: rgba(255,255,255,0.85);
}}

.header-contact .contact-item {{
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}}

.header-contact .github,
.header-contact .linkedin {{
    color: {primary_color};
}}

/* Body - Two column layout */
.body-container {{
    display: flex;
    min-height: calc(297mm - 100px);
}}

.sidebar {{
    width: 175px;
    background: #f8f9fa;
    padding: 28px 18px;
    border-right: 3px solid {primary_color};
}}

.main-content {{
    flex: 1;
    padding: 28px 30px;
}}

/* Sidebar */
.sidebar-section {{
    margin-bottom: 24px;
}}

.sidebar-title {{
    font-size: 9pt;
    font-weight: 700;
    color: #1a1a1a;
    letter-spacing: 1px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}

.tech-skills {{
    list-style: none;
}}

.tech-skills li {{
    font-size: 9pt;
    color: #333;
    padding: 5px 8px;
    margin-bottom: 4px;
    background: #fff;
    border-left: 2px solid {primary_color};
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}}

/* Sections */
.section {{
    margin-bottom: 24px;
}}

.section-title {{
    font-size: 12pt;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}

.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.6;
    text-align: justify;
}}

/* Entries */
.entry {{
    margin-bottom: 18px;
}}

.entry-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 6px;
}}

.entry-left {{
    display: flex;
    flex-direction: column;
}}

.entry-title {{
    font-weight: 600;
    font-size: 10.5pt;
    color: #1a1a1a;
}}

.entry-company {{
    font-size: 9.5pt;
    color: {primary_color};
    margin-top: 2px;
}}

.entry-date {{
    font-size: 9pt;
    color: #666;
    white-space: nowrap;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}}

.entry-bullets {{
    margin: 8px 0 0 0;
    padding-left: 18px;
    list-style-type: disc;
}}

.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.5;
}}

.entry-bullets li strong {{
    font-weight: 600;
    color: #1a1a1a;
}}
'''


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _get_template_styles(template_slug: str, primary_color: str) -> str:
    """Get CSS for specific template."""
    if template_slug == 'modern':
        return _get_modern_styles(primary_color)
    elif template_slug == 'executive':
        return _get_executive_styles(primary_color)
    elif template_slug == 'minimal':
        return _get_minimal_styles(primary_color)
    elif template_slug == 'creative':
        return _get_creative_styles(primary_color)
    elif template_slug == 'technical':
        return _get_technical_styles(primary_color)
    else:
        return _get_professional_styles(primary_color)


def _escape(text) -> str:
    """Escape HTML special characters."""
    if not text:
        return ''
    return (str(text)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def _format_bullet(text: str) -> str:
    """Format bullet text, converting **text** to <strong>."""
    import re
    if not text:
        return ''
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', str(text))


def _get_photo_html(resume) -> str:
    """Get photo HTML with base64 encoding."""
    photo_data = _get_photo_base64(resume)
    if photo_data:
        return f'<img src="data:image/jpeg;base64,{photo_data}" alt="{_escape(resume.full_name)}">'
    return '<div class="photo-placeholder">👤</div>'


def _get_photo_base64(resume) -> Optional[str]:
    """Convert profile photo to base64."""
    if not resume.profile_photo:
        return None
    
    try:
        from PIL import Image
        import os
        
        photo_path = resume.profile_photo.path
        if not os.path.exists(photo_path):
            return None
        
        img = Image.open(photo_path)
        img.thumbnail((400, 400), Image.Resampling.LANCZOS)
        
        if img.mode in ('RGBA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[3])
            else:
                background.paste(img)
            img = background
        
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=95)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    except Exception as e:
        logger.warning(f"Photo processing failed: {e}")
        return None


def _build_skills_html(skills: list, template: str) -> str:
    """Build skills list HTML."""
    if not skills:
        return ''
    items = ''.join([f'<li>{_escape(s)}</li>' for s in skills])
    return f'<ul class="skills-list">{items}</ul>'


def _build_education_html(education: list, template: str) -> str:
    """Build education section for main content."""
    if not education:
        return ''
    
    entries = ''
    for edu in education:
        degree = _escape(edu.get('degree', ''))
        field = _escape(edu.get('field', ''))
        school = _escape(edu.get('school', ''))
        year = _escape(edu.get('graduation_date', ''))
        
        title = f"{degree}, {field}" if field else degree
        
        entries += f'''
        <div class="entry">
            <div class="entry-header">
                <span class="entry-title">{title}</span>
                <span class="entry-date">{year}</span>
            </div>
            <div class="entry-subtitle">{school}</div>
        </div>'''
    
    if template == 'executive':
        return f'''
        <section class="section">
            <h2 class="section-heading"><span class="badge">EDUCATION</span></h2>
            {entries}
        </section>'''
    else:
        return f'''
        <section class="section">
            <h2 class="section-title">Education</h2>
            {entries}
        </section>'''


def _build_education_sidebar(education: list) -> str:
    """Build education for sidebar (Professional template)."""
    if not education:
        return ''
    
    items = ''
    for edu in education:
        degree = _escape(edu.get('degree', ''))
        field = _escape(edu.get('field', ''))
        school = _escape(edu.get('school', ''))
        year = _escape(edu.get('graduation_date', ''))
        
        items += f'''
        <div class="edu-item">
            <div class="edu-degree">{degree}</div>
            {f'<div class="edu-field">{field}</div>' if field else ''}
            <div class="edu-school">{school}</div>
            <div class="edu-year">{year}</div>
        </div>'''
    
    return f'''
    <div class="sidebar-section">
        <h2 class="sidebar-heading">EDUCATION</h2>
        {items}
    </div>'''


def _build_employment_html(experience: list, template: str) -> str:
    """Build employment section."""
    if not experience:
        return ''
    
    entries = ''
    for exp in experience:
        role = _escape(exp.get('role', ''))
        company = _escape(exp.get('company', ''))
        start = _escape(exp.get('start_date', ''))
        end = _escape(exp.get('end_date', ''))
        date_str = f"{start} - {end}" if start else end
        
        bullets_html = ''
        if exp.get('bullets'):
            items = ''.join([f'<li>{_format_bullet(b)}</li>' for b in exp['bullets']])
            bullets_html = f'<ul class="entry-bullets">{items}</ul>'
        
        entries += f'''
        <div class="entry">
            <div class="entry-header">
                <span class="entry-title">{role}</span>
                <span class="entry-date">{date_str}</span>
            </div>
            <div class="entry-subtitle">{company}</div>
            {bullets_html}
        </div>'''
    
    if template in ('executive', 'professional'):
        return f'''
        <section class="section">
            <h2 class="section-heading"><span class="badge">EMPLOYMENT</span></h2>
            {entries}
        </section>'''
    else:
        return f'''
        <section class="section">
            <h2 class="section-title">Employment</h2>
            {entries}
        </section>'''


# =============================================================================
# COVER LETTER HTML BUILDER - Matches preview_cover_letter.html exactly
# =============================================================================

def build_cover_letter_html(cover_letter) -> str:
    """Build complete HTML for cover letter matching preview exactly."""
    from datetime import date
    
    template_slug = cover_letter.template.slug if cover_letter.template else 'classic'
    primary_color = cover_letter.primary_color or (
        cover_letter.template.primary_color if cover_letter.template else '#1a1a1a'
    )
    
    today = date.today().strftime("%B %d, %Y")
    
    # Build template-specific HTML
    if template_slug == 'modern':
        return _build_modern_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'creative':
        return _build_creative_cover_letter(cover_letter, primary_color, today)
    else:
        return _build_classic_cover_letter(cover_letter, primary_color, today)


def _build_classic_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Build Classic cover letter - Georgia serif font, formal style."""
    
    # Contact
    contact_parts = []
    if cover_letter.email:
        contact_parts.append(f'<span>{_escape(cover_letter.email)}</span>')
    if cover_letter.phone:
        contact_parts.append(f'<span>{_escape(cover_letter.phone)}</span>')
    if cover_letter.linkedin:
        contact_parts.append(f'<span>{_escape(cover_letter.linkedin)}</span>')
    
    address_html = ''
    if cover_letter.address:
        address_html = f'<div class="sender-address">{_escape(cover_letter.address)}</div>'
    
    # Recipient
    recipient_name = f'<div class="recipient-name">{_escape(cover_letter.hiring_manager)}</div>' if cover_letter.hiring_manager else ''
    company_address = ''
    if hasattr(cover_letter, 'company_address') and cover_letter.company_address:
        company_address = f'<div class="company-address">{_escape(cover_letter.company_address)}</div>'
    
    # Body content
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        @page {{ size: A4; margin: 0; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #1a1a1a;
        }}
        
        .letter-paper {{
            width: 210mm;
            min-height: 297mm;
            background: #fff;
        }}
        
        /* Header */
        .header {{
            padding: 40px 50px 20px;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        .sender-name {{
            font-size: 22pt;
            font-weight: 400;
            color: #1a1a1a;
            margin: 0 0 8px 0;
            font-family: 'Georgia', serif;
            letter-spacing: 0.5px;
        }}
        
        .sender-contact {{
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            font-size: 10pt;
            color: #555;
            font-family: 'Georgia', serif;
        }}
        
        .sender-address {{
            margin-top: 8px;
            font-size: 10pt;
            color: #666;
        }}
        
        /* Body */
        .letter-body {{
            padding: 30px 50px 50px;
        }}
        
        .date {{
            font-size: 10.5pt;
            color: #333;
            margin-bottom: 24px;
        }}
        
        .recipient {{
            margin-bottom: 24px;
        }}
        
        .recipient-name {{
            font-weight: 600;
            font-size: 11pt;
        }}
        
        .company-name {{
            font-size: 11pt;
            color: #333;
        }}
        
        .company-address {{
            font-size: 10pt;
            color: #666;
            margin-top: 4px;
        }}
        
        .subject {{
            margin-bottom: 24px;
            font-size: 11pt;
        }}
        
        .salutation {{
            margin-bottom: 20px;
            font-size: 11pt;
        }}
        
        .content p {{
            margin: 0 0 16px 0;
            text-align: justify;
        }}
        
        .closing {{
            margin-top: 30px;
        }}
        
        .closing p {{
            margin: 0 0 8px 0;
        }}
        
        .signature {{
            font-weight: 400;
            font-size: 12pt;
            color: #1a1a1a;
            font-family: 'Georgia', serif;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <h1 class="sender-name">{_escape(cover_letter.full_name)}</h1>
            <div class="sender-contact">{''.join(contact_parts)}</div>
            {address_html}
        </header>
        
        <div class="letter-body">
            <div class="date">{today}</div>
            
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            
            <div class="subject">
                <strong>Re: Application for {_escape(cover_letter.position_title)}</strong>
            </div>
            
            <div class="salutation">Dear {manager},</div>
            
            <div class="content">{body_html}</div>
            
            <div class="closing">
                <p>Sincerely,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_modern_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Build Modern cover letter - Sans-serif, clean header with border."""
    
    # Contact
    contact_parts = []
    if cover_letter.email:
        contact_parts.append(f'<span>{_escape(cover_letter.email)}</span>')
    if cover_letter.phone:
        contact_parts.append(f'<span>{_escape(cover_letter.phone)}</span>')
    if cover_letter.linkedin:
        contact_parts.append(f'<span>{_escape(cover_letter.linkedin)}</span>')
    
    address_html = ''
    if cover_letter.address:
        address_html = f'<div class="sender-address">{_escape(cover_letter.address)}</div>'
    
    # Recipient
    recipient_name = f'<div class="recipient-name">{_escape(cover_letter.hiring_manager)}</div>' if cover_letter.hiring_manager else ''
    company_address = ''
    if hasattr(cover_letter, 'company_address') and cover_letter.company_address:
        company_address = f'<div class="company-address">{_escape(cover_letter.company_address)}</div>'
    
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        @page {{ size: A4; margin: 0; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.65;
            color: #1a1a1a;
        }}
        
        .letter-paper {{
            width: 210mm;
            min-height: 297mm;
            background: #fff;
        }}
        
        /* Header */
        .header {{
            padding: 30px 50px 20px;
            border-bottom: 3px solid {primary_color};
        }}
        
        .sender-name {{
            font-size: 24pt;
            font-weight: 600;
            color: {primary_color};
            margin: 0 0 8px 0;
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        
        .sender-contact {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            font-size: 10pt;
            color: #555;
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        
        .sender-address {{
            margin-top: 8px;
            font-size: 10pt;
            color: #666;
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        
        /* Body */
        .letter-body {{
            padding: 30px 50px 50px;
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        
        .date {{
            font-size: 10pt;
            color: #666;
            margin-bottom: 20px;
        }}
        
        .recipient {{
            margin-bottom: 20px;
        }}
        
        .recipient-name {{
            font-weight: 600;
            font-size: 11pt;
        }}
        
        .company-name {{
            font-size: 11pt;
            color: #333;
        }}
        
        .company-address {{
            font-size: 10pt;
            color: #666;
            margin-top: 4px;
        }}
        
        .subject {{
            margin-bottom: 20px;
            font-size: 11pt;
            padding: 10px 0;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        .salutation {{
            margin-bottom: 16px;
            font-size: 11pt;
        }}
        
        .content p {{
            margin: 0 0 14px 0;
            text-align: justify;
            line-height: 1.65;
        }}
        
        .closing {{
            margin-top: 28px;
        }}
        
        .closing p {{
            margin: 0 0 8px 0;
        }}
        
        .signature {{
            font-weight: 600;
            font-size: 12pt;
            color: {primary_color};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <h1 class="sender-name">{_escape(cover_letter.full_name)}</h1>
            <div class="sender-contact">{''.join(contact_parts)}</div>
            {address_html}
        </header>
        
        <div class="letter-body">
            <div class="date">{today}</div>
            
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            
            <div class="subject">
                <strong>Re: Application for {_escape(cover_letter.position_title)}</strong>
            </div>
            
            <div class="salutation">Dear {manager},</div>
            
            <div class="content">{body_html}</div>
            
            <div class="closing">
                <p>Sincerely,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_creative_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Build Creative cover letter - Color header, bold design."""
    
    # Contact
    contact_parts = []
    if cover_letter.email:
        contact_parts.append(f'<span>{_escape(cover_letter.email)}</span>')
    if cover_letter.phone:
        contact_parts.append(f'<span>{_escape(cover_letter.phone)}</span>')
    if cover_letter.linkedin:
        contact_parts.append(f'<span>{_escape(cover_letter.linkedin)}</span>')
    
    # Recipient
    recipient_name = f'<div class="recipient-name">{_escape(cover_letter.hiring_manager)}</div>' if cover_letter.hiring_manager else ''
    company_address = ''
    if hasattr(cover_letter, 'company_address') and cover_letter.company_address:
        company_address = f'<div class="company-address">{_escape(cover_letter.company_address)}</div>'
    
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        @page {{ size: A4; margin: 0; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.65;
            color: #1a1a1a;
        }}
        
        .letter-paper {{
            width: 210mm;
            min-height: 297mm;
            background: #fff;
        }}
        
        /* Header - Colored background */
        .header {{
            background: {primary_color};
            padding: 30px 50px;
            color: #fff;
        }}
        
        .sender-name {{
            font-size: 26pt;
            font-weight: 700;
            color: #fff;
            margin: 0 0 10px 0;
            font-family: 'Segoe UI', Arial, sans-serif;
            letter-spacing: 1px;
        }}
        
        .sender-contact {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            font-size: 10pt;
            color: rgba(255,255,255,0.9);
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        
        /* Body */
        .letter-body {{
            padding: 30px 50px 50px;
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        
        .date {{
            font-size: 10pt;
            color: #666;
            margin-bottom: 20px;
        }}
        
        .recipient {{
            margin-bottom: 20px;
        }}
        
        .recipient-name {{
            font-weight: 600;
            font-size: 11pt;
        }}
        
        .company-name {{
            font-size: 11pt;
            color: #333;
        }}
        
        .company-address {{
            font-size: 10pt;
            color: #666;
            margin-top: 4px;
        }}
        
        .subject {{
            margin-bottom: 20px;
            font-size: 11pt;
            color: {primary_color};
        }}
        
        .salutation {{
            margin-bottom: 16px;
            font-size: 11pt;
        }}
        
        .content p {{
            margin: 0 0 14px 0;
            text-align: justify;
            line-height: 1.65;
        }}
        
        .closing {{
            margin-top: 28px;
        }}
        
        .closing p {{
            margin: 0 0 8px 0;
        }}
        
        .signature {{
            font-weight: 700;
            font-size: 13pt;
            color: {primary_color};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <h1 class="sender-name">{_escape(cover_letter.full_name)}</h1>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        
        <div class="letter-body">
            <div class="date">{today}</div>
            
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            
            <div class="subject">
                <strong>Re: Application for {_escape(cover_letter.position_title)}</strong>
            </div>
            
            <div class="salutation">Dear {manager},</div>
            
            <div class="content">{body_html}</div>
            
            <div class="closing">
                <p>Sincerely,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_cover_letter_body_html(cover_letter) -> str:
    """Build cover letter body paragraphs."""
    paragraphs = []
    
    if cover_letter.opening_paragraph:
        text = cover_letter.opening_paragraph.strip()
        if text and not text.lower().startswith('dear'):
            paragraphs.append(f'<p>{_escape(text)}</p>')
    
    if cover_letter.body_paragraph:
        text = cover_letter.body_paragraph.strip()
        # Handle line breaks properly
        for para in text.split('\n\n'):
            para = para.strip()
            if para and not para.lower().startswith(('dear', 'sincerely')):
                # Replace single newlines with <br> for proper formatting
                formatted = _escape(para).replace('\n', '<br>')
                paragraphs.append(f'<p>{formatted}</p>')
    
    if cover_letter.closing_paragraph:
        text = cover_letter.closing_paragraph.strip()
        if text and not text.lower().startswith('sincerely'):
            paragraphs.append(f'<p>{_escape(text)}</p>')
    
    return '\n'.join(paragraphs)
