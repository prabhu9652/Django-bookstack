"""
Premium Template Themes for Enterprise Resume Builder
Provides role-specific color palettes and theme configurations for each template style.

Features:
- Multiple premium color palettes per template
- Role-optimized color recommendations
- ATS-safe color combinations
- Consistent branding across PDF and preview
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ColorPalette:
    """Represents a complete color palette for a template"""
    name: str
    primary: str
    secondary: str
    accent: str
    text_primary: str
    text_secondary: str
    background: str
    sidebar_bg: str
    description: str
    recommended_roles: List[str]


# ============================================================================
# PROFESSIONAL TEMPLATE PALETTES (With Photo, Left Sidebar)
# ============================================================================

PROFESSIONAL_PALETTES = [
    ColorPalette(
        name='Teal Classic',
        primary='#4a9d9a',
        secondary='#3d8584',
        accent='#5fb3b0',
        text_primary='#1a1a1a',
        text_secondary='#555555',
        background='#ffffff',
        sidebar_bg='#f7f7f7',
        description='Classic teal - professional and trustworthy',
        recommended_roles=['devops_sre', 'software_engineer']
    ),
    ColorPalette(
        name='Navy Executive',
        primary='#1e3a5f',
        secondary='#152d4a',
        accent='#2a4a73',
        text_primary='#1a1a1a',
        text_secondary='#555555',
        background='#ffffff',
        sidebar_bg='#f5f7fa',
        description='Deep navy - authoritative and corporate',
        recommended_roles=['software_engineer', 'ds_ml']
    ),
    ColorPalette(
        name='Forest Green',
        primary='#2d5a3d',
        secondary='#234830',
        accent='#3a7350',
        text_primary='#1a1a1a',
        text_secondary='#555555',
        background='#ffffff',
        sidebar_bg='#f5f8f6',
        description='Forest green - growth and stability',
        recommended_roles=['devops_sre', 'ds_ml']
    ),
    ColorPalette(
        name='Burgundy Premium',
        primary='#722f37',
        secondary='#5a252c',
        accent='#8a3a44',
        text_primary='#1a1a1a',
        text_secondary='#555555',
        background='#ffffff',
        sidebar_bg='#faf7f7',
        description='Rich burgundy - sophisticated and bold',
        recommended_roles=['software_engineer']
    ),
    ColorPalette(
        name='Slate Modern',
        primary='#475569',
        secondary='#374151',
        accent='#64748b',
        text_primary='#1a1a1a',
        text_secondary='#555555',
        background='#ffffff',
        sidebar_bg='#f8fafc',
        description='Modern slate - clean and contemporary',
        recommended_roles=['devops_sre', 'software_engineer', 'ds_ml']
    ),
    ColorPalette(
        name='Royal Purple',
        primary='#5b21b6',
        secondary='#4c1d95',
        accent='#7c3aed',
        text_primary='#1a1a1a',
        text_secondary='#555555',
        background='#ffffff',
        sidebar_bg='#faf5ff',
        description='Royal purple - creative and innovative',
        recommended_roles=['ds_ml', 'software_engineer']
    ),
]


# ============================================================================
# MODERN TEMPLATE PALETTES (No Photo, Right Sidebar, Minimal)
# ============================================================================

MODERN_PALETTES = [
    ColorPalette(
        name='Charcoal Minimal',
        primary='#2d3748',
        secondary='#1a202c',
        accent='#4a5568',
        text_primary='#1a1a1a',
        text_secondary='#4a5568',
        background='#ffffff',
        sidebar_bg='#f8f9fa',
        description='Charcoal - minimal and sophisticated',
        recommended_roles=['software_engineer', 'ds_ml']
    ),
    ColorPalette(
        name='Ocean Blue',
        primary='#1e40af',
        secondary='#1e3a8a',
        accent='#3b82f6',
        text_primary='#1a1a1a',
        text_secondary='#4b5563',
        background='#ffffff',
        sidebar_bg='#f0f9ff',
        description='Ocean blue - tech-forward and reliable',
        recommended_roles=['devops_sre', 'software_engineer']
    ),
    ColorPalette(
        name='Emerald Tech',
        primary='#047857',
        secondary='#065f46',
        accent='#10b981',
        text_primary='#1a1a1a',
        text_secondary='#4b5563',
        background='#ffffff',
        sidebar_bg='#ecfdf5',
        description='Emerald - fresh and innovative',
        recommended_roles=['devops_sre', 'ds_ml']
    ),
    ColorPalette(
        name='Graphite Pro',
        primary='#374151',
        secondary='#1f2937',
        accent='#6b7280',
        text_primary='#111827',
        text_secondary='#4b5563',
        background='#ffffff',
        sidebar_bg='#f9fafb',
        description='Graphite - professional and understated',
        recommended_roles=['software_engineer', 'devops_sre', 'ds_ml']
    ),
    ColorPalette(
        name='Indigo Creative',
        primary='#4338ca',
        secondary='#3730a3',
        accent='#6366f1',
        text_primary='#1a1a1a',
        text_secondary='#4b5563',
        background='#ffffff',
        sidebar_bg='#eef2ff',
        description='Indigo - creative and modern',
        recommended_roles=['ds_ml', 'software_engineer']
    ),
    ColorPalette(
        name='Copper Warm',
        primary='#b45309',
        secondary='#92400e',
        accent='#d97706',
        text_primary='#1a1a1a',
        text_secondary='#4b5563',
        background='#ffffff',
        sidebar_bg='#fffbeb',
        description='Copper - warm and approachable',
        recommended_roles=['software_engineer']
    ),
]


# ============================================================================
# EXECUTIVE TEMPLATE PALETTES (Bold Header, Left Sidebar with Accent Bars)
# ============================================================================

EXECUTIVE_PALETTES = [
    ColorPalette(
        name='Mint Executive',
        primary='#81c9c5',
        secondary='#6bb8b4',
        accent='#9dd5d2',
        text_primary='#1a1a1a',
        text_secondary='#555555',
        background='#ffffff',
        sidebar_bg='#f5f5f5',
        description='Mint - fresh and executive',
        recommended_roles=['devops_sre', 'software_engineer']
    ),
    ColorPalette(
        name='Gold Premium',
        primary='#b8860b',
        secondary='#9a7209',
        accent='#daa520',
        text_primary='#1a1a1a',
        text_secondary='#555555',
        background='#ffffff',
        sidebar_bg='#fefce8',
        description='Gold - premium and distinguished',
        recommended_roles=['software_engineer', 'ds_ml']
    ),
    ColorPalette(
        name='Steel Blue',
        primary='#4682b4',
        secondary='#3a6d96',
        accent='#5a9fd4',
        text_primary='#1a1a1a',
        text_secondary='#555555',
        background='#ffffff',
        sidebar_bg='#f0f7fc',
        description='Steel blue - strong and dependable',
        recommended_roles=['devops_sre', 'software_engineer']
    ),
    ColorPalette(
        name='Rose Executive',
        primary='#be185d',
        secondary='#9d174d',
        accent='#db2777',
        text_primary='#1a1a1a',
        text_secondary='#555555',
        background='#ffffff',
        sidebar_bg='#fdf2f8',
        description='Rose - bold and memorable',
        recommended_roles=['ds_ml', 'software_engineer']
    ),
    ColorPalette(
        name='Sage Professional',
        primary='#65a30d',
        secondary='#4d7c0f',
        accent='#84cc16',
        text_primary='#1a1a1a',
        text_secondary='#555555',
        background='#ffffff',
        sidebar_bg='#f7fee7',
        description='Sage - natural and balanced',
        recommended_roles=['devops_sre', 'ds_ml']
    ),
    ColorPalette(
        name='Coral Vibrant',
        primary='#ea580c',
        secondary='#c2410c',
        accent='#f97316',
        text_primary='#1a1a1a',
        text_secondary='#555555',
        background='#ffffff',
        sidebar_bg='#fff7ed',
        description='Coral - energetic and confident',
        recommended_roles=['software_engineer']
    ),
]


# ============================================================================
# TEMPLATE THEME MANAGER
# ============================================================================

class TemplateThemeManager:
    """Manages template themes and color palettes"""
    
    TEMPLATE_PALETTES = {
        'professional': PROFESSIONAL_PALETTES,
        'modern': MODERN_PALETTES,
        'executive': EXECUTIVE_PALETTES,
    }
    
    @classmethod
    def get_palettes_for_template(cls, template_slug: str) -> List[ColorPalette]:
        """Get all available palettes for a template"""
        return cls.TEMPLATE_PALETTES.get(template_slug, PROFESSIONAL_PALETTES)
    
    @classmethod
    def get_palette_by_name(cls, template_slug: str, palette_name: str) -> Optional[ColorPalette]:
        """Get a specific palette by name"""
        palettes = cls.get_palettes_for_template(template_slug)
        for palette in palettes:
            if palette.name == palette_name:
                return palette
        return palettes[0] if palettes else None
    
    @classmethod
    def get_palette_by_color(cls, template_slug: str, primary_color: str) -> Optional[ColorPalette]:
        """Get a palette by its primary color"""
        palettes = cls.get_palettes_for_template(template_slug)
        for palette in palettes:
            if palette.primary.lower() == primary_color.lower():
                return palette
        return None
    
    @classmethod
    def get_recommended_palettes(cls, template_slug: str, role: str) -> List[ColorPalette]:
        """Get palettes recommended for a specific role"""
        palettes = cls.get_palettes_for_template(template_slug)
        return [p for p in palettes if role in p.recommended_roles]
    
    @classmethod
    def get_all_color_options(cls, template_slug: str) -> List[Dict]:
        """Get color options formatted for the UI"""
        palettes = cls.get_palettes_for_template(template_slug)
        return [
            {
                'name': p.name,
                'value': p.primary,
                'description': p.description,
                'recommended_roles': p.recommended_roles,
            }
            for p in palettes
        ]
    
    @classmethod
    def get_default_palette(cls, template_slug: str) -> ColorPalette:
        """Get the default palette for a template"""
        palettes = cls.get_palettes_for_template(template_slug)
        return palettes[0] if palettes else PROFESSIONAL_PALETTES[0]


# ============================================================================
# ROLE-SPECIFIC TEMPLATE RECOMMENDATIONS
# ============================================================================

ROLE_TEMPLATE_RECOMMENDATIONS = {
    'devops_sre': {
        'recommended_template': 'professional',
        'recommended_palette': 'Teal Classic',
        'reasoning': 'Professional template with teal conveys reliability and technical expertise',
        'alternative_templates': ['executive', 'modern'],
    },
    'software_engineer': {
        'recommended_template': 'modern',
        'recommended_palette': 'Charcoal Minimal',
        'reasoning': 'Modern template with charcoal shows clean code mindset and contemporary skills',
        'alternative_templates': ['professional', 'executive'],
    },
    'ds_ml': {
        'recommended_template': 'executive',
        'recommended_palette': 'Mint Executive',
        'reasoning': 'Executive template conveys analytical thinking and data-driven approach',
        'alternative_templates': ['modern', 'professional'],
    },
}


def get_role_recommendations(role: str) -> Dict:
    """Get template and palette recommendations for a role"""
    return ROLE_TEMPLATE_RECOMMENDATIONS.get(role, ROLE_TEMPLATE_RECOMMENDATIONS['software_engineer'])


def get_color_options_for_ui(template_slug: str = 'professional') -> List[Dict]:
    """Get color options formatted for the edit resume UI"""
    return TemplateThemeManager.get_all_color_options(template_slug)
