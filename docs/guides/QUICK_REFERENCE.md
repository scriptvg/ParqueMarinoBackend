# Quick Reference Guide

This document provides a quick reference to the most important aspects of the Parque Marino Backend system.

## System Overview

- **Framework**: Django 5.2.3
- **API**: Django REST Framework 3.16.0
- **Authentication**: JWT via djangorestframework_simplejwt
- **Database**: SQLite (development), PostgreSQL/MySQL (production)
- **Storage**: AWS S3 via django-storages
- **Caching**: Redis via django-redis
- **Payments**: Stripe 10.10.0, PayPal (custom integration)
- **Messaging**: Twilio 8.8.0

## Key Modules

### Business Modules
1. **Wildlife** - Species, animals, habitats, conservation status
2. **Education** - Programs, instructors, schedules, enrollments
3. **Exhibitions** - Content management for exhibits
4. **Infrastructure** - Physical sections and habitats
5. **Payments** - Payment processing, donations, invoicing
6. **Tickets** - Ticketing and visit management
7. **Documents** - File management and versioning

### Support Modules
1. **Security** - Authentication, authorization, permissions
2. **Audit** - System logging and audit trails
3. **Messaging** - SMS and OTP functionality

### Integration Modules
1. **Payments** - Stripe and PayPal integrations

## API Endpoints

### Authentication
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/token/refresh/` - Refresh access token

### Core Business Modules
- `/api/v1/wildlife/` - Wildlife management
- `/api/v1/education/` - Educational programs
- `/api/v1/exhibitions/` - Exhibition content
- `/api/v1/infrastructure/` - Physical infrastructure
- `/api/v1/payments/` - Payment processing
- `/api/v1/tickets/` - Ticket management
- `/api/v1/documents/` - Document management

### Support Modules
- `/api/v1/audit/` - Audit logs
- `/api/v1/auth/` - Authentication
- `/api/v1/messaging/` - SMS and OTP functionality

## Environment Variables

### Core Settings
```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True/False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database (if not using SQLite)
```env
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### AWS S3
```env
USE_S3=True/False
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_STORAGE_BUCKET_NAME=your-s3-bucket-name
```

### Stripe
```env
STRIPE_PUBLIC_KEY=pk_test_example_public_key_here
STRIPE_SECRET_KEY=sk_test_example_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_example_webhook_secret_here
```

### PayPal
```env
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_CLIENT_SECRET=your_client_secret
PAYPAL_SANDBOX=True/False
PAYPAL_RETURN_URL=http://localhost:8000/paypal/return/
PAYPAL_CANCEL_URL=http://localhost:8000/paypal/cancel/
```

### Twilio
```env
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number
TEST_PHONE_NUMBER=your-test-phone-number
```

## Common Tasks

### Running the Development Server
```bash
python manage.py runserver
```

### Running Migrations
```bash
python manage.py migrate
```

### Creating a Superuser
```bash
python manage.py createsuperuser
```

### Running Tests
```bash
python manage.py test
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Docker Commands

### Building and Running with Docker
```bash
docker-compose -f docker/docker-compose.yml up --build
```

## Key URLs

### API Endpoints
- **API Base**: `/api/v1/`
- **API Documentation**: `/api/v1/docs/` or `/api/v1/redoc/`
- **Admin Interface**: `/admin/`

### Authentication
- **Login**: `/api/v1/auth/login/`
- **Token Refresh**: `/api/v1/auth/token/refresh/`

## Common API Patterns

### Pagination
```
GET /api/v1/wildlife/species/?page=2&page_size=20
```

### Filtering
```
GET /api/v1/wildlife/species/?name=dolphin&conservation_status=VU
```

### Search
```
GET /api/v1/education/programas/?search=marine
```

### Ordering
```
GET /api/v1/wildlife/species/?ordering=name
GET /api/v1/wildlife/species/?ordering=-created_at
```

## Error Handling

### Common HTTP Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

### Error Response Format
```json
{
  "error": "Error message",
  "details": "Additional details"
}
```

## Security Best Practices

1. **Always use HTTPS** in production
2. **Store secrets in environment variables**
3. **Regularly rotate API keys**
4. **Implement proper authentication and authorization**
5. **Validate all input data**
6. **Keep dependencies up to date**
7. **Monitor logs for suspicious activity**

## Useful Documentation Links

- [Complete Backend Overview](../BACKEND_OVERVIEW.md)
- [API Documentation](API_DOCUMENTATION.md)
- [System Modules](../SYSTEM_MODULES.md)
- [Documentation Summary](../DOCUMENTATION_SUMMARY.md)

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check DATABASE_URL environment variable
   - Verify database server is running
   - Ensure database drivers are installed

2. **S3 File Upload Issues**
   - Verify AWS credentials
   - Check bucket permissions
   - Ensure correct region configuration

3. **Payment Processing Failures**
   - Verify Stripe/PayPal API keys
   - Check webhook configurations
   - Review payment logs

4. **Authentication Problems**
   - Verify JWT configuration
   - Check user permissions
   - Review token expiration settings

### Getting Help

1. **Check logs**: `tail -f logs/django.log`
2. **Review documentation**: Start with this quick reference
3. **Run tests**: `python manage.py test`
4. **Consult module-specific documentation**