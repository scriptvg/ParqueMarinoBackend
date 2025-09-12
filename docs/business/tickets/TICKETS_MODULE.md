# Tickets Module

## Overview

The Tickets module manages all aspects of ticket sales and visitor scheduling for the marine park. It provides functionality for creating and selling tickets, scheduling visits, and managing capacity constraints.

## Key Features

- Ticket creation and management
- Visit scheduling and capacity management
- Multi-ticket type support
- Integration with payment processing
- Visitor tracking and analytics
- Seasonal pricing and promotions

## Data Models

### Ticket

Represents an individual ticket for park entry.

**Fields**:
- `tipo`: Ticket type (GENERAL, NIÑO, ADULTO_MAYOR, ESTUDIANTE, GRUPO)
- `precio`: Ticket price
- `moneda`: Currency (CRC or USD)
- `codigo_qr`: QR code for ticket validation
- `fecha_compra`: Purchase date
- `fecha_validez`: Validity date
- `estado`: Ticket status (ACTIVO, USADO, EXPIRADO, CANCELADO)
- `metodo_pago`: Payment method
- `referencia_pago`: Payment reference
- `visitante_nombre`: Visitor name
- `visitante_email`: Visitor email
- `visitante_telefono`: Visitor phone

**Methods**:
- `__str__()`: Returns ticket code and type
- `generar_codigo_qr()`: Generates QR code for the ticket
- `is_valid()`: Checks if ticket is valid for use
- `cancelar()`: Cancels the ticket

### Visita (Visit)

Represents a scheduled visit to the park.

**Fields**:
- `fecha_visita`: Visit date
- `hora_visita`: Visit time slot
- `cantidad_visitantes`: Number of visitors
- `contacto_nombre`: Contact name
- `contacto_email`: Contact email
- `contacto_telefono`: Contact phone
- `estado`: Visit status (CONFIRMADA, CANCELADA, COMPLETADA)
- `notas`: Additional notes

**Methods**:
- `__str__()`: Returns visit date and contact name
- `capacidad_disponible()`: Returns available capacity for the time slot
- `is_full()`: Checks if the time slot is full

## Ticket Types

The system supports multiple ticket types with different pricing:

1. **General**: Standard adult ticket
2. **Child**: Reduced price for children
3. **Senior**: Reduced price for seniors
4. **Student**: Reduced price for students with ID
5. **Group**: Discounted rate for groups of 10 or more

## API Endpoints

### Tickets

- `POST /api/v1/tickets/tickets/` - Create a new ticket
- `GET /api/v1/tickets/tickets/` - List all tickets
- `GET /api/v1/tickets/tickets/{id}/` - Get ticket details
- `PUT /api/v1/tickets/tickets/{id}/` - Update ticket
- `DELETE /api/v1/tickets/tickets/{id}/` - Delete ticket
- `POST /api/v1/tickets/tickets/{id}/cancelar/` - Cancel a ticket

### Visits

- `POST /api/v1/tickets/visitas/` - Create a new visit
- `GET /api/v1/tickets/visitas/` - List all visits
- `GET /api/v1/tickets/visitas/{id}/` - Get visit details
- `PUT /api/v1/tickets/visitas/{id}/` - Update visit
- `DELETE /api/v1/tickets/visitas/{id}/` - Delete visit
- `POST /api/v1/tickets/visitas/{id}/cancelar/` - Cancel a visit

### Availability

- `GET /api/v1/tickets/disponibilidad/` - Check availability for a date
- `GET /api/v1/tickets/precios/` - Get current pricing

## Usage Examples

### Creating a New Ticket

```bash
curl -X POST http://localhost:8000/api/v1/tickets/tickets/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "tipo": "GENERAL",
    "moneda": "USD",
    "visitante_nombre": "John Smith",
    "visitante_email": "john@example.com",
    "visitante_telefono": "+1234567890"
  }'
```

### Scheduling a Visit

```bash
curl -X POST http://localhost:8000/api/v1/tickets/visitas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "fecha_visita": "2023-12-25",
    "hora_visita": "10:00:00",
    "cantidad_visitantes": 4,
    "contacto_nombre": "John Smith",
    "contacto_email": "john@example.com",
    "contacto_telefono": "+1234567890"
  }'
```

### Checking Availability

```bash
curl -X GET "http://localhost:8000/api/v1/tickets/disponibilidad/?fecha=2023-12-25" \
  -H "Authorization: Bearer <token>"
```

## Capacity Management

The Tickets module manages park capacity to ensure optimal visitor experience:

1. **Daily Capacity**: Maximum visitors per day
2. **Time Slot Capacity**: Maximum visitors per time slot
3. **Real-time Tracking**: Current occupancy monitoring
4. **Waitlist Management**: Automatic waitlist when capacity is reached
5. **Dynamic Pricing**: Price adjustments based on demand

## QR Code Validation

Tickets include QR codes for validation at park entry:

1. **Generation**: QR codes are generated upon ticket purchase
2. **Validation**: Scanning validates ticket authenticity
3. **Tracking**: Entry times are recorded
4. **Security**: One-time use codes prevent fraud

## Payment Integration

The Tickets module integrates with the Payments module:

1. **Automatic Payment Creation**: Payments are created when tickets are purchased
2. **Multiple Payment Methods**: Support for cards, PayPal, and cash
3. **Refund Processing**: Canceled tickets can be refunded
4. **Payment Status Tracking**: Real-time payment status updates

## Permissions

- **Administrators**: Full access to all ticket data
- **Ticket Sellers**: Create and manage tickets
- **Gate Staff**: Validate tickets at entry
- **Users**: Purchase tickets and manage their own tickets

## Integration Points

- **Payments Module**: Handles ticket payments
- **Infrastructure Module**: Capacity management based on park sections
- **Audit Module**: Tracks all ticket activities
- **Messaging Module**: Sends ticket confirmations and reminders

## Future Enhancements

- Mobile ticketing app
- Season pass management
- Special event ticketing
- Loyalty program integration
- Advanced analytics and reporting
- Integration with third-party booking platforms
- Contactless entry systems