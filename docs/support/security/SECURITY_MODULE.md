# Security Module

## Overview

The Security module handles all aspects of user authentication, authorization, and permissions for the Parque Marino Backend. It provides JWT-based authentication, role-based access control, and comprehensive security features.

## Key Features

- JWT-based authentication
- Role-based access control
- User management
- Password security
- Session management
- Permission system
- Audit logging integration
- Two-factor authentication support

## Authentication System

### JWT Implementation

The system uses JSON Web Tokens (JWT) for secure authentication:

1. **Access Tokens**: Short-lived tokens for API access (5 minutes)
2. **Refresh Tokens**: Longer-lived tokens for obtaining new access tokens (1 day)
3. **Token Rotation**: Refresh tokens are rotated after use
4. **Blacklisting**: Expired tokens are blacklisted to prevent reuse

### Login Process

1. User provides credentials (username/email and password)
2. Credentials are verified against the database
3. If valid, JWT tokens are generated and returned
4. Tokens are used for subsequent API requests

### Logout Process

1. Refresh token is blacklisted
2. User session is terminated
3. Tokens become invalid

## User Management

### User Roles

The system supports multiple user roles with different permissions:

1. **Superuser**: Full system access (Django admin)
2. **Administrator**: Full application access
3. **Staff**: Limited access based on assigned permissions
4. **User**: Basic access to public features
5. **Content Manager**: Access to content management features
6. **Financial Staff**: Access to payment-related features
7. **Gate Staff**: Access to ticket validation features

### User Permissions

Permissions are managed through Django's built-in permission system:

1. **Model-level Permissions**: CRUD permissions for each model
2. **Object-level Permissions**: Fine-grained control over specific objects
3. **Custom Permissions**: Application-specific permissions
4. **Group Permissions**: Permissions assigned to user groups

## API Endpoints

### Authentication

- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/logout/` - User logout
- `POST /api/v1/auth/token/refresh/` - Refresh access token
- `POST /api/v1/auth/password/reset/` - Request password reset
- `POST /api/v1/auth/password/reset/confirm/` - Confirm password reset

### User Management

- `POST /api/v1/auth/users/` - Create a new user
- `GET /api/v1/auth/users/` - List all users
- `GET /api/v1/auth/users/{id}/` - Get user details
- `PUT /api/v1/auth/users/{id}/` - Update user
- `DELETE /api/v1/auth/users/{id}/` - Delete user
- `POST /api/v1/auth/users/{id}/change-password/` - Change user password

### Group Management

- `POST /api/v1/auth/groups/` - Create a new group
- `GET /api/v1/auth/groups/` - List all groups
- `GET /api/v1/auth/groups/{id}/` - Get group details
- `PUT /api/v1/auth/groups/{id}/` - Update group
- `DELETE /api/v1/auth/groups/{id}/` - Delete group

### Permission Management

- `GET /api/v1/auth/permissions/` - List all permissions
- `GET /api/v1/auth/permissions/{id}/` - Get permission details

## Usage Examples

### User Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure_password123"
  }'
```

Response:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### Accessing Protected Endpoints

```bash
curl -X GET http://localhost:8000/api/v1/wildlife/species/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### Refreshing Access Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

## Password Security

The system implements robust password security measures:

1. **Hashing**: Passwords are hashed using Django's built-in hasher
2. **Validation**: Password complexity requirements
3. **Reset**: Secure password reset workflow
4. **Expiration**: Password expiration policies
5. **History**: Password history to prevent reuse

### Password Requirements

- Minimum 8 characters
- Mix of uppercase and lowercase letters
- At least one number
- At least one special character
- Not based on common passwords
- Not based on user information

## Session Management

The system provides comprehensive session management:

1. **Token Expiration**: Automatic token expiration
2. **Concurrent Sessions**: Multiple active sessions per user
3. **Session Revocation**: Ability to revoke specific sessions
4. **Device Tracking**: Track login devices and locations
5. **Inactivity Timeout**: Automatic logout after inactivity

## Two-Factor Authentication

Support for two-factor authentication is built into the system:

1. **SMS-based 2FA**: Using Twilio for code delivery
2. **Authenticator Apps**: Support for TOTP-based apps
3. **Backup Codes**: Recovery codes for lost devices
4. **Device Management**: Manage trusted devices

## Permissions System

The system uses Django's permission framework with custom enhancements:

1. **Built-in Permissions**: Add, change, delete, view permissions for each model
2. **Custom Permissions**: Application-specific permissions
3. **Permission Checks**: Decorators and mixins for permission enforcement
4. **Object-level Permissions**: Fine-grained control over individual objects

## Security Features

### CORS Configuration

Cross-Origin Resource Sharing is configured to allow only trusted origins:

1. **Allowed Origins**: Specific domains allowed to access the API
2. **Allowed Methods**: HTTP methods permitted
3. **Allowed Headers**: HTTP headers permitted
4. **Credentials**: Cookie and authorization header handling

### Rate Limiting

API rate limiting prevents abuse:

1. **Login Attempts**: Limit login attempts per IP
2. **API Requests**: Limit API requests per user
3. **Password Resets**: Limit password reset requests
4. **Custom Limits**: Configurable rate limits per endpoint

### Input Validation

Comprehensive input validation prevents injection attacks:

1. **Data Sanitization**: Clean user input
2. **Type Validation**: Ensure correct data types
3. **Length Validation**: Prevent buffer overflows
4. **Format Validation**: Validate data formats (emails, phones, etc.)

## Integration Points

- **Audit Module**: Logs all authentication and authorization events
- **Messaging Module**: Sends security notifications and 2FA codes
- **All Business Modules**: Enforces access control on all endpoints

## Future Enhancements

- Single Sign-On (SSO) integration
- Advanced threat detection
- Behavioral analytics for suspicious activity
- Enhanced passwordless authentication options
- Biometric authentication support
- Security incident response automation