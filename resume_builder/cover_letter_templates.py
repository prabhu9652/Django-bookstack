"""
Cover Letter Templates - 37 Additional Premium Templates
=========================================================

This module contains builder functions for 37 new cover letter templates.
Each template generates unique HTML with distinct visual styling.
"""

import html


def _escape(text):
    """Escape HTML special characters."""
    if text is None:
        return ''
    return html.escape(str(text))


def _build_cover_letter_body_html(cover_letter) -> str:
    """Build cover letter body paragraphs."""
    paragraphs = []
    
    if cover_letter.opening_paragraph:
        text = cover_letter.opening_paragraph.strip()
        if text and not text.lower().startswith('dear'):
            paragraphs.append(f'<p>{_escape(text)}</p>')
    
    if cover_letter.body_paragraph:
        text = cover_letter.body_paragraph.strip()
        for para in text.split('\n\n'):
            para = para.strip()
            if para and not para.lower().startswith(('dear', 'sincerely')):
                formatted = _escape(para).replace('\n', '<br>')
                paragraphs.append(f'<p>{formatted}</p>')
    
    if cover_letter.closing_paragraph:
        text = cover_letter.closing_paragraph.strip()
        if text and not text.lower().startswith('sincerely'):
            paragraphs.append(f'<p>{_escape(text)}</p>')
    
    return '\n'.join(paragraphs)


def _get_cl_base_styles():
    """Base styles shared by all cover letter templates."""
    return '''
        @page { size: A4; margin: 0; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #1a1a1a;
        }
        .letter-paper {
            width: 210mm;
            min-height: 297mm;
            background: #fff;
        }
    '''


def _cl_contact_parts(cover_letter):
    """Build contact parts for cover letter header."""
    parts = []
    if cover_letter.email:
        parts.append(f'<span>{_escape(cover_letter.email)}</span>')
    if cover_letter.phone:
        parts.append(f'<span>{_escape(cover_letter.phone)}</span>')
    if cover_letter.linkedin:
        parts.append(f'<span>{_escape(cover_letter.linkedin)}</span>')
    return parts


def _cl_recipient_html(cover_letter):
    """Build recipient section HTML."""
    recipient_name = f'<div class="recipient-name">{_escape(cover_letter.hiring_manager)}</div>' if cover_letter.hiring_manager else ''
    company_address = ''
    if hasattr(cover_letter, 'company_address') and cover_letter.company_address:
        company_address = f'<div class="company-address">{_escape(cover_letter.company_address)}</div>'
    return recipient_name, company_address


# =============================================================================
# FORMAL TEMPLATES (10)
# =============================================================================

def _build_executive_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Executive - Commanding presence with refined typography."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 45px 55px 25px;
            border-bottom: 4px solid {primary_color};
        }}
        .sender-name {{
            font-size: 28pt;
            font-weight: 700;
            color: {primary_color};
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 12px;
        }}
        .sender-contact {{
            display: flex;
            gap: 25px;
            font-size: 10pt;
            color: #555;
        }}
        .letter-body {{
            padding: 35px 55px 50px;
        }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 25px; }}
        .recipient {{ margin-bottom: 25px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 25px;
            font-size: 12pt;
            font-weight: 600;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 18px; font-size: 11pt; }}
        .content p {{ margin: 0 0 16px 0; text-align: justify; }}
        .closing {{ margin-top: 35px; }}
        .closing p {{ margin: 0 0 10px 0; }}
        .signature {{
            font-weight: 700;
            font-size: 13pt;
            color: {primary_color};
            letter-spacing: 1px;
        }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Re: Application for {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Respectfully,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_diplomat_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Diplomat - Elegant formal style for senior positions."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            text-align: center;
            padding: 40px 50px 30px;
            border-bottom: 2px solid #d4af37;
        }}
        .sender-name {{
            font-family: 'Georgia', serif;
            font-size: 26pt;
            font-weight: 400;
            color: {primary_color};
            letter-spacing: 3px;
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            justify-content: center;
            gap: 20px;
            font-size: 10pt;
            color: #666;
        }}
        .letter-body {{
            padding: 30px 60px 50px;
            font-family: 'Georgia', serif;
        }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 25px; text-align: right; }}
        .recipient {{ margin-bottom: 25px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 25px;
            font-size: 11pt;
            font-style: italic;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 18px; font-size: 11pt; }}
        .content p {{ margin: 0 0 16px 0; text-align: justify; line-height: 1.7; }}
        .closing {{ margin-top: 35px; }}
        .closing p {{ margin: 0 0 10px 0; font-style: italic; }}
        .signature {{
            font-family: 'Georgia', serif;
            font-size: 13pt;
            color: {primary_color};
        }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Re: {_escape(cover_letter.position_title)} Position</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>With warm regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_chancellor_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Chancellor - Traditional serif typography with classic appeal."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        body {{ font-family: 'Times New Roman', Georgia, serif; }}
        .header {{
            padding: 40px 50px 25px;
            border-bottom: 1px solid {primary_color};
        }}
        .sender-name {{
            font-size: 24pt;
            font-weight: 400;
            color: #1a1a1a;
            margin-bottom: 8px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: #555;
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #444; margin-bottom: 25px; }}
        .recipient {{ margin-bottom: 25px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 25px;
            font-size: 11pt;
            border-left: 3px solid {primary_color};
            padding-left: 12px;
        }}
        .salutation {{ margin-bottom: 18px; font-size: 11pt; }}
        .content p {{ margin: 0 0 16px 0; text-align: justify; line-height: 1.7; }}
        .closing {{ margin-top: 35px; }}
        .closing p {{ margin: 0 0 10px 0; }}
        .signature {{ font-size: 12pt; color: #1a1a1a; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject"><strong>Subject:</strong> Application for {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Yours faithfully,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_statesman_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Statesman - Distinguished formal layout for leadership roles."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            background: {primary_color};
            color: #fff;
            padding: 35px 50px;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 600;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: rgba(255,255,255,0.9);
        }}
        .letter-body {{ padding: 35px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 25px; }}
        .recipient {{ margin-bottom: 25px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 25px;
            font-size: 11pt;
            font-weight: 600;
            color: {primary_color};
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .salutation {{ margin-bottom: 18px; font-size: 11pt; }}
        .content p {{ margin: 0 0 16px 0; text-align: justify; }}
        .closing {{ margin-top: 35px; }}
        .closing p {{ margin: 0 0 10px 0; }}
        .signature {{ font-weight: 600; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">RE: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Respectfully yours,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_cl_regent_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Regent - Regal formal design with refined spacing."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 45px 55px 30px;
            border-bottom: 3px double {primary_color};
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 500;
            color: {primary_color};
            margin-bottom: 12px;
        }}
        .sender-contact {{
            display: flex;
            gap: 25px;
            font-size: 10pt;
            color: #555;
        }}
        .letter-body {{ padding: 35px 55px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 28px; }}
        .recipient {{ margin-bottom: 28px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 25px;
            font-size: 11pt;
            padding: 10px 0;
            border-top: 1px solid #e5e7eb;
            border-bottom: 1px solid #e5e7eb;
        }}
        .salutation {{ margin-bottom: 18px; font-size: 11pt; }}
        .content p {{ margin: 0 0 16px 0; text-align: justify; line-height: 1.7; }}
        .closing {{ margin-top: 38px; }}
        .closing p {{ margin: 0 0 12px 0; }}
        .signature {{ font-size: 13pt; color: {primary_color}; font-weight: 500; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject"><strong>Re:</strong> {_escape(cover_letter.position_title)} Application</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>With sincere regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_sovereign_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Sovereign - Premium formal template with bold header."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            background: linear-gradient(135deg, {primary_color} 0%, #1a1a1a 100%);
            color: #fff;
            padding: 40px 50px;
        }}
        .sender-name {{
            font-size: 28pt;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 12px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: rgba(255,255,255,0.85);
        }}
        .letter-body {{ padding: 35px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 25px; }}
        .recipient {{ margin-bottom: 25px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 25px;
            font-size: 12pt;
            font-weight: 700;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 18px; font-size: 11pt; }}
        .content p {{ margin: 0 0 16px 0; text-align: justify; }}
        .closing {{ margin-top: 35px; }}
        .closing p {{ margin: 0 0 10px 0; }}
        .signature {{ font-weight: 700; font-size: 13pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Application: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Most sincerely,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_ambassador_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Ambassador - Diplomatic formal style with elegant borders."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .letter-paper {{
            border: 2px solid {primary_color};
            margin: 10mm;
            width: calc(210mm - 20mm);
            min-height: calc(297mm - 20mm);
        }}
        .header {{
            padding: 35px 45px 25px;
            border-bottom: 1px solid #e5e7eb;
        }}
        .sender-name {{
            font-size: 24pt;
            font-weight: 500;
            color: {primary_color};
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: #555;
        }}
        .letter-body {{ padding: 30px 45px 45px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 25px; }}
        .recipient {{ margin-bottom: 25px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 25px;
            font-size: 11pt;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 18px; font-size: 11pt; }}
        .content p {{ margin: 0 0 16px 0; text-align: justify; }}
        .closing {{ margin-top: 35px; }}
        .closing p {{ margin: 0 0 10px 0; }}
        .signature {{ font-size: 12pt; color: {primary_color}; font-weight: 500; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject"><em>Re: {_escape(cover_letter.position_title)}</em></div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Cordially,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


# =============================================================================
# PROFESSIONAL TEMPLATES (10)
# =============================================================================

def _build_corporate_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Corporate - Clean corporate style for business professionals."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 25px;
            background: #f8f9fa;
            border-bottom: 3px solid {primary_color};
        }}
        .sender-name {{
            font-size: 24pt;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 8px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: #555;
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            font-weight: 600;
            padding-bottom: 10px;
            border-bottom: 1px solid #e5e7eb;
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 600; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Re: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_enterprise_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Enterprise - Enterprise-grade professional design."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            padding: 35px 50px 25px;
            border-bottom: 2px solid {primary_color};
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 700;
            color: {primary_color};
            margin-bottom: 8px;
        }}
        .sender-contact {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            font-size: 9pt;
            color: #555;
            text-align: right;
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            background: #f8f9fa;
            padding: 10px 15px;
            border-left: 4px solid {primary_color};
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 700; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div>
                <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            </div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject"><strong>Subject:</strong> Application for {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Kind regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_cl_sterling_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Sterling - Premium professional with refined details."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 40px 55px 28px;
            border-bottom: 1px solid #d1d5db;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 300;
            color: #1a1a1a;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 25px;
            font-size: 10pt;
            color: {primary_color};
        }}
        .letter-body {{ padding: 32px 55px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 24px; }}
        .recipient {{ margin-bottom: 24px; }}
        .recipient-name {{ font-weight: 500; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 24px;
            font-size: 11pt;
            color: {primary_color};
            font-weight: 500;
        }}
        .salutation {{ margin-bottom: 18px; font-size: 11pt; }}
        .content p {{ margin: 0 0 15px 0; text-align: justify; line-height: 1.7; }}
        .closing {{ margin-top: 32px; }}
        .closing p {{ margin: 0 0 10px 0; }}
        .signature {{ font-size: 12pt; color: #1a1a1a; font-weight: 500; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Re: {_escape(cover_letter.position_title)}</div>
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


def _build_cl_pinnacle_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Pinnacle - Top-tier professional layout."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            background: {primary_color};
            color: #fff;
            padding: 38px 50px;
            text-align: center;
        }}
        .sender-name {{
            font-size: 28pt;
            font-weight: 600;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 12px;
        }}
        .sender-contact {{
            display: flex;
            justify-content: center;
            gap: 25px;
            font-size: 10pt;
            color: rgba(255,255,255,0.9);
        }}
        .letter-body {{ padding: 35px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 25px; }}
        .recipient {{ margin-bottom: 25px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 25px;
            font-size: 11pt;
            font-weight: 600;
            color: {primary_color};
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .salutation {{ margin-bottom: 18px; font-size: 11pt; }}
        .content p {{ margin: 0 0 15px 0; text-align: justify; }}
        .closing {{ margin-top: 35px; }}
        .closing p {{ margin: 0 0 10px 0; }}
        .signature {{ font-weight: 600; font-size: 13pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">RE: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_cl_summit_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Summit - Peak professional design."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 40px 50px 30px;
            border-left: 6px solid {primary_color};
            background: linear-gradient(90deg, #f8f9fa 0%, #fff 100%);
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 700;
            color: {primary_color};
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: #555;
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 24px; }}
        .recipient {{ margin-bottom: 24px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 24px;
            font-size: 11pt;
            font-weight: 600;
        }}
        .salutation {{ margin-bottom: 18px; font-size: 11pt; }}
        .content p {{ margin: 0 0 15px 0; text-align: justify; }}
        .closing {{ margin-top: 32px; }}
        .closing p {{ margin: 0 0 10px 0; }}
        .signature {{ font-weight: 700; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Application for {_escape(cover_letter.position_title)}</div>
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


def _build_cl_keystone_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Keystone - Foundational professional structure."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 25px;
            border-bottom: 5px solid {primary_color};
        }}
        .sender-name {{
            font-size: 28pt;
            font-weight: 800;
            color: {primary_color};
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: #555;
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 700; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            font-weight: 700;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 800; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">RE: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_cl_anchor_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Anchor - Solid dependable professional layout."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 28px;
            background: #1a365d;
            color: #fff;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: rgba(255,255,255,0.85);
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            font-weight: 600;
            color: #1a365d;
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 600; font-size: 12pt; color: #1a365d; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Application: {_escape(cover_letter.position_title)}</div>
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


# =============================================================================
# MODERN TEMPLATES (10)
# =============================================================================

def _build_cl_streamline_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Streamline - Flowing modern layout with smooth transitions."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 25px;
            border-bottom: 2px solid {primary_color};
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 300;
            color: {primary_color};
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: #666;
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #888; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 500; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #444; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; line-height: 1.7; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 500; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Re: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_cl_metro_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Metro - Urban modern style with accent sidebar."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .letter-paper {{
            display: flex;
        }}
        .sidebar {{
            width: 8px;
            background: {primary_color};
        }}
        .main {{
            flex: 1;
        }}
        .header {{
            padding: 35px 45px 25px;
            border-bottom: 1px solid #e5e7eb;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 600;
            color: {primary_color};
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: #555;
        }}
        .letter-body {{ padding: 28px 45px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            font-weight: 600;
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 600; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <div class="sidebar"></div>
        <div class="main">
            <header class="header">
                <div class="sender-name">{_escape(cover_letter.full_name)}</div>
                <div class="sender-contact">{''.join(contact_parts)}</div>
            </header>
            <div class="letter-body">
                <div class="date">{today}</div>
                <div class="recipient">
                    {recipient_name}
                    <div class="company-name">{_escape(cover_letter.company_name)}</div>
                    {company_address}
                </div>
                <div class="subject">Re: {_escape(cover_letter.position_title)}</div>
                <div class="salutation">Dear {manager},</div>
                <div class="content">{body_html}</div>
                <div class="closing">
                    <p>Best regards,</p>
                    <div class="signature">{_escape(cover_letter.full_name)}</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_cl_nordic_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Nordic - Scandinavian minimalism with generous whitespace."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 50px 60px 35px;
        }}
        .sender-name {{
            font-size: 24pt;
            font-weight: 300;
            color: #333;
            letter-spacing: 2px;
            margin-bottom: 15px;
        }}
        .sender-contact {{
            display: flex;
            gap: 25px;
            font-size: 9pt;
            color: #888;
        }}
        .letter-body {{ padding: 25px 60px 60px; }}
        .date {{ font-size: 9pt; color: #999; margin-bottom: 30px; }}
        .recipient {{ margin-bottom: 30px; }}
        .recipient-name {{ font-weight: 400; font-size: 10pt; color: #555; }}
        .company-name {{ font-size: 10pt; color: #555; }}
        .subject {{
            margin-bottom: 30px;
            font-size: 10pt;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 20px; font-size: 10pt; color: #444; }}
        .content p {{ margin: 0 0 18px 0; text-align: left; line-height: 1.8; font-size: 10pt; color: #444; }}
        .closing {{ margin-top: 40px; }}
        .closing p {{ margin: 0 0 12px 0; font-size: 10pt; color: #444; }}
        .signature {{ font-size: 11pt; color: #333; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">{_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Kind regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_cl_slate_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Slate - Dark header with sophisticated typography."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            background: #334155;
            color: #fff;
            padding: 35px 50px;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 500;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: rgba(255,255,255,0.8);
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            font-weight: 500;
            color: #334155;
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 500; font-size: 12pt; color: #334155; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Re: {_escape(cover_letter.position_title)}</div>
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


def _build_prism_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Prism - Light and airy with subtle color accents."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 40px 50px 30px;
            background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(255,255,255,0) 100%);
            border-bottom: 1px solid #e5e7eb;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 600;
            color: {primary_color};
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: #666;
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #888; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 500; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #444; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; line-height: 1.7; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 600; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Re: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_nova_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Nova - Fresh contemporary with dynamic spacing."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 28px;
            border-bottom: 3px solid {primary_color};
        }}
        .sender-name {{
            font-size: 28pt;
            font-weight: 700;
            color: {primary_color};
            margin-bottom: 8px;
        }}
        .sender-contact {{
            display: flex;
            gap: 18px;
            font-size: 10pt;
            color: #555;
        }}
        .letter-body {{ padding: 28px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 20px; }}
        .recipient {{ margin-bottom: 20px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 20px;
            font-size: 12pt;
            font-weight: 600;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 28px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 700; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">{_escape(cover_letter.position_title)} Application</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Cheers,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_pulse_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Pulse - Energetic modern with gradient accent."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 28px;
            background: linear-gradient(90deg, {primary_color} 0%, #ff6b6b 100%);
            color: #fff;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: rgba(255,255,255,0.9);
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            font-weight: 600;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 600; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Re: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_flux_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Flux - Flowing design with rounded corners."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 28px;
            background: {primary_color};
            color: #fff;
            border-radius: 0 0 20px 20px;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 500;
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: rgba(255,255,255,0.85);
        }}
        .letter-body {{ padding: 35px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 500; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            color: {primary_color};
            font-weight: 500;
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; line-height: 1.7; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 500; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Application: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Warm regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_vertex_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Vertex - Sharp angular modern design."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 28px;
            background: {primary_color};
            color: #fff;
            clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
            padding-bottom: 45px;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: rgba(255,255,255,0.9);
        }}
        .letter-body {{ padding: 25px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            font-weight: 700;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 700; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">RE: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_circuit_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Circuit - Tech-inspired modern with monospace accents."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 28px;
            border-bottom: 2px solid {primary_color};
            background: #f8f9fa;
        }}
        .sender-name {{
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 24pt;
            font-weight: 600;
            color: {primary_color};
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-family: 'Consolas', monospace;
            font-size: 9pt;
            color: #555;
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; font-family: 'Consolas', monospace; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            font-family: 'Consolas', monospace;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-family: 'Consolas', monospace; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">// {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_matrix_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Matrix - Grid-based modern structure."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            display: grid;
            grid-template-columns: 1fr auto;
            padding: 35px 50px 28px;
            border-bottom: 3px solid {primary_color};
            align-items: end;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 700;
            color: {primary_color};
            margin-bottom: 0;
        }}
        .sender-contact {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            font-size: 9pt;
            color: #555;
            text-align: right;
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            font-weight: 600;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 700; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Application: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


# =============================================================================
# CREATIVE TEMPLATES (10)
# =============================================================================

def _build_artisan_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Artisan - Crafted creative design with unique header."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 40px 50px 30px;
            text-align: center;
            border-bottom: 2px dashed {primary_color};
        }}
        .sender-name {{
            font-size: 28pt;
            font-weight: 300;
            color: {primary_color};
            letter-spacing: 4px;
            text-transform: uppercase;
            margin-bottom: 12px;
        }}
        .sender-contact {{
            display: flex;
            justify-content: center;
            gap: 25px;
            font-size: 10pt;
            color: #666;
        }}
        .letter-body {{ padding: 35px 55px 50px; }}
        .date {{ font-size: 10pt; color: #888; margin-bottom: 25px; text-align: center; }}
        .recipient {{ margin-bottom: 25px; }}
        .recipient-name {{ font-weight: 500; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #444; }}
        .subject {{
            margin-bottom: 25px;
            font-size: 11pt;
            color: {primary_color};
            font-style: italic;
        }}
        .salutation {{ margin-bottom: 18px; font-size: 11pt; }}
        .content p {{ margin: 0 0 16px 0; text-align: justify; line-height: 1.75; }}
        .closing {{ margin-top: 35px; }}
        .closing p {{ margin: 0 0 10px 0; font-style: italic; }}
        .signature {{ font-size: 13pt; color: {primary_color}; letter-spacing: 1px; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Re: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Warmly,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_cl_canvas_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Canvas - Blank slate creative aesthetic."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 50px 60px 35px;
        }}
        .sender-name {{
            font-size: 32pt;
            font-weight: 200;
            color: #1a1a1a;
            margin-bottom: 15px;
        }}
        .sender-contact {{
            display: flex;
            gap: 25px;
            font-size: 9pt;
            color: #999;
        }}
        .letter-body {{ padding: 20px 60px 60px; }}
        .date {{ font-size: 9pt; color: #bbb; margin-bottom: 30px; }}
        .recipient {{ margin-bottom: 30px; }}
        .recipient-name {{ font-weight: 400; font-size: 10pt; color: #666; }}
        .company-name {{ font-size: 10pt; color: #666; }}
        .subject {{
            margin-bottom: 30px;
            font-size: 10pt;
            color: #333;
        }}
        .salutation {{ margin-bottom: 20px; font-size: 10pt; color: #555; }}
        .content p {{ margin: 0 0 18px 0; text-align: left; line-height: 1.9; font-size: 10pt; color: #444; }}
        .closing {{ margin-top: 40px; }}
        .closing p {{ margin: 0 0 12px 0; font-size: 10pt; color: #555; }}
        .signature {{ font-size: 12pt; color: #1a1a1a; font-weight: 300; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">{_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_palette_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Palette - Colorful creative with bold accents."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 28px;
            background: {primary_color};
            color: #fff;
        }}
        .sender-name {{
            font-size: 28pt;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: rgba(255,255,255,0.9);
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 12pt;
            font-weight: 700;
            color: {primary_color};
            padding: 8px 0;
            border-bottom: 3px solid {primary_color};
            display: inline-block;
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 700; font-size: 13pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">{_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Cheers,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_studio_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Studio - Designer studio creative style."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .letter-paper {{
            background: #fafafa;
        }}
        .header {{
            padding: 40px 50px 30px;
            background: #fff;
            border-bottom: 1px solid #e5e7eb;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 600;
            color: {primary_color};
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: #666;
        }}
        .letter-body {{
            padding: 30px 50px 50px;
            background: #fff;
            margin: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}
        .date {{ font-size: 10pt; color: #888; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 500; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #444; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            color: {primary_color};
            font-weight: 600;
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; line-height: 1.7; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 600; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Re: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_gallery_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Gallery - Gallery-inspired creative layout."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 45px 55px 35px;
            border-bottom: 1px solid #1a1a1a;
        }}
        .sender-name {{
            font-size: 30pt;
            font-weight: 300;
            color: #1a1a1a;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 15px;
        }}
        .sender-contact {{
            display: flex;
            gap: 25px;
            font-size: 9pt;
            color: #666;
            letter-spacing: 1px;
        }}
        .letter-body {{ padding: 35px 55px 55px; }}
        .date {{ font-size: 9pt; color: #888; margin-bottom: 28px; letter-spacing: 1px; }}
        .recipient {{ margin-bottom: 28px; }}
        .recipient-name {{ font-weight: 400; font-size: 10pt; letter-spacing: 0.5px; }}
        .company-name {{ font-size: 10pt; color: #444; }}
        .subject {{
            margin-bottom: 28px;
            font-size: 10pt;
            color: {primary_color};
            letter-spacing: 1px;
        }}
        .salutation {{ margin-bottom: 20px; font-size: 10pt; }}
        .content p {{ margin: 0 0 16px 0; text-align: justify; line-height: 1.8; font-size: 10pt; }}
        .closing {{ margin-top: 38px; }}
        .closing p {{ margin: 0 0 12px 0; font-size: 10pt; }}
        .signature {{ font-size: 11pt; color: #1a1a1a; letter-spacing: 1px; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">{_escape(cover_letter.position_title)}</div>
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


def _build_spectrum_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Spectrum - Full spectrum creative style."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 28px;
            background: linear-gradient(135deg, {primary_color} 0%, #667eea 50%, #764ba2 100%);
            color: #fff;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: rgba(255,255,255,0.9);
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            font-weight: 600;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 600; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Re: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_spark_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Spark - Energetic creative with spark."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 28px;
            border-bottom: 4px solid {primary_color};
        }}
        .sender-name {{
            font-size: 28pt;
            font-weight: 700;
            color: {primary_color};
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: #555;
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 12pt;
            font-weight: 700;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 700; font-size: 13pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">{_escape(cover_letter.position_title)} Application</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Cheers,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_bloom_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Bloom - Fresh blooming creative style."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 40px 50px 30px;
            background: linear-gradient(180deg, rgba(104,211,145,0.15) 0%, #fff 100%);
            border-bottom: 2px solid {primary_color};
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 500;
            color: {primary_color};
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: #555;
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 500; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            color: {primary_color};
            font-weight: 500;
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; line-height: 1.7; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 500; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Re: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Warm regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_aurora_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Aurora - Northern lights inspired creative."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 28px;
            background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
            color: #fff;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 400;
            letter-spacing: 2px;
            margin-bottom: 10px;
            color: {primary_color};
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: rgba(255,255,255,0.8);
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 500; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            color: #2c5364;
            font-weight: 500;
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 500; font-size: 12pt; color: #2c5364; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Application: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_cl_zen_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Zen - Peaceful zen creative minimalism."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 55px 65px 40px;
            text-align: center;
        }}
        .sender-name {{
            font-size: 24pt;
            font-weight: 300;
            color: #555;
            letter-spacing: 4px;
            margin-bottom: 18px;
        }}
        .sender-contact {{
            display: flex;
            justify-content: center;
            gap: 30px;
            font-size: 9pt;
            color: #999;
        }}
        .letter-body {{ padding: 25px 65px 65px; }}
        .date {{ font-size: 9pt; color: #aaa; margin-bottom: 35px; text-align: center; }}
        .recipient {{ margin-bottom: 35px; }}
        .recipient-name {{ font-weight: 300; font-size: 10pt; color: #666; }}
        .company-name {{ font-size: 10pt; color: #666; }}
        .subject {{
            margin-bottom: 35px;
            font-size: 10pt;
            color: #777;
        }}
        .salutation {{ margin-bottom: 22px; font-size: 10pt; color: #555; }}
        .content p {{ margin: 0 0 20px 0; text-align: left; line-height: 2; font-size: 10pt; color: #555; }}
        .closing {{ margin-top: 45px; }}
        .closing p {{ margin: 0 0 15px 0; font-size: 10pt; color: #555; }}
        .signature {{ font-size: 11pt; color: #555; font-weight: 300; letter-spacing: 1px; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">{_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>With gratitude,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_cl_pure_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Pure - Ultra-clean creative simplicity."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 45px 55px 30px;
            border-bottom: 1px solid #eee;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 200;
            color: #333;
            margin-bottom: 12px;
        }}
        .sender-contact {{
            display: flex;
            gap: 25px;
            font-size: 9pt;
            color: #888;
        }}
        .letter-body {{ padding: 30px 55px 55px; }}
        .date {{ font-size: 9pt; color: #999; margin-bottom: 28px; }}
        .recipient {{ margin-bottom: 28px; }}
        .recipient-name {{ font-weight: 400; font-size: 10pt; color: #555; }}
        .company-name {{ font-size: 10pt; color: #555; }}
        .subject {{
            margin-bottom: 28px;
            font-size: 10pt;
            color: #444;
        }}
        .salutation {{ margin-bottom: 20px; font-size: 10pt; color: #444; }}
        .content p {{ margin: 0 0 16px 0; text-align: left; line-height: 1.85; font-size: 10pt; color: #444; }}
        .closing {{ margin-top: 38px; }}
        .closing p {{ margin: 0 0 12px 0; font-size: 10pt; color: #444; }}
        .signature {{ font-size: 11pt; color: #333; font-weight: 400; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">{_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_cl_essence_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Essence - Distilled creative clarity."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 40px 50px 28px;
            border-left: 4px solid {primary_color};
            margin-left: 30px;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 400;
            color: #2d3748;
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: #666;
        }}
        .letter-body {{ padding: 30px 50px 50px 80px; }}
        .date {{ font-size: 10pt; color: #888; margin-bottom: 25px; }}
        .recipient {{ margin-bottom: 25px; }}
        .recipient-name {{ font-weight: 500; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #444; }}
        .subject {{
            margin-bottom: 25px;
            font-size: 11pt;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 18px; font-size: 11pt; }}
        .content p {{ margin: 0 0 15px 0; text-align: justify; line-height: 1.75; }}
        .closing {{ margin-top: 32px; }}
        .closing p {{ margin: 0 0 10px 0; }}
        .signature {{ font-size: 12pt; color: #2d3748; font-weight: 500; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Re: {_escape(cover_letter.position_title)}</div>
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


# =============================================================================
# ADDITIONAL TEMPLATES (7 more to reach 37)
# =============================================================================

def _build_quantum_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Quantum - Modern tech aesthetic with gradient header."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 28px;
            background: linear-gradient(135deg, {primary_color} 0%, #667eea 100%);
            color: #fff;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: rgba(255,255,255,0.9);
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            font-weight: 600;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 600; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Re: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_binary_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Binary - Developer-focused modern minimalism."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 28px;
            background: #1a1a2e;
            color: #fff;
        }}
        .sender-name {{
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 24pt;
            font-weight: 400;
            color: {primary_color};
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-family: 'Consolas', monospace;
            font-size: 9pt;
            color: rgba(255,255,255,0.7);
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            color: {primary_color};
            font-family: 'Consolas', monospace;
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-family: 'Consolas', monospace; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">&gt; {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_stack_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Stack - Full-stack friendly modern layout."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 28px;
            border-bottom: 4px solid {primary_color};
            background: #f8fafc;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 700;
            color: {primary_color};
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: #555;
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            font-weight: 700;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 700; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">{_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_startup_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Startup - Dynamic startup culture style."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 28px;
            background: {primary_color};
            color: #fff;
        }}
        .sender-name {{
            font-size: 28pt;
            font-weight: 800;
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: rgba(255,255,255,0.9);
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 12pt;
            font-weight: 800;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 800; font-size: 13pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">{_escape(cover_letter.position_title)} 🚀</div>
            <div class="salutation">Hey {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Cheers,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_agile_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Agile - Fast-paced modern tech design."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 32px 50px 25px;
            border-left: 5px solid {primary_color};
            background: #f0fdf4;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 600;
            color: {primary_color};
            margin-bottom: 8px;
        }}
        .sender-contact {{
            display: flex;
            gap: 18px;
            font-size: 10pt;
            color: #555;
        }}
        .letter-body {{ padding: 28px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 20px; }}
        .recipient {{ margin-bottom: 20px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 20px;
            font-size: 11pt;
            font-weight: 600;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 14px; font-size: 11pt; }}
        .content p {{ margin: 0 0 12px 0; text-align: justify; }}
        .closing {{ margin-top: 28px; }}
        .closing p {{ margin: 0 0 6px 0; }}
        .signature {{ font-weight: 600; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Re: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_sprint_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Sprint - Quick impact modern layout."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 35px 50px 28px;
            background: linear-gradient(90deg, {primary_color} 0%, #f472b6 100%);
            color: #fff;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: rgba(255,255,255,0.9);
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            font-weight: 700;
            color: {primary_color};
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 700; font-size: 12pt; color: {primary_color}; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">{_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Best regards,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''


def _build_ember_cover_letter(cover_letter, primary_color: str, today: str) -> str:
    """Ember - Warm ember creative design."""
    contact_parts = _cl_contact_parts(cover_letter)
    recipient_name, company_address = _cl_recipient_html(cover_letter)
    body_html = _build_cover_letter_body_html(cover_letter)
    manager = _escape(cover_letter.hiring_manager) if cover_letter.hiring_manager else 'Hiring Manager'
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{_escape(cover_letter.full_name)} - Cover Letter</title>
    <style>
        {_get_cl_base_styles()}
        .header {{
            padding: 38px 50px 30px;
            background: linear-gradient(135deg, #fc8181 0%, #f6ad55 100%);
            color: #fff;
        }}
        .sender-name {{
            font-size: 26pt;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .sender-contact {{
            display: flex;
            gap: 20px;
            font-size: 10pt;
            color: rgba(255,255,255,0.95);
        }}
        .letter-body {{ padding: 30px 50px 50px; }}
        .date {{ font-size: 10pt; color: #666; margin-bottom: 22px; }}
        .recipient {{ margin-bottom: 22px; }}
        .recipient-name {{ font-weight: 600; font-size: 11pt; }}
        .company-name {{ font-size: 11pt; color: #333; }}
        .subject {{
            margin-bottom: 22px;
            font-size: 11pt;
            font-weight: 600;
            color: #c53030;
        }}
        .salutation {{ margin-bottom: 16px; font-size: 11pt; }}
        .content p {{ margin: 0 0 14px 0; text-align: justify; line-height: 1.7; }}
        .closing {{ margin-top: 30px; }}
        .closing p {{ margin: 0 0 8px 0; }}
        .signature {{ font-weight: 600; font-size: 12pt; color: #c53030; }}
    </style>
</head>
<body>
    <div class="letter-paper">
        <header class="header">
            <div class="sender-name">{_escape(cover_letter.full_name)}</div>
            <div class="sender-contact">{''.join(contact_parts)}</div>
        </header>
        <div class="letter-body">
            <div class="date">{today}</div>
            <div class="recipient">
                {recipient_name}
                <div class="company-name">{_escape(cover_letter.company_name)}</div>
                {company_address}
            </div>
            <div class="subject">Re: {_escape(cover_letter.position_title)}</div>
            <div class="salutation">Dear {manager},</div>
            <div class="content">{body_html}</div>
            <div class="closing">
                <p>Warmly,</p>
                <div class="signature">{_escape(cover_letter.full_name)}</div>
            </div>
        </div>
    </div>
</body>
</html>'''
