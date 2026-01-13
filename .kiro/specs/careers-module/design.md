# Careers Module - Design Document

## Overview

The Careers Module adds a professional job portal to the platform, enabling candidates to browse and apply for positions using their existing Resume Builder documents, while Super Admins manage job postings and review applications through an ATS-style dashboard.

This design follows industry-standard patterns from companies like Stripe, Notion, and Linear, integrating seamlessly with the existing Django application architecture.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Templates)                      │
├─────────────────────────────────────────────────────────────────┤
│  Candidate Views          │         Admin Views                  │
│  ├─ Careers Landing       │         ├─ Job Management           │
│  ├─ Job Details           │         ├─ Applications Dashboard   │
│  ├─ Application Form      │         └─ Application Detail       │
│  └─ My Applications       │                                      │
├─────────────────────────────────────────────────────────────────┤
│                        Django Views                              │
│  ├─ Public Views (careers_home, job_detail)                     │
│  ├─ Candidate Views (apply_job, my_applications)                │
│  └─ Admin Views (manage_jobs, manage_applications)              │
├─────────────────────────────────────────────────────────────────┤
│                        Django Models                             │
│  ├─ JobPosting                                                   │
│  ├─ Application                                                  │
│  └─ ApplicationNote (Admin internal notes)                      │
├─────────────────────────────────────────────────────────────────┤
│                    Existing Models (FK References)               │
│  ├─ User (django.contrib.auth)                                  │
│  ├─ Resume (resume_builder)                                     │
│  └─ CoverLetter (resume_builder)                                │
└─────────────────────────────────────────────────────────────────┘
```

### URL Structure

```
/careers/                           # Careers landing page (public)
/careers/job/<slug>/                # Job details page (public)
/careers/job/<slug>/apply/          # Application form (login required)
/careers/my-applications/           # User's applications dashboard
/careers/my-applications/<id>/      # Application detail view

# Admin URLs
/careers/admin/jobs/                # Job management dashboard
/careers/admin/jobs/create/         # Create new job
/careers/admin/jobs/<id>/edit/      # Edit job
/careers/admin/applications/        # All applications dashboard
/careers/admin/applications/<id>/   # Application detail + actions

# API Endpoints
/careers/api/apply/                 # POST - Submit application
/careers/api/application/<id>/status/  # POST - Update status (admin)
/careers/api/job/<id>/toggle/       # POST - Toggle job active (admin)
```

## Components and Interfaces

### Django App Structure

```
careers/
├── __init__.py
├── admin.py              # Django admin registration
├── apps.py               # App configuration
├── models.py             # JobPosting, Application, ApplicationNote
├── views.py              # All view functions
├── urls.py               # URL routing
├── forms.py              # Django forms for validation
├── decorators.py         # @superuser_required decorator
├── migrations/
│   └── 0001_initial.py
├── templates/
│   └── careers/
│       ├── careers_home.html        # Job listings
│       ├── job_detail.html          # Single job view
│       ├── apply_job.html           # Application form
│       ├── my_applications.html     # User dashboard
│       ├── application_detail.html  # User's application view
│       ├── admin/
│       │   ├── jobs_dashboard.html
│       │   ├── job_form.html
│       │   ├── applications_dashboard.html
│       │   └── application_detail.html
│       └── partials/
│           ├── job_card.html
│           ├── application_card.html
│           └── status_badge.html
└── static/
    └── careers/
        └── css/
            └── careers.css
```

### View Functions Interface

```python
# Public Views
def careers_home(request) -> HttpResponse
def job_detail(request, slug: str) -> HttpResponse

# Candidate Views (login_required)
def apply_job(request, slug: str) -> HttpResponse
def my_applications(request) -> HttpResponse
def application_detail(request, application_id: int) -> HttpResponse

# Admin Views (superuser_required)
def admin_jobs_dashboard(request) -> HttpResponse
def admin_create_job(request) -> HttpResponse
def admin_edit_job(request, job_id: int) -> HttpResponse
def admin_applications_dashboard(request) -> HttpResponse
def admin_application_detail(request, application_id: int) -> HttpResponse

# API Endpoints
def api_submit_application(request) -> JsonResponse
def api_update_application_status(request, application_id: int) -> JsonResponse
def api_toggle_job_status(request, job_id: int) -> JsonResponse
def api_add_application_note(request, application_id: int) -> JsonResponse
```

## Data Models

### JobPosting Model

```python
class JobPosting(models.Model):
    LOCATION_TYPES = [
        ('remote', 'Remote'),
        ('onsite', 'On-site'),
        ('hybrid', 'Hybrid'),
    ]
    
    EMPLOYMENT_TYPES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    
    # Core fields
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPES)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES)
    
    # Rich text content
    description = models.TextField()
    responsibilities = models.TextField(help_text="One responsibility per line")
    requirements = models.TextField(help_text="One requirement per line")
    tech_stack = models.JSONField(default=list, help_text="List of technologies")
    
    # Optional fields
    salary_range = models.CharField(max_length=100, blank=True)
    
    # Status and dates
    is_active = models.BooleanField(default=True)
    closes_at = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Handle duplicates
            if JobPosting.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)
    
    def is_open(self):
        """Check if job is accepting applications"""
        if not self.is_active:
            return False
        if self.closes_at and self.closes_at < timezone.now():
            return False
        return True
    
    def get_responsibilities_list(self):
        return [r.strip() for r in self.responsibilities.split('\n') if r.strip()]
    
    def get_requirements_list(self):
        return [r.strip() for r in self.requirements.split('\n') if r.strip()]
```

### Application Model

```python
class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    
    # Relationships
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    resume = models.ForeignKey('resume_builder.Resume', on_delete=models.SET_NULL, null=True)
    cover_letter = models.ForeignKey('resume_builder.CoverLetter', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Snapshot of user data at application time (data integrity)
    applicant_name = models.CharField(max_length=200)
    applicant_email = models.EmailField()
    
    # Optional links
    portfolio_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # Application content
    additional_notes = models.TextField(blank=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-applied_at']
        unique_together = ['job', 'user']  # Prevent duplicate applications
    
    def save(self, *args, **kwargs):
        # Snapshot user data on first save
        if not self.pk:
            self.applicant_name = f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
            self.applicant_email = self.user.email
        super().save(*args, **kwargs)
```

### ApplicationNote Model (Admin Internal Notes)

```python
class ApplicationNote(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Slug Generation Uniqueness
*For any* JobPosting title, the auto-generated slug SHALL be URL-friendly (lowercase, hyphenated, no special characters) and unique across all job postings.
**Validates: Requirements 1.3**

### Property 2: Active Job Filtering
*For any* query to the public job listings, only jobs where `is_active=True` AND (`closes_at` is null OR `closes_at > now()`) SHALL appear in results.
**Validates: Requirements 1.5, 3.3**

### Property 3: Application Uniqueness Constraint
*For any* (job, user) pair, attempting to create a second Application SHALL raise an IntegrityError, preventing duplicate applications.
**Validates: Requirements 2.2, 11.2**

### Property 4: Application Status Validity
*For any* Application, the status field SHALL only accept values from the defined choices: 'applied', 'under_review', 'interview', 'rejected', 'hired'.
**Validates: Requirements 2.3**

### Property 5: Applicant Data Snapshot Integrity
*For any* Application, the `applicant_name` and `applicant_email` fields SHALL be populated from the user's profile at creation time and SHALL NOT change if the user later updates their profile.
**Validates: Requirements 2.4**

### Property 6: Default Application Status
*For any* newly created Application, the status SHALL default to 'applied' without explicit assignment.
**Validates: Requirements 2.5**

### Property 7: Job Card Data Completeness
*For any* job card rendered in the listings, the output SHALL contain: title, department, location, location_type badge, employment_type badge, and posted date.
**Validates: Requirements 3.4**

### Property 8: Search Filter Accuracy
*For any* search query on the careers page, all returned jobs SHALL contain the search term in either the title or description fields.
**Validates: Requirements 3.6**

### Property 9: Already Applied State
*For any* user who has an existing Application for a job, the job detail page SHALL display "Already Applied" with a disabled apply button.
**Validates: Requirements 4.5**

### Property 10: Closed Job Message
*For any* job where `is_open()` returns False, the job detail page SHALL display "This position is no longer accepting applications" and hide the apply button.
**Validates: Requirements 4.6**

### Property 11: Form Pre-fill Accuracy
*For any* authenticated user viewing the application form, the full_name and email fields SHALL be pre-populated with the user's profile data.
**Validates: Requirements 5.2**

### Property 12: Resume Dropdown Population
*For any* user with existing resumes, the application form's resume dropdown SHALL contain all of the user's Resume objects from My Documents.
**Validates: Requirements 5.3**

### Property 13: Resume Required Validation
*For any* application submission without a selected resume, the system SHALL reject the submission with a validation error.
**Validates: Requirements 5.10**

### Property 14: Application Submission Creates Record
*For any* valid application form submission, exactly one Application record SHALL be created with all provided data correctly stored.
**Validates: Requirements 5.8**

### Property 15: My Applications Ordering
*For any* user's applications list, the applications SHALL be ordered by `applied_at` in descending order (newest first).
**Validates: Requirements 6.2**

### Property 16: Application Status Filter
*For any* status filter applied to My Applications, only applications with matching status SHALL appear in results.
**Validates: Requirements 6.7**

### Property 17: Admin Access Control
*For any* request to admin views from a user where `is_superuser=False`, the system SHALL return a 403 Forbidden response.
**Validates: Requirements 7.1**

### Property 18: Job Toggle Preserves Applications
*For any* job with existing applications, toggling `is_active` to False SHALL NOT delete or modify any associated Application records.
**Validates: Requirements 7.7**

### Property 19: Status Change Timestamp Update
*For any* Application status change, the `updated_at` timestamp SHALL be updated to the current time.
**Validates: Requirements 9.2**

### Property 20: URL Validation
*For any* Application with portfolio_url, linkedin_url, or github_url fields, the values SHALL be valid URLs or empty strings.
**Validates: Requirements 11.5**

### Property 21: Resume Deletion Handling
*For any* Resume that is deleted while linked to an Application, the Application SHALL retain its reference (via SET_NULL) and remain accessible.
**Validates: Requirements 11.3**

## Error Handling

### User-Facing Errors

| Scenario | Error Message | HTTP Status |
|----------|---------------|-------------|
| Apply to closed job | "This position is no longer accepting applications." | 400 |
| Duplicate application | "You have already applied to this position." | 400 |
| No resume selected | "Please select a resume to continue." | 400 |
| Invalid URL format | "Please enter a valid URL." | 400 |
| Job not found | "Job posting not found." | 404 |
| Unauthorized access | Redirect to login | 302 |

### Admin Errors

| Scenario | Error Message | HTTP Status |
|----------|---------------|-------------|
| Non-admin access | "You don't have permission to access this page." | 403 |
| Invalid status transition | "Invalid status value." | 400 |
| Delete job with applications | Confirmation modal required | N/A |

### Error Response Format (API)

```python
{
    "success": False,
    "error": "Error message here",
    "field_errors": {  # Optional, for form validation
        "field_name": ["Error 1", "Error 2"]
    }
}
```

## Testing Strategy

### Unit Tests
- Model field validation and constraints
- Slug generation uniqueness
- `is_open()` method logic
- Status choices validation
- Data snapshot on application creation

### Property-Based Tests (using Hypothesis)
- Property 1: Slug generation produces valid URL-safe strings
- Property 2: Active job filtering correctness
- Property 3: Duplicate application prevention
- Property 5: Applicant data immutability after creation
- Property 8: Search filter returns only matching results
- Property 15: Application ordering consistency

### Integration Tests
- Full application flow (browse → view → apply → confirm)
- Admin job management workflow
- Admin application review workflow
- Resume Builder integration (dropdown population)

### Edge Case Tests
- User with no resumes attempting to apply
- Job closing while user is on application form
- Admin deleting job with pending applications
- User profile changes after application submission

### Test Configuration
- Minimum 100 iterations per property test
- Use Django's TestCase for database tests
- Use Hypothesis for property-based testing
- Tag format: **Feature: careers-module, Property {number}: {property_text}**

## UI/UX Design Notes

### Color Scheme (Status Badges)
```css
.status-applied { background: #3b82f6; }      /* Blue */
.status-under_review { background: #f59e0b; } /* Yellow/Amber */
.status-interview { background: #8b5cf6; }    /* Purple */
.status-rejected { background: #ef4444; }     /* Red */
.status-hired { background: #22c55e; }        /* Green */
```

### Layout Patterns
- Max content width: 1200px (consistent with existing pages)
- Job cards: 3-column grid on desktop, 1-column on mobile
- Application form: Single column, max-width 600px
- Admin tables: Full-width with horizontal scroll on mobile

### Interaction Patterns
- Toast notifications at TOP of screen (per user preference)
- Confirmation modals for destructive actions
- Loading states for async operations
- Subtle hover animations on cards

## Security Considerations

1. **Access Control**: All admin views check `is_superuser` via decorator
2. **CSRF Protection**: All forms include `{% csrf_token %}`
3. **XSS Prevention**: All user inputs escaped via Django templates
4. **SQL Injection**: Use Django ORM exclusively, no raw SQL
5. **File Access**: Resume/cover letter files served with authentication check
6. **Rate Limiting**: Consider adding for application submissions (future)

## Future Enhancements (Out of Scope)

- Email notifications for status changes
- Interview scheduling integration
- Candidate rating/scoring system
- Multiple hiring team members
- Analytics dashboard
- Job posting templates
- Referral tracking
