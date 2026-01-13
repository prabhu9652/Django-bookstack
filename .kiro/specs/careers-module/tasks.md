# Implementation Plan: Careers Module

## Overview

This implementation plan breaks down the Careers Module into discrete, incremental tasks. Each task builds on previous work, ensuring no orphaned code. The module integrates with the existing Resume Builder for document selection during job applications.

## Tasks

- [x] 1. Set up Django app structure and models
  - [x] 1.1 Create careers Django app with initial structure
    - Run `python manage.py startapp careers`
    - Create app directory structure (templates, static, migrations)
    - Register app in `booksstore/settings.py` INSTALLED_APPS
    - _Requirements: 1.1, 2.1_

  - [x] 1.2 Implement JobPosting model
    - Create model with all fields: title, slug, department, location, location_type, employment_type, description, responsibilities, requirements, tech_stack, salary_range, is_active, closes_at, view_count, created_at, updated_at
    - Implement auto-slug generation in save() method
    - Add is_open() method for checking if job accepts applications
    - Add helper methods: get_responsibilities_list(), get_requirements_list()
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

  - [x] 1.3 Implement Application model
    - Create model with fields: job (FK), user (FK), resume (FK), cover_letter (FK optional), applicant_name, applicant_email, portfolio_url, linkedin_url, github_url, additional_notes, status, applied_at, updated_at
    - Add unique_together constraint for (job, user)
    - Implement save() to snapshot user data on creation
    - Define STATUS_CHOICES with default 'applied'
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [x] 1.4 Implement ApplicationNote model
    - Create model for admin internal notes
    - Fields: application (FK), author (FK), content, created_at
    - _Requirements: 8.8_

  - [x] 1.5 Create and run migrations
    - Generate migrations with `python manage.py makemigrations careers`
    - Apply migrations with `python manage.py migrate`
    - _Requirements: 1.1, 2.1_

  - [x] 1.6 Write property tests for models
    - **Property 1: Slug Generation Uniqueness**
    - **Property 3: Application Uniqueness Constraint**
    - **Property 4: Application Status Validity**
    - **Property 5: Applicant Data Snapshot Integrity**
    - **Property 6: Default Application Status**
    - **Validates: Requirements 1.3, 2.2, 2.3, 2.4, 2.5**

- [x] 2. Checkpoint - Ensure models are correct
  - Ensure all migrations run successfully
  - Verify models in Django admin
  - Ask the user if questions arise

- [x] 3. Implement URL routing and base views
  - [x] 3.1 Create careers/urls.py with all URL patterns
    - Public routes: careers_home, job_detail
    - Candidate routes: apply_job, my_applications, application_detail
    - Admin routes: admin_jobs_dashboard, admin_create_job, admin_edit_job, admin_applications_dashboard, admin_application_detail
    - API routes: api_submit_application, api_update_application_status, api_toggle_job_status, api_add_application_note
    - _Requirements: 3.1, 4.1, 5.1, 6.1, 7.1, 8.1_

  - [x] 3.2 Include careers URLs in main urls.py
    - Add `path('careers/', include('careers.urls'))` to booksstore/urls.py
    - _Requirements: 10.1_

  - [x] 3.3 Create superuser_required decorator
    - Create careers/decorators.py
    - Implement decorator that checks is_superuser and returns 403 if False
    - _Requirements: 7.1_

  - [x] 3.4 Write property test for admin access control
    - **Property 17: Admin Access Control**
    - **Validates: Requirements 7.1**

- [x] 4. Implement public views (Careers Landing & Job Details)
  - [x] 4.1 Implement careers_home view
    - Query active jobs using is_open() logic
    - Support filtering by department, location_type, employment_type
    - Support search by title/description
    - Pass job count for hero section
    - _Requirements: 3.2, 3.3, 3.5, 3.6, 3.7_

  - [x] 4.2 Create careers_home.html template
    - Hero section with hiring message and job count
    - Filter controls (department, location_type, employment_type dropdowns)
    - Search input
    - Job cards grid (3-column desktop, 1-column mobile)
    - Empty state when no jobs match
    - _Requirements: 3.2, 3.3, 3.4, 3.7, 3.8_

  - [x] 4.3 Create job_card.html partial template
    - Display: title, department, location, location_type badge, employment_type badge, posted date
    - Link to job detail page
    - _Requirements: 3.4_

  - [x] 4.4 Implement job_detail view
    - Fetch job by slug, increment view_count
    - Check if user has already applied
    - Check if job is open
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_

  - [x] 4.5 Create job_detail.html template
    - Full job information display
    - Responsibilities and requirements as lists
    - Tech stack as tags
    - Salary range (if provided)
    - Apply Now button with conditional states
    - Back to All Jobs link
    - _Requirements: 4.1, 4.2, 4.3, 4.5, 4.6, 4.7_

  - [x] 4.6 Write property tests for public views
    - **Property 2: Active Job Filtering**
    - **Property 7: Job Card Data Completeness**
    - **Property 8: Search Filter Accuracy**
    - **Property 9: Already Applied State**
    - **Property 10: Closed Job Message**
    - **Validates: Requirements 1.5, 3.3, 3.4, 3.6, 4.5, 4.6**

- [x] 5. Checkpoint - Verify public pages work
  - Test careers landing page displays correctly
  - Test job detail page with various states
  - Ensure all tests pass, ask the user if questions arise

- [x] 6. Implement candidate application flow
  - [x] 6.1 Implement apply_job view
    - Require login (redirect with return URL if not)
    - Check job is open, redirect with error if closed
    - Check for existing application, show message if duplicate
    - Pre-fill form with user data
    - Fetch user's resumes and cover letters for dropdowns
    - Handle empty resume case
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

  - [x] 6.2 Create apply_job.html template
    - Pre-filled name and email fields (readonly)
    - Resume dropdown (required) with "Create Resume" link if empty
    - Cover letter dropdown (optional)
    - Optional URL fields: portfolio, LinkedIn, GitHub
    - Additional notes textarea
    - Submit button
    - _Requirements: 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

  - [x] 6.3 Implement api_submit_application endpoint
    - Validate resume is selected
    - Validate URLs format
    - Create Application record
    - Return success with job title and date
    - Handle duplicate application error
    - _Requirements: 5.8, 5.9, 5.10, 11.1, 11.2, 11.5_

  - [x] 6.4 Create application success confirmation
    - Success message with job title and application date
    - Link to My Applications
    - _Requirements: 5.9_

  - [x] 6.5 Write property tests for application flow
    - **Property 11: Form Pre-fill Accuracy**
    - **Property 12: Resume Dropdown Population**
    - **Property 13: Resume Required Validation**
    - **Property 14: Application Submission Creates Record**
    - **Property 20: URL Validation**
    - **Validates: Requirements 5.2, 5.3, 5.8, 5.10, 11.5**

- [x] 7. Implement My Applications dashboard
  - [x] 7.1 Implement my_applications view
    - Require login
    - Query user's applications ordered by applied_at desc
    - Support filtering by status
    - _Requirements: 6.1, 6.2, 6.7_

  - [x] 7.2 Create my_applications.html template
    - Status filter dropdown
    - Application cards with: job title, department, applied date, status badge
    - Empty state with link to Careers page
    - _Requirements: 6.2, 6.3, 6.4, 6.6_

  - [x] 7.3 Create status_badge.html partial
    - Color-coded badges: Applied (blue), Under Review (yellow), Interview (purple), Rejected (red), Hired (green)
    - _Requirements: 6.4_

  - [x] 7.4 Implement application_detail view (candidate)
    - Show application details
    - Display submitted resume/cover letter info
    - _Requirements: 6.5_

  - [x] 7.5 Create application_detail.html template (candidate)
    - Job information
    - Application status and date
    - Submitted documents info
    - _Requirements: 6.5_

  - [ ] 7.6 Write property tests for My Applications
    - **Property 15: My Applications Ordering**
    - **Property 16: Application Status Filter**
    - **Validates: Requirements 6.2, 6.7**

- [x] 8. Checkpoint - Verify candidate flow works
  - Test full application flow end-to-end
  - Test My Applications dashboard
  - Ensure all tests pass, ask the user if questions arise

- [x] 9. Implement admin job management
  - [x] 9.1 Implement admin_jobs_dashboard view
    - Require superuser
    - List all jobs with: title, department, status, application count, created date
    - Support filtering by status and department
    - _Requirements: 7.1, 7.2, 7.8_

  - [x] 9.2 Create admin/jobs_dashboard.html template
    - Filter controls
    - Jobs table with action buttons
    - Create new job button
    - _Requirements: 7.2, 7.8_

  - [x] 9.3 Implement admin_create_job view
    - Require superuser
    - Job creation form with all fields
    - _Requirements: 7.3_

  - [x] 9.4 Implement admin_edit_job view
    - Require superuser
    - Pre-filled form for editing
    - _Requirements: 7.4_

  - [x] 9.5 Create admin/job_form.html template
    - All job fields with appropriate inputs
    - Rich text areas for description, responsibilities, requirements
    - Tech stack as comma-separated or tag input
    - Active toggle and closes_at date picker
    - _Requirements: 7.3, 7.4, 7.5, 7.6_

  - [x] 9.6 Implement api_toggle_job_status endpoint
    - Toggle is_active without affecting applications
    - _Requirements: 7.5, 7.7_

  - [ ] 9.7 Write property test for job toggle
    - **Property 18: Job Toggle Preserves Applications**
    - **Validates: Requirements 7.7**

- [x] 10. Implement admin applications dashboard
  - [x] 10.1 Implement admin_applications_dashboard view
    - Require superuser
    - List all applications across all jobs
    - Support filtering by job, status, date range
    - Support search by candidate name/email
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

  - [x] 10.2 Create admin/applications_dashboard.html template
    - Filter controls (job dropdown, status, date range)
    - Search input
    - Applications table with: candidate name, job title, applied date, status, actions
    - _Requirements: 8.2, 8.3, 8.4_

  - [x] 10.3 Implement admin_application_detail view
    - Require superuser
    - Full application details
    - Resume preview/download link
    - Cover letter display
    - Status update dropdown
    - Internal notes section
    - _Requirements: 8.5, 8.6, 8.7, 8.8, 8.9_

  - [x] 10.4 Create admin/application_detail.html template
    - Candidate info section
    - Resume preview (link to PDF)
    - Cover letter content
    - Links (portfolio, LinkedIn, GitHub)
    - Status dropdown with update button
    - Notes section with add form
    - _Requirements: 8.6, 8.7, 8.8, 8.9_

  - [x] 10.5 Implement api_update_application_status endpoint
    - Validate status value
    - Update status and updated_at timestamp
    - _Requirements: 9.1, 9.2_

  - [x] 10.6 Implement api_add_application_note endpoint
    - Create ApplicationNote record
    - _Requirements: 8.8_

  - [ ] 10.7 Write property test for status updates
    - **Property 19: Status Change Timestamp Update**
    - **Validates: Requirements 9.2**

- [x] 11. Checkpoint - Verify admin functionality
  - Test admin job management
  - Test admin applications dashboard
  - Ensure all tests pass, ask the user if questions arise

- [x] 12. Integrate with navigation and existing pages
  - [x] 12.1 Add "Careers" link to main navigation
    - Update base.html navbar
    - _Requirements: 10.1_

  - [x] 12.2 Add "My Applications" to user dropdown menu
    - Update user menu in base.html
    - Only show for logged-in users
    - _Requirements: 10.2_

  - [x] 12.3 Add "Apply to Jobs" quick action to Resume Builder dashboard
    - Update resume_builder/dashboard.html
    - _Requirements: 10.3_

  - [x] 12.4 Add admin links for Super Admins
    - Add "Manage Jobs" and "Applications" links visible only to superusers
    - _Requirements: 10.4_

- [ ] 13. Implement edge case handling
  - [ ] 13.1 Handle resume deletion gracefully
    - Verify SET_NULL behavior works correctly
    - Application remains accessible when resume is deleted
    - _Requirements: 11.3_

  - [ ] 13.2 Add job deletion confirmation
    - Modal confirmation when deleting job with applications
    - Option to close job instead of delete
    - _Requirements: 11.4_

  - [ ] 13.3 Add XSS sanitization
    - Ensure all user inputs are properly escaped in templates
    - _Requirements: 11.6_

  - [ ] 13.4 Write property test for resume deletion handling
    - **Property 21: Resume Deletion Handling**
    - **Validates: Requirements 11.3**

- [ ] 14. Add CSS styling
  - [ ] 14.1 Create careers/static/careers/css/careers.css
    - Status badge colors
    - Job card styling
    - Form styling
    - Admin table styling
    - Mobile responsive styles
    - _Requirements: 6.4, 12.1, 12.2, 12.3, 12.4, 12.5_

- [x] 15. Register models in Django admin
  - [x] 15.1 Create careers/admin.py
    - Register JobPosting with list display and filters
    - Register Application with list display and filters
    - Register ApplicationNote inline
    - _Requirements: 7.1_

- [ ] 16. Final checkpoint - Full integration test
  - Test complete candidate flow: browse → view → apply → track
  - Test complete admin flow: create job → review applications → update status
  - Verify navigation integration
  - Ensure all tests pass, ask the user if questions arise

## Notes

- All tasks including property-based tests are required for comprehensive validation
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- The implementation uses Python with Django, following existing patterns in resume_builder app
