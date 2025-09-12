# Development Documentation

This directory contains all development-related documentation for the Parque Marino Backend.

## Contents

- [GUIA_DESARROLLO.md](GUIA_DESARROLLO.md) - Main development guide in Spanish
- [WILDLIFE_TEST_REPORT.md](WILDLIFE_TEST_REPORT.md) - Test report for wildlife module
- [Coding Standards](CODING_STANDARDS.md) - Code style and best practices (to be created)
- [Testing Guidelines](TESTING.md) - How to write and run tests (to be created)
- [Development Environment Setup](SETUP.md) - Detailed setup instructions (to be created)

## Project Structure

The project follows a modular architecture:

```
apps/
  business/     # Core business logic modules
  support/      # Support modules (security, audit)
  integrations/ # Third-party integrations
api/            # API layer with versioning
config/         # Configuration files
docs/           # Documentation
```

## Getting Started

1. Set up your development environment
2. Install dependencies with `pip install -r requirements.txt`
3. Configure environment variables
4. Run migrations with `python manage.py migrate`
5. Start the development server with `python manage.py runserver`

For detailed instructions, see [GUIA_DESARROLLO.md](GUIA_DESARROLLO.md).