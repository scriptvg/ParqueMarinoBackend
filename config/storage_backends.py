from storages.backends.s3boto3 import S3Boto3Storage
from django.core.exceptions import ValidationError
import os

class StaticStorage(S3Boto3Storage):
    """
    Configuración para archivos estáticos en S3
    - Ubicación: carpeta 'static/' en el bucket
    """
    location = 'static'
    default_acl = None  # ⚠ ACL deshabilitada


class MediaStorage(S3Boto3Storage):
    """
    Configuración para archivos media en S3
    - Ubicación: carpeta 'media/' en el bucket
    - Tipos permitidos: PDF e imágenes
    """
    location = 'media'
    default_acl = None  # ⚠ ACL deshabilitada
    file_overwrite = False

    def _save(self, name, content):
        """
        Validación de tipos de archivo permitidos
        """
        # Extensiones permitidas
        ALLOWED_EXTENSIONS = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', 'webp', '.doc', '.docx', '.xls', '.xlsx', '.csv']
        
        def convertIMAGE(image):
            """
            Convertir imagen a formato webp
            """
            from PIL import Image
            from io import BytesIO
            from webp import WebPImage
            
            # Convertir imagen a formato webp
            img = Image.open(content)
            img = img.convert('RGB')
            img = img.resize((800, 600))
            webp_image = WebPImage.from_pil_image(img)
            webp_bytes = webp_image.to_bytes()
            
            # Devolver imagen convertida como BytesIO
            return BytesIO(webp_bytes)
        
        ALLOWED_MAX_SIZE = 20 * 1024 * 1024
        
        ext = os.path.splitext(name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValidationError(f'Tipo de archivo no permitido. Use: {", ".join(ALLOWED_EXTENSIONS)}')
          
        if ext not in ALLOWED_MAX_SIZE:
            raise ValidationError(f'Tamaño de archivo no permitido. Máximo: {ALLOWED_MAX_SIZE} bytes')
        
        return super()._save(name, content)
