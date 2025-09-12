# API Documentation

## Overview

This document provides comprehensive documentation for the Parque Marino Backend REST API. The API follows RESTful principles and uses JSON for request and response bodies.

## Authentication

Most API endpoints require authentication using JWT (JSON Web Tokens). To authenticate, include the token in the Authorization header:

```
Authorization: Bearer <token>
```

### Obtaining a Token

To obtain a token, use the login endpoint:

```
POST /api/v1/auth/login/
```

Request body:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Response:
```json
{
  "refresh": "refresh_token",
  "access": "access_token",
  "user": {
    "id": 1,
    "username": "your_username",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### Refreshing a Token

To refresh an expired access token:

```
POST /api/v1/auth/token/refresh/
```

Request body:
```json
{
  "refresh": "refresh_token"
}
```

Response:
```json
{
  "access": "new_access_token"
}
```

## API Endpoints by Module

### Authentication (`/api/v1/auth/`)

#### User Authentication
- `POST /login/` - User login
- `POST /logout/` - User logout
- `POST /token/refresh/` - Refresh access token

#### User Management
- `POST /users/` - Create a new user
- `GET /users/` - List all users
- `GET /users/{id}/` - Get user details
- `PUT /users/{id}/` - Update user
- `DELETE /users/{id}/` - Delete user
- `POST /users/{id}/change-password/` - Change user password

#### Group Management
- `POST /groups/` - Create a new group
- `GET /groups/` - List all groups
- `GET /groups/{id}/` - Get group details
- `PUT /groups/{id}/` - Update group
- `DELETE /groups/{id}/` - Delete group

#### Permission Management
- `GET /permissions/` - List all permissions
- `GET /permissions/{id}/` - Get permission details

### Wildlife (`/api/v1/wildlife/`)

#### Conservation Status
- `GET /conservation-status/` - List all conservation statuses
- `POST /conservation-status/` - Create a new conservation status
- `GET /conservation-status/{id}/` - Get conservation status details
- `PUT /conservation-status/{id}/` - Update conservation status
- `DELETE /conservation-status/{id}/` - Delete conservation status

#### Species
- `GET /species/` - List all species
- `POST /species/` - Create a new species
- `GET /species/{id}/` - Get species details
- `PUT /species/{id}/` - Update species
- `DELETE /species/{id}/` - Delete species

#### Animals
- `GET /animals/` - List all animals
- `POST /animals/` - Create a new animal
- `GET /animals/{id}/` - Get animal details
- `PUT /animals/{id}/` - Update animal
- `DELETE /animals/{id}/` - Delete animal

#### Habitats
- `GET /habitats/` - List all habitats
- `POST /habitats/` - Create a new habitat
- `GET /habitats/{id}/` - Get habitat details
- `PUT /habitats/{id}/` - Update habitat
- `DELETE /habitats/{id}/` - Delete habitat

### Education (`/api/v1/education/`)

#### Programs
- `GET /programas/` - List all programs
- `POST /programas/` - Create a new program
- `GET /programas/{id}/` - Get program details
- `PUT /programas/{id}/` - Update program
- `DELETE /programas/{id}/` - Delete program

#### Instructors
- `GET /instructores/` - List all instructors
- `POST /instructores/` - Create a new instructor
- `GET /instructores/{id}/` - Get instructor details
- `PUT /instructores/{id}/` - Update instructor
- `DELETE /instructores/{id}/` - Delete instructor

#### Schedules
- `GET /horarios/` - List all schedules
- `POST /horarios/` - Create a new schedule
- `GET /horarios/{id}/` - Get schedule details
- `PUT /horarios/{id}/` - Update schedule
- `DELETE /horarios/{id}/` - Delete schedule

#### Enrollments
- `GET /inscripciones/` - List all enrollments
- `POST /inscripciones/` - Create a new enrollment
- `GET /inscripciones/{id}/` - Get enrollment details
- `PUT /inscripciones/{id}/` - Update enrollment
- `DELETE /inscripciones/{id}/` - Delete enrollment

### Exhibitions (`/api/v1/exhibitions/`)

#### Exhibitions
- `GET /exhibiciones/` - List all exhibitions
- `POST /exhibiciones/` - Create a new exhibition
- `GET /exhibiciones/{id}/` - Get exhibition details
- `PUT /exhibiciones/{id}/` - Update exhibition
- `DELETE /exhibiciones/{id}/` - Delete exhibition

#### Exhibition Images
- `GET /imagenes/` - List all exhibition images
- `POST /imagenes/` - Create a new exhibition image
- `GET /imagenes/{id}/` - Get exhibition image details
- `PUT /imagenes/{id}/` - Update exhibition image
- `DELETE /imagenes/{id}/` - Delete exhibition image

#### Exhibition Facts
- `GET /hechos/` - List all exhibition facts
- `POST /hechos/` - Create a new exhibition fact
- `GET /hechos/{id}/` - Get exhibition fact details
- `PUT /hechos/{id}/` - Update exhibition fact
- `DELETE /hechos/{id}/` - Delete exhibition fact

#### Exhibition Buttons
- `GET /botones/` - List all exhibition buttons
- `POST /botones/` - Create a new exhibition button
- `GET /botones/{id}/` - Get exhibition button details
- `PUT /botones/{id}/` - Update exhibition button
- `DELETE /botones/{id}/` - Delete exhibition button

### Infrastructure (`/api/v1/infrastructure/`)

#### Sections
- `GET /secciones/` - List all sections
- `POST /secciones/` - Create a new section
- `GET /secciones/{id}/` - Get section details
- `PUT /secciones/{id}/` - Update section
- `DELETE /secciones/{id}/` - Delete section

#### Habitats
- `GET /habitats/` - List all habitats
- `POST /habitats/` - Create a new habitat
- `GET /habitats/{id}/` - Get habitat details
- `PUT /habitats/{id}/` - Update habitat
- `DELETE /habitats/{id}/` - Delete habitat

### Payments (`/api/v1/payments/`)

#### General Payments
- `POST /pagos/` - Create a new payment
- `GET /pagos/` - List all payments
- `GET /pagos/{id}/` - Get payment details
- `PUT /pagos/{id}/` - Update payment
- `DELETE /pagos/{id}/` - Delete payment

#### Payment Processing
- `POST /pagos/{id}/procesar_pago/` - Process payment with Stripe
- `POST /pagos/{id}/ejecutar_pago/` - Execute PayPal payment
- `POST /pagos/{id}/reembolsar/` - Refund a payment

#### Enrollment Payments
- `POST /pagos-inscripcion/` - Create a new enrollment payment
- `GET /pagos-inscripcion/` - List all enrollment payments
- `GET /pagos-inscripcion/{id}/` - Get enrollment payment details

#### Donations
- `POST /donaciones/` - Create a new donation
- `GET /donaciones/` - List all donations
- `GET /donaciones/{id}/` - Get donation details
- `PUT /donaciones/{id}/` - Update donation
- `DELETE /donaciones/{id}/` - Delete donation

#### Donation Processing
- `POST /donaciones/{id}/procesar_pago/` - Process donation with Stripe
- `POST /donaciones/{id}/ejecutar_pago/` - Execute PayPal donation
- `POST /donaciones/{id}/reembolsar/` - Refund a donation

#### Stripe Webhook
- `POST /stripe/webhook/` - Receive Stripe events

### Tickets (`/api/v1/tickets/`)

#### Tickets
- `POST /tickets/` - Create a new ticket
- `GET /tickets/` - List all tickets
- `GET /tickets/{id}/` - Get ticket details
- `PUT /tickets/{id}/` - Update ticket
- `DELETE /tickets/{id}/` - Delete ticket
- `POST /tickets/{id}/cancelar/` - Cancel a ticket

#### Visits
- `POST /visitas/` - Create a new visit
- `GET /visitas/` - List all visits
- `GET /visitas/{id}/` - Get visit details
- `PUT /visitas/{id}/` - Update visit
- `DELETE /visitas/{id}/` - Delete visit
- `POST /visitas/{id}/cancelar/` - Cancel a visit

#### Availability
- `GET /disponibilidad/` - Check availability for a date
- `GET /precios/` - Get current pricing

### Documents (`/api/v1/documents/`)

#### Document Types
- `POST /tipos/` - Create a new document type
- `GET /tipos/` - List all document types
- `GET /tipos/{id}/` - Get document type details
- `PUT /tipos/{id}/` - Update document type
- `DELETE /tipos/{id}/` - Delete document type

#### Documents
- `POST /documentos/` - Upload a new document
- `GET /documentos/` - List all documents
- `GET /documentos/{id}/` - Get document details
- `PUT /documentos/{id}/` - Update document
- `DELETE /documentos/{id}/` - Delete document
- `GET /documentos/{id}/descargar/` - Download document
- `GET /documentos/{id}/vista-previa/` - Preview document

#### Access History
- `GET /historial/` - List access history
- `GET /historial/{id}/` - Get access record details

### Audit (`/api/v1/audit/`)

#### Audit Logs
- `GET /logs/` - List audit logs
- `GET /logs/{id}/` - Get audit log details
- `POST /logs/export/` - Export audit logs
- `POST /logs/search/` - Search audit logs

#### Audit Reports
- `GET /reports/summary/` - Get audit summary report
- `GET /reports/user-activity/` - Get user activity report
- `GET /reports/model-changes/` - Get model changes report
- `GET /reports/security-events/` - Get security events report

### Messaging (`/api/v1/messaging/`)

#### OTP Management
- `POST /send-otp/` - Send OTP to phone number
- `POST /verify-otp/` - Verify OTP code
- `GET /test-twilio/` - Test Twilio configuration

## Common Response Formats

### Success Responses

Most successful requests return a JSON object with the requested data:

```json
{
  "id": 1,
  "name": "Example Resource",
  "created_at": "2023-01-01T00:00:00Z"
}
```

### Error Responses

Error responses follow a consistent format:

```json
{
  "error": "Error message",
  "details": "Additional details about the error"
}
```

### Pagination

List endpoints support pagination:

```json
{
  "count": 100,
  "next": "http://example.com/api/v1/resources/?page=2",
  "previous": null,
  "results": [
    // Array of resources
  ]
}
```

## Filtering and Search

Many list endpoints support filtering and search parameters:

- `search`: Text search across multiple fields
- `ordering`: Sort results by field (prefix with `-` for descending)
- `page_size`: Number of results per page
- Field-specific filters (e.g., `status=active`)

Example:
```
GET /api/v1/wildlife/species/?search=dolphin&ordering=name&page_size=20
```

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Authentication endpoints**: 10 requests per minute per IP
- **General endpoints**: 100 requests per minute per user
- **Payment endpoints**: 20 requests per minute per user

Exceeding rate limits will result in a 429 (Too Many Requests) response.

## HTTP Status Codes

The API uses standard HTTP status codes:

- `200`: Success
- `201`: Created
- `204`: No Content
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `429`: Too Many Requests
- `500`: Internal Server Error

## Data Validation

All endpoints validate input data and return detailed error messages for invalid data:

```json
{
  "name": [
    "This field is required."
  ],
  "email": [
    "Enter a valid email address."
  ]
}
```

## Versioning

The API is versioned through the URL path:

```
/api/v1/endpoint/
```

Future versions will be available at `/api/v2/`, etc.

## CORS Policy

The API allows cross-origin requests from the following origins:

- `http://localhost:5173`
- `http://127.0.0.1:5173`

Requests must include credentials and use allowed methods and headers.

## Security Considerations

- All API communication should use HTTPS in production
- Tokens should be stored securely and never exposed in client-side code
- Sensitive data should be encrypted at rest
- Input validation is performed on all endpoints
- Rate limiting prevents abuse
- Audit logging tracks all user actions