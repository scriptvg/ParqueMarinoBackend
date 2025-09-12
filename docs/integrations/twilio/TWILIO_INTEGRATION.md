# Twilio Integration

## Overview

The Twilio integration enables SMS messaging and OTP (One-Time Password) validation functionality for the Parque Marino Backend. It provides secure phone number verification, two-factor authentication, and general SMS messaging capabilities.

## Key Features

- SMS messaging via Twilio integration
- OTP generation and validation
- Phone number verification
- Security-focused implementation
- Rate limiting to prevent abuse
- Integration with user authentication
- Configurable expiration times

## Configuration

### Environment Variables

The following environment variables are required for Twilio integration:

```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
TEST_PHONE_NUMBER=your_test_phone_number
```

### Installation

Twilio Python library is included in requirements.txt:

```bash
pip install twilio==8.8.0
```

## Implementation

### TwilioService Class

The core functionality is implemented in the `TwilioService` class located in `apps/support/messaging/services/twilio_service.py`.

#### Key Methods

1. **`is_enabled()`**
   - Checks if Twilio is properly configured
   - Returns boolean indicating service availability

2. **`generate_otp()`**
   - Generates a 6-digit random OTP code
   - Returns string OTP code

3. **`send_otp_sms(phone_number, user, purpose)`**
   - Sends OTP via SMS using Twilio
   - Creates OTP record in database
   - Returns success status and message

4. **`verify_otp(phone_number, otp_code, user, purpose)`**
   - Verifies OTP code against stored record
   - Marks OTP as verified if valid
   - Returns verification status and message

5. **`send_test_message(to_number)`**
   - Sends a test message to verify configuration
   - Returns success status and message

### OTP Flow

1. **OTP Request**: User requests OTP for verification
2. **Code Generation**: System generates 6-digit OTP
3. **Database Storage**: OTP record stored with expiration
4. **SMS Sending**: OTP sent via Twilio SMS
5. **User Verification**: User enters received OTP
6. **Code Validation**: System validates OTP against stored record
7. **Verification Update**: OTP marked as verified if valid

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

Response:
```json
{
  "message": "Test message sent successfully with SID: SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

## Frontend Integration

### JavaScript Example

```javascript
// Request OTP
async function requestOTP(phoneNumber) {
  const response = await fetch('/api/v1/messaging/send-otp/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    },
    body: JSON.stringify({
      phone_number: phoneNumber,
      purpose: 'registration'
    })
  });
  
  const data = await response.json();
  if (data.message) {
    console.log('OTP sent successfully');
  }
}

// Verify OTP
async function verifyOTP(phoneNumber, otpCode) {
  const response = await fetch('/api/v1/messaging/verify-otp/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    },
    body: JSON.stringify({
      phone_number: phoneNumber,
      otp_code: otpCode,
      purpose: 'registration'
    })
  });
  
  const data = await response.json();
  return data.verified;
}
```

### React Example

```jsx
import React, { useState } from 'react';

function PhoneVerification() {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [otpCode, setOtpCode] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [verified, setVerified] = useState(false);

  const requestOTP = async () => {
    const response = await fetch('/api/v1/messaging/send-otp/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
      },
      body: JSON.stringify({
        phone_number: phoneNumber,
        purpose: 'registration'
      })
    });
    
    if (response.ok) {
      setOtpSent(true);
    }
  };

  const verifyOTP = async () => {
    const response = await fetch('/api/v1/messaging/verify-otp/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
      },
      body: JSON.stringify({
        phone_number: phoneNumber,
        otp_code: otpCode,
        purpose: 'registration'
      })
    });
    
    const data = await response.json();
    setVerified(data.verified);
  };

  return (
    <div>
      {!otpSent ? (
        <div>
          <input
            type="tel"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            placeholder="Enter phone number"
          />
          <button onClick={requestOTP}>Send OTP</button>
        </div>
      ) : (
        <div>
          <input
            type="text"
            value={otpCode}
            onChange={(e) => setOtpCode(e.target.value)}
            placeholder="Enter OTP"
          />
          <button onClick={verifyOTP}>Verify OTP</button>
          {verified && <p>Phone number verified successfully!</p>}
        </div>
      )}
    </div>
  );
}
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

### Test Credentials

Twilio provides test credentials for development:

```env
TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
TWILIO_AUTH_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
TWILIO_PHONE_NUMBER=+15005550006
TEST_PHONE_NUMBER=+15005550006
```

Test phone numbers:
- `+15005550006`: Valid number for testing
- `+15005550001`: Number that fails
- `+15005550002`: Number that sends invalid response

## Security

### OTP Security

1. **Random Generation**: Cryptographically secure random number generation
2. **Short Lifespan**: 10-minute expiration time
3. **Single Use**: OTPs invalidated after successful verification
4. **Purpose Binding**: OTPs tied to specific purposes
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

## Error Handling

The integration handles various error conditions:

1. **Configuration Errors**: Missing or invalid Twilio credentials
2. **Network Issues**: Connection problems with Twilio API
3. **Invalid OTPs**: Expired or incorrect codes
4. **Rate Limiting**: Too many requests from same user/phone
5. **Twilio API Errors**: Service-specific error responses

### Common Error Responses

```json
{
  "error": "Failed to send OTP: Unable to create record: Authenticate",
  "details": "Invalid Account SID or Auth Token"
}
```

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

### Manual Testing Script

A manual test script is available for quick verification:

```bash
python manual_messaging_test.py
```

## Integration Points

- **Security Module**: Phone number verification during registration/login
- **User Management**: Two-factor authentication
- **Password Reset**: Secure password reset workflow
- **Audit Module**: Logs OTP generation and verification events

## Future Enhancements

- WhatsApp integration for additional messaging channels
- Rich messaging with media attachments
- International phone number formatting
- Advanced analytics and reporting
- Template-based messaging system
- Scheduled message delivery
- Message status tracking and callbacks
- Integration with other messaging providers