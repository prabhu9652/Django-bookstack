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

# Import cover letter template builders
from resume_builder.cover_letter_templates import (
    _build_executive_cover_letter,
    _build_diplomat_cover_letter,
    _build_chancellor_cover_letter,
    _build_statesman_cover_letter,
    _build_cl_regent_cover_letter,
    _build_sovereign_cover_letter,
    _build_ambassador_cover_letter,
    _build_corporate_cover_letter,
    _build_enterprise_cover_letter,
    _build_cl_sterling_cover_letter,
    _build_cl_pinnacle_cover_letter,
    _build_cl_summit_cover_letter,
    _build_cl_keystone_cover_letter,
    _build_cl_anchor_cover_letter,
    _build_cl_streamline_cover_letter,
    _build_cl_metro_cover_letter,
    _build_cl_nordic_cover_letter,
    _build_cl_slate_cover_letter,
    _build_prism_cover_letter,
    _build_nova_cover_letter,
    _build_pulse_cover_letter,
    _build_flux_cover_letter,
    _build_vertex_cover_letter,
    _build_circuit_cover_letter,
    _build_matrix_cover_letter,
    _build_quantum_cover_letter,
    _build_binary_cover_letter,
    _build_stack_cover_letter,
    _build_startup_cover_letter,
    _build_agile_cover_letter,
    _build_sprint_cover_letter,
    _build_artisan_cover_letter,
    _build_cl_canvas_cover_letter,
    _build_palette_cover_letter,
    _build_studio_cover_letter,
    _build_gallery_cover_letter,
    _build_spectrum_cover_letter,
    _build_spark_cover_letter,
    _build_bloom_cover_letter,
    _build_aurora_cover_letter,
    _build_cl_zen_cover_letter,
    _build_cl_pure_cover_letter,
    _build_cl_essence_cover_letter,
    _build_ember_cover_letter,
)

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
    # New templates (7-16)
    elif template_slug == 'compact':
        body_html = _build_compact_template(resume, primary_color)
    elif template_slug == 'elegant':
        body_html = _build_elegant_template(resume, primary_color)
    elif template_slug == 'bold':
        body_html = _build_bold_template(resume, primary_color)
    elif template_slug == 'classic':
        body_html = _build_classic_template(resume, primary_color)
    elif template_slug == 'timeline':
        body_html = _build_timeline_template(resume, primary_color)
    elif template_slug == 'infographic':
        body_html = _build_infographic_template(resume, primary_color)
    elif template_slug == 'corporate':
        body_html = _build_corporate_template(resume, primary_color)
    elif template_slug == 'startup':
        body_html = _build_startup_template(resume, primary_color)
    elif template_slug == 'academic':
        body_html = _build_academic_template(resume, primary_color)
    elif template_slug == 'swiss':
        body_html = _build_swiss_template(resume, primary_color)
    # Premium templates (17-26)
    elif template_slug == 'slate':
        body_html = _build_slate_template(resume, primary_color)
    elif template_slug == 'metro':
        body_html = _build_metro_template(resume, primary_color)
    elif template_slug == 'horizon':
        body_html = _build_horizon_template(resume, primary_color)
    elif template_slug == 'nordic':
        body_html = _build_nordic_template(resume, primary_color)
    elif template_slug == 'apex':
        body_html = _build_apex_template(resume, primary_color)
    elif template_slug == 'clarity':
        body_html = _build_clarity_template(resume, primary_color)
    elif template_slug == 'prestige':
        body_html = _build_prestige_template(resume, primary_color)
    elif template_slug == 'streamline':
        body_html = _build_streamline_template(resume, primary_color)
    elif template_slug == 'foundation':
        body_html = _build_foundation_template(resume, primary_color)
    elif template_slug == 'zenith':
        body_html = _build_zenith_template(resume, primary_color)
    # Premium templates batch 2 (27-51) - Executive
    elif template_slug == 'monarch':
        body_html = _build_monarch_template(resume, primary_color)
    elif template_slug == 'summit':
        body_html = _build_summit_template(resume, primary_color)
    elif template_slug == 'regent':
        body_html = _build_regent_template(resume, primary_color)
    elif template_slug == 'pinnacle':
        body_html = _build_pinnacle_template(resume, primary_color)
    elif template_slug == 'dynasty':
        body_html = _build_dynasty_template(resume, primary_color)
    # Technical templates
    elif template_slug == 'circuit':
        body_html = _build_circuit_template(resume, primary_color)
    elif template_slug == 'matrix':
        body_html = _build_matrix_template(resume, primary_color)
    elif template_slug == 'quantum':
        body_html = _build_quantum_template(resume, primary_color)
    elif template_slug == 'binary':
        body_html = _build_binary_template(resume, primary_color)
    elif template_slug == 'stack':
        body_html = _build_stack_template(resume, primary_color)
    # Modern templates
    elif template_slug == 'prism':
        body_html = _build_prism_template(resume, primary_color)
    elif template_slug == 'nova':
        body_html = _build_nova_template(resume, primary_color)
    elif template_slug == 'pulse':
        body_html = _build_pulse_template(resume, primary_color)
    elif template_slug == 'flux':
        body_html = _build_flux_template(resume, primary_color)
    elif template_slug == 'vertex':
        body_html = _build_vertex_template(resume, primary_color)
    # Minimal templates
    elif template_slug == 'zen':
        body_html = _build_zen_template(resume, primary_color)
    elif template_slug == 'pure':
        body_html = _build_pure_template(resume, primary_color)
    elif template_slug == 'essence':
        body_html = _build_essence_template(resume, primary_color)
    elif template_slug == 'canvas':
        body_html = _build_canvas_template(resume, primary_color)
    elif template_slug == 'whisper':
        body_html = _build_whisper_template(resume, primary_color)
    # Professional templates
    elif template_slug == 'sterling':
        body_html = _build_sterling_template(resume, primary_color)
    elif template_slug == 'anchor':
        body_html = _build_anchor_template(resume, primary_color)
    elif template_slug == 'merit':
        body_html = _build_merit_template(resume, primary_color)
    elif template_slug == 'beacon':
        body_html = _build_beacon_template(resume, primary_color)
    elif template_slug == 'keystone':
        body_html = _build_keystone_template(resume, primary_color)
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
    
    # Photo (optional - only shown if uploaded)
    photo_html = _get_photo_html(resume)
    photo_section = ''
    if photo_html:
        photo_section = f'<div class="header-photo">{photo_html}</div>'
    
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
        {photo_section}
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{''.join(contact_parts)}</div>
        </div>
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
    display: flex;
    align-items: center;
    gap: 24px;
}}

.header-photo {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
}}

.header-photo img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

.header-info {{
    flex: 1;
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
    
    # Photo (optional - only shown if uploaded)
    photo_html = _get_photo_html(resume)
    photo_section = ''
    if photo_html:
        photo_section = f'<div class="header-photo">{photo_html}</div>'
    
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
        {photo_section}
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name).upper()}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{''.join(contact_items)}</div>
        </div>
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
    display: flex;
    align-items: center;
    gap: 24px;
}}

.header-photo {{
    width: 100px;
    height: 100px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
}}

.header-photo img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

.header-info {{
    flex: 1;
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
    
    # Photo - use placeholder version for Professional template
    photo_html = _get_photo_html_with_placeholder(resume)
    
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
    
    # Profile
    profile_html = ''
    if resume.summary:
        profile_html = f'''
        <section class="section">
            <h2 class="section-heading"><span class="badge">PROFILE</span></h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    # Education in main content (above Employment)
    education_html = _build_education_html(resume.education, 'professional')
    
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
        </aside>
        
        <main class="main-content">
            {profile_html}
            {education_html}
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
    # Photo (optional - only shown if uploaded)
    photo_html = _get_photo_html(resume)
    photo_section = ''
    if photo_html:
        photo_section = f'<div class="header-photo">{photo_html}</div>'
    
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
        {photo_section}
        <h1 class="name">{_escape(resume.full_name)}</h1>
        <p class="role">{_escape(resume.role_title or '')}</p>
        <p class="contact">{contact_html}</p>
    </header>
    
    <main class="content">
        {summary_html}
        {education_html}
        {experience_html}
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

.header-photo {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    overflow: hidden;
    margin: 0 auto 16px auto;
    border: 2px solid {primary_color};
}}

.header-photo img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
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
    # Photo (optional - only shown if uploaded)
    photo_html = _get_photo_html(resume)
    photo_section = ''
    if photo_html:
        photo_section = f'<div class="header-photo">{photo_html}</div>'
    
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
        {photo_section}
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
            {education_html}
            {experience_html}
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
    display: flex;
    align-items: flex-start;
    gap: 0;
}}

.header-photo {{
    width: 100px;
    height: 100px;
    border-radius: 50%;
    overflow: hidden;
    margin: 20px 0 0 20px;
    flex-shrink: 0;
    border: 3px solid {primary_color};
}}

.header-photo img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

.name-block {{
    background: {primary_color};
    color: #fff;
    padding: 35px 40px;
    margin: 20px 20px 0 20px;
    flex: 1;
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
    # Photo (optional - only shown if uploaded)
    photo_html = _get_photo_html(resume)
    photo_section = ''
    if photo_html:
        photo_section = f'<div class="header-photo">{photo_html}</div>'
    
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
        {photo_section}
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
            {education_html}
            {experience_html}
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
    gap: 20px;
}}

.header-photo {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    overflow: hidden;
    border: 2px solid {primary_color};
    flex-shrink: 0;
}}

.header-photo img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
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
    # New templates (7-16)
    elif template_slug == 'compact':
        return _get_compact_styles(primary_color)
    elif template_slug == 'elegant':
        return _get_elegant_styles(primary_color)
    elif template_slug == 'bold':
        return _get_bold_styles(primary_color)
    elif template_slug == 'classic':
        return _get_classic_styles(primary_color)
    elif template_slug == 'timeline':
        return _get_timeline_styles(primary_color)
    elif template_slug == 'infographic':
        return _get_infographic_styles(primary_color)
    elif template_slug == 'corporate':
        return _get_corporate_styles(primary_color)
    elif template_slug == 'startup':
        return _get_startup_styles(primary_color)
    elif template_slug == 'academic':
        return _get_academic_styles(primary_color)
    elif template_slug == 'swiss':
        return _get_swiss_styles(primary_color)
    # Premium templates (17-26)
    elif template_slug == 'slate':
        return _get_slate_styles(primary_color)
    elif template_slug == 'metro':
        return _get_metro_styles(primary_color)
    elif template_slug == 'horizon':
        return _get_horizon_styles(primary_color)
    elif template_slug == 'nordic':
        return _get_nordic_styles(primary_color)
    elif template_slug == 'apex':
        return _get_apex_styles(primary_color)
    elif template_slug == 'clarity':
        return _get_clarity_styles(primary_color)
    elif template_slug == 'prestige':
        return _get_prestige_styles(primary_color)
    elif template_slug == 'streamline':
        return _get_streamline_styles(primary_color)
    elif template_slug == 'foundation':
        return _get_foundation_styles(primary_color)
    elif template_slug == 'zenith':
        return _get_zenith_styles(primary_color)
    # Premium templates batch 2 (27-51) - Executive
    elif template_slug == 'monarch':
        return _get_monarch_styles(primary_color)
    elif template_slug == 'summit':
        return _get_summit_styles(primary_color)
    elif template_slug == 'regent':
        return _get_regent_styles(primary_color)
    elif template_slug == 'pinnacle':
        return _get_pinnacle_styles(primary_color)
    elif template_slug == 'dynasty':
        return _get_dynasty_styles(primary_color)
    # Technical templates
    elif template_slug == 'circuit':
        return _get_circuit_styles(primary_color)
    elif template_slug == 'matrix':
        return _get_matrix_styles(primary_color)
    elif template_slug == 'quantum':
        return _get_quantum_styles(primary_color)
    elif template_slug == 'binary':
        return _get_binary_styles(primary_color)
    elif template_slug == 'stack':
        return _get_stack_styles(primary_color)
    # Modern templates
    elif template_slug == 'prism':
        return _get_prism_styles(primary_color)
    elif template_slug == 'nova':
        return _get_nova_styles(primary_color)
    elif template_slug == 'pulse':
        return _get_pulse_styles(primary_color)
    elif template_slug == 'flux':
        return _get_flux_styles(primary_color)
    elif template_slug == 'vertex':
        return _get_vertex_styles(primary_color)
    # Minimal templates
    elif template_slug == 'zen':
        return _get_zen_styles(primary_color)
    elif template_slug == 'pure':
        return _get_pure_styles(primary_color)
    elif template_slug == 'essence':
        return _get_essence_styles(primary_color)
    elif template_slug == 'canvas':
        return _get_canvas_styles(primary_color)
    elif template_slug == 'whisper':
        return _get_whisper_styles(primary_color)
    # Professional templates
    elif template_slug == 'sterling':
        return _get_sterling_styles(primary_color)
    elif template_slug == 'anchor':
        return _get_anchor_styles(primary_color)
    elif template_slug == 'merit':
        return _get_merit_styles(primary_color)
    elif template_slug == 'beacon':
        return _get_beacon_styles(primary_color)
    elif template_slug == 'keystone':
        return _get_keystone_styles(primary_color)
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
    """Get photo HTML with base64 encoding. Works for all templates."""
    # First check for base64 photo (from live preview)
    if hasattr(resume, 'profile_photo_base64') and resume.profile_photo_base64:
        # Base64 data already includes the data URI prefix
        return f'<img src="{resume.profile_photo_base64}" alt="{_escape(resume.full_name)}">'
    
    # Then check for file-based photo
    photo_data = _get_photo_base64(resume)
    if photo_data:
        return f'<img src="data:image/jpeg;base64,{photo_data}" alt="{_escape(resume.full_name)}">'
    
    # No photo - return empty string (no placeholder)
    return ''


def _get_photo_html_with_placeholder(resume) -> str:
    """Get photo HTML with placeholder fallback (for Professional template)."""
    # First check for base64 photo (from live preview)
    if hasattr(resume, 'profile_photo_base64') and resume.profile_photo_base64:
        return f'<img src="{resume.profile_photo_base64}" alt="{_escape(resume.full_name)}">'
    
    # Then check for file-based photo
    photo_data = _get_photo_base64(resume)
    if photo_data:
        return f'<img src="data:image/jpeg;base64,{photo_data}" alt="{_escape(resume.full_name)}">'
    
    # Return placeholder for Professional template
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
    
    if template in ('executive', 'professional'):
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
    # FORMAL TEMPLATES (7)
    elif template_slug == 'executive':
        return _build_executive_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'diplomat':
        return _build_diplomat_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'chancellor':
        return _build_chancellor_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'statesman':
        return _build_statesman_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'cl_regent':
        return _build_cl_regent_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'sovereign':
        return _build_sovereign_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'ambassador':
        return _build_ambassador_cover_letter(cover_letter, primary_color, today)
    # PROFESSIONAL TEMPLATES (7)
    elif template_slug == 'corporate':
        return _build_corporate_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'enterprise':
        return _build_enterprise_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'cl_sterling':
        return _build_cl_sterling_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'cl_pinnacle':
        return _build_cl_pinnacle_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'cl_summit':
        return _build_cl_summit_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'cl_keystone':
        return _build_cl_keystone_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'cl_anchor':
        return _build_cl_anchor_cover_letter(cover_letter, primary_color, today)
    # MODERN TEMPLATES (10)
    elif template_slug == 'cl_streamline':
        return _build_cl_streamline_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'cl_metro':
        return _build_cl_metro_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'cl_nordic':
        return _build_cl_nordic_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'cl_slate':
        return _build_cl_slate_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'prism':
        return _build_prism_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'nova':
        return _build_nova_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'pulse':
        return _build_pulse_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'flux':
        return _build_flux_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'vertex':
        return _build_vertex_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'circuit':
        return _build_circuit_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'matrix':
        return _build_matrix_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'quantum':
        return _build_quantum_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'binary':
        return _build_binary_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'stack':
        return _build_stack_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'startup':
        return _build_startup_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'agile':
        return _build_agile_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'sprint':
        return _build_sprint_cover_letter(cover_letter, primary_color, today)
    # CREATIVE TEMPLATES (10)
    elif template_slug == 'artisan':
        return _build_artisan_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'cl_canvas':
        return _build_cl_canvas_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'palette':
        return _build_palette_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'studio':
        return _build_studio_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'gallery':
        return _build_gallery_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'spectrum':
        return _build_spectrum_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'spark':
        return _build_spark_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'bloom':
        return _build_bloom_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'aurora':
        return _build_aurora_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'cl_zen':
        return _build_cl_zen_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'cl_pure':
        return _build_cl_pure_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'cl_essence':
        return _build_cl_essence_cover_letter(cover_letter, primary_color, today)
    elif template_slug == 'ember':
        return _build_ember_cover_letter(cover_letter, primary_color, today)
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
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
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
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
        }}
        
        .sender-contact {{
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            font-size: 10pt;
            color: #555;
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
        }}
        
        .sender-address {{
            margin-top: 8px;
            font-size: 10pt;
            color: #666;
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
        }}
        
        /* Body */
        .letter-body {{
            padding: 30px 50px 50px;
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
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
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
        }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
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


# =============================================================================
# NEW TEMPLATES (7-16) - 10 Additional High-Quality Resume Templates
# =============================================================================


# =============================================================================
# TEMPLATE 7: COMPACT - Dense, information-rich single column
# =============================================================================

def _build_compact_template(resume, primary_color: str) -> str:
    """Compact template - Dense, information-rich layout for experienced professionals."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_parts = []
    if resume.email:
        contact_parts.append(f'<span>{_escape(resume.email)}</span>')
    if resume.phone:
        contact_parts.append(f'<span>{_escape(resume.phone)}</span>')
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_parts.append(f'<span>{_escape(loc)}</span>')
    if resume.linkedin:
        contact_parts.append(f'<span>{_escape(resume.linkedin)}</span>')
    if resume.github:
        contact_parts.append(f'<span>{_escape(resume.github)}</span>')
    
    summary_html = ''
    if resume.summary:
        summary_html = f'<section class="section"><p class="summary">{_escape(resume.summary)}</p></section>'
    
    skills_html = ''
    if resume.skills:
        skills_inline = ' • '.join([_escape(s) for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Technical Skills</h2>
            <p class="skills-inline">{skills_inline}</p>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'compact')
    employment_html = _build_employment_html(resume.experience, 'compact')
    
    return f'''
    <header class="header">
        {photo_section}
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{'  |  '.join(contact_parts)}</div>
        </div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_compact_styles(primary_color: str) -> str:
    return f'''
.header {{
    padding: 20px 30px;
    border-bottom: 2px solid {primary_color};
    display: flex;
    align-items: center;
    gap: 20px;
}}
.header-photo {{
    width: 60px;
    height: 60px;
    border-radius: 50%;
    overflow: hidden;
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-info {{ flex: 1; }}
.header .name {{
    font-size: 22pt;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 2px;
}}
.header .role {{
    font-size: 11pt;
    color: {primary_color};
    margin-bottom: 6px;
}}
.header .contact {{
    font-size: 8.5pt;
    color: #555;
}}
.content {{ padding: 20px 30px; }}
.section {{ margin-bottom: 16px; }}
.section-title {{
    font-size: 10pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid #e5e7eb;
}}
.summary {{
    font-size: 9.5pt;
    color: #333;
    line-height: 1.5;
}}
.skills-inline {{
    font-size: 9pt;
    color: #444;
    line-height: 1.6;
}}
.entry {{ margin-bottom: 12px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}}
.entry-title {{ font-weight: 600; font-size: 10pt; color: #1a1a1a; }}
.entry-date {{ font-size: 8.5pt; color: #666; }}
.entry-subtitle {{ font-size: 9pt; color: {primary_color}; margin-bottom: 4px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 14px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9pt;
    color: #444;
    margin-bottom: 3px;
    line-height: 1.4;
}}
'''


# =============================================================================
# TEMPLATE 8: ELEGANT - Refined serif typography, classic feel
# =============================================================================

def _build_elegant_template(resume, primary_color: str) -> str:
    """Elegant template - Refined serif typography with classic feel."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_parts = []
    if resume.email:
        contact_parts.append(_escape(resume.email))
    if resume.phone:
        contact_parts.append(_escape(resume.phone))
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_parts.append(_escape(loc))
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Profile</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Expertise</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    languages_html = ''
    if resume.languages:
        items = ''.join([f'<li>{_escape(l)}</li>' for l in resume.languages])
        languages_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Languages</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'elegant')
    employment_html = _build_employment_html(resume.experience, 'elegant')
    
    return f'''
    <header class="header">
        {photo_section}
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{' · '.join(contact_parts)}</div>
        </div>
    </header>
    <div class="body-container">
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
        <aside class="sidebar">
            {skills_html}
            {languages_html}
        </aside>
    </div>'''


def _get_elegant_styles(primary_color: str) -> str:
    return f'''
.header {{
    text-align: center;
    padding: 35px 40px 25px;
    border-bottom: 1px solid #d4af37;
}}
.header-photo {{
    width: 85px;
    height: 85px;
    border-radius: 50%;
    overflow: hidden;
    margin: 0 auto 12px;
    border: 2px solid #d4af37;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 28pt;
    font-weight: 400;
    color: #1a1a1a;
    letter-spacing: 2px;
    margin-bottom: 6px;
}}
.header .role {{
    font-family: 'Georgia', serif;
    font-size: 12pt;
    font-style: italic;
    color: {primary_color};
    margin-bottom: 10px;
}}
.header .contact {{
    font-size: 9pt;
    color: #666;
}}
.body-container {{
    display: flex;
    min-height: calc(297mm - 140px);
}}
.main-content {{
    flex: 1;
    padding: 25px 30px;
    border-right: 1px solid #e5e7eb;
}}
.sidebar {{
    width: 170px;
    padding: 25px 20px;
    background: #fafafa;
}}
.section {{ margin-bottom: 22px; }}
.section-title {{
    font-family: 'Georgia', serif;
    font-size: 12pt;
    font-weight: 400;
    color: #1a1a1a;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 1px solid #d4af37;
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.6;
    text-align: justify;
}}
.sidebar-section {{ margin-bottom: 20px; }}
.sidebar-title {{
    font-family: 'Georgia', serif;
    font-size: 10pt;
    color: #1a1a1a;
    margin-bottom: 10px;
    padding-bottom: 4px;
    border-bottom: 1px solid #d4af37;
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    font-size: 9pt;
    color: #444;
    padding: 4px 0;
}}
.entry {{ margin-bottom: 16px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}}
.entry-title {{
    font-family: 'Georgia', serif;
    font-weight: 600;
    font-size: 10.5pt;
    color: #1a1a1a;
}}
.entry-date {{ font-size: 9pt; color: #888; }}
.entry-subtitle {{ font-size: 9.5pt; color: {primary_color}; margin-bottom: 6px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 16px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 4px;
    line-height: 1.5;
}}
'''


# =============================================================================
# TEMPLATE 9: BOLD - Strong visual hierarchy, impactful headers
# =============================================================================

def _build_bold_template(resume, primary_color: str) -> str:
    """Bold template - Strong visual hierarchy with impactful headers."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">ABOUT</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<span class="skill-tag">{_escape(s)}</span>' for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">SKILLS</h2>
            <div class="skills-tags">{items}</div>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'bold')
    employment_html = _build_employment_html(resume.experience, 'bold')
    
    return f'''
    <header class="header">
        {photo_section}
        <div class="header-main">
            <h1 class="name">{_escape(resume.full_name).upper()}</h1>
            <p class="role">{_escape(resume.role_title or '').upper()}</p>
        </div>
        <div class="header-contact">{''.join(contact_items)}</div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_bold_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: #1a1a1a;
    color: #fff;
    padding: 30px 35px;
    display: flex;
    align-items: center;
    gap: 25px;
}}
.header-photo {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid {primary_color};
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-main {{ flex: 1; }}
.header .name {{
    font-size: 30pt;
    font-weight: 800;
    letter-spacing: 3px;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 11pt;
    font-weight: 600;
    color: {primary_color};
    letter-spacing: 2px;
}}
.header-contact {{
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 9pt;
    color: rgba(255,255,255,0.8);
}}
.content {{ padding: 25px 35px; }}
.section {{ margin-bottom: 22px; }}
.section-title {{
    font-size: 12pt;
    font-weight: 800;
    color: #1a1a1a;
    letter-spacing: 2px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 3px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.6;
}}
.skills-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}}
.skill-tag {{
    background: {primary_color};
    color: #fff;
    padding: 4px 12px;
    border-radius: 3px;
    font-size: 9pt;
    font-weight: 600;
}}
.entry {{ margin-bottom: 16px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; font-weight: 600; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; font-weight: 600; margin-bottom: 6px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 16px;
    list-style-type: square;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 4px;
    line-height: 1.5;
}}
'''


# =============================================================================
# TEMPLATE 10: CLASSIC - Traditional, timeless design
# =============================================================================

def _build_classic_template(resume, primary_color: str) -> str:
    """Classic template - Traditional, timeless resume design."""
    contact_parts = []
    if resume.address:
        contact_parts.append(_escape(resume.address))
    if resume.phone:
        contact_parts.append(_escape(resume.phone))
    if resume.email:
        contact_parts.append(_escape(resume.email))
    if resume.linkedin:
        contact_parts.append(_escape(resume.linkedin))
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Professional Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        skills_text = ', '.join([_escape(s) for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Core Competencies</h2>
            <p class="skills-text">{skills_text}</p>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'classic')
    employment_html = _build_employment_html(resume.experience, 'classic')
    
    return f'''
    <header class="header">
        <h1 class="name">{_escape(resume.full_name)}</h1>
        <p class="role">{_escape(resume.role_title or '')}</p>
        <div class="contact">{' | '.join(contact_parts)}</div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_classic_styles(primary_color: str) -> str:
    return f'''
.header {{
    text-align: center;
    padding: 35px 40px 25px;
    border-bottom: 2px solid #1a1a1a;
}}
.header .name {{
    font-size: 26pt;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 12pt;
    color: #444;
    margin-bottom: 10px;
}}
.header .contact {{
    font-size: 9.5pt;
    color: #555;
}}
.content {{ padding: 25px 40px; }}
.section {{ margin-bottom: 22px; }}
.section-title {{
    font-size: 12pt;
    font-weight: 700;
    color: #1a1a1a;
    text-transform: uppercase;
    margin-bottom: 10px;
    padding-bottom: 4px;
    border-bottom: 1px solid #ccc;
}}
.section-text {{
    font-size: 10pt;
    color: #333;
    line-height: 1.6;
    text-align: justify;
}}
.skills-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.6;
}}
.entry {{ margin-bottom: 16px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9.5pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: #444; font-style: italic; margin-bottom: 6px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 10pt;
    color: #333;
    margin-bottom: 4px;
    line-height: 1.5;
}}
'''


# =============================================================================
# TEMPLATE 11: TIMELINE - Visual timeline for experience
# =============================================================================

def _build_timeline_template(resume, primary_color: str) -> str:
    """Timeline template - Visual timeline layout for experience."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_parts = []
    if resume.email:
        contact_parts.append(f'<span>✉ {_escape(resume.email)}</span>')
    if resume.phone:
        contact_parts.append(f'<span>✆ {_escape(resume.phone)}</span>')
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_parts.append(f'<span>⌂ {_escape(loc)}</span>')
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Profile</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Skills</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    # Build timeline experience
    exp_entries = ''
    for exp in (resume.experience or []):
        role = _escape(exp.get('role', ''))
        company = _escape(exp.get('company', ''))
        start = _escape(exp.get('start_date', ''))
        end = _escape(exp.get('end_date', ''))
        bullets_html = ''
        if exp.get('bullets'):
            items = ''.join([f'<li>{_format_bullet(b)}</li>' for b in exp['bullets']])
            bullets_html = f'<ul class="entry-bullets">{items}</ul>'
        exp_entries += f'''
        <div class="timeline-entry">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
                <div class="entry-header">
                    <span class="entry-title">{role}</span>
                    <span class="entry-date">{start} - {end}</span>
                </div>
                <div class="entry-subtitle">{company}</div>
                {bullets_html}
            </div>
        </div>'''
    
    experience_html = f'''<section class="section">
        <h2 class="section-title">Experience</h2>
        <div class="timeline">{exp_entries}</div>
    </section>''' if exp_entries else ''
    
    education_html = _build_education_html(resume.education, 'timeline')
    
    return f'''
    <header class="header">
        {photo_section}
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{' '.join(contact_parts)}</div>
        </div>
    </header>
    <div class="body-container">
        <main class="main-content">
            {summary_html}
            {education_html}
            {experience_html}
        </main>
        <aside class="sidebar">
            {skills_html}
        </aside>
    </div>'''


def _get_timeline_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: linear-gradient(135deg, {primary_color} 0%, #1a1a1a 100%);
    color: #fff;
    padding: 28px 35px;
    display: flex;
    align-items: center;
    gap: 20px;
}}
.header-photo {{
    width: 85px;
    height: 85px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-info {{ flex: 1; }}
.header .name {{
    font-size: 26pt;
    font-weight: 600;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 12pt;
    color: rgba(255,255,255,0.9);
    margin-bottom: 10px;
}}
.header .contact {{
    display: flex;
    gap: 15px;
    font-size: 9pt;
    color: rgba(255,255,255,0.8);
}}
.body-container {{
    display: flex;
    min-height: calc(297mm - 120px);
}}
.main-content {{
    flex: 1;
    padding: 25px 30px;
}}
.sidebar {{
    width: 170px;
    background: #f8f9fa;
    padding: 25px 18px;
}}
.section {{ margin-bottom: 22px; }}
.section-title {{
    font-size: 12pt;
    font-weight: 600;
    color: {primary_color};
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.6;
}}
.sidebar-section {{ margin-bottom: 20px; }}
.sidebar-title {{
    font-size: 10pt;
    font-weight: 600;
    color: {primary_color};
    margin-bottom: 10px;
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    font-size: 9pt;
    color: #444;
    padding: 5px 0;
    border-bottom: 1px solid #e5e7eb;
}}
.timeline {{
    position: relative;
    padding-left: 20px;
    border-left: 2px solid {primary_color};
}}
.timeline-entry {{
    position: relative;
    margin-bottom: 18px;
}}
.timeline-marker {{
    position: absolute;
    left: -26px;
    top: 4px;
    width: 10px;
    height: 10px;
    background: {primary_color};
    border-radius: 50%;
}}
.timeline-content {{ padding-left: 10px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}}
.entry-title {{ font-weight: 600; font-size: 10.5pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 9.5pt; color: {primary_color}; margin-bottom: 6px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 16px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 4px;
    line-height: 1.5;
}}
.entry {{ margin-bottom: 14px; }}
'''


# =============================================================================
# TEMPLATE 12: INFOGRAPHIC - Data visualization style
# =============================================================================

def _build_infographic_template(resume, primary_color: str) -> str:
    """Infographic template - Data visualization style with skill bars."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_items = []
    if resume.email:
        contact_items.append(f'<div class="contact-item"><span class="icon">✉</span>{_escape(resume.email)}</div>')
    if resume.phone:
        contact_items.append(f'<div class="contact-item"><span class="icon">✆</span>{_escape(resume.phone)}</div>')
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_items.append(f'<div class="contact-item"><span class="icon">⌂</span>{_escape(loc)}</div>')
    if resume.linkedin:
        contact_items.append(f'<div class="contact-item"><span class="icon">in</span>{_escape(resume.linkedin)}</div>')
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">About Me</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    # Skills with visual bars
    skills_html = ''
    if resume.skills:
        items = ''
        for i, skill in enumerate(resume.skills[:10]):
            width = 95 - (i * 5) if i < 6 else 70
            items += f'''<div class="skill-bar-item">
                <span class="skill-name">{_escape(skill)}</span>
                <div class="skill-bar"><div class="skill-fill" style="width: {width}%"></div></div>
            </div>'''
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Skills</h3>
            {items}
        </div>'''
    
    languages_html = ''
    if resume.languages:
        items = ''.join([f'<span class="lang-tag">{_escape(l)}</span>' for l in resume.languages])
        languages_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Languages</h3>
            <div class="lang-tags">{items}</div>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'infographic')
    employment_html = _build_employment_html(resume.experience, 'infographic')
    
    return f'''
    <div class="body-container">
        <aside class="sidebar">
            {photo_section}
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{''.join(contact_items)}</div>
            {skills_html}
            {languages_html}
        </aside>
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
    </div>'''


def _get_infographic_styles(primary_color: str) -> str:
    return f'''
.body-container {{
    display: flex;
    min-height: 297mm;
}}
.sidebar {{
    width: 200px;
    background: {primary_color};
    color: #fff;
    padding: 30px 20px;
}}
.header-photo {{
    width: 100px;
    height: 100px;
    border-radius: 50%;
    overflow: hidden;
    margin: 0 auto 15px;
    border: 3px solid rgba(255,255,255,0.3);
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.name {{
    font-size: 18pt;
    font-weight: 700;
    text-align: center;
    margin-bottom: 4px;
}}
.role {{
    font-size: 10pt;
    text-align: center;
    color: rgba(255,255,255,0.9);
    margin-bottom: 20px;
}}
.contact {{
    margin-bottom: 25px;
}}
.contact-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 8.5pt;
    margin-bottom: 8px;
    color: rgba(255,255,255,0.9);
}}
.contact-item .icon {{
    width: 16px;
    text-align: center;
}}
.sidebar-section {{ margin-bottom: 22px; }}
.sidebar-title {{
    font-size: 10pt;
    font-weight: 600;
    margin-bottom: 12px;
    padding-bottom: 4px;
    border-bottom: 1px solid rgba(255,255,255,0.3);
}}
.skill-bar-item {{ margin-bottom: 10px; }}
.skill-name {{
    font-size: 8.5pt;
    display: block;
    margin-bottom: 3px;
}}
.skill-bar {{
    height: 6px;
    background: rgba(255,255,255,0.2);
    border-radius: 3px;
}}
.skill-fill {{
    height: 100%;
    background: #fff;
    border-radius: 3px;
}}
.lang-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}}
.lang-tag {{
    background: rgba(255,255,255,0.2);
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 8pt;
}}
.main-content {{
    flex: 1;
    padding: 30px 35px;
}}
.section {{ margin-bottom: 24px; }}
.section-title {{
    font-size: 13pt;
    font-weight: 600;
    color: {primary_color};
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.6;
}}
.entry {{ margin-bottom: 16px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}}
.entry-title {{ font-weight: 600; font-size: 10.5pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 9.5pt; color: {primary_color}; margin-bottom: 6px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 16px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 4px;
    line-height: 1.5;
}}
'''


# =============================================================================
# TEMPLATE 13: CORPORATE - Professional enterprise style
# =============================================================================

def _build_corporate_template(resume, primary_color: str) -> str:
    """Corporate template - Professional enterprise style."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Executive Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        mid = len(resume.skills) // 2
        col1 = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills[:mid]])
        col2 = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills[mid:]])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Core Competencies</h2>
            <div class="skills-columns">
                <ul class="skills-col">{col1}</ul>
                <ul class="skills-col">{col2}</ul>
            </div>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'corporate')
    employment_html = _build_employment_html(resume.experience, 'corporate')
    
    return f'''
    <header class="header">
        {photo_section}
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
        </div>
        <div class="header-contact">{' | '.join(contact_parts)}</div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_corporate_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: #fff;
    padding: 30px 40px;
    border-bottom: 4px solid {primary_color};
    display: flex;
    align-items: center;
    gap: 25px;
}}
.header-photo {{
    width: 90px;
    height: 90px;
    border-radius: 8px;
    overflow: hidden;
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-info {{ flex: 1; }}
.header .name {{
    font-size: 26pt;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 12pt;
    color: {primary_color};
    font-weight: 500;
}}
.header-contact {{
    font-size: 9pt;
    color: #555;
    text-align: right;
}}
.content {{ padding: 25px 40px; }}
.section {{ margin-bottom: 24px; }}
.section-title {{
    font-size: 11pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 1px solid #e5e7eb;
}}
.section-text {{
    font-size: 10pt;
    color: #333;
    line-height: 1.6;
    text-align: justify;
}}
.skills-columns {{
    display: flex;
    gap: 40px;
}}
.skills-col {{
    flex: 1;
    list-style: none;
}}
.skills-col li {{
    font-size: 9.5pt;
    color: #444;
    padding: 4px 0;
    padding-left: 15px;
    position: relative;
}}
.skills-col li::before {{
    content: '▸';
    position: absolute;
    left: 0;
    color: {primary_color};
}}
.entry {{ margin-bottom: 18px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 6px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #333;
    margin-bottom: 4px;
    line-height: 1.5;
}}
'''


# =============================================================================
# TEMPLATE 14: STARTUP - Modern, dynamic tech startup style
# =============================================================================

def _build_startup_template(resume, primary_color: str) -> str:
    """Startup template - Modern, dynamic tech startup style."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_parts = []
    if resume.email:
        contact_parts.append(f'<a class="contact-link">{_escape(resume.email)}</a>')
    if resume.github:
        contact_parts.append(f'<a class="contact-link">{_escape(resume.github)}</a>')
    if resume.linkedin:
        contact_parts.append(f'<a class="contact-link">{_escape(resume.linkedin)}</a>')
    if resume.phone:
        contact_parts.append(f'<span>{_escape(resume.phone)}</span>')
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section hero-section">
            <p class="hero-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<span class="skill-chip">{_escape(s)}</span>' for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Tech Stack</h2>
            <div class="skills-chips">{items}</div>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'startup')
    employment_html = _build_employment_html(resume.experience, 'startup')
    
    return f'''
    <header class="header">
        <div class="header-left">
            {photo_section}
            <div class="header-info">
                <h1 class="name">{_escape(resume.full_name)}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
            </div>
        </div>
        <div class="header-contact">{' '.join(contact_parts)}</div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_startup_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
    padding: 25px 35px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.header-left {{
    display: flex;
    align-items: center;
    gap: 20px;
}}
.header-photo {{
    width: 75px;
    height: 75px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.3);
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 24pt;
    font-weight: 700;
    margin-bottom: 2px;
}}
.header .role {{
    font-size: 11pt;
    color: rgba(255,255,255,0.9);
}}
.header-contact {{
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 4px;
}}
.contact-link {{
    font-size: 9pt;
    color: rgba(255,255,255,0.9);
    text-decoration: none;
}}
.content {{ padding: 25px 35px; }}
.hero-section {{
    background: #f8f9fa;
    padding: 20px;
    border-radius: 12px;
    border-left: 4px solid {primary_color};
}}
.hero-text {{
    font-size: 10.5pt;
    color: #333;
    line-height: 1.6;
    font-style: italic;
}}
.section {{ margin-bottom: 24px; }}
.section-title {{
    font-size: 12pt;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}}
.section-title::after {{
    content: '';
    flex: 1;
    height: 2px;
    background: linear-gradient(90deg, {primary_color} 0%, transparent 100%);
}}
.skills-chips {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}}
.skill-chip {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 9pt;
    font-weight: 500;
}}
.entry {{ margin-bottom: 18px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{
    font-size: 9pt;
    color: #fff;
    background: {primary_color};
    padding: 2px 10px;
    border-radius: 10px;
}}
.entry-subtitle {{ font-size: 10pt; color: #667eea; margin-bottom: 6px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: none;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 4px;
    line-height: 1.5;
    position: relative;
    padding-left: 15px;
}}
.entry-bullets li::before {{
    content: '→';
    position: absolute;
    left: 0;
    color: #667eea;
}}
'''


# =============================================================================
# TEMPLATE 15: ACADEMIC - Research/academic focused
# =============================================================================

def _build_academic_template(resume, primary_color: str) -> str:
    """Academic template - Research and academic focused."""
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Research Interests</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ', '.join([_escape(s) for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Technical Proficiencies</h2>
            <p class="skills-text">{items}</p>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'academic')
    employment_html = _build_employment_html(resume.experience, 'academic')
    
    return f'''
    <header class="header">
        <h1 class="name">{_escape(resume.full_name)}</h1>
        <p class="role">{_escape(resume.role_title or '')}</p>
        <div class="contact">{' • '.join(contact_parts)}</div>
    </header>
    <main class="content">
        {summary_html}
        {education_html}
        {employment_html}
        {skills_html}
    </main>'''


def _get_academic_styles(primary_color: str) -> str:
    return f'''
.header {{
    text-align: center;
    padding: 35px 50px 25px;
    border-bottom: 1px solid #1a1a1a;
}}
.header .name {{
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 24pt;
    font-weight: 400;
    color: #1a1a1a;
    margin-bottom: 4px;
}}
.header .role {{
    font-family: 'Georgia', serif;
    font-size: 12pt;
    color: #444;
    font-style: italic;
    margin-bottom: 12px;
}}
.header .contact {{
    font-size: 9.5pt;
    color: #555;
}}
.content {{ padding: 25px 50px; }}
.section {{ margin-bottom: 24px; }}
.section-title {{
    font-family: 'Georgia', serif;
    font-size: 12pt;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 10px;
    padding-bottom: 4px;
    border-bottom: 1px solid #ccc;
}}
.section-text {{
    font-size: 10pt;
    color: #333;
    line-height: 1.7;
    text-align: justify;
}}
.skills-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.6;
}}
.entry {{ margin-bottom: 16px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}}
.entry-title {{
    font-family: 'Georgia', serif;
    font-weight: 700;
    font-size: 11pt;
    color: #1a1a1a;
}}
.entry-date {{ font-size: 9.5pt; color: #666; }}
.entry-subtitle {{
    font-family: 'Georgia', serif;
    font-size: 10pt;
    color: #444;
    font-style: italic;
    margin-bottom: 6px;
}}
.entry-bullets {{
    margin: 0;
    padding-left: 20px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 10pt;
    color: #333;
    margin-bottom: 4px;
    line-height: 1.6;
    text-align: justify;
}}
'''


# =============================================================================
# TEMPLATE 16: SWISS - Clean Swiss/International style
# =============================================================================

def _build_swiss_template(resume, primary_color: str) -> str:
    """Swiss template - Clean Swiss/International typographic style."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_items = []
    if resume.email:
        contact_items.append(f'<div class="contact-row"><span class="label">Email</span><span>{_escape(resume.email)}</span></div>')
    if resume.phone:
        contact_items.append(f'<div class="contact-row"><span class="label">Phone</span><span>{_escape(resume.phone)}</span></div>')
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_items.append(f'<div class="contact-row"><span class="label">Location</span><span>{_escape(loc)}</span></div>')
    if resume.linkedin:
        contact_items.append(f'<div class="contact-row"><span class="label">LinkedIn</span><span>{_escape(resume.linkedin)}</span></div>')
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <div class="section-grid">
                <h2 class="section-label">Profile</h2>
                <p class="section-content">{_escape(resume.summary)}</p>
            </div>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-label">Skills</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    languages_html = ''
    if resume.languages:
        items = ''.join([f'<li>{_escape(l)}</li>' for l in resume.languages])
        languages_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-label">Languages</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'swiss')
    employment_html = _build_employment_html(resume.experience, 'swiss')
    
    return f'''
    <div class="body-container">
        <aside class="sidebar">
            {photo_section}
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{''.join(contact_items)}</div>
            {skills_html}
            {languages_html}
        </aside>
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
    </div>'''


def _get_swiss_styles(primary_color: str) -> str:
    return f'''
.body-container {{
    display: flex;
    min-height: 297mm;
}}
.sidebar {{
    width: 200px;
    background: #f5f5f5;
    padding: 35px 25px;
}}
.header-photo {{
    width: 100%;
    aspect-ratio: 1;
    overflow: hidden;
    margin-bottom: 20px;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.name {{
    font-size: 18pt;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 4px;
    line-height: 1.2;
}}
.role {{
    font-size: 10pt;
    color: {primary_color};
    margin-bottom: 20px;
}}
.contact {{ margin-bottom: 25px; }}
.contact-row {{
    display: flex;
    flex-direction: column;
    margin-bottom: 10px;
}}
.contact-row .label {{
    font-size: 8pt;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
}}
.contact-row span:last-child {{
    font-size: 9pt;
    color: #333;
}}
.sidebar-section {{ margin-bottom: 22px; }}
.sidebar-label {{
    font-size: 8pt;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    font-size: 9pt;
    color: #333;
    padding: 4px 0;
}}
.main-content {{
    flex: 1;
    padding: 35px 40px;
}}
.section {{ margin-bottom: 28px; }}
.section-grid {{
    display: grid;
    grid-template-columns: 100px 1fr;
    gap: 20px;
}}
.section-label {{
    font-size: 8pt;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding-top: 3px;
}}
.section-content {{
    font-size: 10pt;
    color: #333;
    line-height: 1.6;
}}
.entry {{ margin-bottom: 18px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}}
.entry-title {{ font-weight: 600; font-size: 10.5pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #888; }}
.entry-subtitle {{ font-size: 9.5pt; color: {primary_color}; margin-bottom: 6px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 16px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 4px;
    line-height: 1.5;
}}
'''


# =============================================================================
# PREMIUM TEMPLATES (17-26) - 10 Modern ATS-Compliant Resume Templates
# =============================================================================


# =============================================================================
# TEMPLATE 17: SLATE - Dark header with clean body, sophisticated typography
# =============================================================================

def _build_slate_template(resume, primary_color: str) -> str:
    """Slate template - Dark header with clean body, sophisticated typography."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_parts = []
    if resume.email:
        contact_parts.append(f'<span>{_escape(resume.email)}</span>')
    if resume.phone:
        contact_parts.append(f'<span>{_escape(resume.phone)}</span>')
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_parts.append(f'<span>{_escape(loc)}</span>')
    if resume.linkedin:
        contact_parts.append(f'<span>{_escape(resume.linkedin)}</span>')
    if resume.github:
        contact_parts.append(f'<span>{_escape(resume.github)}</span>')
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Professional Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Skills</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    languages_html = ''
    if resume.languages:
        items = ''.join([f'<li>{_escape(l)}</li>' for l in resume.languages])
        languages_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Languages</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'slate')
    employment_html = _build_employment_html(resume.experience, 'slate')
    
    return f'''
    <header class="header">
        {photo_section}
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{' • '.join(contact_parts)}</div>
        </div>
    </header>
    <div class="body-container">
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
        <aside class="sidebar">
            {skills_html}
            {languages_html}
        </aside>
    </div>'''


def _get_slate_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: {primary_color};
    color: #fff;
    padding: 32px 40px;
    display: flex;
    align-items: center;
    gap: 25px;
}}
.header-photo {{
    width: 95px;
    height: 95px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.25);
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-info {{ flex: 1; }}
.header .name {{
    font-size: 28pt;
    font-weight: 300;
    letter-spacing: 1px;
    margin-bottom: 6px;
}}
.header .role {{
    font-size: 12pt;
    font-weight: 400;
    color: rgba(255,255,255,0.9);
    margin-bottom: 12px;
}}
.header .contact {{
    font-size: 9pt;
    color: rgba(255,255,255,0.8);
}}
.body-container {{
    display: flex;
    min-height: calc(297mm - 130px);
}}
.main-content {{
    flex: 1;
    padding: 28px 32px;
}}
.sidebar {{
    width: 175px;
    background: #f8f9fa;
    padding: 28px 20px;
    border-left: 1px solid #e5e7eb;
}}
.section {{ margin-bottom: 24px; }}
.section-title {{
    font-size: 11pt;
    font-weight: 600;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.65;
    text-align: justify;
}}
.sidebar-section {{ margin-bottom: 22px; }}
.sidebar-title {{
    font-size: 10pt;
    font-weight: 600;
    color: {primary_color};
    margin-bottom: 10px;
    padding-bottom: 4px;
    border-bottom: 1px solid #dee2e6;
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    font-size: 9pt;
    color: #444;
    padding: 5px 0;
    border-bottom: 1px solid #e9ecef;
}}
.skills-list li:last-child {{ border-bottom: none; }}
.entry {{ margin-bottom: 18px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}}
.entry-title {{ font-weight: 600; font-size: 10.5pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 9.5pt; color: {primary_color}; margin-bottom: 6px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 16px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 4px;
    line-height: 1.5;
}}
'''


# =============================================================================
# TEMPLATE 18: METRO - Clean lines, accent sidebar, urban professional feel
# =============================================================================

def _build_metro_template(resume, primary_color: str) -> str:
    """Metro template - Clean lines, accent sidebar, urban professional feel."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Profile</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li><span class="bullet">▪</span>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Expertise</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    languages_html = ''
    if resume.languages:
        items = ''.join([f'<li><span class="bullet">▪</span>{_escape(l)}</li>' for l in resume.languages])
        languages_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Languages</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'metro')
    employment_html = _build_employment_html(resume.experience, 'metro')
    
    return f'''
    <div class="body-container">
        <aside class="sidebar">
            {photo_section}
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{''.join(contact_items)}</div>
            {skills_html}
            {languages_html}
        </aside>
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
    </div>'''


def _get_metro_styles(primary_color: str) -> str:
    return f'''
.body-container {{
    display: flex;
    min-height: 297mm;
}}
.sidebar {{
    width: 195px;
    background: {primary_color};
    color: #fff;
    padding: 32px 22px;
}}
.header-photo {{
    width: 110px;
    height: 110px;
    border-radius: 50%;
    overflow: hidden;
    margin: 0 auto 18px;
    border: 3px solid rgba(255,255,255,0.3);
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.name {{
    font-size: 20pt;
    font-weight: 600;
    text-align: center;
    margin-bottom: 4px;
}}
.role {{
    font-size: 10pt;
    text-align: center;
    color: rgba(255,255,255,0.9);
    margin-bottom: 22px;
}}
.contact {{ margin-bottom: 25px; }}
.contact-item {{
    font-size: 8.5pt;
    color: rgba(255,255,255,0.85);
    margin-bottom: 8px;
    padding-left: 8px;
    border-left: 2px solid rgba(255,255,255,0.4);
}}
.sidebar-section {{ margin-bottom: 22px; }}
.sidebar-title {{
    font-size: 10pt;
    font-weight: 600;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(255,255,255,0.3);
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    display: flex;
    align-items: flex-start;
    gap: 8px;
    font-size: 9pt;
    color: rgba(255,255,255,0.9);
    margin-bottom: 6px;
}}
.skills-list .bullet {{ color: rgba(255,255,255,0.6); }}
.main-content {{
    flex: 1;
    padding: 32px 35px;
}}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 12pt;
    font-weight: 600;
    color: {primary_color};
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.65;
    text-align: justify;
}}
.entry {{ margin-bottom: 18px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}}
.entry-title {{ font-weight: 600; font-size: 10.5pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 9.5pt; color: {primary_color}; margin-bottom: 6px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 16px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 4px;
    line-height: 1.5;
}}
'''


# =============================================================================
# TEMPLATE 19: HORIZON - Wide header band, balanced sections, executive presence
# =============================================================================

def _build_horizon_template(resume, primary_color: str) -> str:
    """Horizon template - Wide header band, balanced sections, executive presence."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section summary-section">
            <p class="summary-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ' • '.join([_escape(s) for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Core Competencies</h2>
            <p class="skills-inline">{items}</p>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'horizon')
    employment_html = _build_employment_html(resume.experience, 'horizon')
    
    return f'''
    <header class="header">
        <div class="header-top">
            {photo_section}
            <div class="header-info">
                <h1 class="name">{_escape(resume.full_name)}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
            </div>
        </div>
        <div class="header-contact">{' | '.join(contact_parts)}</div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_horizon_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: {primary_color};
    color: #fff;
    padding: 0;
}}
.header-top {{
    display: flex;
    align-items: center;
    gap: 25px;
    padding: 30px 40px 20px;
}}
.header-photo {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-info {{ flex: 1; }}
.header .name {{
    font-size: 30pt;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 13pt;
    font-weight: 400;
    color: rgba(255,255,255,0.9);
}}
.header-contact {{
    background: rgba(0,0,0,0.15);
    padding: 12px 40px;
    font-size: 9pt;
    color: rgba(255,255,255,0.9);
    text-align: center;
}}
.content {{ padding: 28px 40px; }}
.summary-section {{
    background: #f8f9fa;
    padding: 18px 22px;
    border-left: 4px solid {primary_color};
    margin-bottom: 26px;
}}
.summary-text {{
    font-size: 10.5pt;
    color: #333;
    line-height: 1.65;
    font-style: italic;
}}
.section {{ margin-bottom: 24px; }}
.section-title {{
    font-size: 12pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.skills-inline {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
}}
.entry {{ margin-bottom: 18px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 6px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 4px;
    line-height: 1.5;
}}
'''


# =============================================================================
# TEMPLATE 20: NORDIC - Scandinavian minimalism, generous whitespace
# =============================================================================

def _build_nordic_template(resume, primary_color: str) -> str:
    """Nordic template - Scandinavian minimalism, generous whitespace, subtle accents."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <p class="summary-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<span class="skill-item">{_escape(s)}</span>' for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Skills</h2>
            <div class="skills-wrap">{items}</div>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'nordic')
    employment_html = _build_employment_html(resume.experience, 'nordic')
    
    return f'''
    <header class="header">
        {photo_section}
        <h1 class="name">{_escape(resume.full_name)}</h1>
        <p class="role">{_escape(resume.role_title or '')}</p>
        <div class="contact">{' — '.join(contact_parts)}</div>
    </header>
    <main class="content">
        {summary_html}
        {education_html}
        {employment_html}
        {skills_html}
    </main>'''


def _get_nordic_styles(primary_color: str) -> str:
    return f'''
.header {{
    text-align: center;
    padding: 45px 50px 35px;
}}
.header-photo {{
    width: 85px;
    height: 85px;
    border-radius: 50%;
    overflow: hidden;
    margin: 0 auto 18px;
    border: 2px solid {primary_color};
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 32pt;
    font-weight: 300;
    color: #1a1a1a;
    letter-spacing: 3px;
    margin-bottom: 8px;
}}
.header .role {{
    font-size: 11pt;
    font-weight: 400;
    color: {primary_color};
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 16px;
}}
.header .contact {{
    font-size: 9pt;
    color: #888;
    letter-spacing: 0.5px;
}}
.content {{
    padding: 30px 55px;
}}
.section {{ margin-bottom: 32px; }}
.section-title {{
    font-size: 10pt;
    font-weight: 500;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 16px;
}}
.summary-text {{
    font-size: 10.5pt;
    color: #555;
    line-height: 1.8;
    text-align: center;
    max-width: 90%;
    margin: 0 auto;
}}
.skills-wrap {{
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
}}
.skill-item {{
    font-size: 9pt;
    color: #555;
    padding: 6px 16px;
    border: 1px solid #ddd;
    border-radius: 20px;
}}
.entry {{ margin-bottom: 22px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
}}
.entry-title {{ font-weight: 500; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #999; }}
.entry-subtitle {{ font-size: 9.5pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: none;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #555;
    margin-bottom: 5px;
    line-height: 1.6;
    position: relative;
    padding-left: 12px;
}}
.entry-bullets li::before {{
    content: '–';
    position: absolute;
    left: 0;
    color: {primary_color};
}}
'''


# =============================================================================
# TEMPLATE 21: APEX - Bold name treatment, structured sections, leadership focus
# =============================================================================

def _build_apex_template(resume, primary_color: str) -> str:
    """Apex template - Bold name treatment, structured sections, leadership focus."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_items = []
    if resume.email:
        contact_items.append(f'<div class="contact-item"><span class="label">Email</span>{_escape(resume.email)}</div>')
    if resume.phone:
        contact_items.append(f'<div class="contact-item"><span class="label">Phone</span>{_escape(resume.phone)}</div>')
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_items.append(f'<div class="contact-item"><span class="label">Location</span>{_escape(loc)}</div>')
    if resume.linkedin:
        contact_items.append(f'<div class="contact-item"><span class="label">LinkedIn</span>{_escape(resume.linkedin)}</div>')
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Executive Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Key Skills</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    languages_html = ''
    if resume.languages:
        items = ''.join([f'<li>{_escape(l)}</li>' for l in resume.languages])
        languages_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Languages</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'apex')
    employment_html = _build_employment_html(resume.experience, 'apex')
    
    return f'''
    <header class="header">
        <div class="header-main">
            {photo_section}
            <div class="header-text">
                <h1 class="name">{_escape(resume.full_name).upper()}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
            </div>
        </div>
        <div class="header-contact">{''.join(contact_items)}</div>
    </header>
    <div class="body-container">
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
        <aside class="sidebar">
            {skills_html}
            {languages_html}
        </aside>
    </div>'''


def _get_apex_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: #fff;
    padding: 28px 35px;
    border-bottom: 4px solid {primary_color};
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}}
.header-main {{
    display: flex;
    align-items: center;
    gap: 20px;
}}
.header-photo {{
    width: 85px;
    height: 85px;
    border-radius: 8px;
    overflow: hidden;
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 28pt;
    font-weight: 800;
    color: {primary_color};
    letter-spacing: 2px;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 11pt;
    color: #555;
    font-weight: 500;
}}
.header-contact {{
    display: flex;
    flex-direction: column;
    gap: 6px;
    text-align: right;
}}
.contact-item {{
    font-size: 9pt;
    color: #444;
}}
.contact-item .label {{
    color: {primary_color};
    font-weight: 600;
    margin-right: 8px;
}}
.body-container {{
    display: flex;
    min-height: calc(297mm - 130px);
}}
.main-content {{
    flex: 1;
    padding: 28px 32px;
}}
.sidebar {{
    width: 180px;
    background: #f5f7fa;
    padding: 28px 20px;
}}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 11pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.65;
    text-align: justify;
}}
.sidebar-section {{ margin-bottom: 24px; }}
.sidebar-title {{
    font-size: 10pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
    padding-bottom: 4px;
    border-bottom: 2px solid {primary_color};
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    font-size: 9pt;
    color: #444;
    padding: 5px 0;
    padding-left: 12px;
    position: relative;
}}
.skills-list li::before {{
    content: '▸';
    position: absolute;
    left: 0;
    color: {primary_color};
}}
.entry {{ margin-bottom: 18px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 6px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 4px;
    line-height: 1.5;
}}
'''


# =============================================================================
# TEMPLATE 22: CLARITY - Crystal clear hierarchy, perfect readability
# =============================================================================

def _build_clarity_template(resume, primary_color: str) -> str:
    """Clarity template - Crystal clear hierarchy, perfect readability, ATS optimized."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<span class="skill-tag">{_escape(s)}</span>' for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Skills</h2>
            <div class="skills-tags">{items}</div>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'clarity')
    employment_html = _build_employment_html(resume.experience, 'clarity')
    
    return f'''
    <header class="header">
        {photo_section}
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{' '.join(contact_parts)}</div>
        </div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_clarity_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: #fff;
    padding: 30px 40px;
    border-bottom: 3px solid {primary_color};
    display: flex;
    align-items: center;
    gap: 25px;
}}
.header-photo {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid {primary_color};
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-info {{ flex: 1; }}
.header .name {{
    font-size: 28pt;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 12pt;
    color: {primary_color};
    font-weight: 500;
    margin-bottom: 12px;
}}
.header .contact {{
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    font-size: 9pt;
    color: #555;
}}
.content {{ padding: 28px 40px; }}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 12pt;
    font-weight: 600;
    color: {primary_color};
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
    text-align: justify;
}}
.skills-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}}
.skill-tag {{
    background: {primary_color};
    color: #fff;
    padding: 5px 14px;
    border-radius: 4px;
    font-size: 9pt;
    font-weight: 500;
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 600; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 10pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# =============================================================================
# TEMPLATE 23: PRESTIGE - Premium feel, refined typography, senior-level
# =============================================================================

def _build_prestige_template(resume, primary_color: str) -> str:
    """Prestige template - Premium feel, refined typography, senior-level positioning."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Professional Profile</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Expertise</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    languages_html = ''
    if resume.languages:
        items = ''.join([f'<li>{_escape(l)}</li>' for l in resume.languages])
        languages_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Languages</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'prestige')
    employment_html = _build_employment_html(resume.experience, 'prestige')
    
    return f'''
    <header class="header">
        {photo_section}
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{' · '.join(contact_parts)}</div>
        </div>
    </header>
    <div class="body-container">
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
        <aside class="sidebar">
            {skills_html}
            {languages_html}
        </aside>
    </div>'''


def _get_prestige_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: linear-gradient(135deg, {primary_color} 0%, #1a1a1a 100%);
    color: #fff;
    padding: 35px 40px;
    display: flex;
    align-items: center;
    gap: 28px;
}}
.header-photo {{
    width: 100px;
    height: 100px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-info {{ flex: 1; }}
.header .name {{
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 30pt;
    font-weight: 400;
    letter-spacing: 1px;
    margin-bottom: 6px;
}}
.header .role {{
    font-size: 12pt;
    font-weight: 300;
    color: rgba(255,255,255,0.9);
    margin-bottom: 14px;
}}
.header .contact {{
    font-size: 9pt;
    color: rgba(255,255,255,0.8);
}}
.body-container {{
    display: flex;
    min-height: calc(297mm - 145px);
}}
.main-content {{
    flex: 1;
    padding: 30px 35px;
}}
.sidebar {{
    width: 180px;
    background: #fafafa;
    padding: 30px 22px;
    border-left: 1px solid #e5e7eb;
}}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-family: 'Georgia', serif;
    font-size: 12pt;
    font-weight: 400;
    color: {primary_color};
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 1px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
    text-align: justify;
}}
.sidebar-section {{ margin-bottom: 24px; }}
.sidebar-title {{
    font-family: 'Georgia', serif;
    font-size: 10pt;
    color: {primary_color};
    margin-bottom: 12px;
    padding-bottom: 4px;
    border-bottom: 1px solid #ddd;
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    font-size: 9pt;
    color: #444;
    padding: 5px 0;
    border-bottom: 1px solid #eee;
}}
.skills-list li:last-child {{ border-bottom: none; }}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{
    font-family: 'Georgia', serif;
    font-weight: 600;
    font-size: 11pt;
    color: #1a1a1a;
}}
.entry-date {{ font-size: 9pt; color: #888; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# =============================================================================
# TEMPLATE 24: STREAMLINE - Flowing layout, smooth transitions
# =============================================================================

def _build_streamline_template(resume, primary_color: str) -> str:
    """Streamline template - Flowing layout, smooth transitions, contemporary design."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">About</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<span class="skill-pill">{_escape(s)}</span>' for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Skills</h2>
            <div class="skills-pills">{items}</div>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'streamline')
    employment_html = _build_employment_html(resume.experience, 'streamline')
    
    return f'''
    <header class="header">
        <div class="header-left">
            {photo_section}
            <div class="header-text">
                <h1 class="name">{_escape(resume.full_name)}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
            </div>
        </div>
        <div class="header-contact">{' | '.join(contact_parts)}</div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_streamline_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: #fff;
    padding: 28px 38px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e5e7eb;
}}
.header-left {{
    display: flex;
    align-items: center;
    gap: 20px;
}}
.header-photo {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid {primary_color};
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 26pt;
    font-weight: 600;
    color: {primary_color};
    margin-bottom: 2px;
}}
.header .role {{
    font-size: 11pt;
    color: #666;
}}
.header-contact {{
    font-size: 9pt;
    color: #666;
    text-align: right;
    max-width: 200px;
}}
.content {{ padding: 28px 38px; }}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 11pt;
    font-weight: 600;
    color: {primary_color};
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.section-title::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, {primary_color} 0%, transparent 100%);
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
}}
.skills-pills {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}}
.skill-pill {{
    background: #f0f9ff;
    color: {primary_color};
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 9pt;
    border: 1px solid {primary_color};
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 600; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{
    font-size: 9pt;
    color: #fff;
    background: {primary_color};
    padding: 2px 10px;
    border-radius: 10px;
}}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# =============================================================================
# TEMPLATE 25: FOUNDATION - Solid structure, traditional excellence
# =============================================================================

def _build_foundation_template(resume, primary_color: str) -> str:
    """Foundation template - Solid structure, traditional excellence, timeless appeal."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Professional Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        mid = len(resume.skills) // 2
        col1 = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills[:mid]])
        col2 = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills[mid:]])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Core Competencies</h2>
            <div class="skills-columns">
                <ul class="skills-col">{col1}</ul>
                <ul class="skills-col">{col2}</ul>
            </div>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'foundation')
    employment_html = _build_employment_html(resume.experience, 'foundation')
    
    return f'''
    <header class="header">
        {photo_section}
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{' | '.join(contact_parts)}</div>
        </div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_foundation_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: {primary_color};
    color: #fff;
    padding: 30px 40px;
    display: flex;
    align-items: center;
    gap: 25px;
}}
.header-photo {{
    width: 95px;
    height: 95px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-info {{ flex: 1; }}
.header .name {{
    font-size: 28pt;
    font-weight: 700;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 12pt;
    color: rgba(255,255,255,0.9);
    margin-bottom: 12px;
}}
.header .contact {{
    font-size: 9pt;
    color: rgba(255,255,255,0.85);
}}
.content {{ padding: 28px 40px; }}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 12pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
    text-align: justify;
}}
.skills-columns {{
    display: flex;
    gap: 40px;
}}
.skills-col {{
    flex: 1;
    list-style: none;
}}
.skills-col li {{
    font-size: 9.5pt;
    color: #444;
    padding: 5px 0;
    padding-left: 16px;
    position: relative;
    border-bottom: 1px solid #f0f0f0;
}}
.skills-col li::before {{
    content: '●';
    position: absolute;
    left: 0;
    color: {primary_color};
    font-size: 8pt;
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# =============================================================================
# TEMPLATE 26: ZENITH - Peak professional design, commanding presence
# =============================================================================

def _build_zenith_template(resume, primary_color: str) -> str:
    """Zenith template - Peak professional design, commanding presence, top-tier layout."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Executive Profile</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li><span class="skill-marker"></span>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Core Skills</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    languages_html = ''
    if resume.languages:
        items = ''.join([f'<li><span class="skill-marker"></span>{_escape(l)}</li>' for l in resume.languages])
        languages_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Languages</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'zenith')
    employment_html = _build_employment_html(resume.experience, 'zenith')
    
    return f'''
    <header class="header">
        <div class="header-main">
            {photo_section}
            <div class="header-text">
                <h1 class="name">{_escape(resume.full_name).upper()}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
            </div>
        </div>
    </header>
    <div class="body-container">
        <aside class="sidebar">
            <div class="sidebar-section contact-section">
                <h3 class="sidebar-title">Contact</h3>
                {''.join(contact_items)}
            </div>
            {skills_html}
            {languages_html}
        </aside>
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
    </div>'''


def _get_zenith_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: {primary_color};
    color: #fff;
    padding: 35px 40px;
}}
.header-main {{
    display: flex;
    align-items: center;
    gap: 25px;
}}
.header-photo {{
    width: 100px;
    height: 100px;
    border-radius: 50%;
    overflow: hidden;
    border: 4px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 32pt;
    font-weight: 800;
    letter-spacing: 3px;
    margin-bottom: 6px;
}}
.header .role {{
    font-size: 13pt;
    font-weight: 400;
    color: rgba(255,255,255,0.9);
    letter-spacing: 1px;
}}
.body-container {{
    display: flex;
    min-height: calc(297mm - 145px);
}}
.sidebar {{
    width: 190px;
    background: #f5f5f5;
    padding: 28px 22px;
}}
.main-content {{
    flex: 1;
    padding: 28px 35px;
}}
.sidebar-section {{ margin-bottom: 24px; }}
.sidebar-title {{
    font-size: 10pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.contact-section .contact-item {{
    font-size: 9pt;
    color: #444;
    margin-bottom: 8px;
    padding-left: 10px;
    border-left: 2px solid {primary_color};
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 9pt;
    color: #444;
    margin-bottom: 8px;
}}
.skill-marker {{
    width: 8px;
    height: 8px;
    background: {primary_color};
    border-radius: 2px;
    flex-shrink: 0;
}}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 12pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 3px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
    text-align: justify;
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# =============================================================================
# PREMIUM TEMPLATES BATCH 2 (27-51) - 25 New Modern ATS-Compliant Templates
# =============================================================================


# =============================================================================
# EXECUTIVE TEMPLATES (5)
# =============================================================================

# TEMPLATE 27: MONARCH - Commanding presence with bold header
def _build_monarch_template(resume, primary_color: str) -> str:
    """Monarch template - Commanding presence with bold header for C-suite."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Executive Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Leadership Skills</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'monarch')
    employment_html = _build_employment_html(resume.experience, 'monarch')
    
    return f'''
    <header class="header">
        <div class="header-band"></div>
        <div class="header-content">
            {photo_section}
            <div class="header-info">
                <h1 class="name">{_escape(resume.full_name).upper()}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
                <div class="contact">{' · '.join(contact_parts)}</div>
            </div>
        </div>
    </header>
    <div class="body-container">
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
        <aside class="sidebar">
            {skills_html}
        </aside>
    </div>'''


def _get_monarch_styles(primary_color: str) -> str:
    return f'''
.header {{
    position: relative;
    background: #fff;
}}
.header-band {{
    height: 8px;
    background: {primary_color};
}}
.header-content {{
    padding: 28px 40px;
    display: flex;
    align-items: center;
    gap: 25px;
    border-bottom: 1px solid #e5e7eb;
}}
.header-photo {{
    width: 100px;
    height: 100px;
    border-radius: 50%;
    overflow: hidden;
    border: 4px solid {primary_color};
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-info {{ flex: 1; }}
.header .name {{
    font-size: 32pt;
    font-weight: 800;
    color: {primary_color};
    letter-spacing: 3px;
    margin-bottom: 6px;
}}
.header .role {{
    font-size: 13pt;
    color: #555;
    font-weight: 500;
    margin-bottom: 10px;
}}
.header .contact {{
    font-size: 9pt;
    color: #666;
}}
.body-container {{
    display: flex;
    min-height: calc(297mm - 160px);
}}
.main-content {{
    flex: 1;
    padding: 28px 35px;
}}
.sidebar {{
    width: 185px;
    background: #f8f9fa;
    padding: 28px 22px;
    border-left: 3px solid {primary_color};
}}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 12pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
    text-align: justify;
}}
.sidebar-section {{ margin-bottom: 24px; }}
.sidebar-title {{
    font-size: 10pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    font-size: 9pt;
    color: #444;
    padding: 6px 0;
    border-bottom: 1px solid #e9ecef;
}}
.skills-list li:last-child {{ border-bottom: none; }}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# TEMPLATE 28: SUMMIT - Peak professional design
def _build_summit_template(resume, primary_color: str) -> str:
    """Summit template - Peak professional design with elegant hierarchy."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Profile</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<span class="skill-badge">{_escape(s)}</span>' for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Core Competencies</h2>
            <div class="skills-badges">{items}</div>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'summit')
    employment_html = _build_employment_html(resume.experience, 'summit')
    
    return f'''
    <header class="header">
        <div class="header-left">
            {photo_section}
            <div class="header-text">
                <h1 class="name">{_escape(resume.full_name)}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
            </div>
        </div>
        <div class="header-right">{''.join(contact_items)}</div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_summit_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: linear-gradient(180deg, {primary_color} 0%, #1a1a1a 100%);
    color: #fff;
    padding: 32px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.header-left {{
    display: flex;
    align-items: center;
    gap: 22px;
}}
.header-photo {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 28pt;
    font-weight: 700;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 12pt;
    color: rgba(255,255,255,0.9);
}}
.header-right {{
    text-align: right;
}}
.contact-item {{
    font-size: 9pt;
    color: rgba(255,255,255,0.85);
    margin-bottom: 6px;
}}
.content {{ padding: 28px 40px; }}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 11pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
    text-align: justify;
}}
.skills-badges {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}}
.skill-badge {{
    background: {primary_color};
    color: #fff;
    padding: 5px 14px;
    border-radius: 3px;
    font-size: 9pt;
    font-weight: 500;
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# TEMPLATE 29: REGENT - Refined serif typography
def _build_regent_template(resume, primary_color: str) -> str:
    """Regent template - Refined serif typography with classic executive appeal."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Professional Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ' · '.join([_escape(s) for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Areas of Expertise</h2>
            <p class="skills-text">{items}</p>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'regent')
    employment_html = _build_employment_html(resume.experience, 'regent')
    
    return f'''
    <header class="header">
        {photo_section}
        <h1 class="name">{_escape(resume.full_name)}</h1>
        <p class="role">{_escape(resume.role_title or '')}</p>
        <div class="divider"></div>
        <div class="contact">{' | '.join(contact_parts)}</div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_regent_styles(primary_color: str) -> str:
    return f'''
.header {{
    text-align: center;
    padding: 40px 50px 30px;
}}
.header-photo {{
    width: 95px;
    height: 95px;
    border-radius: 50%;
    overflow: hidden;
    margin: 0 auto 16px;
    border: 2px solid {primary_color};
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 30pt;
    font-weight: 400;
    color: #1a1a1a;
    letter-spacing: 2px;
    margin-bottom: 6px;
}}
.header .role {{
    font-family: 'Georgia', serif;
    font-size: 12pt;
    font-style: italic;
    color: {primary_color};
    margin-bottom: 16px;
}}
.divider {{
    width: 60px;
    height: 2px;
    background: {primary_color};
    margin: 0 auto 16px;
}}
.header .contact {{
    font-size: 9pt;
    color: #666;
}}
.content {{ padding: 28px 50px; }}
.section {{ margin-bottom: 28px; }}
.section-title {{
    font-family: 'Georgia', serif;
    font-size: 12pt;
    font-weight: 400;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 1px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.75;
    text-align: justify;
}}
.skills-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.8;
    text-align: center;
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{
    font-family: 'Georgia', serif;
    font-weight: 600;
    font-size: 11pt;
    color: #1a1a1a;
}}
.entry-date {{ font-size: 9pt; color: #888; }}
.entry-subtitle {{
    font-family: 'Georgia', serif;
    font-size: 10pt;
    color: {primary_color};
    font-style: italic;
    margin-bottom: 8px;
}}
.entry-bullets {{
    margin: 0;
    padding-left: 20px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.6;
}}
'''


# TEMPLATE 30: PINNACLE - Top-tier layout with commanding name
def _build_pinnacle_template(resume, primary_color: str) -> str:
    """Pinnacle template - Top-tier layout with commanding name treatment."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_items = []
    if resume.email:
        contact_items.append(f'<div class="contact-row"><span class="label">Email</span><span class="value">{_escape(resume.email)}</span></div>')
    if resume.phone:
        contact_items.append(f'<div class="contact-row"><span class="label">Phone</span><span class="value">{_escape(resume.phone)}</span></div>')
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_items.append(f'<div class="contact-row"><span class="label">Location</span><span class="value">{_escape(loc)}</span></div>')
    if resume.linkedin:
        contact_items.append(f'<div class="contact-row"><span class="label">LinkedIn</span><span class="value">{_escape(resume.linkedin)}</span></div>')
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section highlight-section">
            <p class="highlight-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Expertise</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'pinnacle')
    employment_html = _build_employment_html(resume.experience, 'pinnacle')
    
    return f'''
    <header class="header">
        <div class="header-top">
            {photo_section}
            <h1 class="name">{_escape(resume.full_name).upper()}</h1>
            <p class="role">{_escape(resume.role_title or '').upper()}</p>
        </div>
        <div class="header-contact">{''.join(contact_items)}</div>
    </header>
    <div class="body-container">
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
        <aside class="sidebar">
            {skills_html}
        </aside>
    </div>'''


def _get_pinnacle_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: {primary_color};
    color: #fff;
}}
.header-top {{
    text-align: center;
    padding: 35px 40px 25px;
}}
.header-photo {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    overflow: hidden;
    margin: 0 auto 14px;
    border: 3px solid rgba(255,255,255,0.3);
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 34pt;
    font-weight: 800;
    letter-spacing: 4px;
    margin-bottom: 6px;
}}
.header .role {{
    font-size: 11pt;
    font-weight: 500;
    letter-spacing: 3px;
    color: rgba(255,255,255,0.9);
}}
.header-contact {{
    background: rgba(0,0,0,0.15);
    padding: 14px 40px;
    display: flex;
    justify-content: center;
    gap: 30px;
}}
.contact-row {{
    display: flex;
    flex-direction: column;
    align-items: center;
}}
.contact-row .label {{
    font-size: 7pt;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: rgba(255,255,255,0.7);
    margin-bottom: 2px;
}}
.contact-row .value {{
    font-size: 9pt;
    color: #fff;
}}
.body-container {{
    display: flex;
    min-height: calc(297mm - 170px);
}}
.main-content {{
    flex: 1;
    padding: 28px 35px;
}}
.sidebar {{
    width: 180px;
    background: #f5f7fa;
    padding: 28px 22px;
}}
.highlight-section {{
    background: #f8f9fa;
    padding: 18px 22px;
    border-left: 4px solid {primary_color};
    margin-bottom: 26px;
}}
.highlight-text {{
    font-size: 10.5pt;
    color: #333;
    line-height: 1.7;
    font-style: italic;
}}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 11pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.sidebar-section {{ margin-bottom: 24px; }}
.sidebar-title {{
    font-size: 10pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    font-size: 9pt;
    color: #444;
    padding: 5px 0;
    border-bottom: 1px solid #e9ecef;
}}
.skills-list li:last-child {{ border-bottom: none; }}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# TEMPLATE 31: DYNASTY - Prestigious design with refined spacing
def _build_dynasty_template(resume, primary_color: str) -> str:
    """Dynasty template - Prestigious design with refined spacing for executives."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Executive Profile</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li><span class="bullet">▪</span>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Key Strengths</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'dynasty')
    employment_html = _build_employment_html(resume.experience, 'dynasty')
    
    return f'''
    <div class="body-container">
        <aside class="sidebar">
            {photo_section}
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{'<br>'.join(contact_parts)}</div>
            {skills_html}
        </aside>
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
    </div>'''


def _get_dynasty_styles(primary_color: str) -> str:
    return f'''
.body-container {{
    display: flex;
    min-height: 297mm;
}}
.sidebar {{
    width: 210px;
    background: {primary_color};
    color: #fff;
    padding: 35px 25px;
}}
.header-photo {{
    width: 120px;
    height: 120px;
    border-radius: 50%;
    overflow: hidden;
    margin: 0 auto 20px;
    border: 4px solid rgba(255,255,255,0.3);
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.name {{
    font-size: 18pt;
    font-weight: 700;
    text-align: center;
    margin-bottom: 6px;
    line-height: 1.2;
}}
.role {{
    font-size: 10pt;
    text-align: center;
    color: rgba(255,255,255,0.9);
    margin-bottom: 20px;
}}
.contact {{
    font-size: 8.5pt;
    color: rgba(255,255,255,0.85);
    text-align: center;
    margin-bottom: 28px;
    line-height: 1.8;
}}
.sidebar-section {{ margin-bottom: 24px; }}
.sidebar-title {{
    font-size: 10pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(255,255,255,0.3);
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    display: flex;
    align-items: flex-start;
    gap: 8px;
    font-size: 9pt;
    color: rgba(255,255,255,0.9);
    margin-bottom: 8px;
}}
.skills-list .bullet {{ color: rgba(255,255,255,0.6); }}
.main-content {{
    flex: 1;
    padding: 35px 40px;
}}
.section {{ margin-bottom: 28px; }}
.section-title {{
    font-size: 12pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.75;
    text-align: justify;
}}
.entry {{ margin-bottom: 22px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.6;
}}
'''


# =============================================================================
# TECHNICAL TEMPLATES (5)
# =============================================================================

# TEMPLATE 32: CIRCUIT - Clean technical layout with monospace accents
def _build_circuit_template(resume, primary_color: str) -> str:
    """Circuit template - Clean technical layout with monospace accents."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_parts = []
    if resume.email:
        contact_parts.append(f'<span class="contact-item">{_escape(resume.email)}</span>')
    if resume.phone:
        contact_parts.append(f'<span class="contact-item">{_escape(resume.phone)}</span>')
    if resume.github:
        contact_parts.append(f'<span class="contact-item highlight">{_escape(resume.github)}</span>')
    if resume.linkedin:
        contact_parts.append(f'<span class="contact-item">{_escape(resume.linkedin)}</span>')
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">// Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<span class="skill-tag">{_escape(s)}</span>' for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">// Tech Stack</h2>
            <div class="skills-tags">{items}</div>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'circuit')
    employment_html = _build_employment_html(resume.experience, 'circuit')
    
    return f'''
    <header class="header">
        <div class="header-main">
            {photo_section}
            <div class="header-text">
                <h1 class="name">{_escape(resume.full_name)}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
            </div>
        </div>
        <div class="header-contact">{' '.join(contact_parts)}</div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_circuit_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: #0d1117;
    color: #fff;
    padding: 28px 38px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.header-main {{
    display: flex;
    align-items: center;
    gap: 20px;
}}
.header-photo {{
    width: 80px;
    height: 80px;
    border-radius: 8px;
    overflow: hidden;
    border: 2px solid {primary_color};
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 26pt;
    font-weight: 600;
    margin-bottom: 4px;
    font-family: 'Segoe UI', Arial, sans-serif;
}}
.header .role {{
    font-size: 11pt;
    color: {primary_color};
    font-family: 'Consolas', 'Monaco', monospace;
}}
.header-contact {{
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 5px;
}}
.contact-item {{
    font-size: 9pt;
    color: rgba(255,255,255,0.8);
    font-family: 'Consolas', 'Monaco', monospace;
}}
.contact-item.highlight {{ color: {primary_color}; }}
.content {{ padding: 28px 38px; }}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 11pt;
    font-weight: 600;
    color: {primary_color};
    font-family: 'Consolas', 'Monaco', monospace;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
}}
.skills-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}}
.skill-tag {{
    background: #0d1117;
    color: {primary_color};
    padding: 5px 12px;
    border-radius: 4px;
    font-size: 9pt;
    font-family: 'Consolas', 'Monaco', monospace;
    border: 1px solid {primary_color};
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 600; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{
    font-size: 9pt;
    color: #666;
    font-family: 'Consolas', 'Monaco', monospace;
}}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: none;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
    position: relative;
    padding-left: 14px;
}}
.entry-bullets li::before {{
    content: '>';
    position: absolute;
    left: 0;
    color: {primary_color};
    font-family: 'Consolas', monospace;
}}
'''


# TEMPLATE 33: MATRIX - Grid-based structure for technical roles
def _build_matrix_template(resume, primary_color: str) -> str:
    """Matrix template - Grid-based structure optimized for technical roles."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_items = []
    if resume.email:
        contact_items.append(f'<div class="contact-item">{_escape(resume.email)}</div>')
    if resume.phone:
        contact_items.append(f'<div class="contact-item">{_escape(resume.phone)}</div>')
    if resume.github:
        contact_items.append(f'<div class="contact-item">{_escape(resume.github)}</div>')
    if resume.linkedin:
        contact_items.append(f'<div class="contact-item">{_escape(resume.linkedin)}</div>')
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Profile</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Technical Skills</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'matrix')
    employment_html = _build_employment_html(resume.experience, 'matrix')
    
    return f'''
    <header class="header">
        {photo_section}
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
        </div>
        <div class="header-contact">{''.join(contact_items)}</div>
    </header>
    <div class="body-container">
        <aside class="sidebar">
            {skills_html}
        </aside>
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
    </div>'''


def _get_matrix_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: #fff;
    padding: 28px 38px;
    display: flex;
    align-items: center;
    gap: 22px;
    border-bottom: 3px solid {primary_color};
}}
.header-photo {{
    width: 85px;
    height: 85px;
    border-radius: 6px;
    overflow: hidden;
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-info {{ flex: 1; }}
.header .name {{
    font-size: 26pt;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 12pt;
    color: {primary_color};
}}
.header-contact {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px 20px;
}}
.contact-item {{
    font-size: 9pt;
    color: #555;
}}
.body-container {{
    display: flex;
    min-height: calc(297mm - 130px);
}}
.sidebar {{
    width: 180px;
    background: #f5f7fa;
    padding: 28px 20px;
    border-right: 2px solid {primary_color};
}}
.main-content {{
    flex: 1;
    padding: 28px 35px;
}}
.sidebar-section {{ margin-bottom: 24px; }}
.sidebar-title {{
    font-size: 10pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    font-size: 9pt;
    color: #444;
    padding: 6px 10px;
    margin-bottom: 4px;
    background: #fff;
    border-left: 3px solid {primary_color};
}}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 11pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# TEMPLATE 34: QUANTUM - Modern tech aesthetic with skills-first layout
def _build_quantum_template(resume, primary_color: str) -> str:
    """Quantum template - Modern tech aesthetic with skills-first layout."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_parts = []
    if resume.email:
        contact_parts.append(_escape(resume.email))
    if resume.phone:
        contact_parts.append(_escape(resume.phone))
    if resume.github:
        contact_parts.append(_escape(resume.github))
    if resume.linkedin:
        contact_parts.append(_escape(resume.linkedin))
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">About</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<span class="skill-chip">{_escape(s)}</span>' for s in resume.skills])
        skills_html = f'''<section class="section skills-section">
            <h2 class="section-title">Skills & Technologies</h2>
            <div class="skills-chips">{items}</div>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'quantum')
    employment_html = _build_employment_html(resume.experience, 'quantum')
    
    return f'''
    <header class="header">
        <div class="header-content">
            {photo_section}
            <div class="header-text">
                <h1 class="name">{_escape(resume.full_name)}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
                <div class="contact">{' · '.join(contact_parts)}</div>
            </div>
        </div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_quantum_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: linear-gradient(135deg, {primary_color} 0%, #1a1a2e 100%);
    color: #fff;
    padding: 32px 40px;
}}
.header-content {{
    display: flex;
    align-items: center;
    gap: 24px;
}}
.header-photo {{
    width: 95px;
    height: 95px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 28pt;
    font-weight: 700;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 12pt;
    color: rgba(255,255,255,0.9);
    margin-bottom: 10px;
}}
.header .contact {{
    font-size: 9pt;
    color: rgba(255,255,255,0.8);
}}
.content {{ padding: 28px 40px; }}
.section {{ margin-bottom: 26px; }}
.skills-section {{
    background: #f8f9fa;
    padding: 20px 24px;
    margin: 0 -40px 26px;
    padding-left: 40px;
    padding-right: 40px;
}}
.section-title {{
    font-size: 11pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
}}
.skills-chips {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}}
.skill-chip {{
    background: {primary_color};
    color: #fff;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 9pt;
    font-weight: 500;
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# TEMPLATE 35: BINARY - Minimalist developer-focused design
def _build_binary_template(resume, primary_color: str) -> str:
    """Binary template - Minimalist developer-focused design with code aesthetics."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_parts = []
    if resume.email:
        contact_parts.append(_escape(resume.email))
    if resume.phone:
        contact_parts.append(_escape(resume.phone))
    if resume.github:
        contact_parts.append(_escape(resume.github))
    if resume.linkedin:
        contact_parts.append(_escape(resume.linkedin))
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">README</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">DEPENDENCIES</h2>
            <ul class="skills-list">{items}</ul>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'binary')
    employment_html = _build_employment_html(resume.experience, 'binary')
    
    return f'''
    <header class="header">
        {photo_section}
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{' | '.join(contact_parts)}</div>
        </div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_binary_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: #1a1a1a;
    color: #fff;
    padding: 30px 40px;
    display: flex;
    align-items: center;
    gap: 24px;
}}
.header-photo {{
    width: 85px;
    height: 85px;
    border-radius: 4px;
    overflow: hidden;
    border: 2px solid {primary_color};
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-info {{ flex: 1; }}
.header .name {{
    font-size: 26pt;
    font-weight: 600;
    font-family: 'Consolas', 'Monaco', monospace;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 11pt;
    color: {primary_color};
    font-family: 'Consolas', 'Monaco', monospace;
    margin-bottom: 10px;
}}
.header .contact {{
    font-size: 9pt;
    color: rgba(255,255,255,0.7);
    font-family: 'Consolas', 'Monaco', monospace;
}}
.content {{ padding: 28px 40px; }}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 10pt;
    font-weight: 600;
    color: {primary_color};
    font-family: 'Consolas', 'Monaco', monospace;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 1px dashed {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
}}
.skills-list {{
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}}
.skills-list li {{
    font-size: 9pt;
    color: #333;
    padding: 4px 12px;
    background: #f5f5f5;
    border: 1px solid #ddd;
    font-family: 'Consolas', 'Monaco', monospace;
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 600; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{
    font-size: 9pt;
    color: #666;
    font-family: 'Consolas', 'Monaco', monospace;
}}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: none;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
    position: relative;
    padding-left: 14px;
}}
.entry-bullets li::before {{
    content: '-';
    position: absolute;
    left: 0;
    color: {primary_color};
}}
'''


# TEMPLATE 36: STACK - Full-stack friendly layout
def _build_stack_template(resume, primary_color: str) -> str:
    """Stack template - Full-stack friendly layout with prominent tech skills."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_items = []
    if resume.email:
        contact_items.append(f'<span>{_escape(resume.email)}</span>')
    if resume.phone:
        contact_items.append(f'<span>{_escape(resume.phone)}</span>')
    if resume.github:
        contact_items.append(f'<span class="highlight">{_escape(resume.github)}</span>')
    if resume.linkedin:
        contact_items.append(f'<span>{_escape(resume.linkedin)}</span>')
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<div class="skill-item"><span class="skill-dot"></span>{_escape(s)}</div>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Tech Stack</h3>
            <div class="skills-grid">{items}</div>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'stack')
    employment_html = _build_employment_html(resume.experience, 'stack')
    
    return f'''
    <header class="header">
        <div class="header-left">
            {photo_section}
            <div class="header-text">
                <h1 class="name">{_escape(resume.full_name)}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
            </div>
        </div>
        <div class="header-contact">{' '.join(contact_items)}</div>
    </header>
    <div class="body-container">
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
        <aside class="sidebar">
            {skills_html}
        </aside>
    </div>'''


def _get_stack_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: {primary_color};
    color: #fff;
    padding: 28px 38px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.header-left {{
    display: flex;
    align-items: center;
    gap: 20px;
}}
.header-photo {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 26pt;
    font-weight: 700;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 11pt;
    color: rgba(255,255,255,0.9);
}}
.header-contact {{
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 5px;
    font-size: 9pt;
    color: rgba(255,255,255,0.85);
}}
.header-contact .highlight {{ color: #fff; font-weight: 600; }}
.body-container {{
    display: flex;
    min-height: calc(297mm - 120px);
}}
.main-content {{
    flex: 1;
    padding: 28px 35px;
}}
.sidebar {{
    width: 175px;
    background: #f8f9fa;
    padding: 28px 20px;
}}
.sidebar-section {{ margin-bottom: 24px; }}
.sidebar-title {{
    font-size: 10pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.skills-grid {{
    display: flex;
    flex-direction: column;
    gap: 8px;
}}
.skill-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 9pt;
    color: #444;
}}
.skill-dot {{
    width: 6px;
    height: 6px;
    background: {primary_color};
    border-radius: 50%;
    flex-shrink: 0;
}}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 11pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# =============================================================================
# MODERN TEMPLATES (5)
# =============================================================================

# TEMPLATE 37: PRISM - Light and airy design with subtle color accents
def _build_prism_template(resume, primary_color: str) -> str:
    """Prism template - Light and airy design with subtle color accents."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">About Me</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<span class="skill-pill">{_escape(s)}</span>' for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Skills</h2>
            <div class="skills-pills">{items}</div>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'prism')
    employment_html = _build_employment_html(resume.experience, 'prism')
    
    return f'''
    <header class="header">
        {photo_section}
        <h1 class="name">{_escape(resume.full_name)}</h1>
        <p class="role">{_escape(resume.role_title or '')}</p>
        <div class="contact">{' · '.join(contact_parts)}</div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_prism_styles(primary_color: str) -> str:
    return f'''
.header {{
    text-align: center;
    padding: 40px 50px 32px;
    background: linear-gradient(180deg, rgba(102,126,234,0.08) 0%, #fff 100%);
}}
.header-photo {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    overflow: hidden;
    margin: 0 auto 16px;
    border: 3px solid {primary_color};
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 30pt;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 6px;
}}
.header .role {{
    font-size: 12pt;
    color: {primary_color};
    margin-bottom: 14px;
}}
.header .contact {{
    font-size: 9pt;
    color: #666;
}}
.content {{ padding: 28px 50px; }}
.section {{ margin-bottom: 28px; }}
.section-title {{
    font-size: 11pt;
    font-weight: 600;
    color: {primary_color};
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.section-title::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, {primary_color}40 0%, transparent 100%);
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.75;
}}
.skills-pills {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}}
.skill-pill {{
    background: rgba(102,126,234,0.1);
    color: {primary_color};
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 9pt;
    font-weight: 500;
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 600; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #888; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.6;
}}
'''


# TEMPLATE 38: NOVA - Fresh contemporary style with dynamic spacing
def _build_nova_template(resume, primary_color: str) -> str:
    """Nova template - Fresh contemporary style with dynamic spacing."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Profile</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Skills</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'nova')
    employment_html = _build_employment_html(resume.experience, 'nova')
    
    return f'''
    <header class="header">
        <div class="header-main">
            {photo_section}
            <div class="header-text">
                <h1 class="name">{_escape(resume.full_name)}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
            </div>
        </div>
        <div class="header-contact">{''.join(contact_items)}</div>
    </header>
    <div class="body-container">
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
        <aside class="sidebar">
            {skills_html}
        </aside>
    </div>'''


def _get_nova_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: #fff;
    padding: 30px 38px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 4px solid {primary_color};
}}
.header-main {{
    display: flex;
    align-items: center;
    gap: 20px;
}}
.header-photo {{
    width: 85px;
    height: 85px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid {primary_color};
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 28pt;
    font-weight: 700;
    color: {primary_color};
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 11pt;
    color: #555;
}}
.header-contact {{
    text-align: right;
}}
.contact-item {{
    font-size: 9pt;
    color: #555;
    margin-bottom: 5px;
}}
.body-container {{
    display: flex;
    min-height: calc(297mm - 140px);
}}
.main-content {{
    flex: 1;
    padding: 28px 35px;
}}
.sidebar {{
    width: 170px;
    background: {primary_color};
    color: #fff;
    padding: 28px 20px;
}}
.sidebar-section {{ margin-bottom: 24px; }}
.sidebar-title {{
    font-size: 10pt;
    font-weight: 600;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(255,255,255,0.3);
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    font-size: 9pt;
    color: rgba(255,255,255,0.9);
    padding: 5px 0;
    border-bottom: 1px solid rgba(255,255,255,0.15);
}}
.skills-list li:last-child {{ border-bottom: none; }}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 12pt;
    font-weight: 700;
    color: {primary_color};
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# TEMPLATE 39: PULSE - Energetic layout with modern typography
def _build_pulse_template(resume, primary_color: str) -> str:
    """Pulse template - Energetic layout with modern typography."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">About</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<span class="skill-tag">{_escape(s)}</span>' for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Skills</h2>
            <div class="skills-tags">{items}</div>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'pulse')
    employment_html = _build_employment_html(resume.experience, 'pulse')
    
    return f'''
    <header class="header">
        <div class="header-accent"></div>
        <div class="header-content">
            {photo_section}
            <div class="header-info">
                <h1 class="name">{_escape(resume.full_name)}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
                <div class="contact">{' | '.join(contact_parts)}</div>
            </div>
        </div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_pulse_styles(primary_color: str) -> str:
    return f'''
.header {{
    position: relative;
    background: #fff;
}}
.header-accent {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6px;
    background: linear-gradient(90deg, {primary_color} 0%, #ff6b6b 50%, {primary_color} 100%);
}}
.header-content {{
    padding: 32px 40px;
    display: flex;
    align-items: center;
    gap: 24px;
}}
.header-photo {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid {primary_color};
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-info {{ flex: 1; }}
.header .name {{
    font-size: 30pt;
    font-weight: 800;
    color: #1a1a1a;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 12pt;
    color: {primary_color};
    font-weight: 600;
    margin-bottom: 10px;
}}
.header .contact {{
    font-size: 9pt;
    color: #666;
}}
.content {{ padding: 28px 40px; }}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 12pt;
    font-weight: 800;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 3px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
}}
.skills-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}}
.skill-tag {{
    background: {primary_color};
    color: #fff;
    padding: 5px 14px;
    border-radius: 4px;
    font-size: 9pt;
    font-weight: 600;
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; font-weight: 600; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# TEMPLATE 40: FLUX - Flowing design with seamless section transitions
def _build_flux_template(resume, primary_color: str) -> str:
    """Flux template - Flowing design with seamless section transitions."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ' • '.join([_escape(s) for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Skills</h2>
            <p class="skills-flow">{items}</p>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'flux')
    employment_html = _build_employment_html(resume.experience, 'flux')
    
    return f'''
    <header class="header">
        {photo_section}
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{' · '.join(contact_parts)}</div>
        </div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_flux_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: {primary_color};
    color: #fff;
    padding: 32px 40px;
    display: flex;
    align-items: center;
    gap: 24px;
    border-radius: 0 0 30px 0;
}}
.header-photo {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-info {{ flex: 1; }}
.header .name {{
    font-size: 28pt;
    font-weight: 600;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 12pt;
    color: rgba(255,255,255,0.9);
    margin-bottom: 10px;
}}
.header .contact {{
    font-size: 9pt;
    color: rgba(255,255,255,0.8);
}}
.content {{ padding: 28px 40px; }}
.section {{ margin-bottom: 28px; }}
.section-title {{
    font-size: 11pt;
    font-weight: 600;
    color: {primary_color};
    margin-bottom: 14px;
    padding-left: 14px;
    border-left: 4px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.75;
}}
.skills-flow {{
    font-size: 10pt;
    color: #444;
    line-height: 1.8;
}}
.entry {{ margin-bottom: 22px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 600; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #888; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.6;
}}
'''


# TEMPLATE 41: VERTEX - Sharp, angular design with bold section headers
def _build_vertex_template(resume, primary_color: str) -> str:
    """Vertex template - Sharp, angular design with bold section headers."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_items = []
    if resume.email:
        contact_items.append(f'<span>{_escape(resume.email)}</span>')
    if resume.phone:
        contact_items.append(f'<span>{_escape(resume.phone)}</span>')
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_items.append(f'<span>{_escape(loc)}</span>')
    if resume.linkedin:
        contact_items.append(f'<span>{_escape(resume.linkedin)}</span>')
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title"><span class="title-text">Profile</span></h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Skills</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'vertex')
    employment_html = _build_employment_html(resume.experience, 'vertex')
    
    return f'''
    <header class="header">
        <div class="header-content">
            {photo_section}
            <div class="header-text">
                <h1 class="name">{_escape(resume.full_name)}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
            </div>
        </div>
        <div class="header-contact">{' | '.join(contact_items)}</div>
    </header>
    <div class="body-container">
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
        <aside class="sidebar">
            {skills_html}
        </aside>
    </div>'''


def _get_vertex_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: {primary_color};
    color: #fff;
    padding: 0;
    clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
    padding-bottom: 20px;
}}
.header-content {{
    padding: 30px 40px 10px;
    display: flex;
    align-items: center;
    gap: 22px;
}}
.header-photo {{
    width: 85px;
    height: 85px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 28pt;
    font-weight: 700;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 11pt;
    color: rgba(255,255,255,0.9);
}}
.header-contact {{
    padding: 0 40px 10px;
    font-size: 9pt;
    color: rgba(255,255,255,0.85);
}}
.body-container {{
    display: flex;
    min-height: calc(297mm - 150px);
    margin-top: -10px;
}}
.main-content {{
    flex: 1;
    padding: 28px 35px;
}}
.sidebar {{
    width: 175px;
    background: #f5f5f5;
    padding: 28px 20px;
}}
.sidebar-section {{ margin-bottom: 24px; }}
.sidebar-title {{
    font-size: 10pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    font-size: 9pt;
    color: #444;
    padding: 5px 0;
    border-bottom: 1px solid #e5e5e5;
}}
.skills-list li:last-child {{ border-bottom: none; }}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 12pt;
    font-weight: 700;
    color: #fff;
    background: {primary_color};
    padding: 6px 14px;
    margin-bottom: 14px;
    display: inline-block;
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# =============================================================================
# MINIMAL TEMPLATES (5)
# =============================================================================

# TEMPLATE 42: ZEN - Maximum whitespace with peaceful, focused layout
def _build_zen_template(resume, primary_color: str) -> str:
    """Zen template - Maximum whitespace with peaceful, focused layout."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_parts = []
    if resume.email:
        contact_parts.append(_escape(resume.email))
    if resume.phone:
        contact_parts.append(_escape(resume.phone))
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_parts.append(_escape(loc))
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <p class="summary-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ' · '.join([_escape(s) for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Skills</h2>
            <p class="skills-text">{items}</p>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'zen')
    employment_html = _build_employment_html(resume.experience, 'zen')
    
    return f'''
    <header class="header">
        {photo_section}
        <h1 class="name">{_escape(resume.full_name)}</h1>
        <p class="role">{_escape(resume.role_title or '')}</p>
        <div class="contact">{' — '.join(contact_parts)}</div>
    </header>
    <main class="content">
        {summary_html}
        {education_html}
        {employment_html}
        {skills_html}
    </main>'''


def _get_zen_styles(primary_color: str) -> str:
    return f'''
.header {{
    text-align: center;
    padding: 50px 60px 40px;
}}
.header-photo {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    overflow: hidden;
    margin: 0 auto 20px;
    border: 1px solid #ddd;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 28pt;
    font-weight: 300;
    color: #333;
    letter-spacing: 4px;
    margin-bottom: 10px;
}}
.header .role {{
    font-size: 11pt;
    font-weight: 400;
    color: {primary_color};
    letter-spacing: 2px;
    margin-bottom: 18px;
}}
.header .contact {{
    font-size: 9pt;
    color: #999;
    letter-spacing: 1px;
}}
.content {{
    padding: 35px 60px;
}}
.section {{ margin-bottom: 35px; }}
.section-title {{
    font-size: 9pt;
    font-weight: 500;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 18px;
}}
.summary-text {{
    font-size: 10.5pt;
    color: #555;
    line-height: 1.9;
    text-align: center;
    max-width: 85%;
    margin: 0 auto;
}}
.skills-text {{
    font-size: 10pt;
    color: #666;
    line-height: 1.8;
    text-align: center;
}}
.entry {{ margin-bottom: 25px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
}}
.entry-title {{ font-weight: 500; font-size: 11pt; color: #333; }}
.entry-date {{ font-size: 9pt; color: #aaa; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 10px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 20px;
    list-style-type: none;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #555;
    margin-bottom: 6px;
    line-height: 1.7;
    position: relative;
    padding-left: 12px;
}}
.entry-bullets li::before {{
    content: '–';
    position: absolute;
    left: 0;
    color: #ccc;
}}
'''


# TEMPLATE 43: PURE - Ultra-clean single column with perfect typography
def _build_pure_template(resume, primary_color: str) -> str:
    """Pure template - Ultra-clean single column with perfect typography."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ', '.join([_escape(s) for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Skills</h2>
            <p class="skills-text">{items}</p>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'pure')
    employment_html = _build_employment_html(resume.experience, 'pure')
    
    return f'''
    <header class="header">
        {photo_section}
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{' | '.join(contact_parts)}</div>
        </div>
    </header>
    <main class="content">
        {summary_html}
        {education_html}
        {employment_html}
        {skills_html}
    </main>'''


def _get_pure_styles(primary_color: str) -> str:
    return f'''
.header {{
    padding: 35px 45px;
    display: flex;
    align-items: center;
    gap: 22px;
    border-bottom: 1px solid #e5e5e5;
}}
.header-photo {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    overflow: hidden;
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-info {{ flex: 1; }}
.header .name {{
    font-size: 26pt;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 11pt;
    color: {primary_color};
    margin-bottom: 10px;
}}
.header .contact {{
    font-size: 9pt;
    color: #777;
}}
.content {{ padding: 30px 45px; }}
.section {{ margin-bottom: 28px; }}
.section-title {{
    font-size: 10pt;
    font-weight: 600;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 1px solid #e5e5e5;
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.75;
}}
.skills-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
}}
.entry {{ margin-bottom: 22px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 600; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #888; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.6;
}}
'''


# TEMPLATE 44: ESSENCE - Distilled design focusing on content clarity
def _build_essence_template(resume, primary_color: str) -> str:
    """Essence template - Distilled design focusing on content clarity."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_parts = []
    if resume.email:
        contact_parts.append(_escape(resume.email))
    if resume.phone:
        contact_parts.append(_escape(resume.phone))
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_parts.append(_escape(loc))
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Profile</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<span class="skill">{_escape(s)}</span>' for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Expertise</h2>
            <div class="skills-wrap">{items}</div>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'essence')
    employment_html = _build_employment_html(resume.experience, 'essence')
    
    return f'''
    <header class="header">
        {photo_section}
        <h1 class="name">{_escape(resume.full_name)}</h1>
        <p class="role">{_escape(resume.role_title or '')}</p>
        <div class="divider"></div>
        <div class="contact">{' · '.join(contact_parts)}</div>
    </header>
    <main class="content">
        {summary_html}
        {education_html}
        {employment_html}
        {skills_html}
    </main>'''


def _get_essence_styles(primary_color: str) -> str:
    return f'''
.header {{
    text-align: center;
    padding: 40px 50px 30px;
}}
.header-photo {{
    width: 85px;
    height: 85px;
    border-radius: 50%;
    overflow: hidden;
    margin: 0 auto 16px;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 28pt;
    font-weight: 600;
    color: {primary_color};
    margin-bottom: 6px;
}}
.header .role {{
    font-size: 11pt;
    color: #555;
    margin-bottom: 14px;
}}
.divider {{
    width: 40px;
    height: 2px;
    background: {primary_color};
    margin: 0 auto 14px;
}}
.header .contact {{
    font-size: 9pt;
    color: #888;
}}
.content {{ padding: 28px 50px; }}
.section {{ margin-bottom: 28px; }}
.section-title {{
    font-size: 10pt;
    font-weight: 600;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 14px;
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.75;
}}
.skills-wrap {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}}
.skill {{
    font-size: 9pt;
    color: #555;
    padding: 5px 14px;
    border: 1px solid #ddd;
    border-radius: 3px;
}}
.entry {{ margin-bottom: 22px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 600; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #888; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.6;
}}
'''


# TEMPLATE 45: CANVAS - Blank slate aesthetic with subtle structure
def _build_canvas_template(resume, primary_color: str) -> str:
    """Canvas template - Blank slate aesthetic with subtle structure."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <p class="summary-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ' | '.join([_escape(s) for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Skills</h2>
            <p class="skills-text">{items}</p>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'canvas')
    employment_html = _build_employment_html(resume.experience, 'canvas')
    
    return f'''
    <header class="header">
        <div class="header-left">
            {photo_section}
            <div class="header-text">
                <h1 class="name">{_escape(resume.full_name)}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
            </div>
        </div>
        <div class="header-contact">{' · '.join(contact_parts)}</div>
    </header>
    <main class="content">
        {summary_html}
        {education_html}
        {employment_html}
        {skills_html}
    </main>'''


def _get_canvas_styles(primary_color: str) -> str:
    return f'''
.header {{
    padding: 35px 45px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #eee;
}}
.header-left {{
    display: flex;
    align-items: center;
    gap: 18px;
}}
.header-photo {{
    width: 75px;
    height: 75px;
    border-radius: 50%;
    overflow: hidden;
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 24pt;
    font-weight: 600;
    color: {primary_color};
    margin-bottom: 2px;
}}
.header .role {{
    font-size: 10pt;
    color: #666;
}}
.header-contact {{
    font-size: 9pt;
    color: #888;
    text-align: right;
    max-width: 180px;
}}
.content {{ padding: 30px 45px; }}
.section {{ margin-bottom: 28px; }}
.section-title {{
    font-size: 9pt;
    font-weight: 600;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 12px;
}}
.summary-text {{
    font-size: 10pt;
    color: #555;
    line-height: 1.75;
    border-left: 2px solid {primary_color};
    padding-left: 16px;
}}
.skills-text {{
    font-size: 9.5pt;
    color: #555;
    line-height: 1.7;
}}
.entry {{ margin-bottom: 22px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 600; font-size: 10.5pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #999; }}
.entry-subtitle {{ font-size: 9.5pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #555;
    margin-bottom: 5px;
    line-height: 1.6;
}}
'''


# TEMPLATE 46: WHISPER - Soft, understated elegance with light typography
def _build_whisper_template(resume, primary_color: str) -> str:
    """Whisper template - Soft, understated elegance with light typography."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_parts = []
    if resume.email:
        contact_parts.append(_escape(resume.email))
    if resume.phone:
        contact_parts.append(_escape(resume.phone))
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_parts.append(_escape(loc))
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">About</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Skills</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'whisper')
    employment_html = _build_employment_html(resume.experience, 'whisper')
    
    return f'''
    <header class="header">
        {photo_section}
        <h1 class="name">{_escape(resume.full_name)}</h1>
        <p class="role">{_escape(resume.role_title or '')}</p>
        <div class="contact">{' · '.join(contact_parts)}</div>
    </header>
    <div class="body-container">
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
        <aside class="sidebar">
            {skills_html}
        </aside>
    </div>'''


def _get_whisper_styles(primary_color: str) -> str:
    return f'''
.header {{
    text-align: center;
    padding: 40px 50px 30px;
    background: #fafafa;
}}
.header-photo {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    overflow: hidden;
    margin: 0 auto 16px;
    border: 1px solid #e5e5e5;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 26pt;
    font-weight: 300;
    color: #555;
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
    color: #999;
}}
.body-container {{
    display: flex;
    min-height: calc(297mm - 160px);
}}
.main-content {{
    flex: 1;
    padding: 28px 35px;
}}
.sidebar {{
    width: 165px;
    background: #fafafa;
    padding: 28px 20px;
}}
.sidebar-section {{ margin-bottom: 22px; }}
.sidebar-title {{
    font-size: 9pt;
    font-weight: 500;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    font-size: 9pt;
    color: #666;
    padding: 5px 0;
    border-bottom: 1px solid #eee;
}}
.skills-list li:last-child {{ border-bottom: none; }}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 10pt;
    font-weight: 500;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 14px;
}}
.section-text {{
    font-size: 10pt;
    color: #555;
    line-height: 1.75;
}}
.entry {{ margin-bottom: 22px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 500; font-size: 10.5pt; color: #444; }}
.entry-date {{ font-size: 9pt; color: #aaa; }}
.entry-subtitle {{ font-size: 9.5pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #555;
    margin-bottom: 5px;
    line-height: 1.6;
}}
'''


# =============================================================================
# PROFESSIONAL TEMPLATES (5)
# =============================================================================

# TEMPLATE 47: STERLING - Premium corporate design with refined details
def _build_sterling_template(resume, primary_color: str) -> str:
    """Sterling template - Premium corporate design with refined details."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Professional Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        mid = len(resume.skills) // 2
        col1 = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills[:mid]])
        col2 = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills[mid:]])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Core Competencies</h2>
            <div class="skills-columns">
                <ul class="skills-col">{col1}</ul>
                <ul class="skills-col">{col2}</ul>
            </div>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'sterling')
    employment_html = _build_employment_html(resume.experience, 'sterling')
    
    return f'''
    <header class="header">
        <div class="header-main">
            {photo_section}
            <div class="header-text">
                <h1 class="name">{_escape(resume.full_name)}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
            </div>
        </div>
        <div class="header-contact">{''.join(contact_items)}</div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_sterling_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: #fff;
    padding: 30px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 3px solid {primary_color};
}}
.header-main {{
    display: flex;
    align-items: center;
    gap: 22px;
}}
.header-photo {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid {primary_color};
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 28pt;
    font-weight: 700;
    color: {primary_color};
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 11pt;
    color: #555;
}}
.header-contact {{
    text-align: right;
}}
.contact-item {{
    font-size: 9pt;
    color: #555;
    margin-bottom: 5px;
}}
.content {{ padding: 28px 40px; }}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 11pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
    text-align: justify;
}}
.skills-columns {{
    display: flex;
    gap: 40px;
}}
.skills-col {{
    flex: 1;
    list-style: none;
}}
.skills-col li {{
    font-size: 9.5pt;
    color: #444;
    padding: 5px 0;
    padding-left: 16px;
    position: relative;
    border-bottom: 1px solid #f0f0f0;
}}
.skills-col li::before {{
    content: '▸';
    position: absolute;
    left: 0;
    color: {primary_color};
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# TEMPLATE 48: ANCHOR - Solid, dependable layout for established professionals
def _build_anchor_template(resume, primary_color: str) -> str:
    """Anchor template - Solid, dependable layout for established professionals."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Skills</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'anchor')
    employment_html = _build_employment_html(resume.experience, 'anchor')
    
    return f'''
    <header class="header">
        {photo_section}
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{' | '.join(contact_parts)}</div>
        </div>
    </header>
    <div class="body-container">
        <aside class="sidebar">
            {skills_html}
        </aside>
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
    </div>'''


def _get_anchor_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: {primary_color};
    color: #fff;
    padding: 30px 40px;
    display: flex;
    align-items: center;
    gap: 24px;
}}
.header-photo {{
    width: 95px;
    height: 95px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-info {{ flex: 1; }}
.header .name {{
    font-size: 28pt;
    font-weight: 700;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 12pt;
    color: rgba(255,255,255,0.9);
    margin-bottom: 10px;
}}
.header .contact {{
    font-size: 9pt;
    color: rgba(255,255,255,0.85);
}}
.body-container {{
    display: flex;
    min-height: calc(297mm - 140px);
}}
.sidebar {{
    width: 180px;
    background: #f5f7fa;
    padding: 28px 22px;
    border-right: 3px solid {primary_color};
}}
.main-content {{
    flex: 1;
    padding: 28px 35px;
}}
.sidebar-section {{ margin-bottom: 24px; }}
.sidebar-title {{
    font-size: 10pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    font-size: 9pt;
    color: #444;
    padding: 6px 0;
    border-bottom: 1px solid #e5e5e5;
}}
.skills-list li:last-child {{ border-bottom: none; }}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 12pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
    text-align: justify;
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# TEMPLATE 49: MERIT - Achievement-focused design highlighting accomplishments
def _build_merit_template(resume, primary_color: str) -> str:
    """Merit template - Achievement-focused design highlighting accomplishments."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section highlight-box">
            <h2 class="section-title">Professional Profile</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<span class="skill-badge">{_escape(s)}</span>' for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Key Skills</h2>
            <div class="skills-badges">{items}</div>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'merit')
    employment_html = _build_employment_html(resume.experience, 'merit')
    
    return f'''
    <header class="header">
        {photo_section}
        <div class="header-info">
            <h1 class="name">{_escape(resume.full_name)}</h1>
            <p class="role">{_escape(resume.role_title or '')}</p>
            <div class="contact">{' · '.join(contact_parts)}</div>
        </div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_merit_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: linear-gradient(135deg, {primary_color} 0%, #1a3c34 100%);
    color: #fff;
    padding: 32px 40px;
    display: flex;
    align-items: center;
    gap: 24px;
}}
.header-photo {{
    width: 95px;
    height: 95px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-info {{ flex: 1; }}
.header .name {{
    font-size: 28pt;
    font-weight: 700;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 12pt;
    color: rgba(255,255,255,0.9);
    margin-bottom: 10px;
}}
.header .contact {{
    font-size: 9pt;
    color: rgba(255,255,255,0.85);
}}
.content {{ padding: 28px 40px; }}
.section {{ margin-bottom: 26px; }}
.highlight-box {{
    background: #f8f9fa;
    padding: 20px 24px;
    border-left: 4px solid {primary_color};
}}
.section-title {{
    font-size: 11pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
}}
.skills-badges {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}}
.skill-badge {{
    background: {primary_color};
    color: #fff;
    padding: 5px 14px;
    border-radius: 4px;
    font-size: 9pt;
    font-weight: 500;
}}
.entry {{ margin-bottom: 22px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: none;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
    position: relative;
    padding-left: 14px;
}}
.entry-bullets li::before {{
    content: '✓';
    position: absolute;
    left: 0;
    color: {primary_color};
    font-weight: 700;
}}
'''


# TEMPLATE 50: BEACON - Guiding light design with clear visual hierarchy
def _build_beacon_template(resume, primary_color: str) -> str:
    """Beacon template - Guiding light design with clear visual hierarchy."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
    contact_items = []
    if resume.email:
        contact_items.append(f'<div class="contact-item"><span class="label">Email</span>{_escape(resume.email)}</div>')
    if resume.phone:
        contact_items.append(f'<div class="contact-item"><span class="label">Phone</span>{_escape(resume.phone)}</div>')
    if resume.location or resume.address:
        loc = resume.location or (resume.address.split('\n')[0] if resume.address else '')
        contact_items.append(f'<div class="contact-item"><span class="label">Location</span>{_escape(loc)}</div>')
    if resume.linkedin:
        contact_items.append(f'<div class="contact-item"><span class="label">LinkedIn</span>{_escape(resume.linkedin)}</div>')
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">About</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<li>{_escape(s)}</li>' for s in resume.skills])
        skills_html = f'''<div class="sidebar-section">
            <h3 class="sidebar-title">Expertise</h3>
            <ul class="skills-list">{items}</ul>
        </div>'''
    
    education_html = _build_education_html(resume.education, 'beacon')
    employment_html = _build_employment_html(resume.experience, 'beacon')
    
    return f'''
    <header class="header">
        <div class="header-top">
            {photo_section}
            <div class="header-text">
                <h1 class="name">{_escape(resume.full_name)}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
            </div>
        </div>
        <div class="header-contact">{''.join(contact_items)}</div>
    </header>
    <div class="body-container">
        <main class="main-content">
            {summary_html}
            {education_html}
            {employment_html}
        </main>
        <aside class="sidebar">
            {skills_html}
        </aside>
    </div>'''


def _get_beacon_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: {primary_color};
    color: #fff;
}}
.header-top {{
    padding: 28px 40px 18px;
    display: flex;
    align-items: center;
    gap: 22px;
}}
.header-photo {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header .name {{
    font-size: 28pt;
    font-weight: 700;
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 11pt;
    color: rgba(255,255,255,0.9);
}}
.header-contact {{
    background: rgba(0,0,0,0.1);
    padding: 12px 40px;
    display: flex;
    gap: 30px;
}}
.contact-item {{
    font-size: 9pt;
    color: rgba(255,255,255,0.9);
}}
.contact-item .label {{
    display: block;
    font-size: 7pt;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: rgba(255,255,255,0.6);
    margin-bottom: 2px;
}}
.body-container {{
    display: flex;
    min-height: calc(297mm - 160px);
}}
.main-content {{
    flex: 1;
    padding: 28px 35px;
}}
.sidebar {{
    width: 175px;
    background: #f8f9fa;
    padding: 28px 20px;
}}
.sidebar-section {{ margin-bottom: 24px; }}
.sidebar-title {{
    font-size: 10pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.skills-list {{ list-style: none; }}
.skills-list li {{
    font-size: 9pt;
    color: #444;
    padding: 5px 0;
    border-bottom: 1px solid #e9ecef;
}}
.skills-list li:last-child {{ border-bottom: none; }}
.section {{ margin-bottom: 26px; }}
.section-title {{
    font-size: 11pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.7;
}}
.entry {{ margin-bottom: 20px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}}
.entry-title {{ font-weight: 700; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: disc;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.55;
}}
'''


# TEMPLATE 51: KEYSTONE - Foundational design with strong structural elements
def _build_keystone_template(resume, primary_color: str) -> str:
    """Keystone template - Foundational design with strong structural elements."""
    photo_html = _get_photo_html(resume)
    photo_section = f'<div class="header-photo">{photo_html}</div>' if photo_html else ''
    
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
    
    summary_html = ''
    if resume.summary:
        summary_html = f'''<section class="section">
            <h2 class="section-title">Professional Summary</h2>
            <p class="section-text">{_escape(resume.summary)}</p>
        </section>'''
    
    skills_html = ''
    if resume.skills:
        items = ''.join([f'<span class="skill-block">{_escape(s)}</span>' for s in resume.skills])
        skills_html = f'''<section class="section">
            <h2 class="section-title">Core Competencies</h2>
            <div class="skills-blocks">{items}</div>
        </section>'''
    
    education_html = _build_education_html(resume.education, 'keystone')
    employment_html = _build_employment_html(resume.experience, 'keystone')
    
    return f'''
    <header class="header">
        <div class="header-content">
            {photo_section}
            <div class="header-text">
                <h1 class="name">{_escape(resume.full_name)}</h1>
                <p class="role">{_escape(resume.role_title or '')}</p>
                <div class="contact">{' | '.join(contact_parts)}</div>
            </div>
        </div>
    </header>
    <main class="content">
        {summary_html}
        {skills_html}
        {education_html}
        {employment_html}
    </main>'''


def _get_keystone_styles(primary_color: str) -> str:
    return f'''
.header {{
    background: #fff;
    border-bottom: 6px solid {primary_color};
}}
.header-content {{
    padding: 32px 40px;
    display: flex;
    align-items: center;
    gap: 24px;
}}
.header-photo {{
    width: 95px;
    height: 95px;
    border-radius: 50%;
    overflow: hidden;
    border: 4px solid {primary_color};
    flex-shrink: 0;
}}
.header-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
.header-text {{ flex: 1; }}
.header .name {{
    font-size: 30pt;
    font-weight: 800;
    color: {primary_color};
    margin-bottom: 4px;
}}
.header .role {{
    font-size: 12pt;
    color: #555;
    margin-bottom: 10px;
}}
.header .contact {{
    font-size: 9pt;
    color: #777;
}}
.content {{ padding: 28px 40px; }}
.section {{ margin-bottom: 28px; }}
.section-title {{
    font-size: 12pt;
    font-weight: 800;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 3px solid {primary_color};
}}
.section-text {{
    font-size: 10pt;
    color: #444;
    line-height: 1.75;
    text-align: justify;
}}
.skills-blocks {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}}
.skill-block {{
    background: {primary_color};
    color: #fff;
    padding: 8px 18px;
    font-size: 9pt;
    font-weight: 600;
}}
.entry {{ margin-bottom: 22px; }}
.entry-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
}}
.entry-title {{ font-weight: 800; font-size: 11pt; color: #1a1a1a; }}
.entry-date {{ font-size: 9pt; color: #666; font-weight: 600; }}
.entry-subtitle {{ font-size: 10pt; color: {primary_color}; font-weight: 600; margin-bottom: 8px; }}
.entry-bullets {{
    margin: 0;
    padding-left: 18px;
    list-style-type: square;
}}
.entry-bullets li {{
    font-size: 9.5pt;
    color: #444;
    margin-bottom: 5px;
    line-height: 1.6;
}}
'''
