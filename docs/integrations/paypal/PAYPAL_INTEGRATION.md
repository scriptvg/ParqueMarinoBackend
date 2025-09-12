# PayPal Integration

## Overview

The PayPal integration enables secure payment processing through PayPal's REST API. It provides functionality for creating payments, executing approved payments, and handling refunds for the Parque Marino Backend.

## Key Features

- PayPal payment processing
- Payment creation and execution
- Refund processing
- Secure API integration
- Webhook handling for payment events
- Multi-currency support
- PayPal account integration

## Configuration

### Environment Variables

The following environment variables are required for PayPal integration:

```env
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_CLIENT_SECRET=your_client_secret
PAYPAL_SANDBOX=True  # Set to False for production
PAYPAL_RETURN_URL=http://localhost:8000/paypal/return/
PAYPAL_CANCEL_URL=http://localhost:8000/paypal/cancel/
```

### Installation

PayPal REST SDK is included in requirements.txt:

```bash
pip install paypalrestsdk
```

## Implementation

### PayPalClient Class

The core functionality is implemented in the `PayPalClient` class located in `apps/integrations/payments/paypal.py`.

#### Key Methods

1. **`create_payment(amount, currency, description)`**
   - Creates a payment in PayPal
   - Returns approval URL for user redirection
   - Accepts custom description for payment

2. **`execute_payment(payment_id, payer_id)`**
   - Executes an approved payment
   - Confirms payment completion
   - Updates payment status

3. **`refund_payment(sale_id, amount=None)`**
   - Processes a refund for a sale
   - Supports partial refunds
   - Returns refund details

### Payment Flow

1. **Payment Creation**: Backend creates payment in PayPal
2. **Approval URL**: Backend returns approval URL to frontend
3. **User Redirection**: User is redirected to PayPal for approval
4. **Payment Execution**: Backend executes approved payment
5. **Status Update**: Payment status is updated in the system

## API Endpoints

### Payment Processing

- `POST /api/v1/payments/pagos/{id}/ejecutar_pago/` - Execute general payment with PayPal
- `POST /api/v1/payments/pagos-inscripcion/{id}/ejecutar_pago/` - Execute enrollment payment with PayPal
- `POST /api/v1/payments/donaciones/{id}/ejecutar_pago/` - Execute donation with PayPal

### Refund Processing

- `POST /api/v1/payments/pagos/{id}/reembolsar/` - Refund a general payment
- `POST /api/v1/payments/pagos-inscripcion/{id}/reembolsar/` - Refund an enrollment payment
- `POST /api/v1/payments/donaciones/{id}/reembolsar/` - Refund a donation

## Usage Examples

### Creating a Payment

```bash
curl -X POST http://localhost:8000/api/v1/payments/pagos/1/ejecutar_pago/ \
  -H "Authorization: Bearer <token>"
```

Response:
```json
{
  "message": "Pago creado exitosamente",
  "approval_url": "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token=EC-XXXXXXXXXXXXXXXXX"
}
```

### Executing a Payment

After user approves the payment on PayPal and returns to the return URL:

```bash
curl -X POST http://localhost:8000/api/v1/payments/pagos/1/ejecutar_pago/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "payment_id": "PAYID_XXXXXXXXXXXXXXXX",
    "payer_id": "PAYER_XXXXXXXXXXXXXX"
  }'
```

Response:
```json
{
  "message": "Pago ejecutado exitosamente",
  "status": "completed"
}
```

### Frontend Implementation

```javascript
// Redirect user to PayPal approval URL
window.location.href = approval_url;

// After PayPal redirects back to return URL
// Extract payment_id and payer_id from URL parameters
const urlParams = new URLSearchParams(window.location.search);
const paymentId = urlParams.get('paymentId');
const payerId = urlParams.get('PayerID');

// Execute payment
fetch('/api/v1/payments/pagos/1/ejecutar_pago/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  },
  body: JSON.stringify({
    payment_id: paymentId,
    payer_id: payerId
  })
})
.then(response => response.json())
.then(data => {
  if (data.status === 'completed') {
    console.log('Payment successful!');
  }
});
```

## Security

### API Credentials

PayPal API credentials are secured through:

1. **Environment Variables**: Credentials stored in environment variables
2. **Sandbox vs Production**: Separate credentials for testing and production
3. **Access Control**: Restricted access to credential management
4. **Regular Rotation**: Periodic credential rotation

### Payment Validation

1. **Signature Verification**: Payment execution validates authenticity
2. **State Verification**: Ensures payments are in correct state for execution
3. **Amount Verification**: Confirms payment amounts match expectations
4. **Payer Verification**: Validates payer identity

### HTTPS Requirements

All PayPal API communications use HTTPS:

1. **Encrypted Communication**: All data transmitted securely
2. **Certificate Validation**: PayPal certificates are verified
3. **Secure Redirects**: User redirections are secure

## Error Handling

The integration handles various error conditions:

1. **Authentication Errors**: Invalid API credentials
2. **Payment Errors**: Declined payments, insufficient funds
3. **Network Errors**: Connection issues with PayPal API
4. **Validation Errors**: Invalid request parameters
5. **Execution Errors**: Payment already executed or expired

### Common Error Responses

```json
{
  "error": "La tarjeta fue declinada",
  "code": "PAYMENT_DENIED",
  "details": "Insufficient funds"
}
```

## Testing

### Sandbox Environment

PayPal provides a sandbox environment for testing:

1. **Sandbox Accounts**: Create test buyer and seller accounts
2. **Test Credentials**: Use sandbox client ID and secret
3. **Realistic Testing**: Simulate various payment scenarios
4. **Webhook Testing**: Test webhook notifications

### Test Accounts

Create sandbox accounts at https://developer.paypal.com/

1. **Personal Account**: For testing as a buyer
2. **Business Account**: For testing as a seller
3. **Funding Sources**: Add test credit cards and bank accounts

### Test Scenarios

1. **Successful Payment**: Normal payment flow
2. **Declined Payment**: Insufficient funds scenario
3. **Cancelled Payment**: User cancels payment
4. **Refund Processing**: Test refund functionality

## Refunds

The system supports both full and partial refunds:

### Full Refund

```bash
curl -X POST http://localhost:8000/api/v1/payments/pagos/1/reembolsar/ \
  -H "Authorization: Bearer <token>"
```

### Partial Refund

```bash
curl -X POST http://localhost:8000/api/v1/payments/pagos/1/reembolsar/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "amount": 50.00
  }'
```

## Multi-currency Support

The integration supports multiple currencies:

1. **Currency Conversion**: PayPal handles currency conversion
2. **Local Pricing**: Display prices in local currency
3. **Exchange Rates**: PayPal's competitive exchange rates
4. **Currency Restrictions**: Some payment methods have currency limitations

## Webhook Handling

PayPal webhooks can be configured to receive payment notifications:

1. **Payment Completed**: Notification when payment is completed
2. **Payment Denied**: Notification when payment is denied
3. **Refund Completed**: Notification when refund is processed
4. **Dispute Created**: Notification when payment is disputed

## Integration Points

- **Payments Module**: Core payment processing functionality
- **Audit Module**: Logs all PayPal-related activities
- **Messaging Module**: Sends payment confirmations
- **Documents Module**: Stores payment receipts

## Future Enhancements

- PayPal Checkout integration for improved user experience
- Vault API for storing payment methods
- Subscription billing for recurring payments
- Advanced fraud detection
- Invoice generation and management
- Automated payout processing
- Integration with PayPal's alternative payment methods