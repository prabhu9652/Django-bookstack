# Implementation Plan: Roadmap Skills Enhancement

## Overview

This implementation plan covers adding dynamic skill chips to the "Start Your Journey" section of roadmap path detail pages. The implementation follows Django best practices and integrates with the existing roadmap application.

## Tasks

- [x] 1. Create JourneySkill model
  - [x] 1.1 Add JourneySkill model to roadmap/models.py
    - Add model with fields: name, icon_class, roadmap_path (FK), display_order, is_active
    - Add Meta class with ordering and verbose names
    - Add __str__ method
    - _Requirements: 1.1, 1.2, 1.4, 1.5_

  - [x] 1.2 Create and run migration
    - Generate migration file with makemigrations
    - Run migrate to apply changes
    - _Requirements: 1.1_

- [x] 2. Configure Django Admin
  - [x] 2.1 Add JourneySkillAdmin to roadmap/admin.py
    - Configure list_display with name, roadmap_path, icon_class, display_order, is_active
    - Add list_filter for roadmap_path and is_active
    - Add search_fields for name
    - Add list_editable for display_order and is_active
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [x] 2.2 Add JourneySkillInline to RoadmapPathAdmin
    - Create TabularInline for JourneySkill
    - Add inline to RoadmapPathAdmin inlines list
    - _Requirements: 2.5_

- [x] 3. Update view layer
  - [x] 3.1 Update path_detail view in roadmap/views.py
    - Import JourneySkill model
    - Query active journey skills for current roadmap_path
    - Order by display_order ascending
    - Add journey_skills to context
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 4. Update template
  - [x] 4.1 Add journey skills section to path_detail.html
    - Locate "Start Your Journey" section (roadmap-start div)
    - Add journey-skills-container after start-label
    - Implement skill chip loop with icon and name
    - Add CSS custom property for animation delay
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

  - [x] 4.2 Add CSS styles for skill chips
    - Add journey-skills-container styles
    - Add journey-skills-grid with responsive layout
    - Add journey-skill-chip styles with icon and text
    - _Requirements: 4.5_

  - [x] 4.3 Add CSS animations
    - Add fade-in keyframe animation
    - Add staggered animation delay (50-100ms per chip)
    - Add hover elevation/glow effect
    - Add prefers-reduced-motion media query
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 5. Create initial data migration
  - [x] 5.1 Create data migration for initial skills
    - Create migration file with RunPython operation
    - Add DevOps/SRE skills (AWS, Azure, GCP, DigitalOcean, AWS Migration, Terraform, Terragrunt, Shell Scripting, Docker, Kubernetes, Jenkins, Ansible, Puppet, Packer, Python, Git, GitHub, Bitbucket, GitLab, Bamboo, GitLab CI/CD, GitHub Actions)
    - Add Full-Stack skills (Python, JavaScript, TypeScript, Java, Go, React, Vue.js, Node.js, Django, FastAPI, PostgreSQL, MySQL, MongoDB, Redis, REST APIs, GraphQL, Docker, Kubernetes, Git, CI/CD, AWS, System Design)
    - Add Data Science/ML skills (Python, R, SQL, Scala, TensorFlow, PyTorch, Scikit-learn, Keras, Pandas, NumPy, Spark, Airflow, AWS SageMaker, MLflow, Docker, Matplotlib, Seaborn, Tableau, PostgreSQL, MongoDB, BigQuery)
    - Assign appropriate Font Awesome icons
    - Set is_active=True and sequential display_order
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [x] 5.2 Run data migration
    - Apply migration to populate initial skills
    - Verify skills appear in admin
    - _Requirements: 6.1, 6.2, 6.3_

- [x] 6. Checkpoint - Verify implementation
  - Ensure all migrations applied successfully
  - Verify admin interface works correctly
  - Test all three roadmap paths display skills
  - Verify animations work as expected
  - Ask the user if questions arise

- [x] 7. Write property tests
  - [x] 7.1 Write property test for ordering
    - **Property 1: Journey Skills Ordering**
    - **Validates: Requirements 1.5, 3.2**
    - Use hypothesis to generate random skills with various display_order values
    - Verify query results are always in ascending order

  - [x] 7.2 Write property test for filtering
    - **Property 2: Active Skills Filtering**
    - **Validates: Requirements 3.1**
    - Use hypothesis to generate skills with mixed is_active values
    - Verify filter returns only active skills for correct path

- [x] 8. Final checkpoint
  - Ensure all tests pass
  - Verify no changes to existing roadmap layout
  - Ask the user if questions arise

## Notes

- All tasks are required for comprehensive implementation
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- The implementation only modifies the "Start Your Journey" section - no changes to existing layout
