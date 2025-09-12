# Documents Module

## Overview

The Documents module manages all file uploads, versioning, and access tracking for the marine park. It provides functionality for storing, organizing, and tracking access to various types of documents.

## Key Features

- File upload and storage management
- Document versioning and history
- Access tracking and auditing
- Document type classification
- Integration with AWS S3 for storage
- Metadata management
- Search and filtering capabilities

## Data Models

### TipoDocumento (Document Type)

Represents different types of documents in the system.

**Fields**:
- `nombre`: Document type name
- `descripcion`: Detailed description
- `extensiones_permitidas`: Allowed file extensions
- `tamano_maximo`: Maximum file size (in MB)

**Methods**:
- `__str__()`: Returns document type name

### Documento (Document)

Represents a document file with its metadata.

**Fields**:
- `titulo`: Document title
- `descripcion`: Document description
- `tipo`: Foreign key to TipoDocumento
- `archivo`: File field for document storage
- `version`: Document version number
- `fecha_creacion`: Creation date
- `fecha_modificacion`: Last modification date
- `creado_por`: User who created the document
- `modificado_por`: User who last modified the document
- `publico`: Whether the document is publicly accessible
- `activo`: Whether the document is active

**Methods**:
- `__str__()`: Returns document title
- `get_archivo_url()`: Returns URL of document file
- `get_file_size()`: Returns formatted file size
- `get_file_extension()`: Returns file extension

### HistorialAcceso (Access History)

Tracks access to documents for auditing purposes.

**Fields**:
- `documento`: Foreign key to Documento
- `usuario`: Foreign key to User (nullable for anonymous access)
- `fecha_acceso`: Access date and time
- `direccion_ip`: IP address of accessing user
- `user_agent`: Browser information

**Methods**:
- `__str__()`: Returns access record details

## Document Types

The system supports various document types with specific configurations:

1. **PDF**: Portable Document Format files
2. **Image**: Image files (JPG, PNG, GIF)
3. **Document**: Office documents (DOC, DOCX, XLS, XLSX)
4. **Spreadsheet**: Spreadsheet files
5. **Presentation**: Presentation files
6. **Video**: Video files
7. **Audio**: Audio files
8. **Archive**: Compressed files (ZIP, RAR)

## API Endpoints

### Document Types

- `POST /api/v1/documents/tipos/` - Create a new document type
- `GET /api/v1/documents/tipos/` - List all document types
- `GET /api/v1/documents/tipos/{id}/` - Get document type details
- `PUT /api/v1/documents/tipos/{id}/` - Update document type
- `DELETE /api/v1/documents/tipos/{id}/` - Delete document type

### Documents

- `POST /api/v1/documents/documentos/` - Upload a new document
- `GET /api/v1/documents/documentos/` - List all documents
- `GET /api/v1/documents/documentos/{id}/` - Get document details
- `PUT /api/v1/documents/documentos/{id}/` - Update document
- `DELETE /api/v1/documents/documentos/{id}/` - Delete document
- `GET /api/v1/documents/documentos/{id}/descargar/` - Download document
- `GET /api/v1/documents/documentos/{id}/vista-previa/` - Preview document

### Access History

- `GET /api/v1/documents/historial/` - List access history
- `GET /api/v1/documents/historial/{id}/` - Get access record details

## Usage Examples

### Creating a New Document Type

```bash
curl -X POST http://localhost:8000/api/v1/documents/tipos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "nombre": "Annual Report",
    "descripcion": "Annual financial and operational reports",
    "extensiones_permitidas": "pdf,doc,docx",
    "tamano_maximo": 50
  }'
```

### Uploading a New Document

```bash
curl -X POST http://localhost:8000/api/v1/documents/documentos/ \
  -H "Content-Type: multipart/form-data" \
  -H "Authorization: Bearer <token>" \
  -F "titulo=2023 Annual Report" \
  -F "descripcion=Annual report for 2023" \
  -F "tipo=1" \
  -F "archivo=@2023_annual_report.pdf" \
  -F "publico=true"
```

### Downloading a Document

```bash
curl -X GET http://localhost:8000/api/v1/documents/documentos/1/descargar/ \
  -H "Authorization: Bearer <token>" \
  -o downloaded_document.pdf
```

## Storage Management

The Documents module integrates with AWS S3 for secure file storage:

1. **Automatic Upload**: Files are automatically uploaded to S3
2. **Versioning**: S3 versioning tracks document history
3. **CDN Integration**: CloudFront serves files for better performance
4. **Security**: Private files are served through secure URLs
5. **Cleanup**: Automatic deletion of old versions and unused files

## Access Control

The module provides granular access control:

1. **Public Documents**: Accessible to anyone
2. **Private Documents**: Access restricted to authorized users
3. **Role-based Access**: Permissions based on user roles
4. **User-based Access**: Specific user access permissions
5. **Time-based Access**: Documents available only during specific periods

## Metadata Management

Documents include comprehensive metadata:

1. **File Information**: Size, type, creation date
2. **User Information**: Creator, modifier, access history
3. **Version Information**: Version number, change history
4. **Classification**: Document type, tags, categories
5. **Security**: Access permissions, encryption status

## Search and Filtering

The module provides powerful search capabilities:

1. **Text Search**: Search by title, description, content
2. **Metadata Filtering**: Filter by type, date, size, user
3. **Version Management**: Access specific versions
4. **Tag-based Search**: Find documents by tags
5. **Advanced Queries**: Complex search combinations

## Permissions

- **Administrators**: Full access to all documents
- **Document Managers**: Create, update, and manage documents
- **Authorized Users**: Access to specific documents based on permissions
- **Public Users**: Access to public documents only

## Integration Points

- **Audit Module**: Tracks all document access and modifications
- **Payments Module**: Documents can be associated with payments
- **Education Module**: Educational materials and resources
- **Wildlife Module**: Research documents and species information
- **Messaging Module**: Document sharing and notifications

## Future Enhancements

- Optical Character Recognition (OCR) for searchable PDFs
- Document collaboration features
- Advanced workflow management
- Integration with document signing services
- Automated document categorization
- AI-powered document analysis
- Mobile document scanning