# Migration Guide: Enhanced Project Structure

This document explains the changes made to improve the project's architecture and how to adapt to the new structure.

## Overview of Changes

We've reorganized the project to follow a more scalable and maintainable architecture while preserving all existing functionality:

1. **Directory Structure** - Created a modular organization under `apps/`
2. **Settings Management** - Split settings into environment-specific configurations
3. **API Structure** - Enhanced with versioning support
4. **Documentation** - Organized into logical sections

## Directory Structure Changes

### New Structure
```
ParqueMarinoBackend/
├── apps/
│   ├── business/          # Core business modules
│   │   ├── wildlife/
│   │   ├── education/
│   │   ├── exhibitions/
│   │   ├── infrastructure/
│   │   ├── payments/
│   │   ├── tickets/
│   │   └── documents/
│   ├── support/           # Support modules
│   │   ├── security/
│   │   └── audit/
│   ├── integrations/      # Third-party integrations
│   │   └── payments/
│   └── core/              # Core framework extensions (future use)
├── api/                   # API layer with versioning
│   └── v1/                # Version 1 of the API
├── config/                # Configuration
│   └── settings/          # Modular settings
├── docs/                  # Organized documentation
│   ├── api/
│   ├── development/
│   └── deployment/
├── templates/             # Email templates
└── ...                    # Other existing files
```

### Benefits
- Clear separation of concerns
- Easier to locate and manage modules
- Better support for scaling
- Improved maintainability

## Settings Management

### New Settings Structure
- `config/settings/base.py` - Base configuration (inherits from original settings.py)
- `config/settings/development.py` - Development-specific settings
- `config/settings/production.py` - Production-specific settings
- `config/settings/__init__.py` - Dynamic loading based on environment

### Migration Steps
1. Set the `DJANGO_SETTINGS_MODULE` environment variable:
   - For development: `config.settings.development`
   - For production: `config.settings.production`
2. The original `config/settings.py` is maintained for backward compatibility

## API Structure

### New API Organization
- `api/v1/` - Version 1 of the API with standardized responses
- `api/v1/base_views.py` - Base API view classes with common functionality
- `api/v1/routers.py` - API routers for viewsets
- `api/v1/urls.py` - URL configuration for API v1
- `api/urls.py` - Main API URL configuration with versioning support

### Benefits
- Clear API versioning
- Standardized response formats
- Easier to maintain and extend
- Backward compatibility preserved

## Documentation Organization

### New Documentation Structure
- `docs/README.md` - Main documentation entry point
- `docs/api/` - API-related documentation
- `docs/development/` - Development guides and resources
- `docs/deployment/` - Deployment instructions and procedures

### Moved Files
- `API_DOCUMENTATION.md` → `docs/api/API_DOCUMENTATION.md`
- `GUIA_DESARROLLO.md` → `docs/development/GUIA_DESARROLLO.md`
- `S3_FILE_DELETION_README.md` → `docs/deployment/S3_FILE_DELETION_README.md`
- `WILDLIFE_TEST_REPORT.md` → `docs/development/WILDLIFE_TEST_REPORT.md`

## Migration Checklist

### Immediate Actions
- [ ] Update environment variables to use new settings modules
- [ ] Verify that all existing functionality works as expected
- [ ] Update any deployment scripts to reference new paths
- [ ] Review documentation updates

### Optional Enhancements
- [ ] Move existing apps to the new `apps/business/` directory structure
- [ ] Utilize the new API base views for standardized responses
- [ ] Take advantage of environment-specific settings

## Backward Compatibility

All existing functionality is preserved:
- Original directory structure remains intact
- Existing URLs continue to work
- Original settings file is maintained
- No code changes required for existing functionality

The new structure is additive and designed to improve maintainability without breaking existing code.