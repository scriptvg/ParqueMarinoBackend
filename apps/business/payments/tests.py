from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch, MagicMock

from .models import Pago, PagoInscripcion, Donacion
from .services import CurrencyConverter
from apps.business.education.models import Instructor, Programa, Horario, Inscripcion

User = get_user_model()


class PagoModelTest(TestCase):
    """Test suite para el modelo Pago."""
    
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_pago_creation(self, mock_currency):
        """Test creación básica de pago."""
        mock_currency.return_value = (Decimal('54000.00'), Decimal('100.00'))
        
        pago = Pago.objects.create(
            monto=Decimal('100.00'),
            moneda='USD',
            metodo_pago='CARD',
            referencia_transaccion='PAY123456',
            estado='PENDING'
        )
        
        self.assertEqual(pago.monto, Decimal('100.00'))
        self.assertEqual(pago.moneda, 'USD')
        self.assertEqual(pago.metodo_pago, 'CARD')
        self.assertEqual(pago.estado, 'PENDING')
        self.assertEqual(pago.monto_crc, Decimal('54000.00'))
        self.assertEqual(pago.monto_usd, Decimal('100.00'))
        
    def test_pago_str_representation(self):
        """Test representación string del pago."""
        with patch('payments.services.CurrencyConverter.get_both_currencies') as mock_currency:
            mock_currency.return_value = (Decimal('27000.00'), Decimal('50.00'))
            
            pago = Pago.objects.create(
                monto=Decimal('50.00'),
                moneda='USD',
                metodo_pago='PAYPAL',
                referencia_transaccion='PP789',
                estado='SUCCESS'
            )
            
            expected_str = 'Pago PP789 - Completado'
            self.assertEqual(str(pago), expected_str)
        
    def test_pago_estado_choices(self):
        """Test opciones válidas de estado."""
        valid_estados = ['PENDING', 'PROCESSING', 'SUCCESS', 'FAILED', 'REFUNDED']
        
        with patch('payments.services.CurrencyConverter.get_both_currencies') as mock_currency:
            mock_currency.return_value = (Decimal('10000.00'), Decimal('18.50'))
            
            for estado in valid_estados:
                pago = Pago.objects.create(
                    monto=Decimal('18.50'),
                    moneda='USD',
                    metodo_pago='CASH',
                    referencia_transaccion=f'TEST{estado}',
                    estado=estado
                )
                # Verificar que el pago se creó correctamente
                self.assertEqual(pago.estado, estado)
                self.assertEqual(pago.monto, Decimal('18.50'))
                
    def test_pago_metodo_pago_choices(self):
        """Test opciones válidas de método de pago."""
        valid_metodos = ['CARD', 'PAYPAL', 'CASH', 'TRANSFER', 'OTHER']
        
        with patch('payments.services.CurrencyConverter.get_both_currencies') as mock_currency:
            mock_currency.return_value = (Decimal('15000.00'), Decimal('27.78'))
            
            for metodo in valid_metodos:
                pago = Pago.objects.create(
                    monto=Decimal('27.78'),
                    moneda='USD',
                    metodo_pago=metodo,
                    referencia_transaccion=f'METHOD{metodo}',
                    estado='PENDING'
                )
                # Verificar que el pago se creó correctamente
                self.assertEqual(pago.metodo_pago, metodo)
                self.assertEqual(pago.monto, Decimal('27.78'))
                
    def test_pago_unique_referencia_constraint(self):
        """Test restricción de unicidad en referencia_transaccion."""
        with patch('payments.services.CurrencyConverter.get_both_currencies') as mock_currency:
            mock_currency.return_value = (Decimal('10000.00'), Decimal('18.50'))
            
            Pago.objects.create(
                monto=Decimal('18.50'),
                moneda='USD',
                metodo_pago='CARD',
                referencia_transaccion='UNIQUE123'
            )
            
            # Intentar crear otro pago con la misma referencia
            with transaction.atomic():
                with self.assertRaises(IntegrityError):
                    Pago.objects.create(
                        monto=Decimal('25.00'),
                        moneda='USD',
                        metodo_pago='PAYPAL',
                        referencia_transaccion='UNIQUE123'
                    )
                    
    def test_pago_monto_validation(self):
        """Test validación de monto positivo."""
        pago = Pago(
            monto=Decimal('-10.00'),  # Monto negativo
            moneda='CRC',
            metodo_pago='CASH',
            referencia_transaccion='NEGATIVE'
        )
        
        with self.assertRaises(ValidationError):
            pago.full_clean()
            
    @patch('payments.models.Pago.comprobante.field.storage.save')
    def test_pago_with_comprobante(self, mock_save):
        """Test pago con archivo de comprobante."""
        mock_save.return_value = 'comprobantes_pago/comprobante.pdf'
        
        with patch('payments.services.CurrencyConverter.get_both_currencies') as mock_currency:
            mock_currency.return_value = (Decimal('50000.00'), Decimal('92.59'))
            
            comprobante_file = SimpleUploadedFile(
                'comprobante.pdf',
                b'fake pdf content',
                content_type='application/pdf'
            )
            
            pago = Pago.objects.create(
                monto=Decimal('92.59'),
                moneda='USD',
                metodo_pago='TRANSFER',
                referencia_transaccion='RECEIPT123',
                comprobante=comprobante_file,
                notas='Pago por transferencia bancaria'
            )
            
            self.assertTrue(pago.comprobante)
            self.assertEqual(pago.notas, 'Pago por transferencia bancaria')
            
    def test_pago_meta_options(self):
        """Test opciones del modelo Meta."""
        with patch('payments.services.CurrencyConverter.get_both_currencies') as mock_currency:
            mock_currency.return_value = (Decimal('25000.00'), Decimal('46.30'))
            
            pago = Pago.objects.create(
                monto=Decimal('46.30'),
                moneda='USD',
                metodo_pago='CARD',
                referencia_transaccion='META123'
            )
            
            self.assertEqual(pago._meta.verbose_name, 'Pago')
            self.assertEqual(pago._meta.verbose_name_plural, 'Pagos')
            self.assertEqual(pago._meta.ordering, ['-fecha_pago'])


class PagoInscripcionModelTest(TestCase):
    """Test suite para el modelo PagoInscripcion."""
    
    def setUp(self):
        """Configurar datos de prueba para cada método de test."""
        self.user_instructor = User.objects.create_user(username='instructor1')
        self.user_participant = User.objects.create_user(username='participant1')
        
        self.instructor = Instructor.objects.create(
            user=self.user_instructor,
            especialidad='Biología Marina',
            experiencia_years=5,
            bio='Instructor experto'
        )
        
        self.programa = Programa.objects.create(
            nombre='Taller de Conservación',
            descripcion='Taller sobre conservación marina',
            duracion_horas=3,
            capacidad_min=5,
            capacidad_max=20,
            edad_minima=10,
            edad_maxima=16,
            requisitos='Ninguno',
            precio=Decimal('35000.00')
        )
        
        fecha_inicio = timezone.now() + timedelta(days=7)
        fecha_fin = fecha_inicio + timedelta(hours=3)
        
        self.horario = Horario.objects.create(
            programa=self.programa,
            instructor=self.instructor,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        
        self.inscripcion = Inscripcion.objects.create(
            horario=self.horario,
            usuario=self.user_participant,
            nombre_participante='Ana Martínez',
            edad_participante=12
        )
        
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_pago_inscripcion_creation(self, mock_currency):
        """Test creación de pago de inscripción."""
        mock_currency.return_value = (Decimal('35000.00'), Decimal('64.81'))
        
        pago_inscripcion = PagoInscripcion.objects.create(
            inscripcion=self.inscripcion,
            monto=self.programa.precio,
            moneda='CRC',
            metodo_pago='CARD',
            referencia_transaccion='INS123456'
        )
        
        self.assertEqual(pago_inscripcion.inscripcion, self.inscripcion)
        self.assertEqual(pago_inscripcion.monto, self.programa.precio)
        self.assertEqual(pago_inscripcion.moneda, 'CRC')
        
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_pago_inscripcion_estado_update(self, mock_currency):
        """Test actualización automática del estado de inscripción."""
        mock_currency.return_value = (Decimal('35000.00'), Decimal('64.81'))
        
        pago_inscripcion = PagoInscripcion.objects.create(
            inscripcion=self.inscripcion,
            monto=self.programa.precio,
            moneda='CRC',
            metodo_pago='CARD',
            referencia_transaccion='INS789',
            estado='SUCCESS'
        )
        
        # Verificar que el estado de la inscripción se actualizó
        self.inscripcion.refresh_from_db()
        self.assertEqual(self.inscripcion.estado_pago, 'pagado')
        
        # Probar con estado FAILED
        pago_inscripcion.estado = 'FAILED'
        pago_inscripcion.save()
        
        self.inscripcion.refresh_from_db()
        self.assertEqual(self.inscripcion.estado_pago, 'pendiente')
        
        # Probar con estado REFUNDED
        pago_inscripcion.estado = 'REFUNDED'
        pago_inscripcion.save()
        
        self.inscripcion.refresh_from_db()
        self.assertEqual(self.inscripcion.estado_pago, 'cancelado')
        
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_pago_inscripcion_one_to_one_relationship(self, mock_currency):
        """Test relación uno a uno con inscripción."""
        mock_currency.return_value = (Decimal('35000.00'), Decimal('64.81'))
        
        pago_inscripcion = PagoInscripcion.objects.create(
            inscripcion=self.inscripcion,
            monto=self.programa.precio,
            moneda='CRC',
            metodo_pago='PAYPAL',
            referencia_transaccion='PAYPAL123'
        )
        
        # Verificar relación directa
        self.assertEqual(pago_inscripcion.inscripcion, self.inscripcion)
        
        # Verificar relación inversa
        self.assertEqual(self.inscripcion.pago, pago_inscripcion)
        
    def test_pago_inscripcion_cascade_delete(self):
        """Test eliminación en cascada cuando se elimina inscripción."""
        with patch('payments.services.CurrencyConverter.get_both_currencies') as mock_currency:
            mock_currency.return_value = (Decimal('35000.00'), Decimal('64.81'))
            
            pago_inscripcion = PagoInscripcion.objects.create(
                inscripcion=self.inscripcion,
                monto=self.programa.precio,
                moneda='CRC',
                metodo_pago='CASH',
                referencia_transaccion='CASCADE123'
            )
            
            pago_id = pago_inscripcion.id
            
            # Eliminar la inscripción
            self.inscripcion.delete()
            
            # El pago debería eliminarse también
            with self.assertRaises(PagoInscripcion.DoesNotExist):
                PagoInscripcion.objects.get(id=pago_id)


class DonacionModelTest(TestCase):
    """Test suite para el modelo Donacion."""
    
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_donacion_creation_with_donor_info(self, mock_currency):
        """Test creación de donación con información del donante."""
        mock_currency.return_value = (Decimal('54000.00'), Decimal('100.00'))
        
        donacion = Donacion.objects.create(
            monto=Decimal('100.00'),
            moneda='USD',
            nombre_donante='Carlos Rodríguez',
            email_donante='carlos@ejemplo.com',
            metodo_pago='PAYPAL',
            referencia_transaccion='DON123456'
        )
        
        self.assertEqual(donacion.monto, Decimal('100.00'))
        self.assertEqual(donacion.moneda, 'USD')
        self.assertEqual(donacion.nombre_donante, 'Carlos Rodríguez')
        self.assertEqual(donacion.email_donante, 'carlos@ejemplo.com')
        self.assertEqual(donacion.monto_crc, Decimal('54000.00'))
        self.assertEqual(donacion.monto_usd, Decimal('100.00'))
        
    @patch('payments.services.CurrencyConverter.get_both_currencies')
    def test_donacion_creation_anonymous(self, mock_currency):
        """Test creación de donación anónima."""
        mock_currency.return_value = (Decimal('25000.00'), Decimal('46.30'))
        
        donacion = Donacion.objects.create(
            monto=Decimal('25000.00'),
            moneda='CRC',
            metodo_pago='CASH',
            referencia_transaccion='ANON789'
        )
        
        self.assertEqual(donacion.monto, Decimal('25000.00'))
        self.assertEqual(donacion.moneda, 'CRC')
        self.assertIsNone(donacion.nombre_donante)
        self.assertIsNone(donacion.email_donante)
        self.assertEqual(donacion.estado, 'PENDING')
        
    def test_donacion_str_representation(self):
        """Test representación string de la donación."""
        with patch('payments.services.CurrencyConverter.get_both_currencies') as mock_currency:
            mock_currency.return_value = (Decimal('27000.00'), Decimal('50.00'))
            
            donacion = Donacion.objects.create(
                monto=Decimal('50.00'),
                moneda='USD',
                metodo_pago='TRANSFER',
                estado='SUCCESS'
            )
            
            expected_str = 'Donación 50.00 USD - Completado'
            self.assertEqual(str(donacion), expected_str)
            
    def test_donacion_monto_validation(self):
        """Test validación de monto positivo en donaciones."""
        donacion = Donacion(
            monto=Decimal('-50.00'),  # Monto negativo
            moneda='USD',
            metodo_pago='PAYPAL'
        )
        
        with self.assertRaises(ValidationError):
            donacion.full_clean()
            
    def test_donacion_meta_options(self):
        """Test opciones del modelo Meta para donaciones."""
        with patch('payments.services.CurrencyConverter.get_both_currencies') as mock_currency:
            mock_currency.return_value = (Decimal('40000.00'), Decimal('74.07'))
            
            donacion = Donacion.objects.create(
                monto=Decimal('74.07'),
                moneda='USD',
                metodo_pago='CARD'
            )
            
            self.assertEqual(donacion._meta.verbose_name, 'Donación')
            self.assertEqual(donacion._meta.verbose_name_plural, 'Donaciones')
            self.assertEqual(donacion._meta.ordering, ['-fecha_creacion'])


class CurrencyConverterTest(TestCase):
    """Test suite para el servicio CurrencyConverter."""
    
    @patch('payments.services.requests.get')
    def test_get_exchange_rate_success(self, mock_get):
        """Test obtención exitosa de tasa de cambio."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'rates': {'CRC': 540.25}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        rate = CurrencyConverter.get_exchange_rate()
        self.assertEqual(rate, Decimal('540.25'))
        
    @patch('payments.services.requests.get')
    def test_get_exchange_rate_failure(self, mock_get):
        """Test manejo de errores al obtener tasa de cambio."""
        mock_get.side_effect = Exception('API Error')
        
        rate = CurrencyConverter.get_exchange_rate()
        self.assertEqual(rate, Decimal('540.00'))  # Tasa por defecto
        
    def test_convert_currency_usd_to_crc(self):
        """Test conversión de USD a CRC."""
        with patch.object(CurrencyConverter, 'get_exchange_rate', return_value=Decimal('540.00')):
            result = CurrencyConverter.convert_currency(100, 'USD', 'CRC')
            self.assertEqual(result, Decimal('54000.00'))
            
    def test_convert_currency_crc_to_usd(self):
        """Test conversión de CRC a USD."""
        with patch.object(CurrencyConverter, 'get_exchange_rate', return_value=Decimal('540.00')):
            result = CurrencyConverter.convert_currency(54000, 'CRC', 'USD')
            self.assertEqual(result, Decimal('100.00'))
            
    def test_convert_currency_same_currency(self):
        """Test conversión entre la misma moneda."""
        result = CurrencyConverter.convert_currency(100, 'USD', 'USD')
        self.assertEqual(result, Decimal('100'))
        
    def test_convert_currency_invalid_currency(self):
        """Test manejo de monedas inválidas."""
        with self.assertRaises(ValueError):
            CurrencyConverter.convert_currency(100, 'EUR', 'USD')
            
    def test_get_both_currencies_from_usd(self):
        """Test obtención de ambas monedas desde USD."""
        with patch.object(CurrencyConverter, 'get_exchange_rate', return_value=Decimal('540.00')):
            monto_crc, monto_usd = CurrencyConverter.get_both_currencies(100, 'USD')
            self.assertEqual(monto_usd, Decimal('100'))
            self.assertEqual(monto_crc, Decimal('54000.00'))
            
    def test_get_both_currencies_from_crc(self):
        """Test obtención de ambas monedas desde CRC."""
        with patch.object(CurrencyConverter, 'get_exchange_rate', return_value=Decimal('540.00')):
            monto_crc, monto_usd = CurrencyConverter.get_both_currencies(54000, 'CRC')
            self.assertEqual(monto_crc, Decimal('54000'))
            self.assertEqual(monto_usd, Decimal('100.00'))
