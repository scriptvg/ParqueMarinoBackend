# Audit Module

## Overview

The Audit module provides comprehensive logging and tracking of all system activities for security, compliance, and operational purposes. It automatically records user actions, data changes, and system events.

## Key Features

- Automatic audit logging of all CRUD operations
- User action tracking
- Timestamped records with detailed change history
- Comprehensive audit reports
- Integration with Django's admin interface
- Performance-optimized logging
- Configurable audit policies

## Data Models

### AuditLog

Represents a single audit log entry recording a system event.

**Fields**:
- `timestamp`: Date and time of the event
- `user`: User who performed the action (nullable for system events)
- `action`: Type of action (CREATE, UPDATE, DELETE, READ, LOGIN, LOGOUT)
- `model_name`: Name of the affected model
- `object_id`: ID of the affected object
- `object_repr`: String representation of the object
- `changes`: JSON field containing detailed changes
- `ip_address`: IP address of the user
- `user_agent`: Browser/user agent information
- `session_key`: Session identifier
- `request_id`: Unique request identifier for tracking

**Methods**:
- `__str__()`: Returns audit log summary
- `get_action_display()`: Returns human-readable action description
- `get_changes()`: Returns formatted changes
- `revert()`: Reverts the logged action (if possible)

## Audit Logging Mechanism

### Automatic Logging

The system automatically logs all data changes through Django signals:

1. **Post-create Signal**: Logs object creation
2. **Post-update Signal**: Logs object updates with before/after values
3. **Post-delete Signal**: Logs object deletion
4. **Custom Signals**: Application-specific events

### Manual Logging

Developers can manually create audit logs for custom events:

```python
from apps.support.audit.models import AuditLog

AuditLog.objects.create(
    user=request.user,
    action='CUSTOM_ACTION',
    model_name='CustomModel',
    object_id=object.id,
    object_repr=str(object),
    changes={'custom_field': 'value'},
    ip_address=request.META.get('REMOTE_ADDR'),
    user_agent=request.META.get('HTTP_USER_AGENT')
)
```

## Logged Information

Each audit log entry captures comprehensive information:

1. **Timestamp**: Precise date and time of the action
2. **User**: Identity of the user performing the action
3. **Action**: Type of action performed
4. **Model**: Affected data model
5. **Object**: Specific object affected
6. **Changes**: Detailed before/after values for updates
7. **Context**: IP address, user agent, session information
8. **Request ID**: For tracking related actions

## Performance Considerations

The audit system is optimized for performance:

1. **Asynchronous Logging**: Non-blocking log creation
2. **Batch Processing**: Bulk log operations
3. **Indexing**: Database indexes for fast queries
4. **Archiving**: Automatic archiving of old logs
5. **Selective Logging**: Configurable logging levels

## API Endpoints

### Audit Logs

- `GET /api/v1/audit/logs/` - List audit logs
- `GET /api/v1/audit/logs/{id}/` - Get audit log details
- `POST /api/v1/audit/logs/export/` - Export audit logs
- `POST /api/v1/audit/logs/search/` - Search audit logs

### Audit Reports

- `GET /api/v1/audit/reports/summary/` - Get audit summary report
- `GET /api/v1/audit/reports/user-activity/` - Get user activity report
- `GET /api/v1/audit/reports/model-changes/` - Get model changes report
- `GET /api/v1/audit/reports/security-events/` - Get security events report

## Usage Examples

### Retrieving Audit Logs

```bash
curl -X GET "http://localhost:8000/api/v1/audit/logs/?model_name=Specie&limit=10" \
  -H "Authorization: Bearer <token>"
```

### Searching Audit Logs

```bash
curl -X POST http://localhost:8000/api/v1/audit/logs/search/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "user_id": 5,
    "action": "UPDATE",
    "date_from": "2023-01-01",
    "date_to": "2023-12-31"
  }'
```

### Exporting Audit Logs

```bash
curl -X POST http://localhost:8000/api/v1/audit/logs/export/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "format": "csv",
    "model_name": "Pago",
    "date_from": "2023-01-01",
    "date_to": "2023-12-31"
  }' \
  -o audit_export.csv
```

## Audit Reports

The system provides several built-in audit reports:

### Summary Report

Provides an overview of system activity:
- Total actions by type
- Actions by user
- Actions by model
- Recent activity timeline

### User Activity Report

Detailed user activity tracking:
- Login/logout events
- Actions performed
- Time spent in system
- Access patterns

### Model Changes Report

Tracking of specific model changes:
- Creation statistics
- Update frequency
- Deletion activity
- Data integrity metrics

### Security Events Report

Security-focused audit information:
- Failed login attempts
- Permission violations
- Suspicious activity
- Security incident tracking

## Configuration

The audit system is highly configurable:

### Logging Policies

1. **Model Selection**: Choose which models to audit
2. **Action Types**: Select which actions to log
3. **User Filtering**: Exclude specific users or roles
4. **Data Sensitivity**: Exclude sensitive fields from logging

### Retention Policies

1. **Log Retention**: How long to keep audit logs
2. **Archiving**: Automatic archiving to cold storage
3. **Purging**: Automatic deletion of old logs
4. **Compliance**: Retention periods for regulatory compliance

### Performance Settings

1. **Batch Size**: Number of logs to process at once
2. **Queue Size**: Maximum pending log entries
3. **Async Processing**: Enable/disable asynchronous logging
4. **Database Indexes**: Configure database optimization

## Integration Points

- **Security Module**: Logs authentication and authorization events
- **All Business Modules**: Automatic logging of data changes
- **Django Admin**: Integration with admin interface
- **Messaging Module**: Security alerts based on audit events

## Privacy and Compliance

The audit system addresses privacy and compliance requirements:

### Data Protection

1. **PII Handling**: Special handling of personal information
2. **Encryption**: Encryption of sensitive audit data
3. **Access Controls**: Restricted access to audit logs
4. **Anonymization**: Options for anonymizing user data

### Regulatory Compliance

1. **GDPR**: Compliance with data protection regulations
2. **SOX**: Sarbanes-Oxley compliance for financial data
3. **HIPAA**: Health information privacy compliance
4. **PCI DSS**: Payment card industry compliance

## Future Enhancements

- Real-time audit stream for monitoring
- Machine learning-based anomaly detection
- Advanced audit visualization and dashboards
- Integration with SIEM systems
- Blockchain-based immutable audit trails
- Automated compliance reporting
- Audit log correlation across systems