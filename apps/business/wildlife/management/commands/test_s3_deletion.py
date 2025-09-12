"""
Comando de gestión para probar la funcionalidad de eliminación de archivos S3

Este comando permite probar la eliminación de archivos en S3 tanto individualmente
como a través de las utilidades de eliminación automática.

Uso:
    python manage.py test_s3_deletion
    python manage.py test_s3_deletion --file-path media/test.jpg
    python manage.py test_s3_deletion --test-utils
    python manage.py test_s3_deletion --file-path media/test.jpg --dry-run

Opciones:
    --file-path: Ruta del archivo en S3 para probar eliminación
    --test-utils: Probar las funciones de utilidades S3
    --dry-run: Ejecutar sin eliminar realmente archivos
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from core.utils.storage.s3_utils import delete_s3_file, get_s3_client
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Prueba la funcionalidad de eliminación de archivos S3'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file-path',
            type=str,
            help='Ruta del archivo en S3 para probar eliminación'
        )
        parser.add_argument(
            '--test-utils',
            action='store_true',
            help='Probar las funciones de utilidades S3'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Ejecutar sin eliminar realmente archivos'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('=== Prueba de Eliminación S3 ==='))
        
        # Verificar configuración S3
        if not getattr(settings, 'USE_S3', False):
            self.stdout.write(
                self.style.WARNING('S3 no está habilitado en la configuración')
            )
            return
        
        # Verificar credenciales
        try:
            s3_client = get_s3_client()
            self.stdout.write(
                self.style.SUCCESS('✓ Cliente S3 configurado correctamente')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error al configurar cliente S3: {e}')
            )
            return
        
        # Probar utilidades si se solicita
        if options['test_utils']:
            self.test_utilities()
        
        # Probar eliminación de archivo específico si se proporciona
        if options['file_path']:
            self.test_file_deletion(options['file_path'], options['dry_run'])
        
        self.stdout.write(self.style.HTTP_INFO('=== Prueba Completada ==='))

    def test_utilities(self):
        """Prueba las funciones de utilidades S3"""
        self.stdout.write(self.style.HTTP_INFO('\n--- Probando Utilidades S3 ---'))
        
        # Importar modelos para probar
        from apps.business.wildlife.models import Specie
        from apps.business.documents.models import Documento
        
        # Probar con una especie (si existe)
        try:
            specie = Specie.objects.first()
            if specie:
                from core.utils.storage.s3_utils import get_file_fields_from_instance
                file_fields = get_file_fields_from_instance(specie)
                self.stdout.write(
                    f'✓ Campos de archivo encontrados en Specie: {len(file_fields)}'
                )
                for field_name, file_field in file_fields:
                    self.stdout.write(f'  - {field_name}: {file_field.name if file_field.name else "No file"}')
            else:
                self.stdout.write('⚠ No hay especies en la base de datos para probar')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error al probar Specie: {e}'))
        
        # Probar con un documento (si existe)
        try:
            documento = Documento.objects.first()
            if documento:
                from core.utils.storage.s3_utils import get_file_fields_from_instance
                file_fields = get_file_fields_from_instance(documento)
                self.stdout.write(
                    f'✓ Campos de archivo encontrados en Documento: {len(file_fields)}'
                )
                for field_name, file_field in file_fields:
                    self.stdout.write(f'  - {field_name}: {file_field.name if file_field.name else "No file"}')
            else:
                self.stdout.write('⚠ No hay documentos en la base de datos para probar')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error al probar Documento: {e}'))

    def test_file_deletion(self, file_path, dry_run=False):
        """Prueba la eliminación de un archivo específico"""
        self.stdout.write(self.style.HTTP_INFO(f'\n--- Probando Eliminación de: {file_path} ---'))
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('MODO DRY-RUN: No se eliminará realmente el archivo')
            )
            
            # Solo verificar si el archivo existe
            try:
                s3_client = get_s3_client()
                bucket_name = settings.AWS_STORAGE_BUCKET_NAME
                
                # Asegurar que la ruta incluya el prefijo media/
                if not file_path.startswith('media/'):
                    test_file_path = f"media/{file_path}"
                else:
                    test_file_path = file_path
                
                response = s3_client.head_object(Bucket=bucket_name, Key=test_file_path)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Archivo existe en S3: {test_file_path}')
                )
                self.stdout.write(f'  - Tamaño: {response["ContentLength"]} bytes')
                self.stdout.write(f'  - Última modificación: {response["LastModified"]}')
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error al verificar archivo: {e}')
                )
        else:
            # Intentar eliminar realmente
            self.stdout.write(
                self.style.WARNING('Eliminando archivo real de S3...')
            )
            
            try:
                result = delete_s3_file(file_path)
                if result:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Archivo eliminado exitosamente: {file_path}')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Error al eliminar archivo: {file_path}')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Excepción al eliminar archivo: {e}')
                )