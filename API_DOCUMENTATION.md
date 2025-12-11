# API Documentation

## Base URL

- **Development**: `http://localhost:8000/api`
- **Production**: `https://your-domain.com/api`

## Authentication

Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Authentication Flow

1. Register or login to get JWT tokens
2. Use the `access` token for API requests
3. Use the `refresh` token to get a new access token when it expires
4. Logout by blacklisting the refresh token

## Endpoints

### Authentication Endpoints

#### Register

Create a new manager account and company.

**Endpoint**: `POST /api/auth/register/`

**Authentication**: None required

**Request Body**:
```json
{
  "email": "manager@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "company_name": "Acme Corporation"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "manager@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "company": "550e8400-e29b-41d4-a716-446655440001",
  "company_name": "Acme Corporation",
  "role": "admin",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Login

Authenticate and receive JWT tokens.

**Endpoint**: `POST /api/auth/login/`

**Authentication**: None required

**Request Body**:
```json
{
  "email": "manager@example.com",
  "password": "securepassword123"
}
```

**Response** (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token

Get a new access token using the refresh token.

**Endpoint**: `POST /api/auth/refresh/`

**Authentication**: None required

**Request Body**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response** (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Logout

Blacklist the refresh token to logout.

**Endpoint**: `POST /api/auth/logout/`

**Authentication**: Required

**Request Body**:
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response** (200 OK):
```json
{
  "message": "Successfully logged out"
}
```

#### Get User Profile

Get the authenticated user's profile.

**Endpoint**: `GET /api/auth/me/`

**Authentication**: Required

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "manager@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "company": "550e8400-e29b-41d4-a716-446655440001",
  "company_name": "Acme Corporation",
  "role": "admin",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Update User Profile

Update the authenticated user's profile.

**Endpoint**: `PUT /api/auth/me/`

**Authentication**: Required

**Request Body**:
```json
{
  "first_name": "Jane",
  "last_name": "Smith"
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "manager@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "company": "550e8400-e29b-41d4-a716-446655440001",
  "company_name": "Acme Corporation",
  "role": "admin",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### Company Endpoints

#### Get My Company

Get the authenticated user's company details.

**Endpoint**: `GET /api/companies/me/`

**Authentication**: Required

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "Acme Corporation",
  "created_by": "550e8400-e29b-41d4-a716-446655440000",
  "created_by_name": "John Doe",
  "users_count": 3,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Update Company

Update the authenticated user's company.

**Endpoint**: `PUT /api/companies/me/`

**Authentication**: Required

**Request Body**:
```json
{
  "name": "Acme Corp"
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "Acme Corp",
  "created_by": "550e8400-e29b-41d4-a716-446655440000",
  "created_by_name": "John Doe",
  "users_count": 3,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T14:22:00Z"
}
```

---

### Magic Link Endpoints

#### List Magic Links

Get all magic links for the user's company.

**Endpoint**: `GET /api/magic-links/`

**Authentication**: Required

**Response** (200 OK):
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "token": "a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890",
    "company": "550e8400-e29b-41d4-a716-446655440001",
    "company_name": "Acme Corporation",
    "created_by": "550e8400-e29b-41d4-a716-446655440000",
    "created_by_name": "John Doe",
    "name": "Employee Portal Link",
    "is_active": true,
    "expires_at": null,
    "created_at": "2024-01-15T10:30:00Z",
    "is_valid": true,
    "url": "http://localhost:5173/report/a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890"
  }
]
```

#### Create Magic Link

Create a new magic link.

**Endpoint**: `POST /api/magic-links/`

**Authentication**: Required

**Request Body**:
```json
{
  "name": "HR Portal Link",
  "is_active": true,
  "expires_at": "2024-12-31T23:59:59Z"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "token": "b2c3d4e5-f6a7-8901-b2c3-d4e5f6a78901",
  "company": "550e8400-e29b-41d4-a716-446655440001",
  "company_name": "Acme Corporation",
  "created_by": "550e8400-e29b-41d4-a716-446655440000",
  "created_by_name": "John Doe",
  "name": "HR Portal Link",
  "is_active": true,
  "expires_at": "2024-12-31T23:59:59Z",
  "created_at": "2024-01-20T14:25:00Z",
  "is_valid": true,
  "url": "http://localhost:5173/report/b2c3d4e5-f6a7-8901-b2c3-d4e5f6a78901"
}
```

#### Get Magic Link

Get details of a specific magic link.

**Endpoint**: `GET /api/magic-links/{id}/`

**Authentication**: Required

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "token": "a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890",
  "company": "550e8400-e29b-41d4-a716-446655440001",
  "company_name": "Acme Corporation",
  "created_by": "550e8400-e29b-41d4-a716-446655440000",
  "created_by_name": "John Doe",
  "name": "Employee Portal Link",
  "is_active": true,
  "expires_at": null,
  "created_at": "2024-01-15T10:30:00Z",
  "is_valid": true,
  "url": "http://localhost:5173/report/a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890"
}
```

#### Update Magic Link

Update a magic link.

**Endpoint**: `PUT /api/magic-links/{id}/`

**Authentication**: Required

**Request Body**:
```json
{
  "name": "Updated Link Name",
  "is_active": false,
  "expires_at": null
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "token": "a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890",
  "company": "550e8400-e29b-41d4-a716-446655440001",
  "company_name": "Acme Corporation",
  "created_by": "550e8400-e29b-41d4-a716-446655440000",
  "created_by_name": "John Doe",
  "name": "Updated Link Name",
  "is_active": false,
  "expires_at": null,
  "created_at": "2024-01-15T10:30:00Z",
  "is_valid": false,
  "url": "http://localhost:5173/report/a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890"
}
```

#### Delete Magic Link

Delete a magic link.

**Endpoint**: `DELETE /api/magic-links/{id}/`

**Authentication**: Required

**Response** (204 No Content)

---

### Report Endpoints (Manager)

#### List Reports

Get all reports for the user's company with optional filtering.

**Endpoint**: `GET /api/reports/`

**Authentication**: Required

**Query Parameters**:
- `status`: Filter by status (new, in_review, investigating, resolved, closed)
- `category`: Filter by category (harassment, fraud, safety, discrimination, other)
- `page`: Page number for pagination

**Response** (200 OK):
```json
{
  "count": 42,
  "next": "http://localhost:8000/api/reports/?page=2",
  "previous": null,
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440004",
      "magic_link": "550e8400-e29b-41d4-a716-446655440002",
      "magic_link_name": "Employee Portal Link",
      "category": "harassment",
      "category_display": "Harassment",
      "description": "Detailed description of the incident...",
      "is_anonymous": true,
      "reporter_name": null,
      "reporter_email": null,
      "status": "new",
      "status_display": "New",
      "internal_notes": "",
      "created_at": "2024-01-20T09:15:00Z",
      "updated_at": "2024-01-20T09:15:00Z"
    }
  ]
}
```

#### Get Report

Get details of a specific report.

**Endpoint**: `GET /api/reports/{id}/`

**Authentication**: Required

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "magic_link": "550e8400-e29b-41d4-a716-446655440002",
  "magic_link_name": "Employee Portal Link",
  "category": "harassment",
  "category_display": "Harassment",
  "description": "Detailed description of the incident...",
  "is_anonymous": false,
  "reporter_name": "Jane Smith",
  "reporter_email": "jane.smith@example.com",
  "status": "in_review",
  "status_display": "In Review",
  "internal_notes": "Contacted HR department",
  "created_at": "2024-01-20T09:15:00Z",
  "updated_at": "2024-01-21T14:30:00Z"
}
```

#### Update Report

Update a report's status and internal notes.

**Endpoint**: `PUT /api/reports/{id}/`

**Authentication**: Required

**Request Body**:
```json
{
  "status": "investigating",
  "internal_notes": "Started formal investigation. Assigned to legal team."
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "magic_link": "550e8400-e29b-41d4-a716-446655440002",
  "magic_link_name": "Employee Portal Link",
  "category": "harassment",
  "category_display": "Harassment",
  "description": "Detailed description of the incident...",
  "is_anonymous": false,
  "reporter_name": "Jane Smith",
  "reporter_email": "jane.smith@example.com",
  "status": "investigating",
  "status_display": "Investigating",
  "internal_notes": "Started formal investigation. Assigned to legal team.",
  "created_at": "2024-01-20T09:15:00Z",
  "updated_at": "2024-01-22T10:00:00Z"
}
```

---

### Public Report Endpoints

#### Validate Magic Link

Validate a magic link token (public endpoint).

**Endpoint**: `GET /api/reports/public/{token}/`

**Authentication**: None required

**Response** (200 OK):
```json
{
  "is_valid": true,
  "company_name": "Acme Corporation",
  "message": "Magic link is valid"
}
```

**Response** (400 Bad Request) - Expired link:
```json
{
  "is_valid": false,
  "company_name": "Acme Corporation",
  "message": "This link has expired or is no longer active"
}
```

**Response** (404 Not Found) - Invalid token:
```json
{
  "is_valid": false,
  "company_name": "",
  "message": "Invalid magic link"
}
```

#### Submit Report

Submit a report via magic link (public endpoint).

**Endpoint**: `POST /api/reports/public/{token}/submit/`

**Authentication**: None required

**Request Body** (Anonymous):
```json
{
  "category": "safety",
  "description": "Detailed description of the safety concern...",
  "is_anonymous": true
}
```

**Request Body** (Named):
```json
{
  "category": "fraud",
  "description": "Detailed description of the fraudulent activity...",
  "is_anonymous": false,
  "reporter_name": "John Doe",
  "reporter_email": "john.doe@example.com"
}
```

**Response** (201 Created):
```json
{
  "message": "Report submitted successfully",
  "report_id": "550e8400-e29b-41d4-a716-446655440005"
}
```

**Response** (400 Bad Request):
```json
{
  "error": "This link has expired or is no longer active"
}
```

---

## Error Responses

### Common Error Codes

- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Error Response Format

```json
{
  "detail": "Error message",
  "field_name": ["Field-specific error message"]
}
```

## Rate Limiting

Rate limiting can be configured on public endpoints to prevent abuse. Contact your system administrator for rate limit details.

## CORS

Cross-Origin Resource Sharing (CORS) is configured to allow requests from specified frontend origins. Configure `CORS_ALLOWED_ORIGINS` in your environment variables.
