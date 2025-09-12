# Wildlife Management Module

## Overview

The Wildlife Management module handles all aspects of wildlife in the marine park, including species information, individual animals, habitats, and conservation status tracking.

## Key Features

- Species and animal tracking
- Habitat management with capacity monitoring
- Conservation status reporting
- Image management for species
- Comprehensive data model for wildlife information

## Data Models

### ConservationStatus

Represents the IUCN conservation status classifications for species.

**Fields**:
- `name`: Conservation status (LC, NT, VU, EN, CR, EW, EX)

**Methods**:
- `__str__()`: Returns the display name of the status

### Specie

Stores information about animal species including common name, scientific name, description, and image.

**Fields**:
- `name`: Common name of the species
- `scientific_name`: Scientific name (genus and species)
- `description`: Detailed description of the species
- `image`: Representative image of the species
- `conservation_status`: Foreign key to ConservationStatus

**Methods**:
- `__str__()`: Returns name and scientific name
- `get_image_url()`: Returns URL of the species image

### Animal

Represents individual animals in the park with their characteristics.

**Fields**:
- `name`: Name of the animal
- `age`: Age in years
- `specie`: Foreign key to Specie
- `habitat`: Foreign key to Habitat

**Methods**:
- `__str__()`: Returns animal name and species

### Habitat

Represents physical habitats where animals reside.

**Fields**:
- `name`: Name of the habitat
- `capacity`: Maximum number of animals
- `description`: Detailed description

**Methods**:
- `__str__()`: Returns habitat name
- `current_occupancy`: Property that calculates current occupancy
- `is_full`: Property that checks if habitat is at capacity
- `get_image_url()`: Returns URL of habitat image

## API Endpoints

### Conservation Status

- `GET /api/v1/wildlife/conservation-status/` - List all conservation statuses
- `POST /api/v1/wildlife/conservation-status/` - Create a new conservation status
- `GET /api/v1/wildlife/conservation-status/{id}/` - Get conservation status details
- `PUT /api/v1/wildlife/conservation-status/{id}/` - Update conservation status
- `DELETE /api/v1/wildlife/conservation-status/{id}/` - Delete conservation status

### Species

- `GET /api/v1/wildlife/species/` - List all species
- `POST /api/v1/wildlife/species/` - Create a new species
- `GET /api/v1/wildlife/species/{id}/` - Get species details
- `PUT /api/v1/wildlife/species/{id}/` - Update species
- `DELETE /api/v1/wildlife/species/{id}/` - Delete species

### Animals

- `GET /api/v1/wildlife/animals/` - List all animals
- `POST /api/v1/wildlife/animals/` - Create a new animal
- `GET /api/v1/wildlife/animals/{id}/` - Get animal details
- `PUT /api/v1/wildlife/animals/{id}/` - Update animal
- `DELETE /api/v1/wildlife/animals/{id}/` - Delete animal

### Habitats

- `GET /api/v1/wildlife/habitats/` - List all habitats
- `POST /api/v1/wildlife/habitats/` - Create a new habitat
- `GET /api/v1/wildlife/habitats/{id}/` - Get habitat details
- `PUT /api/v1/wildlife/habitats/{id}/` - Update habitat
- `DELETE /api/v1/wildlife/habitats/{id}/` - Delete habitat

## Usage Examples

### Creating a New Species

```bash
curl -X POST http://localhost:8000/api/v1/wildlife/species/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "Bottlenose Dolphin",
    "scientific_name": "Tursiops truncatus",
    "description": "A well-known dolphin species commonly found in temperate and tropical oceans.",
    "conservation_status": 1
  }'
```

### Listing All Animals in a Habitat

```bash
curl -X GET http://localhost:8000/api/v1/wildlife/animals/?habitat=1 \
  -H "Authorization: Bearer <token>"
```

## Permissions

- **Administrators**: Full CRUD access to all wildlife data
- **Staff**: Read access to all wildlife data, limited write access
- **Users**: Read-only access to public wildlife information

## Integration Points

- **Documents Module**: Species can have associated documents
- **Exhibitions Module**: Species information displayed in exhibitions
- **Education Module**: Species information used in educational programs

## Future Enhancements

- Integration with wildlife tracking systems
- Advanced conservation reporting
- Breeding program management
- Health record tracking for individual animals