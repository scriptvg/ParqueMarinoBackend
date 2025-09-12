# Documentation Organization

This document explains how the documentation in the Parque Marino Backend project is organized.

## Directory Structure

```
docs/
├── architecture/           # System architecture and design documents
├── business/               # Business module documentation
│   ├── documents/
│   ├── education/
│   ├── exhibitions/
│   ├── infrastructure/
│   ├── payments/
│   ├── tickets/
│   └── wildlife/
├── deployment/            # Deployment and configuration guides
├── guides/                # General guides and tutorials
├── integrations/          # Third-party service integration documentation
│   ├── paypal/
│   ├── stripe/
│   └── twilio/
├── support/               # Support module documentation
│   ├── audit/
│   ├── messaging/
│   └── security/
└── testing/               # Testing documentation and reports
```

## Directory Descriptions

### architecture/
Contains documents related to the overall system architecture, including:
- System design documents
- Architecture diagrams
- Organizational summaries
- Project structure documentation
- Reorganization summaries
- Change summaries

### business/
Contains documentation specific to each business module:
- **documents/**: [Document management system documentation](business/documents/DOCUMENTS_MODULE.md)
- **education/**: [Educational programs documentation](business/education/EDUCATION_MODULE.md)
- **exhibitions/**: [Exhibition management documentation](business/exhibitions/EXHIBITIONS_MODULE.md)
- **infrastructure/**: [Infrastructure management documentation](business/infrastructure/INFRASTRUCTURE_MODULE.md)
- **payments/**: [Payment system documentation](business/payments/PAYMENTS_MODULE.md)
- **tickets/**: [Ticketing system documentation](business/tickets/TICKETS_MODULE.md)
- **wildlife/**: [Wildlife management documentation](business/wildlife/WILDLIFE_MODULE.md)

### deployment/
Contains documentation related to deploying and configuring the system:
- Migration guides
- Settings instructions
- S3 file deletion documentation
- Deployment READMEs

### guides/
Contains general guides and tutorials for developers and users:
- [API documentation](guides/API_DOCUMENTATION.md)
- [Quick Reference Guide](guides/QUICK_REFERENCE.md)
- Development guides
- Frontend integration guides
- Project README
- General tutorials

### integrations/
Contains documentation for third-party service integrations:
- **paypal/**: [PayPal integration documentation](integrations/paypal/PAYPAL_INTEGRATION.md)
- **stripe/**: [Stripe integration documentation](integrations/stripe/STRIPE_INTEGRATION.md)
- **twilio/**: [Twilio integration documentation](integrations/twilio/TWILIO_INTEGRATION.md)

### support/
Contains documentation for support modules:
- **audit/**: [Audit logging documentation](support/audit/AUDIT_MODULE.md)
- **messaging/**: [Messaging system documentation](support/messaging/MESSAGING_MODULE.md)
- **security/**: [Security system documentation](support/security/SECURITY_MODULE.md)

### testing/
Contains testing-related documentation and reports:
- Test reports
- Testing guides
- Quality assurance documentation

## File Naming Conventions

- Use descriptive names that clearly indicate the content
- Use underscores to separate words in filenames
- Use uppercase for the first letter of each major word (Title Case)
- End filenames with the appropriate extension (.md for Markdown)

## Updating Documentation

When adding new documentation:
1. Place files in the most appropriate directory based on content
2. Follow the naming conventions
3. Update this document if adding new categories
4. Ensure all documentation is in Markdown format for consistency