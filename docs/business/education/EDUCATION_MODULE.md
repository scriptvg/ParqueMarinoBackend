# Education Module

## Overview

The Education module manages all educational programs, instructors, schedules, and student enrollments for the marine park. It provides functionality for creating and managing educational content, scheduling classes, and tracking student participation.

## Key Features

- Educational program creation and management
- Instructor scheduling and management
- Class schedule creation and tracking
- Student enrollment and payment processing
- Program capacity management
- Integration with payment systems

## Data Models

### Programa (Program)

Represents an educational program offered by the marine park.

**Fields**:
- `nombre`: Name of the program
- `descripcion`: Detailed description
- `duracion`: Duration in hours
- `precio`: Price in CRC
- `capacidad`: Maximum number of participants
- `imagen`: Representative image
- `activo`: Whether the program is active

**Methods**:
- `__str__()`: Returns program name
- `get_image_url()`: Returns URL of program image

### Instructor

Represents an instructor who teaches educational programs.

**Fields**:
- `nombre`: Instructor's name
- `especialidad`: Specialization area
- `biografia`: Biography
- `foto`: Profile photo
- `activo`: Whether the instructor is active

**Methods**:
- `__str__()`: Returns instructor name
- `get_foto_url()`: Returns URL of instructor photo

### Horario (Schedule)

Represents a class schedule for a program.

**Fields**:
- `programa`: Foreign key to Programa
- `instructor`: Foreign key to Instructor
- `dia_semana`: Day of the week
- `hora_inicio`: Start time
- `hora_fin`: End time
- `fecha_inicio`: Start date
- `fecha_fin`: End date
- `activo`: Whether the schedule is active

**Methods**:
- `__str__()`: Returns program name and schedule details

### Inscripcion (Enrollment)

Represents a student's enrollment in a program.

**Fields**:
- `programa`: Foreign key to Programa
- `usuario`: Foreign key to User
- `horario`: Foreign key to Horario
- `fecha_inscripcion`: Enrollment date
- `estado_pago`: Payment status
- `comprobante_pago`: Payment receipt

**Methods**:
- `__str__()`: Returns enrollment details

## API Endpoints

### Programs

- `GET /api/v1/education/programas/` - List all programs
- `POST /api/v1/education/programas/` - Create a new program
- `GET /api/v1/education/programas/{id}/` - Get program details
- `PUT /api/v1/education/programas/{id}/` - Update program
- `DELETE /api/v1/education/programas/{id}/` - Delete program

### Instructors

- `GET /api/v1/education/instructores/` - List all instructors
- `POST /api/v1/education/instructores/` - Create a new instructor
- `GET /api/v1/education/instructores/{id}/` - Get instructor details
- `PUT /api/v1/education/instructores/{id}/` - Update instructor
- `DELETE /api/v1/education/instructores/{id}/` - Delete instructor

### Schedules

- `GET /api/v1/education/horarios/` - List all schedules
- `POST /api/v1/education/horarios/` - Create a new schedule
- `GET /api/v1/education/horarios/{id}/` - Get schedule details
- `PUT /api/v1/education/horarios/{id}/` - Update schedule
- `DELETE /api/v1/education/horarios/{id}/` - Delete schedule

### Enrollments

- `GET /api/v1/education/inscripciones/` - List all enrollments
- `POST /api/v1/education/inscripciones/` - Create a new enrollment
- `GET /api/v1/education/inscripciones/{id}/` - Get enrollment details
- `PUT /api/v1/education/inscripciones/{id}/` - Update enrollment
- `DELETE /api/v1/education/inscripciones/{id}/` - Delete enrollment

## Usage Examples

### Creating a New Program

```bash
curl -X POST http://localhost:8000/api/v1/education/programas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "nombre": "Marine Life Exploration",
    "descripcion": "An interactive program exploring marine life and conservation.",
    "duracion": 2,
    "precio": 15000,
    "capacidad": 20,
    "activo": true
  }'
```

### Enrolling a Student in a Program

```bash
curl -X POST http://localhost:8000/api/v1/education/inscripciones/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "programa": 1,
    "usuario": 5,
    "horario": 3,
    "estado_pago": "pendiente"
  }'
```

## Payment Integration

The Education module integrates with the Payments module to handle program enrollment fees:

1. When a student enrolls in a program, a `PagoInscripcion` record is created
2. The payment can be processed through Stripe or PayPal
3. Payment status updates the enrollment's `estado_pago` field

## Permissions

- **Administrators**: Full CRUD access to all education data
- **Instructors**: Read access to their own programs and schedules
- **Staff**: Read access to all education data, limited write access
- **Users**: Read access to public programs, ability to enroll

## Integration Points

- **Payments Module**: Handles enrollment fees
- **Documents Module**: Programs can have associated documents
- **Audit Module**: Tracks changes to education data

## Future Enhancements

- Student progress tracking
- Certificate generation
- Program feedback and ratings
- Waitlist management for full programs
- Recurring schedule management