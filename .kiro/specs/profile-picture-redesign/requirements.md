# Requirements Document

## Introduction

This feature redesigns the profile picture experience in the Resume Builder's Professional template to match industry standards (LinkedIn, Google, Canva-style). The enhancement provides users with intuitive image cropping, zoom, and repositioning capabilities within a fixed 1:1 aspect ratio frame, along with live preview before saving. This feature only applies to the Professional template, as Modern and Executive templates do not include profile photos.

## Glossary

- **Crop_Modal**: A modal dialog that appears when uploading or editing a profile photo, containing the cropping interface
- **Crop_Area**: The fixed 1:1 aspect ratio frame within which the user positions their image
- **Zoom_Control**: A slider or button controls allowing users to zoom in/out on their image within the crop area
- **Drag_Reposition**: The ability to click and drag the image within the crop area to adjust positioning
- **Live_Preview**: Real-time preview of the cropped result before confirming
- **Initials_Avatar**: A fallback avatar displaying user's initials when no photo is uploaded
- **Photo_Options**: Existing customization controls for shape (circle/rounded/square), size (S/M/L), and position (top/center/bottom)

## Requirements

### Requirement 1: Image Upload Trigger

**User Story:** As a user, I want to click on the photo area or an upload button to select an image, so that I can easily add or replace my profile photo.

#### Acceptance Criteria

1. WHEN the user clicks the photo preview area, THE system SHALL open the file picker dialog
2. WHEN the user clicks the "Upload Photo" button, THE system SHALL open the file picker dialog
3. THE file picker SHALL accept only image formats (JPEG, PNG, WebP, GIF)
4. WHEN an image is selected, THE system SHALL immediately open the Crop_Modal
5. IF the user already has a photo, THE photo preview area SHALL show a hover overlay with "Change Photo" text

### Requirement 2: Crop Modal Interface

**User Story:** As a user, I want a dedicated modal for cropping my photo, so that I can focus on getting the perfect crop without distractions.

#### Acceptance Criteria

1. WHEN the Crop_Modal opens, THE modal SHALL appear at the TOP of the screen (not center) per project conventions
2. THE Crop_Modal SHALL have a dark semi-transparent backdrop with blur effect
3. THE Crop_Modal SHALL display the uploaded image within a cropping interface
4. THE Crop_Modal SHALL have a fixed 1:1 aspect ratio Crop_Area
5. THE Crop_Modal SHALL include action buttons: "Cancel" and "Apply"
6. WHEN the user clicks "Cancel", THE system SHALL close the modal without saving changes
7. WHEN the user clicks "Apply", THE system SHALL apply the crop and update the photo preview

### Requirement 3: Zoom Functionality

**User Story:** As a user, I want to zoom in and out on my photo, so that I can include more or less of the image in my profile picture.

#### Acceptance Criteria

1. THE Crop_Modal SHALL include a Zoom_Control (slider or +/- buttons)
2. THE Zoom_Control SHALL allow zooming from 1x (fit) to 3x magnification
3. WHEN the user adjusts zoom, THE image SHALL scale in real-time within the Crop_Area
4. THE zoom SHALL be centered on the current crop position
5. THE default zoom level SHALL be 1x (image fits within crop area)

### Requirement 4: Drag to Reposition

**User Story:** As a user, I want to drag my photo within the crop frame, so that I can position my face or subject exactly where I want it.

#### Acceptance Criteria

1. WHEN the user clicks and drags within the Crop_Area, THE image SHALL move accordingly
2. THE image SHALL NOT be draggable outside the Crop_Area boundaries (no empty space visible)
3. THE drag interaction SHALL work on both desktop (mouse) and mobile (touch)
4. THE cursor SHALL change to "grab" when hovering over the image, and "grabbing" when dragging
5. THE drag movement SHALL feel smooth and responsive (no lag)

### Requirement 5: Live Preview

**User Story:** As a user, I want to see a preview of my cropped photo before applying, so that I can be confident in my selection.

#### Acceptance Criteria

1. THE Crop_Modal SHALL display a Live_Preview of the final cropped result
2. THE Live_Preview SHALL update in real-time as the user zooms or repositions
3. THE Live_Preview SHALL respect the current Photo_Options (shape, size)
4. THE Live_Preview SHALL be positioned beside or below the crop area (responsive)

### Requirement 6: Replace and Remove Photo

**User Story:** As a user, I want to easily replace or remove my profile photo, so that I can update my resume as needed.

#### Acceptance Criteria

1. WHEN a photo exists, THE photo section SHALL show a "Replace" button/link
2. WHEN a photo exists, THE photo section SHALL show a "Remove" button/link
3. WHEN the user clicks "Replace", THE system SHALL open the file picker for a new image
4. WHEN the user clicks "Remove", THE system SHALL clear the photo and show the Initials_Avatar
5. THE Remove action SHALL NOT require confirmation (can be undone by uploading new photo)

### Requirement 7: Initials Avatar Fallback

**User Story:** As a user, I want to see my initials displayed when I don't have a profile photo, so that the resume still looks professional.

#### Acceptance Criteria

1. WHEN no photo is uploaded, THE system SHALL display an Initials_Avatar
2. THE Initials_Avatar SHALL use the first letter of first name and first letter of last name
3. IF only one name is provided, THE Initials_Avatar SHALL use the first two letters
4. THE Initials_Avatar SHALL use the current resume primary_color as background
5. THE Initials_Avatar SHALL respect the current Photo_Options (shape, size)
6. THE Initials_Avatar text SHALL be white with appropriate font size based on avatar size

### Requirement 8: Integration with Existing Photo Options

**User Story:** As a user, I want my existing photo customization options (shape, size, position) to work with the new cropping feature, so that I have full control over my photo appearance.

#### Acceptance Criteria

1. THE existing Photo_Options (shape, size, position) SHALL remain functional
2. THE cropped image SHALL be stored and applied independently of Photo_Options
3. WHEN Photo_Options change, THE preview SHALL update to reflect the new settings
4. THE crop data SHALL be preserved when Photo_Options are changed
5. THE PDF generator SHALL receive both crop data and Photo_Options for rendering

### Requirement 9: Mobile Responsiveness

**User Story:** As a user on mobile, I want the cropping interface to work well on my device, so that I can edit my resume photo on the go.

#### Acceptance Criteria

1. THE Crop_Modal SHALL be full-screen on mobile devices (< 768px)
2. THE touch gestures SHALL support pinch-to-zoom on mobile
3. THE Zoom_Control SHALL be easily tappable on mobile (minimum 44px touch target)
4. THE action buttons SHALL be large enough for comfortable tapping
5. THE Live_Preview SHALL stack below the crop area on mobile

### Requirement 10: Performance and File Handling

**User Story:** As a user, I want the cropping to be fast and not slow down my browser, so that I can quickly edit my photo.

#### Acceptance Criteria

1. THE system SHALL handle images up to 10MB in size
2. THE cropped result SHALL be compressed to a reasonable size (< 500KB)
3. THE cropping operation SHALL complete within 2 seconds on average hardware
4. THE system SHALL use client-side processing (no server round-trip for cropping)
5. IF an image is too large, THE system SHALL show a helpful error message

### Requirement 11: Accessibility

**User Story:** As a user with accessibility needs, I want the cropping interface to be usable with keyboard and screen readers.

#### Acceptance Criteria

1. THE Crop_Modal SHALL be keyboard navigable (Tab, Enter, Escape)
2. THE Zoom_Control SHALL be adjustable via keyboard (arrow keys)
3. THE modal SHALL trap focus while open
4. THE modal SHALL have appropriate ARIA labels and roles
5. WHEN prefers-reduced-motion is enabled, THE system SHALL disable animations

### Requirement 12: Preservation of Existing Functionality

**User Story:** As a user, I want all existing resume builder functionality to continue working, so that my workflow is not disrupted.

#### Acceptance Criteria

1. THE enhancement SHALL NOT modify the existing Save/Preview/My Documents flow
2. THE enhancement SHALL NOT modify the Modern or Executive templates
3. THE enhancement SHALL NOT change the existing form field structure
4. THE enhancement SHALL NOT affect the PDF generation for non-photo elements
5. THE enhancement SHALL maintain backward compatibility with existing saved resumes

