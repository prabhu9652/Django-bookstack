# HR Portal - Enterprise HR Management System

A production-ready HR Portal Django application designed for software companies, featuring employee-facing self-service, admin-controlled workflows, and real-world approval processes.

## Admin-Controlled Feature Toggle

The HR Portal includes an enterprise-grade admin-controlled access system:

### Enabling/Disabling HR Portal Access

1. Go to Django Admin (`/admin/`)
2. Navigate to **Users** or **HR Roles**
3. For each user, you can:
   - Enable/disable `can_access_hr_portal` flag
   - Set role type (Employee, Manager, HR Admin, Finance Admin, App Admin)
   - Configure granular permissions

### Access Control Rules

| Setting | Effect |
|---------|--------|
| `can_access_hr_portal = True` | User sees HR Portal in navigation and can access all HR URLs |
| `can_access_hr_portal = False` | User cannot see or access HR Portal (redirected with error) |
| No HRRole assigned | User cannot access HR Portal |
| Superuser | Always has access regardless of HRRole |

### Immediate Effect
Changes to access settings take effect immediately - no server restart required.

### Security
- All HR Portal URLs are protected by the `@hr_portal_required` decorator
- Unauthorized access attempts are logged for security auditing
- Both frontend (navigation) and backend (views) enforce access control

## Features

### Core Modules
- **Employee Management** - Profiles, departments, designations, reporting hierarchy
- **Leave Management** - Leave types, balances, requests with Manager → HR approval workflow
- **Expense Management** - Categories, claims, receipts with Manager → Finance approval workflow
- **Timesheet Management** - Weekly timesheets, project-based time tracking, manager approval
- **Asset Management** - Company asset inventory, assignment tracking, return management
- **Project Management** - Project creation, team assignments, time tracking integration
- **Holiday Calendar** - Company-wide and location-based holidays

### Role-Based Access Control (RBAC)
| Role | Permissions |
|------|-------------|
| App Admin | Full system access, user management, all HR functions |
| HR Admin | Employee management, leave approval, asset management, holidays |
| Finance Admin | Expense approval, payment processing, financial reports |
| Manager | Team management, approve team requests (leave, expense, timesheet) |
| Employee | Self-service (leave, expense, timesheet), view personal data |

### Approval Workflows
- **Leave**: Employee → Manager → HR Admin
- **Expense**: Employee → Manager → Finance Admin → Payment
- **Timesheet**: Employee → Manager

## Quick Start

1. Add `'hr_portal'` to `INSTALLED_APPS` in settings.py
2. Add context processor: `'hr_portal.permissions.hr_portal_context'`
3. Include URLs: `path('hr/', include('hr_portal.urls'))`
4. Run migrations: `python manage.py migrate hr_portal`
5. Assign HR roles to users via Admin or User Management

## Navigation
HR Portal link appears in navigation only for users with `can_access_hr_portal=True`.

## URL Structure
- `/hr/` - Dashboard
- `/hr/leave/` - Leave management
- `/hr/expense/` - Expense management
- `/hr/timesheet/` - Timesheet management
- `/hr/assets/` - Asset management
- `/hr/projects/` - Project management
- `/hr/holidays/` - Holiday calendar
- `/hr/approvals/` - Approval dashboard (managers/admins)
- `/hr/admin/` - HR administration
