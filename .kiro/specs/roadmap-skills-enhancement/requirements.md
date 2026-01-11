# Requirements Document

## Introduction

This feature enhances the "Start Your Journey" section on roadmap path detail pages by adding dynamically managed skill chips/pills that are specific to each roadmap path. Skills will be managed through Django Admin and displayed with subtle, professional animations. This enhancement applies to all three roadmap paths: DevOps/SRE, Full-Stack Development, and Data Science/Machine Learning.

## Glossary

- **Journey_Skill**: A skill/technology displayed in the "Start Your Journey" section, managed via Django Admin
- **Roadmap_Path**: An existing career roadmap path (DevOps/SRE, Full-Stack Development, DSML)
- **Skill_Chip**: A visual pill/card component displaying a single skill with icon and name
- **Admin_Panel**: Django Admin interface for managing Journey Skills
- **Animation_System**: CSS-based animations for fade-in, stagger, and hover effects

## Requirements

### Requirement 1: Journey Skill Data Model

**User Story:** As an administrator, I want to manage skills for the "Start Your Journey" section through Django Admin, so that I can add, edit, remove, and organize skills without code changes.

#### Acceptance Criteria

1. THE Journey_Skill model SHALL have fields for name, icon_class, roadmap_path (foreign key), display_order, and is_active
2. THE Journey_Skill model SHALL NOT have any level classification (no beginner/intermediate/advanced)
3. WHEN a Journey_Skill is created, THE Admin_Panel SHALL allow assignment to a specific Roadmap_Path
4. THE Journey_Skill model SHALL support Font Awesome icon classes for visual representation
5. WHEN display_order is set, THE system SHALL use it to control the rendering sequence of skills

### Requirement 2: Django Admin Configuration

**User Story:** As an administrator, I want a user-friendly admin interface for Journey Skills, so that I can efficiently manage skills for each roadmap path.

#### Acceptance Criteria

1. THE Admin_Panel SHALL display Journey_Skills with columns for name, roadmap_path, icon_class, display_order, and is_active
2. THE Admin_Panel SHALL allow filtering Journey_Skills by roadmap_path and is_active status
3. THE Admin_Panel SHALL allow searching Journey_Skills by name
4. THE Admin_Panel SHALL allow inline editing of display_order for quick reordering
5. WHEN viewing a Roadmap_Path in admin, THE Admin_Panel SHALL show associated Journey_Skills as inline items

### Requirement 3: View Layer Integration

**User Story:** As a developer, I want the path_detail view to pass Journey Skills to the template, so that skills can be rendered dynamically.

#### Acceptance Criteria

1. WHEN the path_detail view is called, THE system SHALL query active Journey_Skills for the current roadmap_path
2. THE system SHALL order Journey_Skills by display_order ascending
3. THE system SHALL pass the Journey_Skills queryset to the template context as 'journey_skills'
4. IF no Journey_Skills exist for a path, THE system SHALL pass an empty queryset (no errors)

### Requirement 4: Template Rendering

**User Story:** As a user, I want to see relevant skills displayed as chips/pills in the "Start Your Journey" section, so that I understand what technologies I'll learn.

#### Acceptance Criteria

1. WHEN journey_skills exist, THE template SHALL render each skill as a chip/pill component
2. THE Skill_Chip SHALL display the skill's icon (using icon_class) and name
3. THE template SHALL use the same component structure across all roadmap paths
4. IF no journey_skills exist, THE template SHALL hide the skills container gracefully
5. THE Skill_Chip layout SHALL be responsive: stacked on mobile, multi-row on tablet, grid on desktop

### Requirement 5: Animation System

**User Story:** As a user, I want subtle, professional animations on skill chips, so that the interface feels polished without being distracting.

#### Acceptance Criteria

1. WHEN the "Start Your Journey" section enters viewport, THE Skill_Chips SHALL fade-in with staggered timing (50-100ms delay between each)
2. WHEN a user hovers over a Skill_Chip, THE system SHALL apply a soft elevation or subtle glow effect
3. THE Animation_System SHALL NOT include flashy, heavy, or gamified effects
4. WHEN prefers-reduced-motion is enabled, THE Animation_System SHALL disable all animations
5. THE Animation_System SHALL use CSS transitions/animations only (no JavaScript animation libraries)

### Requirement 6: Initial Data Population

**User Story:** As an administrator, I want pre-populated skills for each roadmap path, so that the feature is immediately useful after deployment.

#### Acceptance Criteria

1. WHEN the migration runs, THE system SHALL create initial Journey_Skills for DevOps/SRE path (AWS, Azure, GCP, Terraform, Docker, Kubernetes, Jenkins, Ansible, Linux, Git, CI/CD, Prometheus)
2. WHEN the migration runs, THE system SHALL create initial Journey_Skills for Full-Stack Development path (Python, JavaScript, React, Node.js, Django, PostgreSQL, HTML/CSS, TypeScript, REST APIs, Git)
3. WHEN the migration runs, THE system SHALL create initial Journey_Skills for Data Science/ML path (Python, TensorFlow, PyTorch, Pandas, NumPy, Spark, SQL, Jupyter, Scikit-learn, Statistics)
4. THE initial Journey_Skills SHALL have appropriate Font Awesome icons assigned
5. THE initial Journey_Skills SHALL be created with is_active=True and sequential display_order

### Requirement 7: Preservation of Existing Layout

**User Story:** As a user, I want the existing roadmap layout to remain unchanged, so that my familiar navigation and progress tracking continue to work.

#### Acceptance Criteria

1. THE enhancement SHALL NOT modify the existing roadmap page header section
2. THE enhancement SHALL NOT modify the existing roadmap timeline/phases section
3. THE enhancement SHALL NOT modify the existing sidebar components
4. THE enhancement SHALL NOT modify the existing page actions section
5. THE enhancement SHALL only add content within the "Start Your Journey" node area
