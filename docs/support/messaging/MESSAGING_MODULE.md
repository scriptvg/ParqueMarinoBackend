# Messaging Module

## Overview

The Messaging module provides SMS communication and OTP (One-Time Password) validation functionality using Twilio integration. It enables secure phone number verification, two-factor authentication, and general SMS messaging capabilities.

## Key Features

- SMS messaging via Twilio integration
- OTP generation and validation
- Phone number verification
- Security-focused implementation
- Rate limiting to prevent abuse
- Integration with user authentication
- Configurable expiration times

## Data Models

### OTPRecord

Represents a one-time password record for phone verification.

**Fields**:
- `user`: Foreign key to User
- `phone_number`: Phone number for verification
- `otp_code`: 6-digit OTP code
- `created_at`: Creation timestamp
- `expires_at`: Expiration timestamp
- `is_verified`: Whether the OTP has been verified
- `purpose`: Purpose of the OTP (registration, login, password_reset, phone_verification)

**Methods**:
- `__str__()`: Returns OTP summary
- `save()`: Automatically sets expiration time
- `is_expired()`: Checks if OTP has expired

## Twilio Integration

### Configuration

The system integrates with Twilio for SMS messaging:

1. **Account Setup**: Twilio account with SMS capabilities
2. **Credentials**: Account SID, Auth Token, and Phone Number
3. **Environment Variables**: Secure credential storage
4. **Test Credentials**: Sandbox environment for development

### Required Environment Variables

```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

## OTP Functionality

### OTP Generation

1. **Random Generation**: 6-digit numeric codes
2. **Uniqueness**: Codes are unique per phone number and purpose
3. **Timestamping**: Automatic creation and expiration timestamps
4. **Purpose Tracking**: Different OTPs for different purposes

### OTP Validation

1. **Expiration Check**: Validates OTP hasn't expired (10 minutes by default)
2. **Code Matching**: Verifies entered code matches stored code
3. **Single Use**: OTPs can only be verified once
4. **Purpose Validation**: Ensures OTP is used for correct purpose

### Security Measures

1. **Rate Limiting**: Prevents OTP spamming
2. **Expiration**: OTPs expire after 10 minutes
3. **Single Use**: OTPs are invalidated after successful verification
4. **Purpose Binding**: OTPs are tied to specific purposes
5. **User Association**: OTPs are linked to specific users

## API Endpoints

### OTP Management

- `POST /api/v1/messaging/send-otp/` - Send OTP to phone number
- `POST /api/v1/messaging/verify-otp/` - Verify OTP code
- `GET /api/v1/messaging/test-twilio/` - Test Twilio configuration

## Usage Examples

### Sending an OTP

```bash
curl -X POST http://localhost:8000/api/v1/messaging/send-otp/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "phone_number": "+1234567890",
    "purpose": "registration"
  }'
```

Response:
```json
{
  "message": "OTP sent successfully",
  "otp_id": 123
}
```

### Verifying an OTP

```bash
curl -X POST http://localhost:8000/api/v1/messaging/verify-otp/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "phone_number": "+1234567890",
    "otp_code": "123456",
    "purpose": "registration"
  }'
```

Response:
```json
{
  "message": "OTP verified successfully",
  "verified": true
}
```

### Testing Twilio Configuration

```bash
curl -X GET http://localhost:8000/api/v1/messaging/test-twilio/ \
  -H "Authorization: Bearer <token>"
```

## Cost Considerations

With Twilio's pay-per-use pricing model, cost management is important:

### Cost-Saving Measures

1. **Test Credentials**: Use Twilio's test credentials during development
2. **Rate Limiting**: Implement server-side rate limiting
3. **Short Expiration**: OTPs expire after 10 minutes
4. **Purpose Validation**: Prevent unnecessary OTP requests
5. **User Education**: Clear instructions to reduce retries

### Pricing Information

- **SMS Messages**: Typically $0.0075 per message in the US
- **Test Messages**: Free with test credentials
- **Phone Numbers**: Monthly rental fees apply

## Implementation Details

### TwilioService Class

The core functionality is implemented in the TwilioService class:

1. **Initialization**: Loads Twilio credentials from environment variables
2. **Configuration Check**: Verifies Twilio is properly configured
3. **OTP Generation**: Creates random 6-digit codes
4. **SMS Sending**: Sends messages via Twilio API
5. **OTP Verification**: Validates OTP codes
6. **Test Messaging**: Sends test messages for configuration verification

### Error Handling

The system handles various error conditions:

1. **Configuration Errors**: Missing or invalid Twilio credentials
2. **Network Issues**: Connection problems with Twilio API
3. **Invalid OTPs**: Expired or incorrect codes
4. **Rate Limiting**: Too many requests from same user/phone
5. **Twilio API Errors**: Service-specific error responses

## Security Considerations

### OTP Security

1. **Random Generation**: Cryptographically secure random number generation
2. **Short Lifespan**: 10-minute expiration time
3. **Single Use**: OTPs invalidated after successful verification
4. **Purpose Binding**: OTPs tied to specific use cases
5. **User Association**: OTPs linked to authenticated users

### Communication Security

1. **HTTPS**: All API communication over secure channels
2. **Credential Protection**: Environment variables for secrets
3. **Input Validation**: Sanitization of phone numbers
4. **Logging**: Secure logging without exposing codes

### Rate Limiting

1. **Request Throttling**: Limit OTP requests per user
2. **Phone Number Limits**: Limit requests per phone number
3. **Time Windows**: Sliding window rate limiting
4. **Abuse Detection**: Identify and block suspicious patterns

## Integration Points

- **Security Module**: Phone number verification during registration/login
- **User Management**: Two-factor authentication
- **Password Reset**: Secure password reset workflow
- **Audit Module**: Logs OTP generation and verification events

## Testing

### Unit Tests

The module includes comprehensive unit tests:

1. **OTP Record Creation**: Verify model functionality
2. **OTP Expiration**: Test expiration logic
3. **OTP Generation**: Test code generation
4. **Service Enable/Disable**: Test configuration checks
5. **SMS Sending**: Test Twilio integration with mocking
6. **OTP Verification**: Test verification logic
7. **Expired OTPs**: Test expiration handling
8. **API Endpoints**: Test REST API functionality

### Integration Tests

For testing with actual Twilio services:

1. **Test Credentials**: Use Twilio's test credentials
2. **Test Phone Numbers**: Use Twilio's test phone numbers
3. **Live Testing**: Send actual test messages
4. **Verification Testing**: Test actual OTP generation and verification

## Future Enhancements

- WhatsApp integration for additional messaging channels
- Rich messaging with media attachments
- International phone number formatting
- Advanced analytics and reporting
- Template-based messaging system
- Scheduled message delivery
- Message status tracking and callbacks
- Integration with other messaging providers