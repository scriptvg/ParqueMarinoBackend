# Stripe Integration

## Overview

The Stripe integration enables secure payment processing for the Parque Marino Backend. It provides functionality for processing credit/debit card payments, handling webhooks, and managing refunds through Stripe's API.

## Key Features

- Credit/debit card payment processing
- Payment intent creation and management
- Webhook handling for payment events
- Refund processing
- Secure tokenized payment methods
- Multi-currency support
- PCI compliance through Stripe

## Configuration

### Environment Variables

The following environment variables are required for Stripe integration:

```env
STRIPE_PUBLIC_KEY=pk_test_example_public_key_here
STRIPE_SECRET_KEY=sk_test_example_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_example_webhook_secret_here
```

### Installation

Stripe Python library is included in requirements.txt:

```bash
pip install stripe==10.10.0
```

## Implementation

### StripeClient Class

The core functionality is implemented in the `StripeClient` class located in `apps/integrations/payments/stripe_client.py`.

#### Key Methods

1. **`create_payment_intent(amount, currency, metadata)`**
   - Creates a payment intent in Stripe
   - Returns client secret for frontend processing
   - Accepts custom metadata for tracking

2. **`confirm_payment_intent(payment_intent_id)`**
   - Confirms a payment intent
   - Used for server-side confirmation

3. **`refund_payment(charge_id, amount=None)`**
   - Processes a refund for a charge
   - Supports partial refunds

4. **`handle_webhook(payload, sig_header)`**
   - Processes webhook events from Stripe
   - Verifies webhook signature for security
   - Updates payment status based on events

### Payment Flow

1. **Frontend Request**: Client requests payment processing
2. **Payment Intent Creation**: Backend creates payment intent in Stripe
3. **Client Secret Return**: Backend returns client secret to frontend
4. **Frontend Processing**: Frontend collects payment details and processes payment
5. **Webhook Notification**: Stripe sends webhook with payment result
6. **Backend Update**: Backend updates payment status based on webhook

## API Endpoints

### Payment Processing

- `POST /api/v1/payments/pagos/{id}/procesar_pago/` - Process general payment with Stripe
- `POST /api/v1/payments/pagos-inscripcion/{id}/procesar_pago/` - Process enrollment payment with Stripe
- `POST /api/v1/payments/donaciones/{id}/procesar_pago/` - Process donation with Stripe

### Refund Processing

- `POST /api/v1/payments/pagos/{id}/reembolsar/` - Refund a general payment
- `POST /api/v1/payments/pagos-inscripcion/{id}/reembolsar/` - Refund an enrollment payment
- `POST /api/v1/payments/donaciones/{id}/reembolsar/` - Refund a donation

### Webhook

- `POST /api/v1/payments/stripe/webhook/` - Receive Stripe events

## Usage Examples

### Processing a Payment

```bash
curl -X POST http://localhost:8000/api/v1/payments/pagos/1/procesar_pago/ \
  -H "Authorization: Bearer <token>"
```

Response:
```json
{
  "message": "Pago procesado exitosamente",
  "payment_intent_id": "pi_XXXXXXXXXXXXXXXX",
  "client_secret": "pi_XXXXXXXXXXXXXXXX_secret_YYYYYYYYYYYYYYYY"
}
```

### Frontend Implementation

```javascript
// Using Stripe.js
const stripe = Stripe('pk_test_XXXXXXXXXXXXXXXXXXXXXXXX');

stripe.confirmCardPayment(client_secret, {
  payment_method: {
    card: cardElement,
    billing_details: {
      name: 'John Doe'
    }
  }
}).then(function(result) {
  if (result.error) {
    // Handle error
    console.log(result.error.message);
  } else {
    // Payment succeeded
    if (result.paymentIntent.status === 'succeeded') {
      console.log('Payment successful!');
    }
  }
});
```

### Handling Webhooks

The webhook endpoint automatically handles various Stripe events:

1. **`payment_intent.succeeded`**: Payment completed successfully
2. **`payment_intent.payment_failed`**: Payment failed
3. **`charge.refunded`**: Payment refunded
4. **`charge.dispute.created`**: Payment disputed

## Security

### PCI Compliance

Stripe handles all PCI compliance requirements:

1. **Tokenization**: Card data is tokenized by Stripe
2. **Encryption**: All data transmission is encrypted
3. **No Card Storage**: Card data is never stored in the backend
4. **Compliance Certifications**: Stripe maintains PCI DSS compliance

### Webhook Security

Webhook signatures are verified to prevent unauthorized requests:

1. **Signature Verification**: Each webhook is verified with secret
2. **Timestamp Validation**: Prevents replay attacks
3. **Payload Integrity**: Ensures data hasn't been tampered with

### Environment Security

1. **Secret Management**: API keys stored in environment variables
2. **Test vs Production**: Separate keys for development and production
3. **Key Rotation**: Regular key rotation procedures

## Error Handling

The integration handles various error conditions:

1. **Authentication Errors**: Invalid API keys
2. **Card Errors**: Declined cards, insufficient funds
3. **Network Errors**: Connection issues with Stripe API
4. **Validation Errors**: Invalid request parameters
5. **Webhook Errors**: Signature verification failures

### Common Error Responses

```json
{
  "error": "La tarjeta fue declinada",
  "code": "card_declined",
  "decline_code": "insufficient_funds"
}
```

## Testing

### Test Cards

Stripe provides test card numbers for development:

- **Successful Payment**: `4242 4242 4242 4242`
- **Insufficient Funds**: `4000 0000 0000 0002`
- **Declined**: `4000 0000 0000 0002`
- **Expired Card**: `4000 0000 0000 0069`

### Test API Keys

Use Stripe's test mode API keys during development:

```env
STRIPE_PUBLIC_KEY=pk_test_pk_test_example_public_key_here
STRIPE_SECRET_KEY=sk_test_pk_secret_example_public_key_here
```

### Webhook Testing

Use Stripe CLI for local webhook testing:

```bash
stripe listen --forward-to localhost:8000/api/v1/payments/stripe/webhook/
```

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

1. **Automatic Conversion**: Stripe handles currency conversion
2. **Local Pricing**: Display prices in local currency
3. **Exchange Rates**: Stripe's competitive exchange rates
4. **Currency Restrictions**: Some payment methods have currency limitations

## Integration Points

- **Payments Module**: Core payment processing functionality
- **Audit Module**: Logs all Stripe-related activities
- **Messaging Module**: Sends payment confirmations
- **Documents Module**: Stores payment receipts

## Future Enhancements

- Subscription billing for memberships
- Payment links for easy sharing
- Advanced fraud detection
- Apple Pay and Google Pay integration
- Payment method saving for returning customers
- Invoice generation and management
- Automated payout processing