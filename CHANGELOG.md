# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-20

### Added
- Complete Django REST Framework backend with JWT authentication
- Custom User model with company relationships
- Company management system
- Magic links for anonymous report submission with UUID tokens
- Report management with field-level encryption
- Email notifications for new reports
- Data segregation by company
- React + TypeScript frontend with Tailwind CSS
- User authentication (login/register) with auto-login after registration
- Protected routes with authentication checks
- Reports dashboard with filtering by status and category
- Report detail view with status updates and internal notes
- Magic links management interface
- Public report submission form with anonymous/named options
- Responsive mobile-friendly design
- Docker Compose for development environment
- Docker Compose for production with Nginx reverse proxy
- PostgreSQL database integration
- Comprehensive pytest test suite
- Field-level encryption for sensitive reporter data
- CORS protection and security middleware
- Complete documentation (README, API docs, Contributing, Deployment)
- MIT License

### Security
- JWT authentication with token rotation and blacklisting
- Field-level encryption using Fernet for reporter information
- Company-based data segregation with custom permissions
- Input validation and sanitization
- HTTPS-ready configuration
- Secure password hashing

## Known Issues / Future Improvements

### Frontend
- Window.confirm() and window.alert() should be replaced with custom React modals/toasts for better UX
  - Affected files: `frontend/src/pages/MagicLinks.tsx`, `frontend/src/pages/ReportDetail.tsx`

### Backend
- Error logging using print() should be replaced with Django's logging framework
  - Affected file: `backend/apps/reports/views.py:150`

### Future Enhancements
- File attachment support for reports
- Rich HTML email templates
- Report comment threading
- Audit logging for compliance
- Multi-language support (i18n)
- Analytics dashboard with charts
- PDF/CSV export functionality
- Full-text search across reports
- Webhook integrations
- Mobile apps (iOS/Android)

## [1.0.1] - 2024-01-20

### Security
- **CRITICAL**: Updated Django from 5.0.1 to 5.0.10 to patch multiple vulnerabilities:
  - SQL injection in HasKey(lhs, rhs) on Oracle (CVE-2024-XXXX)
  - Denial-of-service attack in intcomma template filter
  - SQL injection via _connector keyword argument in QuerySet and Q objects
  - Denial-of-service vulnerability in HttpResponseRedirect on Windows
- **CRITICAL**: Updated cryptography from 42.0.0 to 42.0.4 to patch NULL pointer dereference vulnerability
- **CRITICAL**: Updated gunicorn from 21.2.0 to 22.0.0 to patch HTTP Request/Response Smuggling vulnerabilities

### Changed
- Updated requirements.txt with patched dependency versions

## [Unreleased]

### Planned
- Toast notification system for frontend
- Custom confirmation modals
- Enhanced logging system
- File upload functionality
- Email templates
