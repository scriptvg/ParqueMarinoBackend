"""Servicios para la gestión de pagos y conversión de divisas"""

from decimal import Decimal
from typing import Union, Tuple
from datetime import datetime
import requests
from django.conf import settings
from django.core.cache import cache

class CurrencyConverter:
    """Servicio para la conversión de divisas
    
    Este servicio maneja la conversión entre CRC y USD utilizando tasas de cambio
    actualizadas. Implementa un sistema de caché para evitar llamadas excesivas
    al servicio de tasas de cambio.
    
    Attributes:
        CACHE_KEY (str): Clave para almacenar la tasa en caché
        CACHE_TIMEOUT (int): Tiempo de expiración del caché en segundos (4 horas)
    """
    
    CACHE_KEY = 'exchange_rate_usd_crc'
    CACHE_TIMEOUT = 14400  # 4 horas en segundos
    
    @classmethod
    def get_exchange_rate(cls) -> Decimal:
        """Obtiene la tasa de cambio actual USD a CRC
        
        Primero intenta obtener la tasa del caché. Si no está disponible o expiró,
        realiza una llamada al servicio de tasas de cambio y actualiza el caché.
        
        Returns:
            Decimal: Tasa de cambio actual (1 USD = X CRC)
        """
        rate = cache.get(cls.CACHE_KEY)
        if rate is not None:
            return Decimal(str(rate))
        
        # Si no hay tasa en caché, obtener de la API
        try:
            response = requests.get(
                'https://api.exchangerate-api.com/v4/latest/USD',
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            rate = Decimal(str(data['rates']['CRC']))
            
            # Guardar en caché
            cache.set(cls.CACHE_KEY, str(rate), cls.CACHE_TIMEOUT)
            return rate
        except Exception:
            # En caso de error, usar una tasa por defecto
            return Decimal('540.00')
    
    @classmethod
    def convert_currency(
        cls,
        amount: Union[Decimal, float],
        from_currency: str,
        to_currency: str
    ) -> Decimal:
        """Convierte un monto entre CRC y USD
        
        Args:
            amount: Monto a convertir
            from_currency: Moneda origen ('CRC' o 'USD')
            to_currency: Moneda destino ('CRC' o 'USD')
            
        Returns:
            Decimal: Monto convertido
            
        Raises:
            ValueError: Si las monedas no son válidas
        """
        if from_currency not in ['CRC', 'USD'] or to_currency not in ['CRC', 'USD']:
            raise ValueError('Monedas deben ser CRC o USD')
            
        if from_currency == to_currency:
            return Decimal(str(amount))
            
        rate = cls.get_exchange_rate()
        amount = Decimal(str(amount))
        
        if from_currency == 'USD' and to_currency == 'CRC':
            return (amount * rate).quantize(Decimal('0.01'))
        else:  # CRC a USD
            return (amount / rate).quantize(Decimal('0.01'))
    
    @classmethod
    def get_both_currencies(cls, amount: Union[Decimal, float], currency: str) -> Tuple[Decimal, Decimal]:
        """Obtiene el monto en ambas monedas (CRC y USD)
        
        Args:
            amount: Monto original
            currency: Moneda del monto original ('CRC' o 'USD')
            
        Returns:
            Tuple[Decimal, Decimal]: (monto_crc, monto_usd)
        """
        amount = Decimal(str(amount))
        if currency == 'CRC':
            monto_crc = amount
            monto_usd = cls.convert_currency(amount, 'CRC', 'USD')
        else:  # USD
            monto_usd = amount
            monto_crc = cls.convert_currency(amount, 'USD', 'CRC')
            
        return monto_crc, monto_usd