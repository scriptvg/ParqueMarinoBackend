# Testing Twilio Integration

This document explains how to test the Twilio integration for OTP validation in the ParqueMarinoBackend project.

## Overview

The Twilio integration includes comprehensive tests to ensure the functionality works correctly. The tests cover:

1. OTP record creation and expiration logic
2. OTP generation
3. Twilio service functionality
4. API endpoint testing

## Test Structure

The tests are organized in the following files:

- [apps/support/messaging/tests.py](file:///c:/Users/velez/OneDrive/Desktop/ParqueMarinoBackend/apps/support/messaging/tests.py) - Unit tests for models and services
- [manual_messaging_test.py](file:///c:/Users/velez/OneDrive/Desktop/ParqueMarinoBackend/manual_messaging_test.py) - Manual test script for quick verification
- [test_twilio_integration.py](file:///c:/Users/velez/OneDrive/Desktop/ParqueMarinoBackend/test_twilio_integration.py) - Integration tests with actual Twilio API

## Running Tests

### Method 1: Manual Test Script (Recommended for Quick Testing)

The easiest way to run tests is using the manual test script:

```bash
cd c:\Users\velez\OneDrive\Desktop\ParqueMarinoBackend
.venv\Scripts\activate.bat
python manual_messaging_test.py
```

This script runs all unit tests without requiring a full Django test environment.

### Method 2: Django Test Runner

To run the full Django test suite:

```bash
cd c:\Users\velez\OneDrive\Desktop\ParqueMarinoBackend
.venv\Scripts\activate.bat
python manage.py test apps.support.messaging
```

### Method 3: Pytest (if configured)

If pytest is properly configured:

```bash
cd c:\Users\velez\OneDrive\Desktop\ParqueMarinoBackend
.venv\Scripts\activate.bat
python -m pytest apps/support/messaging/tests.py -v
```

## Test Cases

### OTPRecord Model Tests

1. **test_otp_record_creation**: Verifies that OTP records can be created correctly with all required fields
2. **test_otp_expiration**: Tests the expiration logic for OTP records

### TwilioService Tests

1. **test_generate_otp**: Verifies that 6-digit OTP codes are generated correctly
2. **test_is_enabled_without_credentials**: Checks if the service correctly identifies when Twilio is not configured
3. **test_send_otp_sms_success**: Tests successful OTP SMS sending using mocked Twilio client
4. **test_verify_otp_success**: Tests successful OTP verification
5. **test_verify_otp_expired**: Tests OTP verification with expired codes

### API Endpoint Tests

1. **test_send_otp_success**: Tests successful OTP sending via API endpoint
2. **test_send_otp_service_disabled**: Tests API response when Twilio service is disabled
3. **test_verify_otp_success**: Tests successful OTP verification via API endpoint
4. **test_send_otp_unauthorized**: Tests API response for unauthorized access

## Test Data

The tests use the following test data:

- Phone number: `+18777804236` (Twilio test number)
- Purpose: `registration` (can also be `login`, `password_reset`, `phone_verification`)
- OTP codes: 6-digit randomly generated numbers

## Mocking External Services

To avoid making actual API calls during testing, the tests use mocking:

```python
from unittest.mock import patch, MagicMock

@patch('apps.support.messaging.services.twilio_service.Client')
def test_send_otp_sms_success(mock_client):
    # Test implementation with mocked Twilio client
```

## Continuous Integration

For CI/CD pipelines, add the following to your test workflow:

```yaml
- name: Run Messaging Tests
  run: |
    python manual_messaging_test.py
```

## Troubleshooting

### Common Issues

1. **Database Integrity Errors**: Ensure unique usernames are used for each test
2. **Environment Variables**: Make sure Twilio credentials are properly configured
3. **Django Setup**: Ensure Django is properly configured before running tests

### Debugging Tips

1. Add print statements to see what's happening during test execution
2. Use `traceback.print_exc()` to get detailed error information
3. Check Django logs for database-related issues

## Test Coverage

The current test suite covers:

- [x] OTP record creation
- [x] OTP expiration logic
- [x] OTP generation
- [x] Service enable/disable logic
- [x] OTP verification
- [x] Expired OTP handling
- [x] API endpoint testing
- [x] Authentication checks
- [ ] Rate limiting (to be implemented)
- [ ] Error handling for network issues (to be implemented)

## Adding New Tests

To add new tests:

1. Add test methods to the appropriate test class in [apps/support/messaging/tests.py](file:///c:/Users/velez/OneDrive/Desktop/ParqueMarinoBackend/apps/support/messaging/tests.py)
2. Follow the existing naming convention (`test_descriptive_name`)
3. Use mocking for external services
4. Ensure tests are independent and don't rely on shared state
5. Use unique data for each test to avoid conflicts

## Performance Considerations

- Tests use in-memory SQLite database for speed
- Mocking external services prevents network delays
- Tests clean up after themselves to avoid database bloat

## Security Testing

The tests verify:

- OTPs can only be used once
- Expired OTPs are rejected
- Unauthorized access to endpoints is blocked
- Proper validation of input data

## Integration Testing

For integration testing with actual Twilio services:

1. Set up Twilio test credentials in [.env](file:///c:/Users/velez/OneDrive/Desktop/ParqueMarinoBackend/.env) file
2. Run [test_twilio_integration.py](file:///c:/Users/velez/OneDrive/Desktop/ParqueMarinoBackend/test_twilio_integration.py):

```bash
python test_twilio_integration.py
```

This will:
- Send a test SMS to your Twilio test number
- Generate and send an OTP
- Verify the OTP successfully

## Cost Considerations for Testing

When testing with actual Twilio services:

1. Use Twilio's test credentials to avoid charges
2. Use Twilio's test phone numbers
3. Monitor your Twilio account balance
4. Set up alerts for usage limits

The current test suite is designed to be cost-effective while ensuring functionality works correctly.