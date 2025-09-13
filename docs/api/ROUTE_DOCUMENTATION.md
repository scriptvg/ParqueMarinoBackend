# Parque Marino Backend - API Route Documentation

This document provides a comprehensive overview of all available API endpoints in the Parque Marino Backend system, organized by module.

## API Versioning

All endpoints are accessible under two base paths:
- `/api/v1/` - Explicit version 1
- `/api/` - Default to version 1 (backward compatibility)

## Authentication

Most endpoints require authentication via JWT tokens. Include the token in the Authorization header:
```
Authorization: Bearer <token>
```

## Core API Routes

### Authentication Endpoints
- `POST /api/auth/token/` - Obtain JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/register/` - User registration
- `POST /api/auth/forgot-password/` - Request password reset
- `POST /api/auth/reset-password-confirm/` - Confirm password reset

### Messaging Endpoints
- `POST /api/messaging/send-otp/` - Send OTP message
- `POST /api/messaging/verify-otp/` - Verify OTP code
- `GET /api/messaging/test-twilio/` - Test Twilio integration

## Business Modules

### Wildlife Module

#### Animals
- `GET /api/wildlife/animals/` - List all animals
- `POST /api/wildlife/animals/create/` - Create new animal
- `GET /api/wildlife/animals/{id}/` - Get animal details
- `PUT/PATCH /api/wildlife/animals/{id}/update/` - Update animal
- `DELETE /api/wildlife/animals/{id}/delete/` - Delete animal

#### Species
- `GET /api/wildlife/species/` - List all species
- `POST /api/wildlife/species/create/` - Create new species
- `GET /api/wildlife/species/{id}/` - Get species details
- `PUT/PATCH /api/wildlife/species/{id}/update/` - Update species
- `DELETE /api/wildlife/species/{id}/delete/` - Delete species

#### Conservation Status
- `GET /api/wildlife/conservation-status/` - List all conservation statuses
- `POST /api/wildlife/conservation-status/create/` - Create new conservation status
- `GET /api/wildlife/conservation-status/{id}/` - Get conservation status details
- `PUT/PATCH /api/wildlife/conservation-status/{id}/update/` - Update conservation status
- `DELETE /api/wildlife/conservation-status/{id}/delete/` - Delete conservation status

#### Habitats
- `GET /api/wildlife/habitats/` - List all habitats
- `POST /api/wildlife/habitats/create/` - Create new habitat
- `GET /api/wildlife/habitats/{id}/` - Get habitat details
- `PUT/PATCH /api/wildlife/habitats/{id}/update/` - Update habitat
- `DELETE /api/wildlife/habitats/{id}/delete/` - Delete habitat

### Exhibitions Module

#### Exhibitions
- `GET /api/exhibitions/exhibiciones/` - List all exhibitions
- `POST /api/exhibitions/exhibiciones/create/` - Create new exhibition
- `GET /api/exhibitions/exhibiciones/{id}/` - Get exhibition details
- `GET /api/exhibitions/exhibiciones/{id}/full_details/` - Get full exhibition details
- `PUT/PATCH /api/exhibitions/exhibiciones/{id}/update/` - Update exhibition
- `DELETE /api/exhibitions/exhibiciones/{id}/delete/` - Delete exhibition

#### Exhibition Images
- `GET /api/exhibitions/exhibicion-images/` - List all exhibition images
- `POST /api/exhibitions/exhibicion-images/create/` - Create new exhibition image
- `GET /api/exhibitions/exhibicion-images/{id}/` - Get exhibition image details
- `PUT/PATCH /api/exhibitions/exhibicion-images/{id}/update/` - Update exhibition image
- `DELETE /api/exhibitions/exhibicion-images/{id}/delete/` - Delete exhibition image

#### Exhibition Descriptions
- `GET /api/exhibitions/exhibicion-descriptions/` - List all exhibition descriptions
- `POST /api/exhibitions/exhibicion-descriptions/create/` - Create new exhibition description
- `GET /api/exhibitions/exhibicion-descriptions/{id}/` - Get exhibition description details
- `PUT/PATCH /api/exhibitions/exhibicion-descriptions/{id}/update/` - Update exhibition description
- `DELETE /api/exhibitions/exhibicion-descriptions/{id}/delete/` - Delete exhibition description

#### Exhibition Facts
- `GET /api/exhibitions/exhibicion-facts/` - List all exhibition facts
- `POST /api/exhibitions/exhibicion-facts/create/` - Create new exhibition fact
- `GET /api/exhibitions/exhibicion-facts/{id}/` - Get exhibition fact details
- `PUT/PATCH /api/exhibitions/exhibicion-facts/{id}/update/` - Update exhibition fact
- `DELETE /api/exhibitions/exhibicion-facts/{id}/delete/` - Delete exhibition fact

#### Exhibition Buttons
- `GET /api/exhibitions/exhibicion-buttons/` - List all exhibition buttons
- `POST /api/exhibitions/exhibicion-buttons/create/` - Create new exhibition button
- `GET /api/exhibitions/exhibicion-buttons/{id}/` - Get exhibition button details
- `PUT/PATCH /api/exhibitions/exhibicion-buttons/{id}/update/` - Update exhibition button
- `DELETE /api/exhibitions/exhibicion-buttons/{id}/delete/` - Delete exhibition button

### Education Module

#### Educational Programs
- `GET /api/education/programas-educativos/` - List all educational programs
- `POST /api/education/programas-educativos/create/` - Create new educational program
- `GET /api/education/programas-educativos/{id}/` - Get educational program details
- `PUT/PATCH /api/education/programas-educativos/{id}/update/` - Update educational program
- `DELETE /api/education/programas-educativos/{id}/delete/` - Delete educational program

#### Educational Services
- `GET /api/education/servicios-educativos/` - List all educational services
- `POST /api/education/servicios-educativos/create/` - Create new educational service
- `GET /api/education/servicios-educativos/{id}/` - Get educational service details
- `PUT/PATCH /api/education/servicios-educativos/{id}/update/` - Update educational service
- `DELETE /api/education/servicios-educativos/{id}/delete/` - Delete educational service

#### Educational Service Images
- `GET /api/education/servicios-educativos-images/` - List all educational service images
- `POST /api/education/servicios-educativos-images/create/` - Create new educational service image
- `GET /api/education/servicios-educativos-images/{id}/` - Get educational service image details
- `PUT/PATCH /api/education/servicios-educativos-images/{id}/update/` - Update educational service image
- `DELETE /api/education/servicios-educativos-images/{id}/delete/` - Delete educational service image

#### Educational Service Descriptions
- `GET /api/education/servicios-educativos-descriptions/` - List all educational service descriptions
- `POST /api/education/servicios-educativos-descriptions/create/` - Create new educational service description
- `GET /api/education/servicios-educativos-descriptions/{id}/` - Get educational service description details
- `PUT/PATCH /api/education/servicios-educativos-descriptions/{id}/update/` - Update educational service description
- `DELETE /api/education/servicios-educativos-descriptions/{id}/delete/` - Delete educational service description

#### Educational Service Facts
- `GET /api/education/servicios-educativos-facts/` - List all educational service facts
- `POST /api/education/servicios-educativos-facts/create/` - Create new educational service fact
- `GET /api/education/servicios-educativos-facts/{id}/` - Get educational service fact details
- `PUT/PATCH /api/education/servicios-educativos-facts/{id}/update/` - Update educational service fact
- `DELETE /api/education/servicios-educativos-facts/{id}/delete/` - Delete educational service fact

#### Educational Service Buttons
- `GET /api/education/servicios-educativos-buttons/` - List all educational service buttons
- `POST /api/education/servicios-educativos-buttons/create/` - Create new educational service button
- `GET /api/education/servicios-educativos-buttons/{id}/` - Get educational service button details
- `PUT/PATCH /api/education/servicios-educativos-buttons/{id}/update/` - Update educational service button
- `DELETE /api/education/servicios-educativos-buttons/{id}/delete/` - Delete educational service button

#### Instructors
- `GET /api/education/instructores/` - List all instructors
- `POST /api/education/instructores/create/` - Create new instructor
- `GET /api/education/instructores/{id}/` - Get instructor details
- `PUT/PATCH /api/education/instructores/{id}/update/` - Update instructor
- `DELETE /api/education/instructores/{id}/delete/` - Delete instructor

#### Schedules
- `GET /api/education/horarios/` - List all schedules
- `POST /api/education/horarios/create/` - Create new schedule
- `GET /api/education/horarios/{id}/` - Get schedule details
- `PUT/PATCH /api/education/horarios/{id}/update/` - Update schedule
- `DELETE /api/education/horarios/{id}/delete/` - Delete schedule

#### Enrollments
- `GET /api/education/inscripciones/` - List all enrollments
- `POST /api/education/inscripciones/create/` - Create new enrollment
- `GET /api/education/inscripciones/{id}/` - Get enrollment details
- `PUT/PATCH /api/education/inscripciones/{id}/update/` - Update enrollment
- `DELETE /api/education/inscripciones/{id}/delete/` - Delete enrollment

#### Program Items
- `GET /api/education/programa-items/` - List all program items
- `POST /api/education/programa-items/create/` - Create new program item
- `GET /api/education/programa-items/{id}/` - Get program item details
- `PUT/PATCH /api/education/programa-items/{id}/update/` - Update program item
- `DELETE /api/education/programa-items/{id}/delete/` - Delete program item

### Payments Module

#### Payments
- `GET /api/payments/pagos/` - List all payments
- `POST /api/payments/pagos/create/` - Create new payment
- `GET /api/payments/pagos/{id}/` - Get payment details
- `POST /api/payments/pagos/{id}/procesar_pago/` - Process payment with Stripe
- `PUT/PATCH /api/payments/pagos/{id}/update/` - Update payment
- `DELETE /api/payments/pagos/{id}/delete/` - Delete payment

#### Enrollment Payments
- `GET /api/payments/pagos-inscripcion/` - List all enrollment payments
- `POST /api/payments/pagos-inscripcion/create/` - Create new enrollment payment
- `GET /api/payments/pagos-inscripcion/{id}/` - Get enrollment payment details
- `POST /api/payments/pagos-inscripcion/{id}/procesar_pago_inscripcion/` - Process enrollment payment
- `PUT/PATCH /api/payments/pagos-inscripcion/{id}/update/` - Update enrollment payment
- `DELETE /api/payments/pagos-inscripcion/{id}/delete/` - Delete enrollment payment

#### Donations
- `GET /api/payments/donaciones/` - List all donations
- `POST /api/payments/donaciones/create/` - Create new donation
- `GET /api/payments/donaciones/{id}/` - Get donation details
- `POST /api/payments/donaciones/{id}/procesar_donacion/` - Process donation with Stripe
- `PUT/PATCH /api/payments/donaciones/{id}/update/` - Update donation
- `DELETE /api/payments/donaciones/{id}/delete/` - Delete donation

#### Admin Payments
- `GET /api/payments/admin-pagos/` - List all admin payments
- `POST /api/payments/admin-pagos/create/` - Create new admin payment
- `GET /api/payments/admin-pagos/{id}/` - Get admin payment details
- `POST /api/payments/admin-pagos/{id}/procesar_pago_admin/` - Process admin payment
- `PUT/PATCH /api/payments/admin-pagos/{id}/update/` - Update admin payment
- `DELETE /api/payments/admin-pagos/{id}/delete/` - Delete admin payment

#### Admin Enrollment Payments
- `GET /api/payments/admin-pagos-inscripcion/` - List all admin enrollment payments
- `POST /api/payments/admin-pagos-inscripcion/create/` - Create new admin enrollment payment
- `GET /api/payments/admin-pagos-inscripcion/{id}/` - Get admin enrollment payment details
- `POST /api/payments/admin-pagos-inscripcion/{id}/procesar_pago_inscripcion_admin/` - Process admin enrollment payment
- `PUT/PATCH /api/payments/admin-pagos-inscripcion/{id}/update/` - Update admin enrollment payment
- `DELETE /api/payments/admin-pagos-inscripcion/{id}/delete/` - Delete admin enrollment payment

#### Admin Donations
- `GET /api/payments/admin-donaciones/` - List all admin donations
- `POST /api/payments/admin-donaciones/create/` - Create new admin donation
- `GET /api/payments/admin-donaciones/{id}/` - Get admin donation details
- `POST /api/payments/admin-donaciones/{id}/procesar_donacion_admin/` - Process admin donation
- `PUT/PATCH /api/payments/admin-donaciones/{id}/update/` - Update admin donation
- `DELETE /api/payments/admin-donaciones/{id}/delete/` - Delete admin donation

### Tickets Module

#### Tickets
- `GET /api/tickets/tickets/` - List all tickets
- `POST /api/tickets/tickets/create/` - Create new ticket
- `GET /api/tickets/tickets/{id}/` - Get ticket details
- `POST /api/tickets/tickets/{id}/check_availability/` - Check ticket availability
- `PUT/PATCH /api/tickets/tickets/{id}/update/` - Update ticket
- `DELETE /api/tickets/tickets/{id}/delete/` - Delete ticket

#### Visits
- `GET /api/tickets/visits/` - List all visits
- `POST /api/tickets/visits/create/` - Create new visit
- `GET /api/tickets/visits/{id}/` - Get visit details
- `PUT/PATCH /api/tickets/visits/{id}/update/` - Update visit
- `DELETE /api/tickets/visits/{id}/delete/` - Delete visit

### Infrastructure Module

#### Sections
- `GET /api/infrastructure/sections/` - List all sections
- `POST /api/infrastructure/sections/create/` - Create new section
- `GET /api/infrastructure/sections/{id}/` - Get section details
- `PUT/PATCH /api/infrastructure/sections/{id}/update/` - Update section
- `DELETE /api/infrastructure/sections/{id}/delete/` - Delete section

#### Infrastructure Habitats
- `GET /api/infrastructure/habitats/` - List all infrastructure habitats
- `POST /api/infrastructure/habitats/create/` - Create new infrastructure habitat
- `GET /api/infrastructure/habitats/{id}/` - Get infrastructure habitat details
- `PUT/PATCH /api/infrastructure/habitats/{id}/update/` - Update infrastructure habitat
- `DELETE /api/infrastructure/habitats/{id}/delete/` - Delete infrastructure habitat

### Documents Module

#### Documents
- `GET /api/documents/documentos/` - List all documents
- `POST /api/documents/documentos/create/` - Create new document
- `GET /api/documents/documentos/{id}/` - Get document details
- `PUT/PATCH /api/documents/documentos/{id}/update/` - Update document
- `DELETE /api/documents/documentos/{id}/delete/` - Delete document

#### Document History
- `GET /api/documents/historial-documentos/` - List all document history records
- `GET /api/documents/historial-documentos/{id}/` - Get document history record details

### Support Modules

#### Audit
- `GET /api/audit/audit-logs/` - List all audit logs
- `GET /api/audit/audit-logs/{id}/` - Get audit log details

#### Security

##### Users
- `GET /api/auth/users/` - List all users
- `POST /api/auth/users/create/` - Create new user
- `GET /api/auth/users/{id}/` - Get user details
- `PUT/PATCH /api/auth/users/{id}/update/` - Update user
- `DELETE /api/auth/users/{id}/delete/` - Delete user

##### User Profiles
- `GET /api/auth/user-profiles/` - List all user profiles
- `POST /api/auth/user-profiles/create/` - Create new user profile
- `GET /api/auth/user-profiles/{id}/` - Get user profile details
- `PUT/PATCH /api/auth/user-profiles/{id}/update/` - Update user profile
- `DELETE /api/auth/user-profiles/{id}/delete/` - Delete user profile

##### Roles
- `GET /api/auth/roles/` - List all roles
- `GET /api/auth/roles/{id}/` - Get role details

##### Permissions
- `GET /api/auth/permissions/` - List all permissions
- `GET /api/auth/permissions/{id}/` - Get permission details

## Response Format

All API responses follow a consistent JSON format:

```json
{
  "status": "success|error",
  "data": {...},
  "message": "Description of the response"
}
```

## Error Handling

Errors are returned with appropriate HTTP status codes and a JSON response containing error details:

```json
{
  "status": "error",
  "error": "Error code",
  "message": "Human-readable error message"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. Exceeding the limit will result in a 429 (Too Many Requests) response.