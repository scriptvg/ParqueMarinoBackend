# Settings Configuration Instructions

This document explains how to configure and use the new modular settings system.

## Overview

The settings have been reorganized into a modular structure to support different environments:

- `config.settings.base` - Base settings (common to all environments)
- `config.settings.development` - Development environment settings
- `config.settings.production` - Production environment settings

## How to Use

### For Development

Set the `DJANGO_SETTINGS_MODULE` environment variable:

**Windows (PowerShell):**
```powershell
$env:DJANGO_SETTINGS_MODULE = "config.settings.development"
python manage.py runserver
```

**Windows (Command Prompt):**
```cmd
set DJANGO_SETTINGS_MODULE=config.settings.development
python manage.py runserver
```

**macOS/Linux:**
```bash
export DJANGO_SETTINGS_MODULE=config.settings.development
python manage.py runserver
```

### For Production

Set the `DJANGO_SETTINGS_MODULE` environment variable:

**Linux/Unix:**
```bash
export DJANGO_SETTINGS_MODULE=config.settings.production
gunicorn config.wsgi:application
```

**Docker (in Dockerfile):**
```dockerfile
ENV DJANGO_SETTINGS_MODULE=config.settings.production
```

### Using with manage.py

You can also specify the settings module when running manage.py commands:

```bash
python manage.py runserver --settings=config.settings.development
python manage.py migrate --settings=config.settings.production
```

## Environment Variables

The new settings structure makes use of several environment variables:

### Required Variables
- `DJANGO_SECRET_KEY` - Django secret key
- `DATABASE_URL` - Database connection string (production)

### Optional Variables
- `DJANGO_DEBUG` - Enable/disable debug mode
- `DJANGO_ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `AWS_ACCESS_KEY_ID` - AWS credentials for S3
- `AWS_SECRET_ACCESS_KEY` - AWS credentials for S3
- `AWS_STORAGE_BUCKET_NAME` - S3 bucket name
- `STRIPE_PUBLIC_KEY` - Stripe public key
- `STRIPE_SECRET_KEY` - Stripe secret key

## Configuration Files

### Base Settings (`config/settings/base.py`)
Contains all common settings that are shared between environments.

### Development Settings (`config/settings/development.py`)
Overrides settings for development:
- `DEBUG = True`
- Console email backend
- SQLite database
- Detailed logging

### Production Settings (`config/settings/production.py`)
Overrides settings for production:
- `DEBUG = False`
- Security enhancements
- Database configuration from `DATABASE_URL`
- File-based logging

## Backward Compatibility

The original `config/settings.py` file is maintained for backward compatibility. If no `DJANGO_SETTINGS_MODULE` is specified, it will be used by default.

## Best Practices

1. **Never commit secrets** - Always use environment variables for sensitive data
2. **Environment-specific configurations** - Use the appropriate settings module for each environment
3. **Testing** - Test your application with both development and production settings
4. **Documentation** - Document any new environment variables you add

## Troubleshooting

### "Settings not found" Error
Make sure you've set the `DJANGO_SETTINGS_MODULE` environment variable correctly.

### "Module not found" Error
Verify that the settings files exist in the correct locations and that there are no typos in the module names.

### Database Connection Issues
Ensure that the `DATABASE_URL` environment variable is properly configured for production environments.

## Customization

To add environment-specific settings:

1. Create a new settings file in `config/settings/`
2. Import from `base.py`: `from .base import *`
3. Override or add settings as needed
4. Set the `DJANGO_SETTINGS_MODULE` environment variable to point to your new module