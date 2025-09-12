# Frontend Testing Guide for Twilio OTP Integration

This guide explains how to test the Twilio OTP (One-Time Password) integration using the frontend examples provided in this project.

## Prerequisites

1. Django development server running (already started on http://127.0.0.1:8000)
2. Twilio account with test credentials configured in your `.env` file
3. A test phone number (Twilio provides test numbers, or use your own)

## Testing with the HTML/JavaScript Demo

### 1. Open the HTML Demo

Open the `frontend_twilio_demo.html` file in your web browser directly from the file system, or serve it through a simple HTTP server.

### 2. Authentication Step

1. The demo is pre-filled with default credentials:
   - Username: `admin`
   - Password: `admin`
2. Click "Get Authentication Token"
3. If successful, you'll see a success message and the "Send OTP" button will become enabled

### 3. Send OTP

1. Enter a phone number (you can use Twilio's test number `+18777804236` for testing)
2. Select a purpose (e.g., "Registration")
3. Click "Send OTP"
4. If successful, you'll receive a message that the OTP was sent

### 4. Verify OTP

1. Check your phone for the SMS with the OTP code (or check Twilio's console if using test credentials)
2. Enter the 6-digit code in the OTP Code field
3. Click "Verify OTP"
4. If the code is correct, you'll see a success message

## Testing with the React Demo

### 1. Install Dependencies

Navigate to the React demo directory and install dependencies:

```bash
cd frontend_react_demo
npm install
```

### 2. Start the React Development Server

```bash
npm start
```

This will typically start the React app on http://localhost:3000

### 3. Use the React Interface

The React demo has the same functionality as the HTML demo:
1. Enter credentials and click "Get Authentication Token"
2. Enter phone number and select purpose, then click "Send OTP"
3. Enter the received OTP code and click "Verify OTP"

## Configuration

### Backend URL

Both demos are configured to connect to the backend at `http://127.0.0.1:8000`. If your backend is running on a different port or host, update the `BASE_URL` variable in both frontend examples.

### Twilio Test Credentials

Make sure your `.env` file in the backend project contains your Twilio test credentials:

```env
TWILIO_ACCOUNT_SID=your_test_account_sid
TWILIO_AUTH_TOKEN=your_test_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
TEST_PHONE_NUMBER=+18777804236
```

## Cost Considerations

Since you mentioned having only $14.2747 for testing:

1. Always use Twilio's test credentials during development
2. Use Twilio's test phone numbers (like +18777804236) which are free to use
3. The OTP codes sent to test numbers will not actually be delivered to real phones but can be viewed in your Twilio console

## Troubleshooting

### Common Issues

1. **CORS Errors**: If you encounter CORS issues, make sure the Django CORS headers are properly configured in your settings.

2. **Authentication Failures**: Ensure you're using valid credentials. You can create a test user with:
   ```bash
   python manage.py createsuperuser
   ```

3. **Twilio API Errors**: Check that your Twilio credentials are correctly set in the `.env` file and that you're using test credentials for development.

### Testing Without Network

If you want to test without actually sending SMS:

1. Use the manual test script:
   ```bash
   python manual_messaging_test.py
   ```

2. Or run the integration tests:
   ```bash
   python test_twilio_integration.py
   ```

These scripts will test the functionality without requiring a frontend.

## API Endpoints

The frontend demos interact with these backend endpoints:

1. **Authentication**: `POST /api/v1/auth/token/`
2. **Send OTP**: `POST /api/v1/messaging/send-otp/`
3. **Verify OTP**: `POST /api/v1/messaging/verify-otp/`

## Security Notes

1. In a production environment, you would implement rate limiting to prevent abuse
2. OTP codes are stored securely with timestamps and expiration
3. All communication should happen over HTTPS in production