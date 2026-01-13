"""
Tests for Resume Builder Template System
=========================================

Includes both unit tests and property-based tests using Hypothesis.
Property tests validate universal correctness properties across all inputs.
"""

from django.test import TestCase
from hypothesis import given, strategies as st, settings
from hypothesis.extra.django import TestCase as HypothesisTestCase
import re

from .color_utils import (
    hex_to_rgb,
    rgb_to_hex,
    calculate_luminance,
    calculate_contrast_ratio,
    is_wcag_aa_compliant,
    generate_complementary_colors,
    validate_hex_color,
    safe_color_or_default,
)
from .template_themes import (
    PROFESSIONAL_PALETTES,
    MODERN_PALETTES,
    EXECUTIVE_PALETTES,
    MINIMAL_PALETTES,
    CREATIVE_PALETTES,
    TECHNICAL_PALETTES,
    TemplateThemeManager,
    ROLE_TEMPLATE_RECOMMENDATIONS,
)


# =============================================================================
# Custom Hypothesis Strategies
# =============================================================================

def hex_color_strategy():
    """Generate valid hex colors for testing"""
    return st.builds(
        lambda r, g, b: f'#{r:02x}{g:02x}{b:02x}',
        st.integers(min_value=0, max_value=255),
        st.integers(min_value=0, max_value=255),
        st.integers(min_value=0, max_value=255),
    )


def rgb_strategy():
    """Generate valid RGB tuples"""
    return st.tuples(
        st.integers(min_value=0, max_value=255),
        st.integers(min_value=0, max_value=255),
        st.integers(min_value=0, max_value=255),
    )


# =============================================================================
# Unit Tests - Color Utilities
# =============================================================================

class ColorUtilsUnitTests(TestCase):
    """Unit tests for color utility functions"""
    
    def test_hex_to_rgb_basic(self):
        """Test hex to RGB conversion with known values"""
        self.assertEqual(hex_to_rgb('#000000'), (0, 0, 0))
        self.assertEqual(hex_to_rgb('#ffffff'), (255, 255, 255))
        self.assertEqual(hex_to_rgb('#ff0000'), (255, 0, 0))
        self.assertEqual(hex_to_rgb('#4a9d9a'), (74, 157, 154))
    
    def test_hex_to_rgb_without_hash(self):
        """Test hex to RGB works without # prefix"""
        self.assertEqual(hex_to_rgb('4a9d9a'), (74, 157, 154))
    
    def test_rgb_to_hex_basic(self):
        """Test RGB to hex conversion with known values"""
        self.assertEqual(rgb_to_hex(0, 0, 0), '#000000')
        self.assertEqual(rgb_to_hex(255, 255, 255), '#ffffff')
        self.assertEqual(rgb_to_hex(255, 0, 0), '#ff0000')
        self.assertEqual(rgb_to_hex(74, 157, 154), '#4a9d9a')
    
    def test_luminance_black_white(self):
        """Test luminance calculation for black and white"""
        self.assertAlmostEqual(calculate_luminance('#000000'), 0.0, places=4)
        self.assertAlmostEqual(calculate_luminance('#ffffff'), 1.0, places=4)
    
    def test_contrast_ratio_black_white(self):
        """Test contrast ratio between black and white is 21:1"""
        ratio = calculate_contrast_ratio('#000000', '#ffffff')
        self.assertAlmostEqual(ratio, 21.0, places=1)
    
    def test_wcag_aa_black_on_white(self):
        """Test that black on white passes WCAG AA"""
        self.assertTrue(is_wcag_aa_compliant('#000000', '#ffffff'))
    
    def test_wcag_aa_low_contrast_fails(self):
        """Test that low contrast colors fail WCAG AA"""
        # Light gray on white should fail
        self.assertFalse(is_wcag_aa_compliant('#cccccc', '#ffffff'))
    
    def test_validate_hex_color(self):
        """Test hex color validation"""
        self.assertTrue(validate_hex_color('#4a9d9a'))
        self.assertTrue(validate_hex_color('4a9d9a'))
        self.assertTrue(validate_hex_color('#FFFFFF'))
        self.assertFalse(validate_hex_color('#gggggg'))
        self.assertFalse(validate_hex_color('invalid'))
        self.assertFalse(validate_hex_color('#fff'))  # 3-char not supported
    
    def test_safe_color_or_default(self):
        """Test safe color fallback"""
        self.assertEqual(safe_color_or_default('#4a9d9a'), '#4a9d9a')
        self.assertEqual(safe_color_or_default('invalid'), '#4a9d9a')
        self.assertEqual(safe_color_or_default('', '#000000'), '#000000')


# =============================================================================
# Property Tests - Color Utilities
# =============================================================================

class ColorUtilsPropertyTests(HypothesisTestCase):
    """
    Property-based tests for color utilities.
    
    **Feature: template-system-redesign, Property 2: WCAG Color Contrast Compliance**
    **Validates: Requirements 2.4, 8.5**
    """
    
    @given(hex_color_strategy())
    @settings(max_examples=100)
    def test_hex_rgb_roundtrip(self, hex_color):
        """
        Property: Hex to RGB to Hex roundtrip produces equivalent color.
        
        *For any* valid hex color, converting to RGB and back to hex
        should produce the same color (case-insensitive).
        """
        r, g, b = hex_to_rgb(hex_color)
        result = rgb_to_hex(r, g, b)
        self.assertEqual(hex_color.lower(), result.lower())
    
    @given(rgb_strategy())
    @settings(max_examples=100)
    def test_rgb_hex_roundtrip(self, rgb):
        """
        Property: RGB to Hex to RGB roundtrip produces same values.
        
        *For any* valid RGB tuple, converting to hex and back to RGB
        should produce the same values.
        """
        r, g, b = rgb
        hex_color = rgb_to_hex(r, g, b)
        result = hex_to_rgb(hex_color)
        self.assertEqual((r, g, b), result)
    
    @given(hex_color_strategy())
    @settings(max_examples=100)
    def test_luminance_in_valid_range(self, hex_color):
        """
        Property: Luminance is always between 0 and 1.
        
        *For any* valid hex color, the calculated luminance
        should be in the range [0.0, 1.0].
        """
        luminance = calculate_luminance(hex_color)
        self.assertGreaterEqual(luminance, 0.0)
        self.assertLessEqual(luminance, 1.0)
    
    @given(hex_color_strategy(), hex_color_strategy())
    @settings(max_examples=100)
    def test_contrast_ratio_symmetric(self, color1, color2):
        """
        Property: Contrast ratio is symmetric.
        
        *For any* two colors, the contrast ratio should be the same
        regardless of which color is first.
        """
        ratio1 = calculate_contrast_ratio(color1, color2)
        ratio2 = calculate_contrast_ratio(color2, color1)
        self.assertAlmostEqual(ratio1, ratio2, places=10)
    
    @given(hex_color_strategy(), hex_color_strategy())
    @settings(max_examples=100)
    def test_contrast_ratio_valid_range(self, color1, color2):
        """
        Property: Contrast ratio is always between 1 and 21.
        
        *For any* two colors, the contrast ratio should be
        in the range [1.0, 21.0].
        """
        ratio = calculate_contrast_ratio(color1, color2)
        self.assertGreaterEqual(ratio, 1.0)
        self.assertLessEqual(ratio, 21.0)
    
    @given(hex_color_strategy())
    @settings(max_examples=100)
    def test_contrast_with_self_is_one(self, hex_color):
        """
        Property: Contrast ratio of a color with itself is 1.
        
        *For any* color, the contrast ratio with itself should be 1.0.
        """
        ratio = calculate_contrast_ratio(hex_color, hex_color)
        self.assertAlmostEqual(ratio, 1.0, places=10)


class WCAGCompliancePropertyTests(TestCase):
    """
    Property tests for WCAG compliance across all template palettes.
    
    **Feature: template-system-redesign, Property 2: WCAG Color Contrast Compliance**
    **Validates: Requirements 2.4, 8.5**
    
    *For any* color palette in the Template_System, the contrast ratio between
    text_primary and background colors SHALL be at least 4.5:1 (WCAG AA standard).
    """
    
    def test_all_professional_palettes_wcag_compliant(self):
        """All Professional template palettes meet WCAG AA for text contrast"""
        for palette in PROFESSIONAL_PALETTES:
            # Text primary on background
            ratio = calculate_contrast_ratio(palette.text_primary, palette.background)
            self.assertGreaterEqual(
                ratio, 4.5,
                f"Palette '{palette.name}': text_primary on background ratio {ratio:.2f} < 4.5"
            )
            
            # Text secondary on background
            ratio = calculate_contrast_ratio(palette.text_secondary, palette.background)
            self.assertGreaterEqual(
                ratio, 4.5,
                f"Palette '{palette.name}': text_secondary on background ratio {ratio:.2f} < 4.5"
            )
    
    def test_all_modern_palettes_wcag_compliant(self):
        """All Modern template palettes meet WCAG AA for text contrast"""
        for palette in MODERN_PALETTES:
            ratio = calculate_contrast_ratio(palette.text_primary, palette.background)
            self.assertGreaterEqual(
                ratio, 4.5,
                f"Palette '{palette.name}': text_primary on background ratio {ratio:.2f} < 4.5"
            )
    
    def test_all_executive_palettes_wcag_compliant(self):
        """All Executive template palettes meet WCAG AA for text contrast"""
        for palette in EXECUTIVE_PALETTES:
            ratio = calculate_contrast_ratio(palette.text_primary, palette.background)
            self.assertGreaterEqual(
                ratio, 4.5,
                f"Palette '{palette.name}': text_primary on background ratio {ratio:.2f} < 4.5"
            )


# =============================================================================
# Property Tests - Color Palette Generation
# =============================================================================

class ColorPaletteGenerationPropertyTests(HypothesisTestCase):
    """
    Property tests for complementary color generation.
    
    **Feature: template-system-redesign, Property 8: Color Palette Generation**
    **Validates: Requirements 8.3, 8.4**
    
    *For any* valid hex color input to generate_complementary_colors,
    the function SHALL return a dictionary containing keys: 'primary', 'secondary',
    'accent', 'text_on_primary', 'text_primary', 'text_secondary', where all
    color values are valid 7-character hex codes.
    """
    
    @given(hex_color_strategy())
    @settings(max_examples=100)
    def test_generated_palette_has_all_required_keys(self, primary_color):
        """
        Property: Generated palette contains all required keys.
        
        *For any* valid primary color, the generated palette should contain
        all required color keys.
        """
        palette = generate_complementary_colors(primary_color)
        
        required_keys = [
            'primary', 'secondary', 'accent',
            'text_on_primary', 'text_primary', 'text_secondary'
        ]
        
        for key in required_keys:
            self.assertIn(key, palette, f"Missing key: {key}")
    
    @given(hex_color_strategy())
    @settings(max_examples=100)
    def test_generated_colors_are_valid_hex(self, primary_color):
        """
        Property: All generated colors are valid hex codes.
        
        *For any* valid primary color, all colors in the generated palette
        should be valid 7-character hex codes (including #).
        """
        palette = generate_complementary_colors(primary_color)
        
        hex_pattern = re.compile(r'^#[0-9a-fA-F]{6}$')
        
        for key, color in palette.items():
            self.assertTrue(
                hex_pattern.match(color),
                f"Invalid hex color for {key}: {color}"
            )
    
    @given(hex_color_strategy())
    @settings(max_examples=100)
    def test_primary_color_preserved(self, primary_color):
        """
        Property: Primary color is preserved in output.
        
        *For any* valid primary color, the 'primary' key in the output
        should match the input color.
        """
        palette = generate_complementary_colors(primary_color)
        self.assertEqual(palette['primary'].lower(), primary_color.lower())
    
    @given(hex_color_strategy())
    @settings(max_examples=100)
    def test_text_on_primary_is_optimal(self, primary_color):
        """
        Property: Text on primary uses the color with better contrast.
        
        *For any* valid primary color, the text_on_primary color should
        be either white or dark text, whichever provides better contrast.
        """
        palette = generate_complementary_colors(primary_color)
        
        white_contrast = calculate_contrast_ratio('#ffffff', primary_color)
        dark_contrast = calculate_contrast_ratio('#1a1a1a', primary_color)
        
        # The chosen text color should be the one with better contrast
        if white_contrast >= dark_contrast:
            self.assertEqual(palette['text_on_primary'], '#ffffff')
        else:
            self.assertEqual(palette['text_on_primary'], '#1a1a1a')
    
    @given(hex_color_strategy())
    @settings(max_examples=100)
    def test_text_colors_are_standard(self, primary_color):
        """
        Property: Text colors use standard values.
        
        *For any* primary color, text_primary and text_secondary should
        be the standard dark text colors.
        """
        palette = generate_complementary_colors(primary_color)
        
        self.assertEqual(palette['text_primary'], '#1a1a1a')
        self.assertEqual(palette['text_secondary'], '#555555')


# =============================================================================
# Property Tests - Template Inventory Completeness
# =============================================================================

class TemplateInventoryPropertyTests(TestCase):
    """
    Property tests for template inventory completeness.
    
    **Feature: template-system-redesign, Property 1: Template Inventory Completeness**
    **Validates: Requirements 1.1, 1.5, 2.5**
    
    *For any* template in the Template_System, there SHALL exist at least one
    color palette, and the template SHALL have a valid slug, name, and category.
    """
    
    def test_all_templates_have_palettes(self):
        """All templates in the system have at least one color palette"""
        expected_templates = ['professional', 'modern', 'executive', 'minimal', 'creative', 'technical']
        
        for template_slug in expected_templates:
            palettes = TemplateThemeManager.get_palettes_for_template(template_slug)
            self.assertGreater(
                len(palettes), 0,
                f"Template '{template_slug}' has no color palettes"
            )
    
    def test_minimum_template_count(self):
        """System has at least 6 resume templates"""
        all_templates = list(TemplateThemeManager.TEMPLATE_PALETTES.keys())
        self.assertGreaterEqual(
            len(all_templates), 6,
            f"Expected at least 6 templates, found {len(all_templates)}"
        )
    
    def test_all_palettes_have_required_fields(self):
        """All palettes have required color fields"""
        required_fields = ['name', 'primary', 'secondary', 'accent', 
                          'text_primary', 'text_secondary', 'background']
        
        for template_slug, palettes in TemplateThemeManager.TEMPLATE_PALETTES.items():
            for palette in palettes:
                for field in required_fields:
                    self.assertTrue(
                        hasattr(palette, field),
                        f"Palette '{palette.name}' in '{template_slug}' missing field: {field}"
                    )
                    value = getattr(palette, field)
                    self.assertIsNotNone(
                        value,
                        f"Palette '{palette.name}' in '{template_slug}' has None for: {field}"
                    )
    
    def test_all_palette_colors_are_valid_hex(self):
        """All palette colors are valid hex codes"""
        hex_pattern = re.compile(r'^#[0-9a-fA-F]{6}$')
        color_fields = ['primary', 'secondary', 'accent', 'text_primary', 'text_secondary', 'background']
        
        for template_slug, palettes in TemplateThemeManager.TEMPLATE_PALETTES.items():
            for palette in palettes:
                for field in color_fields:
                    color = getattr(palette, field)
                    self.assertTrue(
                        hex_pattern.match(color),
                        f"Invalid hex in '{palette.name}' ({template_slug}): {field}={color}"
                    )


# =============================================================================
# Property Tests - Font Stack Consistency
# =============================================================================

class FontStackConsistencyTests(TestCase):
    """
    Property tests for font stack consistency.
    
    **Feature: template-system-redesign, Property 3: Font Stack Consistency**
    **Validates: Requirements 2.2**
    
    *For any* template style function, the CSS output SHALL include a font-family
    declaration with at least one web-safe fallback font.
    """
    
    def test_base_styles_have_font_family(self):
        """Base styles include font-family declarations"""
        from .pdf_generator import _get_base_styles
        
        css = _get_base_styles()
        self.assertIn(
            'font-family',
            css,
            "Base styles missing font-family declaration"
        )
    
    def test_base_styles_have_fallback_fonts(self):
        """Base styles include web-safe fallback fonts"""
        from .pdf_generator import _get_base_styles
        
        # Common web-safe fallback fonts
        fallback_fonts = ['Arial', 'sans-serif', 'serif', 'monospace', 'Helvetica']
        
        css = _get_base_styles()
        has_fallback = any(font in css for font in fallback_fonts)
        self.assertTrue(
            has_fallback,
            "Base styles missing web-safe fallback font"
        )
    
    def test_technical_template_has_monospace(self):
        """Technical template includes monospace font for code feel"""
        from .pdf_generator import _get_technical_styles
        
        css = _get_technical_styles('#4a9d9a')
        self.assertIn(
            'monospace',
            css,
            "Technical template missing monospace font"
        )
    
    def test_all_template_styles_valid_css(self):
        """All template style functions return valid CSS strings"""
        from .pdf_generator import (
            _get_professional_styles,
            _get_modern_styles,
            _get_executive_styles,
            _get_minimal_styles,
            _get_creative_styles,
            _get_technical_styles,
        )
        
        style_functions = [
            ('professional', _get_professional_styles),
            ('modern', _get_modern_styles),
            ('executive', _get_executive_styles),
            ('minimal', _get_minimal_styles),
            ('creative', _get_creative_styles),
            ('technical', _get_technical_styles),
        ]
        
        for name, style_func in style_functions:
            css = style_func('#4a9d9a')
            # Check it's a non-empty string with CSS-like content
            self.assertIsInstance(css, str)
            self.assertGreater(len(css), 100, f"Template '{name}' CSS too short")
            self.assertIn('{', css, f"Template '{name}' CSS missing opening brace")
            self.assertIn('}', css, f"Template '{name}' CSS missing closing brace")


# =============================================================================
# Property Tests - Role-Based Recommendations
# =============================================================================

class RoleBasedRecommendationTests(TestCase):
    """
    Property tests for role-based template recommendations.
    
    **Feature: template-system-redesign, Property 4: Role-Based Template Recommendations**
    **Validates: Requirements 3.3**
    
    *For any* role in ROLE_TEMPLATE_RECOMMENDATIONS, the recommended_template
    SHALL exist in the template system and have at least one palette.
    """
    
    def test_all_recommended_templates_exist(self):
        """All recommended templates exist in the system"""
        for role, recommendation in ROLE_TEMPLATE_RECOMMENDATIONS.items():
            template = recommendation['recommended_template']
            self.assertIn(
                template,
                TemplateThemeManager.TEMPLATE_PALETTES,
                f"Role '{role}' recommends non-existent template: {template}"
            )
    
    def test_all_alternative_templates_exist(self):
        """All alternative templates exist in the system"""
        for role, recommendation in ROLE_TEMPLATE_RECOMMENDATIONS.items():
            for template in recommendation.get('alternative_templates', []):
                self.assertIn(
                    template,
                    TemplateThemeManager.TEMPLATE_PALETTES,
                    f"Role '{role}' has non-existent alternative: {template}"
                )
    
    def test_recommendations_have_required_fields(self):
        """All role recommendations have required fields"""
        required_fields = ['recommended_template', 'recommended_palette', 'reasoning']
        
        for role, recommendation in ROLE_TEMPLATE_RECOMMENDATIONS.items():
            for field in required_fields:
                self.assertIn(
                    field,
                    recommendation,
                    f"Role '{role}' missing required field: {field}"
                )
    
    def test_minimum_role_coverage(self):
        """System covers minimum number of roles"""
        # Should cover at least 5 distinct roles
        self.assertGreaterEqual(
            len(ROLE_TEMPLATE_RECOMMENDATIONS), 5,
            f"Expected at least 5 role recommendations, found {len(ROLE_TEMPLATE_RECOMMENDATIONS)}"
        )


# =============================================================================
# Property Tests - New Template Palettes WCAG Compliance
# =============================================================================

class NewTemplatePalettesWCAGTests(TestCase):
    """
    WCAG compliance tests for new template palettes.
    
    **Feature: template-system-redesign, Property 2: WCAG Color Contrast Compliance**
    **Validates: Requirements 2.4, 8.5**
    """
    
    def test_all_minimal_palettes_wcag_compliant(self):
        """All Minimal template palettes meet WCAG AA for text contrast"""
        for palette in MINIMAL_PALETTES:
            ratio = calculate_contrast_ratio(palette.text_primary, palette.background)
            self.assertGreaterEqual(
                ratio, 4.5,
                f"Minimal palette '{palette.name}': text_primary on background ratio {ratio:.2f} < 4.5"
            )
    
    def test_all_creative_palettes_wcag_compliant(self):
        """All Creative template palettes meet WCAG AA for text contrast"""
        for palette in CREATIVE_PALETTES:
            ratio = calculate_contrast_ratio(palette.text_primary, palette.background)
            self.assertGreaterEqual(
                ratio, 4.5,
                f"Creative palette '{palette.name}': text_primary on background ratio {ratio:.2f} < 4.5"
            )
    
    def test_all_technical_palettes_wcag_compliant(self):
        """All Technical template palettes meet WCAG AA for text contrast"""
        for palette in TECHNICAL_PALETTES:
            ratio = calculate_contrast_ratio(palette.text_primary, palette.background)
            self.assertGreaterEqual(
                ratio, 4.5,
                f"Technical palette '{palette.name}': text_primary on background ratio {ratio:.2f} < 4.5"
            )


# =============================================================================
# Property Tests - Cover Letter Templates
# =============================================================================

class CoverLetterTemplateTests(TestCase):
    """
    Property tests for cover letter template system.
    
    **Feature: template-system-redesign, Property 5: Cover Letter Template Count**
    **Validates: Requirements 5.1, 5.3**
    
    *For any* cover letter template in the system, there SHALL be at least 3
    distinct templates with different tones.
    """
    
    def test_minimum_cover_letter_template_count(self):
        """System has at least 3 cover letter templates"""
        from .template_pairing import COVER_LETTER_TEMPLATES
        
        self.assertGreaterEqual(
            len(COVER_LETTER_TEMPLATES), 3,
            f"Expected at least 3 cover letter templates, found {len(COVER_LETTER_TEMPLATES)}"
        )
    
    def test_cover_letter_templates_have_required_fields(self):
        """All cover letter templates have required fields"""
        from .template_pairing import COVER_LETTER_TEMPLATES
        
        required_fields = ['name', 'description', 'tone']
        
        for slug, template in COVER_LETTER_TEMPLATES.items():
            for field in required_fields:
                self.assertIn(
                    field,
                    template,
                    f"Cover letter template '{slug}' missing field: {field}"
                )
    
    def test_cover_letter_templates_have_distinct_tones(self):
        """Cover letter templates have distinct tones"""
        from .template_pairing import COVER_LETTER_TEMPLATES
        
        tones = [t['tone'] for t in COVER_LETTER_TEMPLATES.values()]
        unique_tones = set(tones)
        
        # Should have at least 2 distinct tones
        self.assertGreaterEqual(
            len(unique_tones), 2,
            f"Expected at least 2 distinct tones, found {len(unique_tones)}: {unique_tones}"
        )


class ResumeCoverLetterPairingTests(TestCase):
    """
    Property tests for resume-cover letter color consistency.
    
    **Feature: template-system-redesign, Property 6: Resume-Cover Letter Color Consistency**
    **Validates: Requirements 5.2, 6.1, 6.3**
    
    *For any* resume template, there SHALL exist a paired cover letter template,
    and the pairing SHALL maintain color consistency.
    """
    
    def test_all_resume_templates_have_pairs(self):
        """All resume templates have cover letter pairings"""
        from .template_pairing import TEMPLATE_PAIRS
        from .template_themes import TemplateThemeManager
        
        for template_slug in TemplateThemeManager.TEMPLATE_PALETTES.keys():
            self.assertIn(
                template_slug,
                TEMPLATE_PAIRS,
                f"Resume template '{template_slug}' has no cover letter pairing"
            )
    
    def test_paired_cover_letter_templates_exist(self):
        """All paired cover letter templates exist"""
        from .template_pairing import TEMPLATE_PAIRS, COVER_LETTER_TEMPLATES
        
        for resume_slug, pair_info in TEMPLATE_PAIRS.items():
            primary = pair_info['primary']
            self.assertIn(
                primary,
                COVER_LETTER_TEMPLATES,
                f"Resume '{resume_slug}' pairs with non-existent cover letter: {primary}"
            )
            
            for alt in pair_info.get('alternatives', []):
                self.assertIn(
                    alt,
                    COVER_LETTER_TEMPLATES,
                    f"Resume '{resume_slug}' has non-existent alternative: {alt}"
                )
    
    def test_apply_branding_returns_required_colors(self):
        """apply_resume_branding_to_cover_letter returns required color keys"""
        from .template_pairing import apply_resume_branding_to_cover_letter
        
        required_keys = ['primary_color', 'header_color', 'accent_color', 'text_color']
        
        # Test with various colors and templates
        test_cases = [
            ('#4a9d9a', 'classic'),
            ('#1e3a5f', 'modern'),
            ('#e74c3c', 'creative'),
        ]
        
        for color, template in test_cases:
            result = apply_resume_branding_to_cover_letter(color, template)
            for key in required_keys:
                self.assertIn(
                    key,
                    result,
                    f"Missing key '{key}' for color={color}, template={template}"
                )
    
    def test_apply_branding_preserves_primary_color(self):
        """apply_resume_branding_to_cover_letter preserves the primary color"""
        from .template_pairing import apply_resume_branding_to_cover_letter
        
        test_colors = ['#4a9d9a', '#1e3a5f', '#e74c3c', '#2ecc71']
        
        for color in test_colors:
            result = apply_resume_branding_to_cover_letter(color, 'modern')
            self.assertEqual(
                result['primary_color'].lower(),
                color.lower(),
                f"Primary color not preserved: expected {color}, got {result['primary_color']}"
            )


class CoverLetterStructureTests(TestCase):
    """
    Property tests for cover letter structure completeness.
    
    **Feature: template-system-redesign, Property 7: Cover Letter Structure Completeness**
    **Validates: Requirements 5.6**
    
    *For any* cover letter template, the generated HTML SHALL include sections for:
    header, date, recipient, salutation, body, closing, and signature.
    """
    
    def test_cover_letter_html_has_required_sections(self):
        """Cover letter HTML includes all required sections"""
        from .pdf_generator import (
            _build_classic_cover_letter,
            _build_modern_cover_letter,
            _build_creative_cover_letter,
        )
        
        # Create a mock cover letter object
        class MockCoverLetter:
            full_name = "John Doe"
            email = "john@example.com"
            phone = "555-1234"
            linkedin = "linkedin.com/in/johndoe"
            address = "123 Main St"
            company_name = "Acme Corp"
            position_title = "Software Engineer"
            hiring_manager = "Jane Smith"
            opening_paragraph = "I am writing to apply..."
            body_paragraph = "My experience includes..."
            closing_paragraph = "Thank you for your consideration."
        
        mock_cl = MockCoverLetter()
        today = "January 13, 2026"
        
        builders = [
            ('classic', _build_classic_cover_letter),
            ('modern', _build_modern_cover_letter),
            ('creative', _build_creative_cover_letter),
        ]
        
        required_elements = [
            ('header', '.header'),
            ('date', '.date'),
            ('recipient', '.recipient'),
            ('salutation', '.salutation'),
            ('content', '.content'),
            ('closing', '.closing'),
        ]
        
        for name, builder in builders:
            html = builder(mock_cl, '#4a9d9a', today)
            
            for element_name, css_class in required_elements:
                self.assertIn(
                    css_class,
                    html,
                    f"Cover letter '{name}' missing {element_name} section ({css_class})"
                )


# =============================================================================
# Property Tests - PDF Generation Consistency
# =============================================================================

class PDFGenerationConsistencyTests(TestCase):
    """
    Property tests for PDF generation consistency.
    
    **Feature: template-system-redesign, Property 9: PDF Generation Consistency**
    **Validates: Requirements 10.4**
    
    *For any* template, the build_resume_html function SHALL produce valid HTML
    that can be rendered consistently.
    """
    
    def test_all_templates_produce_valid_html(self):
        """All templates produce valid HTML structure"""
        from .pdf_generator import build_resume_html
        
        # Create a mock resume object
        class MockResume:
            full_name = "John Doe"
            role_title = "Software Engineer"
            email = "john@example.com"
            phone = "555-1234"
            location = "San Francisco, CA"
            address = "123 Main St"
            linkedin = "linkedin.com/in/johndoe"
            github = "github.com/johndoe"
            summary = "Experienced software engineer with 10 years of experience."
            skills = ["Python", "JavaScript", "Docker", "Kubernetes"]
            languages = ["English", "Spanish"]
            education = [
                {"degree": "BS", "field": "Computer Science", "school": "MIT", "graduation_date": "2015"}
            ]
            experience = [
                {
                    "role": "Senior Engineer",
                    "company": "Tech Corp",
                    "start_date": "2020",
                    "end_date": "Present",
                    "bullets": ["Led team of 5 engineers", "Improved performance by 50%"]
                }
            ]
            primary_color = "#4a9d9a"
            profile_photo = None
            
            class template:
                slug = "professional"
                primary_color = "#4a9d9a"
        
        # Test each template slug
        template_slugs = ['professional', 'modern', 'executive', 'minimal', 'creative', 'technical']
        
        for slug in template_slugs:
            MockResume.template.slug = slug
            mock_resume = MockResume()
            
            html = build_resume_html(mock_resume)
            
            # Verify basic HTML structure
            self.assertIn('<!DOCTYPE html>', html, f"Template '{slug}' missing DOCTYPE")
            self.assertIn('<html>', html, f"Template '{slug}' missing html tag")
            self.assertIn('<head>', html, f"Template '{slug}' missing head tag")
            self.assertIn('<body>', html, f"Template '{slug}' missing body tag")
            self.assertIn('</html>', html, f"Template '{slug}' missing closing html tag")
            
            # Verify resume content is included
            self.assertIn('John Doe', html, f"Template '{slug}' missing name")
            self.assertIn('Software Engineer', html, f"Template '{slug}' missing role")
    
    def test_all_templates_include_styles(self):
        """All templates include CSS styles"""
        from .pdf_generator import build_resume_html
        
        class MockResume:
            full_name = "Test User"
            role_title = "Developer"
            email = "test@example.com"
            phone = "555-0000"
            location = "NYC"
            address = ""
            linkedin = ""
            github = ""
            summary = "Test summary"
            skills = ["Skill1"]
            languages = []
            education = []
            experience = []
            primary_color = "#4a9d9a"
            profile_photo = None
            
            class template:
                slug = "professional"
                primary_color = "#4a9d9a"
        
        template_slugs = ['professional', 'modern', 'executive', 'minimal', 'creative', 'technical']
        
        for slug in template_slugs:
            MockResume.template.slug = slug
            mock_resume = MockResume()
            
            html = build_resume_html(mock_resume)
            
            # Verify styles are included
            self.assertIn('<style>', html, f"Template '{slug}' missing style tag")
            self.assertIn('</style>', html, f"Template '{slug}' missing closing style tag")
            
            # Verify A4 page setup
            self.assertIn('@page', html, f"Template '{slug}' missing @page rule")
    
    def test_template_color_application(self):
        """Templates correctly apply primary color"""
        from .pdf_generator import build_resume_html
        
        class MockResume:
            full_name = "Color Test"
            role_title = "Tester"
            email = "test@example.com"
            phone = ""
            location = ""
            address = ""
            linkedin = ""
            github = ""
            summary = ""
            skills = []
            languages = []
            education = []
            experience = []
            primary_color = "#e74c3c"  # Custom red color
            profile_photo = None
            
            class template:
                slug = "professional"
                primary_color = "#4a9d9a"
        
        mock_resume = MockResume()
        html = build_resume_html(mock_resume)
        
        # The custom primary color should be used
        self.assertIn('#e74c3c', html, "Custom primary color not applied")
