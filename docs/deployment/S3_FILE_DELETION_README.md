# Eliminación Automática de Archivos S3

Esta implementación proporciona eliminación automática de archivos en S3 cuando se eliminan o actualizan registros en la base de datos.

## 🎯 Funcionalidades Implementadas

### ✅ Eliminación Automática en DELETE
- **Cuándo**: Al eliminar cualquier registro que tenga archivos asociados
- **Qué**: Elimina todos los archivos S3 relacionados automáticamente
- **Cómo**: Usando señales de Django `post_delete`

### ✅ Eliminación de Archivos Anteriores en UPDATE
- **Cuándo**: Al actualizar un campo de archivo (FileField/ImageField)
- **Qué**: Elimina el archivo anterior de S3 si se sube uno nuevo
- **Cómo**: Usando señales de Django `pre_save`

### ✅ Logging Completo
- **Eventos**: Todos los eventos de eliminación se registran
- **Niveles**: Info para éxitos, Warning para advertencias, Error para fallos
- **Detalles**: Incluye nombres de archivos, IDs de registros y resultados

## 📁 Estructura de Archivos

```
backend/
├── utils/
│   ├── __init__.py
│   └── s3_utils.py          # ✨ Utilidades principales para S3
├── wildlife/
│   ├── signals.py           # ✨ Señales para modelos wildlife
│   ├── apps.py              # ✓ Actualizado para cargar señales
│   └── management/commands/
│       └── test_s3_deletion.py  # ✨ Comando para pruebas
├── exhibitions/
│   ├── signals.py           # ✨ Señales para modelos exhibitions
│   └── apps.py              # ✓ Actualizado para cargar señales
├── education/
│   ├── signals.py           # ✨ Señales para modelos education
│   └── apps.py              # ✓ Actualizado para cargar señales
├── payments/
│   ├── signals.py           # ✨ Señales para modelos payments
│   └── apps.py              # ✓ Actualizado para cargar señales
└── documents/
    ├── signals.py           # ✨ Señales para modelos documents
    └── apps.py              # ✓ Actualizado para cargar señales
```

## 🔧 Modelos Cubiertos

### Wildlife App
- **Specie** (campo: `image`)
  - ✅ Eliminación automática en DELETE
  - ✅ Eliminación de imagen anterior en UPDATE

### Exhibitions App
- **ExhibicionImage** (campo: `image`)
  - ✅ Eliminación automática en DELETE
  - ✅ Eliminación de imagen anterior en UPDATE

### Education App
- **ServiciosEducativosImage** (campo: `image`)
  - ✅ Eliminación automática en DELETE
  - ✅ Eliminación de imagen anterior en UPDATE
- **ProgramaEducativo** (campo: `image`)
  - ✅ Eliminación automática en DELETE
  - ✅ Eliminación de imagen anterior en UPDATE

### Payments App
- **Pago** (campo: `comprobante`)
  - ✅ Eliminación automática en DELETE
  - ✅ Eliminación de comprobante anterior en UPDATE

### Documents App
- **Documento** (campo: `archivo`)
  - ✅ Eliminación automática en DELETE
  - ✅ Eliminación de archivo anterior en UPDATE

## 🚀 Uso y Ejemplos

### Eliminación Automática
```python
# Al eliminar una especie, su imagen se elimina automáticamente de S3
specie = Specie.objects.get(id=1)
specie.delete()  # ← La imagen se elimina automáticamente de S3

# Al eliminar un documento, su archivo se elimina automáticamente de S3
documento = Documento.objects.get(id=1)
documento.delete()  # ← El archivo se elimina automáticamente de S3
```

### Actualización de Archivos
```python
# Al actualizar la imagen de una especie, la anterior se elimina de S3
specie = Specie.objects.get(id=1)
specie.image = new_image_file  # ← La imagen anterior se elimina de S3
specie.save()

# Al actualizar un documento, el archivo anterior se elimina de S3
documento = Documento.objects.get(id=1)
documento.archivo = new_file  # ← El archivo anterior se elimina de S3
documento.save()
```

## 🧪 Comandos de Prueba

### Probar Utilidades S3
```bash
python manage.py test_s3_deletion --test-utils --dry-run
```

### Probar Eliminación de Archivo Específico
```bash
# Modo dry-run (solo verificar)
python manage.py test_s3_deletion --file-path "documentos/mi-archivo.pdf" --dry-run

# Eliminación real
python manage.py test_s3_deletion --file-path "documentos/mi-archivo.pdf"
```

## ⚙️ Configuración

### Requisitos
- ✅ `boto3` (ya instalado en requirements.txt)
- ✅ `USE_S3 = True` en configuración
- ✅ Credenciales AWS configuradas
- ✅ Variables de entorno S3 configuradas

### Variables de Entorno Necesarias
```env
USE_S3=True
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_STORAGE_BUCKET_NAME=tu_bucket_name
```

## 🔒 Seguridad y Robustez

### Manejo de Errores
- ✅ **Credenciales faltantes**: Se registra error, no se interrumpe la aplicación
- ✅ **Archivo no encontrado**: Se considera éxito (archivo ya no existe)
- ✅ **Errores de red**: Se registra error, operación continúa
- ✅ **S3 deshabilitado**: Se omite eliminación automáticamente

### Logging
```python
# Ejemplos de logs generados
INFO: Archivo eliminado exitosamente de S3: species/mi-imagen.jpg
WARNING: El archivo no existe en S3: documentos/archivo-inexistente.pdf
ERROR: Error de cliente S3 al eliminar species/imagen.jpg: AccessDenied
```

### Fallbacks
- Si `default_storage.delete()` falla, se usa `boto3` directamente
- Si S3 no está habilitado, se omite eliminación sin errores
- Si el archivo no existe, se considera operación exitosa

## 📈 Beneficios

1. **Limpieza Automática**: No más archivos huérfanos en S3
2. **Ahorro de Costos**: Reduce el almacenamiento innecesario en S3
3. **Mantenimiento**: Sin intervención manual requerida
4. **Consistencia**: Archivos siempre sincronizados con la base de datos
5. **Logging**: Trazabilidad completa de todas las operaciones
6. **Robustez**: Manejo de errores sin interrumpir la aplicación

## 🔧 Extensión para Nuevos Modelos

Para agregar eliminación S3 a un nuevo modelo:

1. **Crear signals.py** en la app:
```python
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import TuModelo
from utils.s3_utils import delete_s3_files_from_instance, delete_old_s3_file

@receiver(post_delete, sender=TuModelo)
def delete_s3_files_on_delete(sender, instance, **kwargs):
    delete_s3_files_from_instance(instance)

@receiver(pre_save, sender=TuModelo)
def delete_old_file_on_update(sender, instance, **kwargs):
    if instance.pk:
        delete_old_s3_file(sender, instance, 'tu_campo_archivo')
```

2. **Actualizar apps.py**:
```python
def ready(self):
    import tu_app.signals
```

¡Listo! La eliminación automática funcionará para tu nuevo modelo.

## ✅ Estado Actual

**🎉 IMPLEMENTACIÓN COMPLETA**
- ✅ Todas las apps con archivos S3 están cubiertas
- ✅ Señales registradas y funcionando
- ✅ Utilidades probadas y validadas
- ✅ Comando de prueba disponible
- ✅ Logging completo implementado
- ✅ Documentación creada

**Los archivos ahora se eliminan automáticamente de S3 cuando se eliminan o actualizan registros en la base de datos.** 🚀