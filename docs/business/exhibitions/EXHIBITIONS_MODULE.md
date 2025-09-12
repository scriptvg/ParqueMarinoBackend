# Exhibitions Module

## Overview

The Exhibitions module manages all exhibition content for the marine park, including images, descriptions, interesting facts, and interactive elements. It provides functionality for creating engaging digital experiences for visitors.

## Key Features

- Exhibition content management
- Image gallery management
- Fact-based learning content
- Interactive exhibit elements
- Content versioning and approval workflows
- Media management with S3 integration

## Data Models

### Exhibicion (Exhibition)

Represents an exhibition with its content and metadata.

**Fields**:
- `titulo`: Exhibition title
- `descripcion`: Detailed description
- `contenido`: Rich text content
- `fecha_publicacion`: Publication date
- `fecha_modificacion`: Last modification date
- `publicado`: Whether the exhibition is published
- `destacado`: Whether the exhibition is featured
- `orden`: Display order
- `categoria`: Exhibition category
- `etiquetas`: Tags for categorization
- `imagen_principal`: Main exhibition image

**Methods**:
- `__str__()`: Returns exhibition title
- `get_imagen_principal_url()`: Returns URL of main image

### ExhibicionImage

Represents images associated with exhibitions.

**Fields**:
- `exhibicion`: Foreign key to Exhibicion
- `image`: Image file
- `titulo`: Image title
- `descripcion`: Image description
- `orden`: Display order

**Methods**:
- `__str__()`: Returns image title
- `get_image_url()`: Returns URL of image

### ExhibicionFact

Represents interesting facts about exhibits.

**Fields**:
- `exhibicion`: Foreign key to Exhibicion
- `titulo`: Fact title
- `contenido`: Fact content
- `orden`: Display order

**Methods**:
- `__str__()`: Returns fact title

### ExhibicionButton

Represents interactive buttons in exhibitions.

**Fields**:
- `exhibicion`: Foreign key to Exhibicion
- `texto`: Button text
- `accion`: Action to perform when clicked
- `orden`: Display order

**Methods**:
- `__str__()`: Returns button text

## API Endpoints

### Exhibitions

- `GET /api/v1/exhibitions/exhibiciones/` - List all exhibitions
- `POST /api/v1/exhibitions/exhibiciones/` - Create a new exhibition
- `GET /api/v1/exhibitions/exhibiciones/{id}/` - Get exhibition details
- `PUT /api/v1/exhibitions/exhibiciones/{id}/` - Update exhibition
- `DELETE /api/v1/exhibitions/exhibiciones/{id}/` - Delete exhibition

### Exhibition Images

- `GET /api/v1/exhibitions/imagenes/` - List all exhibition images
- `POST /api/v1/exhibitions/imagenes/` - Create a new exhibition image
- `GET /api/v1/exhibitions/imagenes/{id}/` - Get exhibition image details
- `PUT /api/v1/exhibitions/imagenes/{id}/` - Update exhibition image
- `DELETE /api/v1/exhibitions/imagenes/{id}/` - Delete exhibition image

### Exhibition Facts

- `GET /api/v1/exhibitions/hechos/` - List all exhibition facts
- `POST /api/v1/exhibitions/hechos/` - Create a new exhibition fact
- `GET /api/v1/exhibitions/hechos/{id}/` - Get exhibition fact details
- `PUT /api/v1/exhibitions/hechos/{id}/` - Update exhibition fact
- `DELETE /api/v1/exhibitions/hechos/{id}/` - Delete exhibition fact

### Exhibition Buttons

- `GET /api/v1/exhibitions/botones/` - List all exhibition buttons
- `POST /api/v1/exhibitions/botones/` - Create a new exhibition button
- `GET /api/v1/exhibitions/botones/{id}/` - Get exhibition button details
- `PUT /api/v1/exhibitions/botones/{id}/` - Update exhibition button
- `DELETE /api/v1/exhibitions/botones/{id}/` - Delete exhibition button

## Usage Examples

### Creating a New Exhibition

```bash
curl -X POST http://localhost:8000/api/v1/exhibitions/exhibiciones/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "titulo": "Coral Reef Ecosystem",
    "descripcion": "Explore the vibrant world of coral reefs and their inhabitants.",
    "contenido": "<p>Discover the beauty and importance of coral reef ecosystems...</p>",
    "publicado": true,
    "destacado": true,
    "categoria": "marine_life",
    "etiquetas": ["coral", "reef", "marine", "ecosystem"]
  }'
```

### Adding an Image to an Exhibition

```bash
curl -X POST http://localhost:8000/api/v1/exhibitions/imagenes/ \
  -H "Content-Type: multipart/form-data" \
  -H "Authorization: Bearer <token>" \
  -F "exhibicion=1" \
  -F "image=@coral_reef.jpg" \
  -F "titulo=Coral Reef" \
  -F "descripcion=Beautiful coral reef ecosystem"
```

## Media Management

The Exhibitions module integrates with AWS S3 for media storage:

1. All images are automatically uploaded to S3
2. Images are served through CloudFront CDN for performance
3. File deletion is handled through Django signals
4. Thumbnails are automatically generated for large images

## Permissions

- **Administrators**: Full CRUD access to all exhibition data
- **Content Managers**: Read and write access to exhibitions
- **Staff**: Read access to published exhibitions
- **Users**: Read access to published exhibitions

## Integration Points

- **Documents Module**: Exhibitions can have associated documents
- **Audit Module**: Tracks changes to exhibition content
- **Infrastructure Module**: Exhibitions can be linked to physical sections

## Future Enhancements

- Interactive 3D models
- Augmented reality experiences
- Visitor engagement tracking
- Content personalization based on visitor interests
- Multi-language support
- Accessibility features for visually impaired visitors