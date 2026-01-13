"""
Color Utility Functions for Template System
============================================

Provides color manipulation, WCAG compliance checking, and complementary color generation
for the resume and cover letter template system.

Features:
- Hex/RGB color conversion
- WCAG AA contrast ratio calculation
- Complementary color generation from primary color
- Color validation utilities
"""

import colorsys
import re
from typing import Tuple, Dict, Optional


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Convert hex color to RGB tuple.
    
    Args:
        hex_color: Hex color string (e.g., '#4a9d9a' or '4a9d9a')
    
    Returns:
        Tuple of (red, green, blue) values (0-255)
    
    Raises:
        ValueError: If hex_color is not a valid hex color
    """
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")
    
    try:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        raise ValueError(f"Invalid hex color: {hex_color}")


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Convert RGB values to hex color string.
    
    Args:
        r: Red value (0-255)
        g: Green value (0-255)
        b: Blue value (0-255)
    
    Returns:
        Hex color string with # prefix (e.g., '#4a9d9a')
    """
    # Clamp values to valid range
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    
    return f'#{r:02x}{g:02x}{b:02x}'


def calculate_luminance(hex_color: str) -> float:
    """
    Calculate relative luminance for WCAG contrast calculations.
    
    Uses the formula from WCAG 2.1:
    L = 0.2126 * R + 0.7152 * G + 0.0722 * B
    
    Where R, G, B are linearized sRGB values.
    
    Args:
        hex_color: Hex color string
    
    Returns:
        Relative luminance value (0.0 to 1.0)
    """
    r, g, b = hex_to_rgb(hex_color)
    
    def linearize(c: int) -> float:
        """Convert sRGB to linear RGB"""
        c = c / 255.0
        if c <= 0.03928:
            return c / 12.92
        return ((c + 0.055) / 1.055) ** 2.4
    
    r_lin = linearize(r)
    g_lin = linearize(g)
    b_lin = linearize(b)
    
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def calculate_contrast_ratio(color1: str, color2: str) -> float:
    """
    Calculate WCAG contrast ratio between two colors.
    
    The contrast ratio is calculated as:
    (L1 + 0.05) / (L2 + 0.05)
    
    Where L1 is the lighter color's luminance and L2 is the darker.
    
    Args:
        color1: First hex color
        color2: Second hex color
    
    Returns:
        Contrast ratio (1.0 to 21.0)
    """
    l1 = calculate_luminance(color1)
    l2 = calculate_luminance(color2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)


def is_wcag_aa_compliant(foreground: str, background: str, large_text: bool = False) -> bool:
    """
    Check if color combination meets WCAG AA standards.
    
    WCAG AA requires:
    - 4.5:1 contrast ratio for normal text
    - 3.0:1 contrast ratio for large text (18pt+ or 14pt+ bold)
    
    Args:
        foreground: Text color (hex)
        background: Background color (hex)
        large_text: Whether the text is large (18pt+ or 14pt+ bold)
    
    Returns:
        True if the combination meets WCAG AA standards
    """
    ratio = calculate_contrast_ratio(foreground, background)
    threshold = 3.0 if large_text else 4.5
    return ratio >= threshold


def is_wcag_aaa_compliant(foreground: str, background: str, large_text: bool = False) -> bool:
    """
    Check if color combination meets WCAG AAA standards.
    
    WCAG AAA requires:
    - 7.0:1 contrast ratio for normal text
    - 4.5:1 contrast ratio for large text
    
    Args:
        foreground: Text color (hex)
        background: Background color (hex)
        large_text: Whether the text is large
    
    Returns:
        True if the combination meets WCAG AAA standards
    """
    ratio = calculate_contrast_ratio(foreground, background)
    threshold = 4.5 if large_text else 7.0
    return ratio >= threshold


def generate_complementary_colors(primary: str) -> Dict[str, str]:
    """
    Generate a complete color palette from a primary color.
    
    Creates:
    - secondary: Darker variant of primary
    - accent: Lighter variant of primary
    - text_on_primary: White or dark text based on primary luminance
    - text_primary: Standard dark text color
    - text_secondary: Muted text color
    
    Args:
        primary: Primary hex color
    
    Returns:
        Dictionary with all generated colors as hex strings
    """
    r, g, b = hex_to_rgb(primary)
    
    # Convert to HLS for manipulation
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    
    # Generate darker variant (secondary)
    secondary_l = max(0.0, l - 0.15)
    sr, sg, sb = colorsys.hls_to_rgb(h, secondary_l, s)
    secondary = rgb_to_hex(int(sr*255), int(sg*255), int(sb*255))
    
    # Generate lighter variant (accent)
    accent_l = min(1.0, l + 0.15)
    ar, ag, ab = colorsys.hls_to_rgb(h, accent_l, s)
    accent = rgb_to_hex(int(ar*255), int(ag*255), int(ab*255))
    
    # Determine text color on primary based on contrast ratio
    # Check both white and dark text, use the one with better contrast
    white_contrast = calculate_contrast_ratio('#ffffff', primary)
    dark_contrast = calculate_contrast_ratio('#1a1a1a', primary)
    
    # Use the color with better contrast
    text_on_primary = '#ffffff' if white_contrast >= dark_contrast else '#1a1a1a'
    
    return {
        'primary': primary,
        'secondary': secondary,
        'accent': accent,
        'text_on_primary': text_on_primary,
        'text_primary': '#1a1a1a',
        'text_secondary': '#555555',
    }


def validate_hex_color(color: str) -> bool:
    """
    Validate that a string is a valid hex color.
    
    Args:
        color: String to validate
    
    Returns:
        True if valid hex color (with or without #)
    """
    if not color:
        return False
    
    pattern = r'^#?[0-9A-Fa-f]{6}$'
    return bool(re.match(pattern, color))


def safe_color_or_default(color: str, default: str = '#4a9d9a') -> str:
    """
    Return color if valid, otherwise return default.
    
    Args:
        color: Color to validate
        default: Default color to return if invalid
    
    Returns:
        Valid hex color string with # prefix
    """
    if validate_hex_color(color):
        return color if color.startswith('#') else f'#{color}'
    return default


def get_readable_text_color(background: str) -> str:
    """
    Get the most readable text color (black or white) for a background.
    
    Args:
        background: Background hex color
    
    Returns:
        '#ffffff' for dark backgrounds, '#1a1a1a' for light backgrounds
    """
    luminance = calculate_luminance(background)
    return '#ffffff' if luminance < 0.5 else '#1a1a1a'


def adjust_color_lightness(hex_color: str, amount: float) -> str:
    """
    Adjust the lightness of a color.
    
    Args:
        hex_color: Original hex color
        amount: Amount to adjust (-1.0 to 1.0, negative = darker)
    
    Returns:
        Adjusted hex color
    """
    r, g, b = hex_to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    
    # Adjust lightness
    new_l = max(0.0, min(1.0, l + amount))
    
    nr, ng, nb = colorsys.hls_to_rgb(h, new_l, s)
    return rgb_to_hex(int(nr*255), int(ng*255), int(nb*255))
