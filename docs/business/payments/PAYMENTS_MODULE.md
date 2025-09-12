# Payments Module

## Overview

The Payments module handles all financial transactions for the marine park, including donations, program fees, ticket sales, and merchandise purchases. It provides secure payment processing through multiple payment gateways.

## Key Features

- Multi-currency support (CRC and USD)
- Stripe and PayPal integration
- Electronic invoicing
- Payment status tracking
- Currency conversion
- Refund processing
- Payment reporting and analytics

## Data Models

### Pago (Payment)

Base model for all payments in the system.

**Fields**:
- `fecha_pago`: Payment date and time
- `monto`: Original payment amount
- `monto_crc`: Amount in Colones
- `monto_usd`: Amount in Dollars
- `moneda`: Original currency (CRC or USD)
- `metodo_pago`: Payment method (CARD, PAYPAL, CASH, TRANSFER, OTHER)
- `referencia_transaccion`: Unique transaction identifier
- `estado`: Payment status (PENDING, PROCESSING, SUCCESS, FAILED, REFUNDED)
- `comprobante`: Payment receipt document
- `notas`: Additional notes

**Methods**:
- `__str__()`: Returns payment reference and status
- `save()`: Automatically calculates CRC and USD amounts

### PagoInscripcion (Enrollment Payment)

Specialized payment model for educational program enrollments.

**Fields**:
- `inscripcion`: One-to-one relationship with enrollment

**Methods**:
- `save()`: Updates enrollment payment status based on payment status

### Donacion (Donation)

Model for handling donations to the marine park.

**Fields**:
- `monto`: Donation amount
- `moneda`: Currency (CRC or USD)
- `monto_crc`: Amount in Colones
- `monto_usd`: Amount in Dollars
- `nombre_donante`: Donor name (optional)
- `email_donante`: Donor email (optional)
- `metodo_pago`: Payment method
- `referencia_transaccion`: Unique transaction identifier
- `estado`: Payment status
- `fecha_creacion`: Creation date

**Methods**:
- `__str__()`: Returns donation amount and status
- `save()`: Automatically calculates CRC and USD amounts

## Payment Gateways

### Stripe Integration

The system integrates with Stripe for credit/debit card payments:

1. **Payment Intent Creation**: Creates a payment intent in Stripe
2. **Client Secret**: Returns client secret for frontend processing
3. **Webhook Handling**: Receives payment confirmation events
4. **Refund Processing**: Handles payment refunds

### PayPal Integration

The system integrates with PayPal for PayPal payments:

1. **Payment Creation**: Creates a payment in PayPal
2. **Approval URL**: Returns approval URL for user redirection
3. **Payment Execution**: Executes approved payments
4. **Refund Processing**: Handles payment refunds

## API Endpoints

### General Payments

- `POST /api/v1/payments/pagos/` - Create a new payment
- `GET /api/v1/payments/pagos/` - List all payments
- `GET /api/v1/payments/pagos/{id}/` - Get payment details
- `PUT /api/v1/payments/pagos/{id}/` - Update payment
- `DELETE /api/v1/payments/pagos/{id}/` - Delete payment

### Payment Processing

- `POST /api/v1/payments/pagos/{id}/procesar_pago/` - Process payment with Stripe
- `POST /api/v1/payments/pagos/{id}/ejecutar_pago/` - Execute PayPal payment
- `POST /api/v1/payments/pagos/{id}/reembolsar/` - Refund a payment

### Enrollment Payments

- `POST /api/v1/payments/pagos-inscripcion/` - Create a new enrollment payment
- `GET /api/v1/payments/pagos-inscripcion/` - List all enrollment payments
- `GET /api/v1/payments/pagos-inscripcion/{id}/` - Get enrollment payment details

### Donations

- `POST /api/v1/payments/donaciones/` - Create a new donation
- `GET /api/v1/payments/donaciones/` - List all donations
- `GET /api/v1/payments/donaciones/{id}/` - Get donation details
- `PUT /api/v1/payments/donaciones/{id}/` - Update donation
- `DELETE /api/v1/payments/donaciones/{id}/` - Delete donation

### Donation Processing

- `POST /api/v1/payments/donaciones/{id}/procesar_pago/` - Process donation with Stripe
- `POST /api/v1/payments/donaciones/{id}/ejecutar_pago/` - Execute PayPal donation
- `POST /api/v1/payments/donaciones/{id}/reembolsar/` - Refund a donation

### Stripe Webhook

- `POST /api/v1/payments/stripe/webhook/` - Receive Stripe events

## Usage Examples

### Creating a New Payment

```bash
curl -X POST http://localhost:8000/api/v1/payments/pagos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "monto": 100.00,
    "moneda": "USD",
    "metodo_pago": "CARD",
    "referencia_transaccion": "PAY123456"
  }'
```

### Processing a Payment with Stripe

```bash
curl -X POST http://localhost:8000/api/v1/payments/pagos/1/procesar_pago/ \
  -H "Authorization: Bearer <token>"
```

### Creating a New Donation

```bash
curl -X POST http://localhost:8000/api/v1/payments/donaciones/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "monto": 50.00,
    "moneda": "USD",
    "nombre_donante": "John Smith",
    "email_donante": "john@example.com",
    "metodo_pago": "PAYPAL"
  }'
```

## Currency Conversion

The system automatically converts between CRC and USD using current exchange rates:

1. All payments are stored with original currency and converted amounts
2. Conversion rates are updated regularly
3. Both CRC and USD amounts are displayed in reports
4. Exchange rate history is maintained for auditing

## Security

Payment processing follows strict security protocols:

1. **PCI Compliance**: Stripe and PayPal handle card data
2. **Encryption**: All sensitive data is encrypted
3. **Tokenization**: Payment methods are tokenized
4. **Fraud Detection**: Built-in fraud prevention
5. **Audit Trail**: Complete payment history tracking

## Permissions

- **Administrators**: Full access to all payment data
- **Financial Staff**: Read access to payments, limited write access
- **Users**: Access to their own payments only

## Integration Points

- **Education Module**: Handles program enrollment fees
- **Tickets Module**: Processes ticket sales
- **Documents Module**: Stores payment receipts
- **Audit Module**: Tracks all payment activities
- **Messaging Module**: Sends payment confirmations

## Future Enhancements

- Additional payment gateways (Apple Pay, Google Pay)
- Subscription billing for memberships
- Automated invoicing
- Advanced reporting and analytics
- Integration with accounting systems
- Multi-language payment forms