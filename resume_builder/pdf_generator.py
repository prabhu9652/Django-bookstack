"""
Production-grade PDF Generator for Resume and Cover Letter
Uses WeasyPrint for high-quality, ATS-friendly PDF generation
"""

import io
import base64
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def generate_resume_pdf(resume, request=None) -> bytes:
    """Generate a professional PDF resume using WeasyPrint."""
    from weasyprint import HTML, CSS
    
    html_content = _generate_resume_html(resume)
    css_content = _get_resume_css(resume.primary_color or '#4a9d9a')
    
    html_doc = HTML(string=html_content)
    css_doc = CSS(string=css_content)
    
    pdf_bytes = html_doc.write_pdf(stylesheets=[css_doc])
    return pdf_bytes


def generate_cover_letter_pdf(cover_letter) -> bytes:
    """Generate a professional PDF cover letter using WeasyPrint."""
    from weasyprint import HTML, CSS
    
    html_content = _generate_cover_letter_html(cover_letter)
    css_content = _get_cover_letter_css(cover_letter.primary_color or '#4a9d9a')
    
    html_doc = HTML(string=html_content)
    css_doc = CSS(string=css_content)
    
    pdf_bytes = html_doc.write_pdf(stylesheets=[css_doc])
    return pdf_bytes


def _get_photo_base64(resume) -> Optional[str]:
    """Get profile photo as base64 encoded string."""
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
        img.save(buffer, format='JPEG', quality=95, optimize=True)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    except Exception as e:
        logger.warning(f"Failed to process profile photo: {e}")
        return None


def _escape_html(text: str) -> str:
    """Escape HTML special characters."""
    if not text:
        return ''
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def _format_bullet(text: str) -> str:
    """Format bullet point text, converting **text** to bold."""
    import re
    if not text:
        return ''
    formatted = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    return formatted


def _generate_resume_html(resume) -> str:
    """Generate HTML matching the reference image exactly."""
    primary_color = resume.primary_color or '#4a9d9a'
    
    # Profile photo
    photo_data = _get_photo_base64(resume)
    if photo_data:
        photo_html = f'<img src="data:image/jpeg;base64,{photo_data}" class="photo">'
    else:
        # Gray placeholder circle when no photo
        photo_html = '<div class="photo-placeholder"></div>'
    
    # Contact rows with icons - matching reference exactly
    contact_rows = []
    if resume.email:
        contact_rows.append(f'''<tr>
            <td class="icon-cell">✉</td>
            <td class="text-cell">{_escape_html(resume.email)}</td>
        </tr>''')
    if resume.phone:
        contact_rows.append(f'''<tr>
            <td class="icon-cell">✆</td>
            <td class="text-cell">{_escape_html(resume.phone)}</td>
        </tr>''')
    if resume.address:
        contact_rows.append(f'''<tr>
            <td class="icon-cell">⌂</td>
            <td class="text-cell">{_escape_html(resume.address)}</td>
        </tr>''')
    if resume.linkedin:
        contact_rows.append(f'''<tr>
            <td class="icon-cell">in</td>
            <td class="text-cell">{_escape_html(resume.linkedin)}</td>
        </tr>''')
    if resume.github:
        contact_rows.append(f'''<tr>
            <td class="icon-cell">⌘</td>
            <td class="text-cell">{_escape_html(resume.github)}</td>
        </tr>''')
    contact_html = '\n'.join(contact_rows)
    
    # Skills list - simple vertical list
    skills_html = ''
    if resume.skills:
        for skill in resume.skills:
            skills_html += f'<div class="skill-item">{_escape_html(skill)}</div>\n'
    
    # Languages section
    languages_section = ''
    if resume.languages and len(resume.languages) > 0:
        langs = ''
        for lang in resume.languages:
            langs += f'<div class="skill-item">{_escape_html(lang)}</div>\n'
        languages_section = f'''
            <div class="sidebar-section">
                <h3 class="sidebar-heading">LANGUAGES</h3>
                {langs}
            </div>
        '''
    
    # Education section
    education_section = ''
    if resume.education and len(resume.education) > 0:
        edus = ''
        for edu in resume.education:
            degree = _escape_html(edu.get('degree', ''))
            field = _escape_html(edu.get('field', ''))
            school = _escape_html(edu.get('school', ''))
            year = _escape_html(edu.get('graduation_date', ''))
            
            edus += f'''
                <div class="edu-entry">
                    <div class="edu-degree">{degree}</div>
                    {'<div class="edu-field">' + field + '</div>' if field else ''}
                    <div class="edu-school">{school}</div>
                    <div class="edu-year">{year}</div>
                </div>
            '''
        education_section = f'''
            <div class="sidebar-section">
                <h3 class="sidebar-heading">EDUCATION</h3>
                {edus}
            </div>
        '''
    
    # Profile/Summary section
    profile_section = ''
    if resume.summary:
        profile_section = f'''
            <div class="content-section">
                <div class="section-label-wrapper">
                    <span class="section-label">PROFILE</span>
                </div>
                <p class="profile-text">{_escape_html(resume.summary)}</p>
            </div>
        '''
    
    # Employment section
    employment_section = ''
    if resume.experience:
        entries = ''
        for exp in resume.experience:
            role = _escape_html(exp.get('role', ''))
            company = _escape_html(exp.get('company', ''))
            start = _escape_html(exp.get('start_date', ''))
            end = _escape_html(exp.get('end_date', ''))
            date_str = f"{start} - {end}" if start else end
            
            bullets = ''
            if exp.get('bullets'):
                items = ''
                for b in exp['bullets']:
                    items += f'<li>{_format_bullet(b)}</li>\n'
                bullets = f'<ul class="job-bullets">{items}</ul>'
            
            entries += f'''
                <div class="job-entry">
                    <table class="job-header-table">
                        <tr>
                            <td class="job-role">{role}</td>
                            <td class="job-date">{date_str}</td>
                        </tr>
                    </table>
                    <div class="job-company">{company}</div>
                    {bullets}
                </div>
            '''
        
        employment_section = f'''
            <div class="content-section">
                <div class="section-label-wrapper">
                    <span class="section-label">EMPLOYMENT</span>
                </div>
                {entries}
            </div>
        '''

    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape_html(resume.full_name)} - Resume</title>
</head>
<body>
    <div class="page">
        <!-- HEADER -->
        <div class="header">
            <table class="header-table">
                <tr>
                    <td class="photo-cell">
                        {photo_html}
                    </td>
                    <td class="info-cell">
                        <div class="name">{_escape_html(resume.full_name).upper()}</div>
                        <div class="role-title">{_escape_html(resume.role_title or '')}</div>
                        <table class="contact-table">
                            {contact_html}
                        </table>
                    </td>
                </tr>
            </table>
        </div>
        
        <!-- BODY -->
        <table class="body-table">
            <tr>
                <!-- SIDEBAR -->
                <td class="sidebar">
                    <div class="sidebar-section">
                        <h3 class="sidebar-heading">SKILLS</h3>
                        {skills_html}
                    </div>
                    {languages_section}
                    {education_section}
                </td>
                
                <!-- MAIN CONTENT -->
                <td class="main-content">
                    {profile_section}
                    {employment_section}
                </td>
            </tr>
        </table>
    </div>
</body>
</html>'''


def _get_resume_css(primary_color: str) -> str:
    """CSS matching the reference image exactly."""
    
    return f'''
@page {{
    size: A4;
    margin: 0;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.4;
    color: #333333;
}}

.page {{
    width: 210mm;
    min-height: 297mm;
}}

/* ==================== HEADER ==================== */
.header {{
    background-color: {primary_color};
    padding: 15mm 12mm 12mm 15mm;
}}

.header-table {{
    width: 100%;
    border-collapse: collapse;
}}

.header-table td {{
    vertical-align: middle;
    border: none;
}}

.photo-cell {{
    width: 35mm;
    padding-right: 12mm;
}}

.photo {{
    width: 32mm;
    height: 32mm;
    border-radius: 50%;
    object-fit: cover;
    border: 2.5px solid rgba(255, 255, 255, 0.3);
    display: block;
}}

.photo-placeholder {{
    width: 32mm;
    height: 32mm;
    border-radius: 50%;
    background-color: #5fb3b0;
    border: 2.5px solid rgba(255, 255, 255, 0.3);
}}

.info-cell {{
    color: #ffffff;
}}

.name {{
    font-size: 26pt;
    font-weight: 700;
    letter-spacing: 2.5pt;
    margin-bottom: 2mm;
    color: #ffffff;
}}

.role-title {{
    font-size: 12pt;
    font-weight: 400;
    color: #ffffff;
    margin-bottom: 5mm;
}}

.contact-table {{
    border-collapse: collapse;
}}

.contact-table td {{
    border: none;
    padding: 1mm 0;
    color: #ffffff;
    font-size: 9pt;
    vertical-align: top;
    line-height: 1.35;
}}

.icon-cell {{
    width: 5mm;
    padding-right: 2mm;
}}

.text-cell {{
    color: #ffffff;
}}

/* ==================== BODY ==================== */
.body-table {{
    width: 100%;
    border-collapse: collapse;
}}

.body-table > tr > td {{
    vertical-align: top;
    border: none;
}}

/* ==================== SIDEBAR ==================== */
.sidebar {{
    width: 52mm;
    background-color: #f7f7f7;
    padding: 10mm 8mm 15mm 10mm;
}}

.sidebar-section {{
    margin-bottom: 8mm;
}}

.sidebar-heading {{
    font-size: 10.5pt;
    font-weight: 600;
    color: {primary_color};
    letter-spacing: 1.2pt;
    margin-bottom: 4mm;
    text-transform: uppercase;
}}

.skill-item {{
    font-size: 9.5pt;
    color: #333333;
    padding: 1.2mm 0;
    line-height: 1.4;
}}

.edu-entry {{
    margin-bottom: 6mm;
}}

.edu-degree {{
    font-size: 9.5pt;
    font-weight: 600;
    color: {primary_color};
    margin-bottom: 1mm;
}}

.edu-field {{
    font-size: 9pt;
    font-weight: 400;
    color: #333333;
    margin-bottom: 0.5mm;
}}

.edu-school {{
    font-size: 9pt;
    font-weight: 400;
    font-style: normal;
    color: #555555;
    margin-bottom: 0.5mm;
}}

.edu-year {{
    font-size: 9pt;
    font-weight: 400;
    color: #666666;
}}

/* ==================== MAIN CONTENT ==================== */
.main-content {{
    padding: 10mm 15mm 15mm 12mm;
    background-color: #ffffff;
}}

.content-section {{
    margin-bottom: 8mm;
}}

.section-label-wrapper {{
    margin-bottom: 4mm;
}}

.section-label {{
    display: inline-block;
    background-color: {primary_color};
    color: #ffffff;
    font-size: 10pt;
    font-weight: 600;
    letter-spacing: 1.2pt;
    padding: 2mm 4mm;
    text-transform: uppercase;
}}

.profile-text {{
    font-size: 10pt;
    color: #333333;
    line-height: 1.55;
    text-align: justify;
}}

/* ==================== EMPLOYMENT ==================== */
.job-entry {{
    margin-bottom: 6mm;
    page-break-inside: avoid;
}}

.job-header-table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1mm;
}}

.job-header-table td {{
    border: none;
    padding: 0;
    vertical-align: baseline;
}}

.job-role {{
    font-size: 10.5pt;
    font-weight: 700;
    color: #333333;
}}

.job-date {{
    font-size: 9pt;
    color: #555555;
    text-align: right;
}}

.job-company {{
    font-size: 9.5pt;
    color: #555555;
    margin-bottom: 2mm;
}}

.job-bullets {{
    margin: 0;
    padding-left: 5mm;
    list-style-type: disc;
}}

.job-bullets li {{
    font-size: 9.5pt;
    color: #333333;
    margin-bottom: 2mm;
    line-height: 1.5;
    text-align: justify;
}}

.job-bullets li strong {{
    font-weight: 700;
    color: #222222;
}}
'''


def _generate_cover_letter_html(cover_letter) -> str:
    """Generate professional HTML for cover letter."""
    from datetime import date
    
    today = date.today().strftime("%B %d, %Y")
    primary_color = cover_letter.primary_color or '#4a9d9a'
    
    # Contact info
    contact_parts = []
    if cover_letter.email:
        contact_parts.append(_escape_html(cover_letter.email))
    if cover_letter.phone:
        contact_parts.append(_escape_html(cover_letter.phone))
    if hasattr(cover_letter, 'linkedin') and cover_letter.linkedin:
        contact_parts.append(_escape_html(cover_letter.linkedin))
    contact_html = ' &nbsp;|&nbsp; '.join(contact_parts)
    
    # Address
    address_html = f'<div class="sender-address">{_escape_html(cover_letter.address)}</div>' if cover_letter.address else ''
    
    # Recipient info
    recipient_lines = []
    if cover_letter.hiring_manager:
        recipient_lines.append(f'<div class="recipient-name">{_escape_html(cover_letter.hiring_manager)}</div>')
    recipient_lines.append(f'<div class="company-name">{_escape_html(cover_letter.company_name)}</div>')
    if hasattr(cover_letter, 'company_address') and cover_letter.company_address:
        recipient_lines.append(f'<div class="company-address">{_escape_html(cover_letter.company_address)}</div>')
    recipient_html = '\n'.join(recipient_lines)
    
    # Build body content
    body_paragraphs = []
    
    # Opening paragraph
    if cover_letter.opening_paragraph:
        opening = cover_letter.opening_paragraph.strip()
        if opening and not opening.lower().startswith('dear'):
            body_paragraphs.append(f'<p>{_escape_html(opening)}</p>')
    
    # Body paragraph(s) - handle bullet points properly
    if cover_letter.body_paragraph:
        body_text = cover_letter.body_paragraph.strip()
        sections = body_text.split('\n\n')
        
        for section in sections:
            section = section.strip()
            if not section or section.lower().startswith('dear') or section.lower().startswith('sincerely'):
                continue
            
            # Check if this section contains bullet points
            lines = section.split('\n')
            has_bullets = any(line.strip().startswith('•') or line.strip().startswith('- ') for line in lines)
            
            if has_bullets:
                # Process as mixed content (intro text + bullets)
                intro_text = []
                bullet_items = []
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('•') or line.startswith('- '):
                        bullet_items.append(line.lstrip('•- ').strip())
                    elif bullet_items and line:
                        # Continuation of previous bullet
                        bullet_items[-1] += ' ' + line
                    elif line:
                        intro_text.append(line)
                
                # Add intro text as paragraph
                if intro_text:
                    body_paragraphs.append(f'<p>{_escape_html(" ".join(intro_text))}</p>')
                
                # Add bullets as list
                if bullet_items:
                    items_html = '\n'.join([f'<li>{_escape_html(item)}</li>' for item in bullet_items])
                    body_paragraphs.append(f'<ul class="achievements">{items_html}</ul>')
            else:
                # Regular paragraph
                body_paragraphs.append(f'<p>{_escape_html(section)}</p>')
    
    # Closing paragraph
    if cover_letter.closing_paragraph:
        closing = cover_letter.closing_paragraph.strip()
        # Split by double newlines
        closing_parts = closing.split('\n\n')
        for part in closing_parts:
            part = part.strip()
            if part and not part.lower().startswith('sincerely'):
                body_paragraphs.append(f'<p>{_escape_html(part)}</p>')
    
    # Fallback to content field
    if not body_paragraphs and hasattr(cover_letter, 'content') and cover_letter.content:
        content = cover_letter.content.strip()
        lines = [l for l in content.split('\n') if l.strip() and not l.strip().lower().startswith(('dear', 'sincerely', '[your'))]
        if lines:
            body_paragraphs.append(f'<p>{_escape_html(" ".join(lines))}</p>')
    
    body_html = '\n'.join(body_paragraphs)
    manager = _escape_html(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape_html(cover_letter.full_name)} - Cover Letter</title>
</head>
<body>
    <div class="page">
        <!-- Header -->
        <div class="header">
            <h1 class="name">{_escape_html(cover_letter.full_name)}</h1>
            <div class="contact-info">{contact_html}</div>
            {address_html}
        </div>
        
        <!-- Letter Content -->
        <div class="content">
            <div class="date">{today}</div>
            
            <div class="recipient">
                {recipient_html}
            </div>
            
            <div class="subject">
                <strong>Re: Application for {_escape_html(cover_letter.position_title)}</strong>
            </div>
            
            <div class="salutation">Dear {manager},</div>
            
            <div class="body">
                {body_html}
            </div>
            
            <div class="closing">
                <p class="closing-text">Sincerely,</p>
                <p class="signature">{_escape_html(cover_letter.full_name)}</p>
            </div>
        </div>
    </div>
</body>
</html>'''


def _get_cover_letter_css(primary_color: str) -> str:
    """CSS for professional cover letter."""
    
    return f'''
@page {{
    size: A4;
    margin: 20mm 25mm 20mm 25mm;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333333;
}}

.page {{
    max-width: 100%;
}}

/* Header */
.header {{
    text-align: center;
    padding-bottom: 15px;
    margin-bottom: 25px;
    border-bottom: 2px solid {primary_color};
}}

.name {{
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 24pt;
    font-weight: 700;
    color: {primary_color};
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}}

.contact-info {{
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 10pt;
    color: #555555;
    margin-bottom: 4px;
}}

.sender-address {{
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 10pt;
    color: #666666;
}}

/* Content */
.content {{
    line-height: 1.65;
}}

.date {{
    margin-bottom: 20px;
    color: #333333;
}}

.recipient {{
    margin-bottom: 20px;
}}

.recipient-name {{
    font-weight: 600;
    color: #333333;
}}

.company-name {{
    color: #333333;
}}

.company-address {{
    color: #666666;
    font-size: 10.5pt;
}}

.subject {{
    margin-bottom: 20px;
    color: #333333;
}}

.salutation {{
    margin-bottom: 15px;
    color: #333333;
}}

/* Body */
.body {{
    margin-bottom: 20px;
}}

.body p {{
    margin-bottom: 12px;
    text-align: justify;
    color: #333333;
}}

.body .achievements {{
    margin: 12px 0 12px 25px;
    padding: 0;
    list-style-type: disc;
}}

.body .achievements li {{
    margin-bottom: 8px;
    text-align: justify;
    color: #333333;
    padding-left: 5px;
}}

/* Closing */
.closing {{
    margin-top: 25px;
}}

.closing-text {{
    margin-bottom: 25px;
    color: #333333;
}}

.signature {{
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-weight: 600;
    font-size: 12pt;
    color: {primary_color};
}}
'''
