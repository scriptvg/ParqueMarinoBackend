# Deployment Documentation

This directory contains all deployment-related documentation for the Parque Marino Backend.

## Contents

- [S3_FILE_DELETION_README.md](S3_FILE_DELETION_README.md) - Instructions for S3 file management
- [Deployment Checklist](CHECKLIST.md) - Pre-deployment verification steps (to be created)
- [Environment Configuration](ENVIRONMENT.md) - How to configure different environments (to be created)
- [Monitoring and Logging](MONITORING.md) - How to monitor the application in production (to be created)

## Deployment Process

1. Prepare the production environment
2. Configure environment variables
3. Set up the database
4. Deploy static files to S3
5. Configure the web server (Gunicorn, Nginx, etc.)
6. Start the application
7. Verify deployment

## Environment Variables

Key environment variables needed for deployment:

- `DJANGO_SECRET_KEY` - Django secret key
- `DJANGO_DEBUG` - Should be False in production
- `DATABASE_URL` - Database connection string
- `AWS_ACCESS_KEY_ID` - AWS credentials for S3
- `AWS_SECRET_ACCESS_KEY` - AWS credentials for S3
- `AWS_STORAGE_BUCKET_NAME` - S3 bucket name
- `STRIPE_PUBLIC_KEY` - Stripe public key
- `STRIPE_SECRET_KEY` - Stripe secret key

For detailed S3 file management instructions, see [S3_FILE_DELETION_README.md](S3_FILE_DELETION_README.md).