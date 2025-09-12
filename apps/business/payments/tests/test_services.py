# tests/test_services.py

from unittest.mock import patch, MagicMock
from django.test import TestCase
from decimal import Decimal
from apps.business.payments.services import CurrencyConverter

class TestCurrencyConverter(TestCase):
    """Pruebas para el servicio de conversión de monedas
    
    Verifica el funcionamiento correcto de las conversiones entre CRC y USD,
    incluyendo el manejo de caché y errores de API.
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.converter = CurrencyConverter()
        self.mock_exchange_rate = 550.0  # Tipo de cambio de prueba

    @patch('payments.services.requests.get')
    def test_obtener_tipo_cambio(self, mock_get):
        """Prueba la obtención del tipo de cambio desde la API"""
        # Simula respuesta exitosa de la API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {'CRC': self.mock_exchange_rate}
        }
        mock_get.return_value = mock_response

        rate = self.converter.get_exchange_rate()
        self.assertEqual(rate, self.mock_exchange_rate)

    @patch('payments.services.requests.get')
    def test_manejo_error_api(self, mock_get):
        """Prueba el manejo de errores de la API"""
        # Simula error de la API
        mock_get.side_effect = Exception('API Error')

        # Debe usar el tipo de cambio por defecto
        rate = self.converter.get_exchange_rate()
        self.assertEqual(rate, self.converter.DEFAULT_RATE)

    def test_conversion_usd_a_crc(self):
        """Prueba la conversión de USD a CRC"""
        with patch.object(CurrencyConverter, 'get_exchange_rate') as mock_rate:
            mock_rate.return_value = self.mock_exchange_rate
            amount_usd = Decimal('100.00')
            amount_crc = self.converter.usd_to_crc(amount_usd)
            expected_crc = amount_usd * Decimal(str(self.mock_exchange_rate))
            self.assertEqual(amount_crc, expected_crc)

    def test_conversion_crc_a_usd(self):
        """Prueba la conversión de CRC a USD"""
        with patch.object(CurrencyConverter, 'get_exchange_rate') as mock_rate:
            mock_rate.return_value = self.mock_exchange_rate
            amount_crc = Decimal('55000.00')
            amount_usd = self.converter.crc_to_usd(amount_crc)
            expected_usd = amount_crc / Decimal(str(self.mock_exchange_rate))
            self.assertEqual(amount_usd, expected_usd)

    def test_obtener_ambas_monedas(self):
        """Prueba obtener un monto en ambas monedas"""
        with patch.object(CurrencyConverter, 'get_exchange_rate') as mock_rate:
            mock_rate.return_value = self.mock_exchange_rate
            amount = Decimal('100.00')
            moneda = 'USD'
            
            crc, usd = self.converter.get_both_currencies(amount, moneda)
            
            if moneda == 'USD':
                self.assertEqual(usd, amount)
                self.assertEqual(crc, amount * Decimal(str(self.mock_exchange_rate)))
            else:
                self.assertEqual(crc, amount)
                self.assertEqual(usd, amount / Decimal(str(self.mock_exchange_rate)))

    @patch('payments.services.requests.get')
    def test_cache_tipo_cambio(self, mock_get):
        """Prueba el funcionamiento del caché del tipo de cambio"""
        # Primera llamada
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {'CRC': self.mock_exchange_rate}
        }
        mock_get.return_value = mock_response

        rate1 = self.converter.get_exchange_rate()
        # Segunda llamada (debería usar caché)
        rate2 = self.converter.get_exchange_rate()

        # Verifica que la API solo se llamó una vez
        mock_get.assert_called_once()
        self.assertEqual(rate1, rate2)

    def test_redondeo_conversion(self):
        """Prueba el redondeo correcto en las conversiones"""
        with patch.object(CurrencyConverter, 'get_exchange_rate') as mock_rate:
            mock_rate.return_value = 550.33  # Tipo de cambio con decimales
            
            # Prueba USD a CRC
            amount_usd = Decimal('100.45')
            amount_crc = self.converter.usd_to_crc(amount_usd)
            self.assertEqual(amount_crc.as_tuple().exponent, -2)  # Verifica 2 decimales
            
            # Prueba CRC a USD
            amount_crc = Decimal('55033.00')
            amount_usd = self.converter.crc_to_usd(amount_crc)
            self.assertEqual(amount_usd.as_tuple().exponent, -2)  # Verifica 2 decimales

    def test_validacion_montos_negativos(self):
        """Prueba el manejo de montos negativos"""
        with patch.object(CurrencyConverter, 'get_exchange_rate') as mock_rate:
            mock_rate.return_value = self.mock_exchange_rate
            
            with self.assertRaises(ValueError):
                self.converter.usd_to_crc(Decimal('-100.00'))
            
            with self.assertRaises(ValueError):
                self.converter.crc_to_usd(Decimal('-55000.00'))