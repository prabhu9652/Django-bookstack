# Careers Module - Requirements Document

## Introduction

This module adds a professional Careers/Jobs portal to the platform, enabling users to browse job openings and submit applications using their existing Resume Builder documents. Super Admins can post jobs, review applications, and manage the hiring pipeline. The module integrates seamlessly with the existing ecosystem (Books, Library, Resume Builder, Roadmaps) and follows industry-standard hiring portal patterns used by companies like Stripe, Notion, and Linear.

## Glossary

- **Job_Posting**: A job opening created by Super Admin with title, description, requirements, and metadata
- **Application**: A user's submission for a specific job, linking their profile, resume, and optional cover letter
- **Application_Status**: The current state of an application (Applied, Under Review, Interview, Rejected, Hired)
- **Candidate**: A logged-in user who browses and applies for jobs
- **Super_Admin**: A user with `is_superuser=True` who manages job postings and reviews applications
- **My_Documents**: The user's saved resumes and cover letters from Resume Builder
- **ATS**: Applicant Tracking System - industry-standard approach to managing job applications

---

## Requirements

### Requirement 1: Job Posting Data Model

**User Story:** As a Super Admin, I want to create and manage job postings with all necessary details, so that candidates can find and apply for relevant positions.

#### Acceptance Criteria

1. THE Job_Posting model SHALL have fields: title, slug, department, location, location_type (remote/onsite/hybrid), employment_type (full-time/part-time/contract/internship), description, responsibilities, requirements, tech_stack, salary_range (optional), is_active, created_at, updated_at, closes_at
2. THE Job_Posting model SHALL support rich text for description, responsibilities, and requirements fields
3. WHEN a Job_Posting is created, THE system SHALL auto-generate a URL-friendly slug from the title
4. THE Job_Posting model SHALL track view_count for analytics
5. WHEN is_active is False OR closes_at has passed, THE job SHALL NOT appear in public listings

### Requirement 2: Application Data Model

**User Story:** As a system, I want to store application data linking candidates to jobs with their documents, so that the hiring process can be tracked efficiently.

#### Acceptance Criteria

1. THE Application model SHALL have fields: job (FK), user (FK), resume (FK to Resume), cover_letter (FK to CoverLetter, optional), status, portfolio_url, linkedin_url, github_url, additional_notes, applied_at, updated_at
2. THE Application model SHALL enforce unique_together on (job, user) to prevent duplicate applications
3. THE Application status choices SHALL be: applied, under_review, interview, rejected, hired
4. THE Application model SHALL store a snapshot of user's name and email at application time for data integrity
5. WHEN an Application is created, THE status SHALL default to "applied"

### Requirement 3: Careers Landing Page (Candidate)

**User Story:** As a candidate, I want to browse all open positions on a clean careers page, so that I can find jobs that match my skills.

#### Acceptance Criteria

1. THE Careers page SHALL be accessible from main navigation as "Careers" link
2. THE page SHALL display a hero section with company hiring message and job count
3. THE page SHALL list all active Job_Postings in a card-based grid layout
4. EACH job card SHALL display: title, department, location, location_type badge, employment_type badge, posted date
5. THE page SHALL support filtering by: department, location_type, employment_type
6. THE page SHALL support search by job title or keywords
7. WHEN no jobs match filters, THE page SHALL show an appropriate empty state
8. THE page SHALL be responsive and mobile-friendly

### Requirement 4: Job Details Page (Candidate)

**User Story:** As a candidate, I want to view complete job details before applying, so that I can determine if the role is right for me.

#### Acceptance Criteria

1. THE Job Details page SHALL display: title, department, location, employment_type, posted date, description, responsibilities (as list), requirements (as list), tech_stack (as tags)
2. THE page SHALL show salary_range if provided by admin
3. THE page SHALL have a prominent "Apply Now" CTA button
4. IF user is not logged in, THE "Apply Now" button SHALL redirect to login with return URL
5. IF user has already applied, THE button SHALL show "Already Applied" and be disabled
6. IF job is closed, THE page SHALL show "This position is no longer accepting applications"
7. THE page SHALL include a "Back to All Jobs" link

### Requirement 5: Application Flow (Candidate)

**User Story:** As a candidate, I want to apply for a job using my existing resume with minimal friction, so that I can submit applications quickly.

#### Acceptance Criteria

1. WHEN user clicks "Apply Now", THE system SHALL open an application modal/page
2. THE application form SHALL pre-fill: full name, email from user profile
3. THE form SHALL show a dropdown to select resume from My Documents (Resume Builder)
4. IF user has no resumes, THE form SHALL show a prompt with link to create one
5. THE form SHALL show an optional dropdown to select cover letter from My Documents
6. THE form SHALL include optional fields: portfolio_url, linkedin_url, github_url
7. THE form SHALL include an optional additional_notes textarea
8. WHEN form is submitted, THE system SHALL create an Application record
9. WHEN submission succeeds, THE system SHALL show a success confirmation with job title and application date
10. THE form SHALL validate that a resume is selected before submission

### Requirement 6: My Applications Dashboard (Candidate)

**User Story:** As a candidate, I want to track all my job applications and their statuses, so that I can manage my job search effectively.

#### Acceptance Criteria

1. THE My Applications page SHALL be accessible from user menu or Resume Builder dashboard
2. THE page SHALL list all user's applications sorted by applied_at descending
3. EACH application card SHALL show: job title, company/department, applied date, current status with color-coded badge
4. THE status badges SHALL use colors: Applied (blue), Under Review (yellow), Interview (purple), Rejected (red), Hired (green)
5. WHEN user clicks an application, THE system SHALL show application details including submitted resume/cover letter
6. IF user has no applications, THE page SHALL show empty state with link to Careers page
7. THE page SHALL support filtering by application status

### Requirement 7: Admin Job Management

**User Story:** As a Super Admin, I want to create, edit, and manage job postings, so that I can control what positions are available.

#### Acceptance Criteria

1. THE Admin Jobs page SHALL be accessible only to users with is_superuser=True
2. THE page SHALL list all Job_Postings with: title, department, status (active/closed), application count, created date
3. THE Admin SHALL be able to create new job postings via a form
4. THE Admin SHALL be able to edit existing job postings
5. THE Admin SHALL be able to toggle job active/inactive status
6. THE Admin SHALL be able to set/update closes_at date
7. WHEN Admin closes a job with pending applications, THE system SHALL keep applications intact
8. THE page SHALL support filtering by status (active/closed) and department

### Requirement 8: Admin Applications Dashboard

**User Story:** As a Super Admin, I want to view and manage all applications, so that I can efficiently review candidates and progress the hiring pipeline.

#### Acceptance Criteria

1. THE Admin Applications page SHALL show all applications across all jobs
2. THE page SHALL support filtering by: job, status, date range
3. THE page SHALL support search by candidate name or email
4. EACH application row SHALL show: candidate name, job title, applied date, status, action buttons
5. THE Admin SHALL be able to click to view full application details
6. THE application detail view SHALL show: candidate info, resume (PDF preview/download), cover letter, links, application notes
7. THE Admin SHALL be able to update application status via dropdown
8. THE Admin SHALL be able to add internal notes to applications
9. THE Admin SHALL be able to download candidate's resume as PDF

### Requirement 9: Application Status Management

**User Story:** As a Super Admin, I want to update application statuses and track candidate progress, so that I can manage the hiring pipeline effectively.

#### Acceptance Criteria

1. THE Admin SHALL be able to change status: applied → under_review → interview → hired/rejected
2. WHEN status changes, THE system SHALL record updated_at timestamp
3. THE system SHALL optionally notify candidate of status changes (future enhancement)
4. THE Admin SHALL be able to bulk-update statuses for multiple applications
5. THE system SHALL maintain an audit trail of status changes (future enhancement)

### Requirement 10: Navigation Integration

**User Story:** As a user, I want the Careers module to feel like a natural part of the platform, so that my experience is seamless.

#### Acceptance Criteria

1. THE main navigation SHALL include "Careers" link visible to all users
2. THE user dropdown menu SHALL include "My Applications" link for logged-in users
3. THE Resume Builder dashboard SHALL show "Apply to Jobs" quick action
4. THE Admin sidebar/menu SHALL include "Manage Jobs" and "Applications" links for Super Admins
5. THE Careers pages SHALL use the same design system (colors, typography, components) as existing pages

### Requirement 11: Edge Cases & Data Integrity

**User Story:** As a system, I want to handle edge cases gracefully, so that users have a reliable experience.

#### Acceptance Criteria

1. IF user tries to apply to closed job, THE system SHALL show appropriate error message
2. IF user tries to apply twice to same job, THE system SHALL prevent duplicate and show message
3. IF user deletes a resume that's linked to an application, THE application SHALL retain resume reference (soft delete or snapshot)
4. IF Admin deletes a job, THE system SHALL prompt to confirm and handle existing applications appropriately
5. THE system SHALL validate all URLs (portfolio, linkedin, github) for proper format
6. THE system SHALL sanitize all user inputs to prevent XSS

### Requirement 12: Mobile Responsiveness

**User Story:** As a candidate on mobile, I want to browse and apply for jobs easily, so that I can job search from any device.

#### Acceptance Criteria

1. THE Careers page SHALL display job cards in single column on mobile
2. THE Job Details page SHALL be fully readable on mobile
3. THE Application form SHALL be usable on mobile with appropriate input sizes
4. THE My Applications page SHALL be scrollable and readable on mobile
5. ALL touch targets SHALL be minimum 44px for accessibility

---

## Non-Functional Requirements

### Performance
- Job listings page SHALL load within 2 seconds
- Application submission SHALL complete within 3 seconds
- Admin dashboard SHALL handle 1000+ applications efficiently with pagination

### Security
- Application data SHALL be accessible only to the applicant and Super Admins
- Resume/cover letter files SHALL be served with proper authentication
- All forms SHALL include CSRF protection
- Admin pages SHALL verify is_superuser on every request

### Scalability
- Database schema SHALL support future enhancements: multiple companies, hiring teams, interview scheduling
- Application status workflow SHALL be extensible for custom statuses

---

## Future Enhancements (Out of Scope for V1)

- Email notifications for status changes
- Interview scheduling integration
- Candidate rating/scoring system
- Hiring team collaboration (multiple reviewers)
- Analytics dashboard for hiring metrics
- Job posting templates
- Referral tracking
