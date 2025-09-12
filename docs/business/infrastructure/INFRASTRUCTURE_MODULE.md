# Infrastructure Module

## Overview

The Infrastructure module manages the physical layout of the marine park, including sections and habitats. It provides functionality for tracking the physical organization of the park and managing capacity constraints.

## Key Features

- Physical section management
- Habitat location tracking
- Capacity management for sections and habitats
- Spatial organization of park facilities
- Integration with wildlife and exhibition modules

## Data Models

### Seccion (Section)

Represents a physical section of the marine park.

**Fields**:
- `nombre`: Section name
- `descripcion`: Detailed description
- `capacidad_maxima`: Maximum capacity
- `ubicacion`: Location coordinates (latitude, longitude)
- `imagen`: Section image

**Methods**:
- `__str__()`: Returns section name
- `get_image_url()`: Returns URL of section image
- `current_occupancy`: Property that calculates current occupancy
- `is_full`: Property that checks if section is at capacity

### Habitat

Represents a habitat within a section where animals reside.

**Fields**:
- `nombre`: Habitat name
- `seccion`: Foreign key to Seccion
- `descripcion`: Detailed description
- `capacidad_maxima`: Maximum capacity
- `tipo_habitat`: Habitat type
- `caracteristicas`: Special characteristics
- `imagen`: Habitat image

**Methods**:
- `__str__()`: Returns habitat name
- `get_image_url()`: Returns URL of habitat image
- `current_occupancy`: Property that calculates current occupancy
- `is_full`: Property that checks if habitat is at capacity

## API Endpoints

### Sections

- `GET /api/v1/infrastructure/secciones/` - List all sections
- `POST /api/v1/infrastructure/secciones/` - Create a new section
- `GET /api/v1/infrastructure/secciones/{id}/` - Get section details
- `PUT /api/v1/infrastructure/secciones/{id}/` - Update section
- `DELETE /api/v1/infrastructure/secciones/{id}/` - Delete section

### Habitats

- `GET /api/v1/infrastructure/habitats/` - List all habitats
- `POST /api/v1/infrastructure/habitats/` - Create a new habitat
- `GET /api/v1/infrastructure/habitats/{id}/` - Get habitat details
- `PUT /api/v1/infrastructure/habitats/{id}/` - Update habitat
- `DELETE /api/v1/infrastructure/habitats/{id}/` - Delete habitat

## Usage Examples

### Creating a New Section

```bash
curl -X POST http://localhost:8000/api/v1/infrastructure/secciones/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "nombre": "Tropical Reef Area",
    "descripcion": "Section dedicated to tropical marine life including coral reefs.",
    "capacidad_maxima": 500,
    "ubicacion": "9.9333° N, 84.0833° W"
  }'
```

### Creating a New Habitat

```bash
curl -X POST http://localhost:8000/api/v1/infrastructure/habitats/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "nombre": "Coral Reef Tank",
    "seccion": 1,
    "descripcion": "Large tank simulating a coral reef environment.",
    "capacidad_maxima": 50,
    "tipo_habitat": "aquatic",
    "caracteristicas": "Saltwater, temperature controlled, coral structures"
  }'
```

## Capacity Management

The Infrastructure module provides real-time capacity tracking:

1. Each section and habitat has a maximum capacity
2. Current occupancy is calculated based on associated animals
3. Warnings are generated when capacity thresholds are approached
4. Integration with wildlife module ensures accurate occupancy tracking

## Permissions

- **Administrators**: Full CRUD access to all infrastructure data
- **Facilities Managers**: Read and write access to infrastructure data
- **Staff**: Read access to infrastructure information
- **Users**: Limited read access to public infrastructure information

## Integration Points

- **Wildlife Module**: Habitats contain animals, sections contain habitats
- **Exhibitions Module**: Exhibitions can be linked to sections
- **Tickets Module**: Section capacity affects ticket sales
- **Audit Module**: Tracks changes to infrastructure data

## Future Enhancements

- Interactive park maps
- Real-time visitor tracking within sections
- Maintenance scheduling for habitats
- Environmental monitoring integration
- Wayfinding and navigation assistance
- Accessibility information for visitors with disabilities