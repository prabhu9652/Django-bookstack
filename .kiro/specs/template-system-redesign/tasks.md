# Implementation Plan: Template System Redesign

## Overview

This implementation plan breaks down the template system redesign into discrete, incremental tasks. Each task builds on previous work and includes testing requirements. The implementation uses Python/Django with Playwright for PDF generation.

## Tasks

- [x] 1. Database Model Updates
  - [x] 1.1 Add new fields to ResumeTemplate model
    - Add `display_order` (IntegerField, default=0)
    - Add `is_ats_safe` (BooleanField, default=True)
    - Add `recommended_roles` (JSONField, default=list)
    - _Requirements: 1.1, 1.5, 3.3_
  - [x] 1.2 Add new fields to CoverLetterTemplate model
    - Add `paired_resume_template` (ForeignKey to ResumeTemplate, nullable)
    - Add `display_order` (IntegerField, default=0)
    - Add `preview_image` (ImageField, optional)
    - _Requirements: 5.2, 6.1_
  - [x] 1.3 Create and run database migrations
    - Generate migrations for model changes
    - Apply migrations to database
    - _Requirements: 7.5_

- [x] 2. Color Utility System
  - [x] 2.1 Create color_utils.py module
    - Implement `hex_to_rgb()` function
    - Implement `rgb_to_hex()` function
    - Implement `calculate_luminance()` function
    - Implement `calculate_contrast_ratio()` function
    - Implement `is_wcag_aa_compliant()` function
    - Implement `generate_complementary_colors()` function
    - _Requirements: 2.4, 8.4, 8.5_
  - [x] 2.2 Write property test for WCAG contrast compliance
    - **Property 2: WCAG Color Contrast Compliance**
    - **Validates: Requirements 2.4, 8.5**
  - [x] 2.3 Write property test for color palette generation
    - **Property 8: Color Palette Generation**
    - **Validates: Requirements 8.3, 8.4**

- [x] 3. Checkpoint - Ensure color utilities work
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. New Resume Templates - Minimal Clean
  - [x] 4.1 Implement Minimal Clean template HTML builder
    - Create `_build_minimal_template()` function in pdf_generator.py
    - Single-column layout with maximum whitespace
    - Inline skills display with bullet separators
    - Clean typography hierarchy
    - _Requirements: 3.1, 1.6, 2.1_
  - [x] 4.2 Implement Minimal Clean template CSS
    - Create `_get_minimal_styles()` function
    - Centered header design
    - Subtle accent colors
    - Professional font stack
    - _Requirements: 2.2, 2.3_
  - [x] 4.3 Create database entry for Minimal Clean template
    - Add template to ResumeTemplate table
    - Set category='minimal', is_ats_safe=True
    - _Requirements: 1.1, 7.5_

- [x] 5. New Resume Templates - Creative Bold
  - [x] 5.1 Implement Creative Bold template HTML builder
    - Create `_build_creative_template()` function
    - Asymmetric two-column layout (narrow left, wide right)
    - Bold name block with color background
    - Skills with visual dot indicators
    - _Requirements: 3.1, 1.6_
  - [x] 5.2 Implement Creative Bold template CSS
    - Create `_get_creative_styles()` function
    - Color blocks for visual interest
    - Bold typography with large name
    - _Requirements: 2.1, 2.2_
  - [x] 5.3 Create database entry for Creative Bold template
    - Add template to ResumeTemplate table
    - Set category='creative'
    - _Requirements: 1.1, 7.5_

- [x] 6. New Resume Templates - Technical
  - [x] 6.1 Implement Technical template HTML builder
    - Create `_build_technical_template()` function
    - Skills prominently displayed in sidebar
    - Projects section emphasized
    - GitHub/LinkedIn in header
    - _Requirements: 3.1, 1.6_
  - [x] 6.2 Implement Technical template CSS
    - Create `_get_technical_styles()` function
    - Clean, scannable layout
    - Monospace accents for technical feel
    - _Requirements: 2.1, 2.2_
  - [x] 6.3 Create database entry for Technical template
    - Add template to ResumeTemplate table
    - Set category='modern', recommended_roles=['software_engineer', 'devops_sre']
    - _Requirements: 1.1, 3.3, 7.5_

- [x] 7. Checkpoint - Verify new templates render correctly
  - Ensure all tests pass, ask the user if questions arise.
  - Manually verify each template produces valid HTML
  - Verify PDF generation works for all templates

- [x] 8. Template Registry and Routing
  - [x] 8.1 Update pdf_generator.py template routing
    - Add routing for 'minimal', 'creative', 'technical' templates
    - Update `build_resume_html()` to handle new templates
    - _Requirements: 7.3, 7.4_
  - [x] 8.2 Write property test for template inventory completeness
    - **Property 1: Template Inventory Completeness**
    - **Validates: Requirements 1.1, 1.5, 2.5**
  - [x] 8.3 Write property test for font stack consistency
    - **Property 3: Font Stack Consistency**
    - **Validates: Requirements 2.2**

- [x] 9. Role-Based Recommendations
  - [x] 9.1 Update template_themes.py with role recommendations
    - Add recommendations for new templates
    - Update ROLE_TEMPLATE_RECOMMENDATIONS dictionary
    - _Requirements: 3.3_
  - [x] 9.2 Write property test for role-based recommendations
    - **Property 4: Role-Based Template Recommendations**
    - **Validates: Requirements 3.3**

- [x] 10. Cover Letter Template Enhancements
  - [x] 10.1 Create template_pairing.py module
    - Implement TEMPLATE_PAIRS dictionary
    - Implement `get_paired_cover_letter_template()` function
    - Implement `apply_resume_branding_to_cover_letter()` function
    - _Requirements: 5.2, 6.1, 6.3_
  - [x] 10.2 Write property test for cover letter template count
    - **Property 5: Cover Letter Template Count**
    - **Validates: Requirements 5.1, 5.3**
  - [x] 10.3 Write property test for resume-cover letter color consistency
    - **Property 6: Resume-Cover Letter Color Consistency**
    - **Validates: Requirements 5.2, 6.1, 6.3**

- [x] 11. Cover Letter Structure Validation
  - [x] 11.1 Add fourth cover letter template (if needed)
    - Ensure at least 4 distinct cover letter templates exist
    - Add 'formal' tone template if missing
    - _Requirements: 5.1, 5.3_
  - [x] 11.2 Write property test for cover letter structure
    - **Property 7: Cover Letter Structure Completeness**
    - **Validates: Requirements 5.6**

- [x] 12. Checkpoint - Verify cover letter system
  - Ensure all tests pass, ask the user if questions arise.
  - Verify cover letter PDF generation
  - Verify color pairing works correctly

- [x] 13. Template Selector UI Updates
  - [x] 13.1 Update resume_templates.html with category badges
    - Add category badge display to template cards
    - Add "Recommended" indicator for role-matched templates
    - _Requirements: 4.4_
  - [x] 13.2 Add template filtering by category
    - Add category filter buttons above template grid
    - Implement JavaScript filtering logic
    - _Requirements: 4.1_
  - [x] 13.3 Update cover_letter_templates.html with improvements
    - Apply same UI improvements as resume templates
    - Add tone badges to template cards
    - _Requirements: 5.1_

- [x] 14. Color Picker Integration
  - [x] 14.1 Add WCAG validation to color picker
    - Validate contrast when user selects custom color
    - Show warning if contrast is insufficient
    - _Requirements: 8.5_
  - [x] 14.2 Add complementary color preview
    - Show generated secondary/accent colors
    - Update preview in real-time
    - _Requirements: 8.4_

- [x] 15. Template Preview Images
  - [x] 15.1 Create fallback SVG previews for new templates
    - Create minimal.svg, creative.svg, technical.svg
    - Place in static/images/template_fallbacks/
    - _Requirements: 9.2_
  - [x] 15.2 Update template selector to use lazy loading
    - Add loading="lazy" to preview images
    - Implement skeleton loading states
    - _Requirements: 9.3, 4.5_

- [x] 16. Final Integration and Testing
  - [x] 16.1 Write property test for PDF generation consistency
    - **Property 9: PDF Generation Consistency**
    - **Validates: Requirements 10.4**
  - [x] 16.2 Run full test suite
    - Execute all property-based tests
    - Verify all templates generate valid PDFs
    - _Requirements: All_

- [x] 17. Final Checkpoint
  - All 49 tests pass
  - Preview matches PDF for all templates (Single Source of Truth architecture)
  - Live editing uses API for pixel-perfect preview

## Architectural Fix: Preview → PDF Mismatch (COMPLETED)

The root cause of the preview → PDF mismatch was identified and fixed:

**Problem:** Two separate sources of truth existed:
1. Django templates (`preview_resume.html`) with inline CSS for preview
2. `pdf_generator.py` with its own HTML builder for PDF

**Solution:** Single Source of Truth architecture:
1. Created API endpoints that use `build_resume_html()` from `pdf_generator.py`
2. Updated preview templates to fetch HTML from these APIs
3. Preview now renders the EXACT same HTML that Playwright uses for PDF

**New API Endpoints:**
- `POST /api/preview/resume/` - Generate preview HTML from form data
- `POST /api/preview/cover-letter/` - Generate cover letter preview HTML
- `GET /api/preview/resume/<id>/` - Get preview HTML for saved resume
- `GET /api/preview/cover-letter/<id>/` - Get preview HTML for saved cover letter

**Files Modified:**
- `resume_builder/views.py` - Added 4 new API endpoints
- `resume_builder/urls.py` - Added URL routes for new endpoints
- `resume_builder/templates/resume_builder/preview_resume.html` - Uses API for preview
- `resume_builder/templates/resume_builder/preview_cover_letter.html` - Uses API for preview

## Notes

- All tasks including property-based tests are required for comprehensive coverage
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties using Hypothesis (100 iterations minimum)
- Unit tests validate specific examples and edge cases
- The implementation preserves the existing preview → PDF → save pipeline

## Premium Live Editor Implementation (COMPLETED)

Implemented industry-standard split-screen live editor similar to premium SaaS products (cvwizard.com style):

**Features:**
- Left panel: Scrollable form editor with collapsible sections
- Right panel: Fixed live preview that updates in real-time (300ms debounce)
- Template selector modal for switching templates without losing data
- Color theme picker with 6 preset colors + custom color
- Photo upload for Professional template
- Zoom controls for preview
- Save to My Documents functionality
- Download PDF functionality

**New Files Created:**
- `resume_builder/templates/resume_builder/live_resume_editor.html` - Premium resume editor
- `resume_builder/templates/resume_builder/live_cover_letter_editor.html` - Premium cover letter editor

**New Views Added:**
- `live_resume_editor(request, template_id)` - Live resume editor view
- `live_cover_letter_editor(request, template_id)` - Live cover letter editor view

**New URL Routes:**
- `/resume-builder/live-resume/<template_id>/` - Live resume editor
- `/resume-builder/live-cover-letter/<template_id>/` - Live cover letter editor

**Key Implementation Details:**
- Uses existing `api_generate_preview_html` API for Single Source of Truth
- Preview updates on every keystroke (debounced 300ms)
- Same HTML rendered in preview as in PDF generation
- Responsive design for mobile/tablet
- All 6 resume templates supported: Professional, Modern, Executive, Minimal, Creative, Technical
- All 3 cover letter templates supported: Classic, Modern, Creative
