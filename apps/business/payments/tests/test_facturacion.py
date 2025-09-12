# tests/test_facturacion.py

from unittest.mock import patch, MagicMock
from django.test import TestCase
from decimal import Decimal
from apps.integrations.payments.facturacion_electronica import FacturacionElectronica, FacturacionError

class TestFacturacionElectronica(TestCase):
    """Pruebas para el servicio de facturación electrónica
    
    Verifica la generación, firma y envío de facturas electrónicas al
    Ministerio de Hacienda de Costa Rica.
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.facturacion = FacturacionElectronica(
            wsdl_url='https://api.hacienda.go.cr/fe/ae',
            cert_path='/path/to/cert.p12',
            pin='1234'
        )
        
        self.factura_data = {
            'receptor': {
                'nombre': 'Juan Pérez',
                'identificacion': '123456789',
                'tipo_identificacion': '01',  # Cédula física
                'email': 'juan@example.com',
                'telefono': '88888888'
            },
            'detalle': [
                {
                    'codigo': '001',
                    'descripcion': 'Curso de Programación',
                    'cantidad': 1,
                    'precio_unitario': Decimal('500.00'),
                    'impuesto': Decimal('0.00'),
                    'subtotal': Decimal('500.00'),
                    'total': Decimal('500.00')
                }
            ],
            'moneda': 'USD',
            'tipo_documento': '01',  # Factura Electrónica
            'condicion_venta': '01',  # Contado
            'medio_pago': '04'  # Tarjeta
        }

    @patch('payments.integrations.facturacion_electronica.zeep.Client')
    def test_generar_xml_factura(self, mock_client):
        """Prueba la generación del XML de la factura"""
        xml = self.facturacion.generar_xml_factura(self.factura_data)
        
        # Verifica estructura básica del XML
        self.assertIn('FacturaElectronica', xml)
        self.assertIn('Receptor', xml)
        self.assertIn('DetalleServicio', xml)

    @patch('payments.integrations.facturacion_electronica.xmlsec')
    def test_firmar_xml(self, mock_xmlsec):
        """Prueba la firma digital del XML"""
        xml = self.facturacion.generar_xml_factura(self.factura_data)
        xml_firmado = self.facturacion.firmar_xml(xml)
        
        # Verifica que el XML contiene la firma
        self.assertIn('ds:Signature', xml_firmado)
        self.assertIn('SignedInfo', xml_firmado)

    @patch('payments.integrations.facturacion_electronica.zeep.Client')
    def test_enviar_factura(self, mock_client):
        """Prueba el envío de la factura al Ministerio de Hacienda"""
        # Simula respuesta exitosa del servicio
        mock_response = MagicMock()
        mock_response.estado = 'aceptado'
        mock_response.clave = '50601234567890'
        mock_client.return_value.service.enviarFactura.return_value = mock_response

        response = self.facturacion.enviar_factura(self.factura_data)
        
        self.assertEqual(response['estado'], 'aceptado')
        self.assertEqual(response['clave'], '50601234567890')

    @patch('payments.integrations.facturacion_electronica.zeep.Client')
    def test_manejo_error_envio(self, mock_client):
        """Prueba el manejo de errores al enviar la factura"""
        # Simula error del servicio
        mock_client.return_value.service.enviarFactura.side_effect = Exception('Error de conexión')

        with self.assertRaises(FacturacionError):
            self.facturacion.enviar_factura(self.factura_data)

    @patch('payments.integrations.facturacion_electronica.zeep.Client')
    def test_consultar_estado_factura(self, mock_client):
        """Prueba la consulta del estado de una factura"""
        # Simula respuesta de consulta
        mock_response = MagicMock()
        mock_response.estado = 'aceptado'
        mock_client.return_value.service.consultarFactura.return_value = mock_response

        estado = self.facturacion.consultar_estado('50601234567890')
        self.assertEqual(estado, 'aceptado')

    def test_validacion_datos_factura(self):
        """Prueba las validaciones de datos de la factura"""
        # Prueba datos inválidos
        datos_invalidos = self.factura_data.copy()
        datos_invalidos['receptor']['identificacion'] = '123'  # Identificación muy corta

        with self.assertRaises(FacturacionError):
            self.facturacion.validar_datos_factura(datos_invalidos)

    def test_calculo_totales(self):
        """Prueba el cálculo de totales de la factura"""
        totales = self.facturacion.calcular_totales(self.factura_data['detalle'])
        
        self.assertEqual(totales['subtotal'], Decimal('500.00'))
        self.assertEqual(totales['total_impuestos'], Decimal('0.00'))
        self.assertEqual(totales['total'], Decimal('500.00'))

    @patch('payments.integrations.facturacion_electronica.zeep.Client')
    def test_generar_nota_credito(self, mock_client):
        """Prueba la generación de notas de crédito"""
        datos_nota = {
            'factura_referencia': '50601234567890',
            'motivo': 'Devolución de dinero',
            'monto': Decimal('500.00')
        }
        
        xml = self.facturacion.generar_xml_nota_credito(datos_nota)
        
        # Verifica estructura básica del XML
        self.assertIn('NotaCreditoElectronica', xml)
        self.assertIn('InformacionReferencia', xml)

    def test_validacion_certificado(self):
        """Prueba la validación del certificado digital"""
        with patch('builtins.open', create=True) as mock_open:
            mock_open.side_effect = FileNotFoundError
            
            with self.assertRaises(FacturacionError):
                FacturacionElectronica(
                    wsdl_url='https://api.hacienda.go.cr/fe/ae',
                    cert_path='/path/invalido/cert.p12',
                    pin='1234'
                )