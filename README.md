# Whistleblower Reporting System

A complete, secure platform for anonymous employee reporting to help EU companies comply with whistleblower protection requirements.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Running Tests](#running-tests)
- [Default Credentials](#default-credentials)
- [Project Structure](#project-structure)
- [Security Features](#security-features)
- [License](#license)

## 🌟 Overview

This whistleblower reporting system enables organizations to receive, track, and manage confidential reports of unethical, illegal, or unsafe behavior. The platform provides:

- **For Employees/Reporters**: Anonymous or confidential report submission via magic links
- **For Managers**: Secure dashboard to manage and track reports
- **For Organizations**: EU-compliant whistleblower protection infrastructure

## ✨ Features

### Manager Features
- 🔐 Secure authentication with JWT tokens
- 🏢 Company profile management
- 🔗 Magic link generation and management
- 📊 Reports dashboard with filtering and sorting
- 📝 Report status tracking and internal notes
- 📧 Email notifications for new reports

### Public Reporting Features
- 🔒 Anonymous or named report submission
- 🎯 Categorized reporting (harassment, fraud, safety, discrimination, other)
- ✅ Magic link validation
- 🔐 Encrypted storage of reporter information
- 📱 Responsive, mobile-friendly design

## 🏗 Architecture

```
┌─────────────────┐
│   Nginx Proxy   │  (Production only)
└────────┬────────┘
         │
    ┌────┴──────────────────┐
    │                       │
┌───▼────┐           ┌─────▼─────┐
│ React  │           │  Django   │
│Frontend│◄─────────►│  Backend  │
│(Vite)  │   REST    │   (DRF)   │
└────────┘    API    └─────┬─────┘
                            │
                      ┌─────▼─────┐
                      │PostgreSQL │
                      └───────────┘
```

## 🛠 Tech Stack

### Backend
- **Framework**: Django 5.0.1 + Django REST Framework 3.14.0
- **Database**: PostgreSQL 16
- **Authentication**: JWT (SimpleJWT)
- **API Documentation**: Django REST Framework browsable API
- **Testing**: pytest + pytest-django
- **Production Server**: Gunicorn

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite 5
- **Styling**: Tailwind CSS 3.4
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **State Management**: React Context API

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Reverse Proxy**: Nginx (production)
- **Development**: Hot reload for both frontend and backend

## 📋 Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/jagomes445/whistleblower-system.git
cd whistleblower-system
```

### 2. Create Environment File

```bash
cp .env.example .env
```

Edit `.env` and update the values as needed (the defaults work for development).

### 3. Start Development Environment

```bash
docker-compose up --build
```

This will start:
- Backend API at http://localhost:8000
- Frontend at http://localhost:5173
- PostgreSQL database at localhost:5432

### 4. Run Database Migrations

In a new terminal:

```bash
docker-compose exec backend python manage.py migrate
```

### 5. Create a Superuser (Optional)

```bash
docker-compose exec backend python manage.py createsuperuser
```

### 6. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api
- **Admin Panel**: http://localhost:8000/admin

## 🔧 Environment Variables

### Django Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DJANGO_SECRET_KEY` | Django secret key | `dev-secret-key-change-in-production` | Yes |
| `DJANGO_DEBUG` | Enable debug mode | `True` | Yes |
| `DJANGO_ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1,backend` | Yes |

### Database Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `POSTGRES_DB` | Database name | `whistleblower_db` | Yes |
| `POSTGRES_USER` | Database user | `whistleblower_user` | Yes |
| `POSTGRES_PASSWORD` | Database password | `whistleblower_password` | Yes |
| `POSTGRES_HOST` | Database host | `db` | Yes |
| `POSTGRES_PORT` | Database port | `5432` | Yes |

### JWT Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `JWT_ACCESS_TOKEN_LIFETIME_MINUTES` | Access token lifetime | `60` | No |
| `JWT_REFRESH_TOKEN_LIFETIME_DAYS` | Refresh token lifetime | `7` | No |

### Email Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `EMAIL_BACKEND` | Email backend | `django.core.mail.backends.console.EmailBackend` | Yes |
| `EMAIL_HOST` | SMTP host | `smtp.example.com` | No |
| `EMAIL_PORT` | SMTP port | `587` | No |
| `EMAIL_USE_TLS` | Use TLS | `True` | No |
| `EMAIL_HOST_USER` | SMTP username | - | No |
| `EMAIL_HOST_PASSWORD` | SMTP password | - | No |
| `DEFAULT_FROM_EMAIL` | From email address | `noreply@whistleblower.com` | Yes |

### Frontend Settings

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FRONTEND_URL` | Frontend URL | `http://localhost:5173` | Yes |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:5173` | Yes |

## 📚 API Documentation

### Authentication Endpoints

- `POST /api/auth/register/` - Register new manager + company
- `POST /api/auth/login/` - Login, returns JWT tokens
- `POST /api/auth/refresh/` - Refresh access token
- `POST /api/auth/logout/` - Blacklist refresh token
- `GET /api/auth/me/` - Get current user profile
- `PUT /api/auth/me/` - Update profile

### Company Endpoints

- `GET /api/companies/me/` - Get current user's company
- `PUT /api/companies/me/` - Update company

### Magic Link Endpoints

- `GET /api/magic-links/` - List magic links for user's company
- `POST /api/magic-links/` - Create new magic link
- `GET /api/magic-links/{id}/` - Get magic link details
- `PUT /api/magic-links/{id}/` - Update magic link
- `DELETE /api/magic-links/{id}/` - Delete magic link

### Report Endpoints (Authenticated)

- `GET /api/reports/` - List reports for user's company
  - Query params: `status`, `category`, `page`
- `GET /api/reports/{id}/` - Get report details
- `PUT /api/reports/{id}/` - Update report status/notes

### Public Report Endpoints

- `GET /api/reports/public/{token}/` - Validate magic link
- `POST /api/reports/public/{token}/submit/` - Submit anonymous report

## 🧪 Running Tests

### Backend Tests

```bash
# Run all tests
docker-compose exec backend pytest

# Run with coverage report
docker-compose exec backend pytest --cov

# Run specific test file
docker-compose exec backend pytest apps/users/tests.py

# Run with verbose output
docker-compose exec backend pytest -v
```

### Test Coverage Goal

The project aims for **80%+ test coverage** including:
- Unit tests for models
- Unit tests for serializers
- Integration tests for API endpoints
- Permission and data segregation tests

## 🔑 Default Credentials

After running migrations and creating a superuser, you can:

1. **Admin Panel**: http://localhost:8000/admin
   - Username: (your superuser email)
   - Password: (your superuser password)

2. **Frontend Registration**: http://localhost:5173/register
   - Register a new company and manager account
   - Auto-login after registration

## 📁 Project Structure

```
whistleblower-system/
├── docker-compose.yml          # Development configuration
├── docker-compose.prod.yml     # Production configuration
├── .env.example                # Environment variables template
├── README.md                   # This file
│
├── backend/                    # Django backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── pytest.ini
│   ├── config/                 # Django configuration
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/                   # Django apps
│   │   ├── users/              # User authentication
│   │   ├── companies/          # Company management
│   │   ├── magic_links/        # Magic link generation
│   │   └── reports/            # Report management
│   └── core/                   # Shared utilities
│       ├── permissions.py
│       └── utils.py
│
├── frontend/                   # React frontend
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── src/
│       ├── api/                # API client
│       ├── components/         # React components
│       ├── pages/              # Page components
│       ├── context/            # React context
│       ├── hooks/              # Custom hooks
│       └── types/              # TypeScript types
│
└── nginx/                      # Nginx configuration
    ├── Dockerfile
    └── nginx.conf
```

## 🔒 Security Features

1. **Data Segregation**: Users can ONLY access reports for their own company
2. **JWT Security**: Short-lived access tokens with refresh token rotation
3. **Encryption**: Reporter information is encrypted at rest
4. **Anonymous Reporting**: No authentication required for public submissions
5. **Input Validation**: All inputs are sanitized and validated
6. **CORS Protection**: Restricted to allowed origins
7. **HTTPS Ready**: Production configuration includes SSL support
8. **Rate Limiting**: Can be configured on public endpoints

## 🚢 Production Deployment

### 1. Update Environment Variables

Update `.env` with production values:

```bash
DJANGO_SECRET_KEY=your-strong-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# ... other production settings
```

### 2. Start Production Stack

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

### 3. Run Migrations

```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
```

### 4. Collect Static Files

```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
```

### 5. Create Superuser

```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub.
