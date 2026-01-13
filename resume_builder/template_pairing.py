"""
Template Pairing Module for Resume-Cover Letter Consistency
============================================================

Provides functionality to pair resume templates with cover letter templates
and apply consistent branding across both document types.

Features:
- Template pairing recommendations
- Color consistency between resume and cover letter
- Branding application for matched pairs
"""

from typing import Dict, Optional, List


# =============================================================================
# TEMPLATE PAIRS - Resume to Cover Letter Mapping
# =============================================================================

TEMPLATE_PAIRS = {
    # Resume template slug -> Recommended cover letter template slugs
    'professional': {
        'primary': 'classic',
        'alternatives': ['modern'],
        'reasoning': 'Classic cover letter matches the formal, photo-based professional resume',
    },
    'modern': {
        'primary': 'modern',
        'alternatives': ['classic'],
        'reasoning': 'Modern cover letter complements the clean, minimal modern resume',
    },
    'executive': {
        'primary': 'modern',
        'alternatives': ['classic'],
        'reasoning': 'Modern cover letter with bold accents matches executive resume style',
    },
    'minimal': {
        'primary': 'classic',
        'alternatives': ['modern'],
        'reasoning': 'Classic cover letter maintains the clean, understated minimal aesthetic',
    },
    'creative': {
        'primary': 'creative',
        'alternatives': ['modern'],
        'reasoning': 'Creative cover letter with color header matches bold creative resume',
    },
    'technical': {
        'primary': 'modern',
        'alternatives': ['classic'],
        'reasoning': 'Modern cover letter provides clean complement to technical resume',
    },
}


# =============================================================================
# COVER LETTER TEMPLATE INFO
# =============================================================================

COVER_LETTER_TEMPLATES = {
    'classic': {
        'name': 'Classic',
        'description': 'Traditional serif font, formal layout',
        'tone': 'formal',
        'font_style': 'serif',
    },
    'modern': {
        'name': 'Modern',
        'description': 'Sans-serif font, clean header with accent border',
        'tone': 'professional',
        'font_style': 'sans-serif',
    },
    'creative': {
        'name': 'Creative',
        'description': 'Bold colored header, contemporary design',
        'tone': 'confident',
        'font_style': 'sans-serif',
    },
}


# =============================================================================
# PAIRING FUNCTIONS
# =============================================================================

def get_paired_cover_letter_template(resume_template_slug: str) -> str:
    """
    Get the recommended cover letter template for a resume template.
    
    Args:
        resume_template_slug: The slug of the resume template
        
    Returns:
        The slug of the recommended cover letter template
    """
    pair_info = TEMPLATE_PAIRS.get(resume_template_slug)
    if pair_info:
        return pair_info['primary']
    # Default to classic if no pairing found
    return 'classic'


def get_alternative_cover_letter_templates(resume_template_slug: str) -> List[str]:
    """
    Get alternative cover letter templates for a resume template.
    
    Args:
        resume_template_slug: The slug of the resume template
        
    Returns:
        List of alternative cover letter template slugs
    """
    pair_info = TEMPLATE_PAIRS.get(resume_template_slug)
    if pair_info:
        return pair_info.get('alternatives', [])
    return ['classic', 'modern']


def get_pairing_reasoning(resume_template_slug: str) -> str:
    """
    Get the reasoning for a template pairing.
    
    Args:
        resume_template_slug: The slug of the resume template
        
    Returns:
        Explanation of why the pairing is recommended
    """
    pair_info = TEMPLATE_PAIRS.get(resume_template_slug)
    if pair_info:
        return pair_info.get('reasoning', '')
    return 'Default pairing for unmatched template'


def apply_resume_branding_to_cover_letter(
    resume_primary_color: str,
    cover_letter_template_slug: str
) -> Dict[str, str]:
    """
    Apply resume branding colors to a cover letter.
    
    This ensures visual consistency between a resume and its paired cover letter
    by using the same primary color scheme.
    
    Args:
        resume_primary_color: The primary color from the resume (hex format)
        cover_letter_template_slug: The cover letter template being used
        
    Returns:
        Dictionary with color values to apply to the cover letter
    """
    # Import color utilities
    from .color_utils import (
        calculate_contrast_ratio,
        generate_complementary_colors,
        validate_hex_color,
        safe_color_or_default,
    )
    
    # Ensure valid color
    primary_color = safe_color_or_default(resume_primary_color)
    
    # Generate complementary colors
    palette = generate_complementary_colors(primary_color)
    
    # Build cover letter specific colors
    cover_letter_colors = {
        'primary_color': primary_color,
        'header_color': primary_color,
        'accent_color': palette['accent'],
        'text_color': palette['text_primary'],
        'text_on_header': palette['text_on_primary'],
    }
    
    # Template-specific adjustments
    if cover_letter_template_slug == 'classic':
        # Classic uses more subtle colors
        cover_letter_colors['header_color'] = palette['text_primary']  # Dark header text
        cover_letter_colors['accent_color'] = primary_color
    elif cover_letter_template_slug == 'creative':
        # Creative uses bold header background
        cover_letter_colors['header_background'] = primary_color
        cover_letter_colors['header_text'] = palette['text_on_primary']
    
    return cover_letter_colors


def get_all_cover_letter_templates() -> List[Dict]:
    """
    Get all available cover letter templates with their info.
    
    Returns:
        List of dictionaries with template information
    """
    return [
        {
            'slug': slug,
            **info
        }
        for slug, info in COVER_LETTER_TEMPLATES.items()
    ]


def get_cover_letter_template_info(slug: str) -> Optional[Dict]:
    """
    Get information about a specific cover letter template.
    
    Args:
        slug: The template slug
        
    Returns:
        Dictionary with template information or None if not found
    """
    info = COVER_LETTER_TEMPLATES.get(slug)
    if info:
        return {'slug': slug, **info}
    return None


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def is_valid_resume_template(slug: str) -> bool:
    """Check if a resume template slug is valid for pairing."""
    return slug in TEMPLATE_PAIRS


def is_valid_cover_letter_template(slug: str) -> bool:
    """Check if a cover letter template slug is valid."""
    return slug in COVER_LETTER_TEMPLATES


def get_compatible_pairs() -> List[Dict]:
    """
    Get all compatible resume-cover letter pairs.
    
    Returns:
        List of dictionaries with pairing information
    """
    pairs = []
    for resume_slug, pair_info in TEMPLATE_PAIRS.items():
        pairs.append({
            'resume_template': resume_slug,
            'cover_letter_template': pair_info['primary'],
            'alternatives': pair_info.get('alternatives', []),
            'reasoning': pair_info.get('reasoning', ''),
        })
    return pairs
