# tests/test_reports.py

from datetime import datetime, timedelta
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from apps.business.payments.models import Pago, PagoInscripcion, Donacion
from apps.business.payments.reports import VentasReporter

class TestVentasReporter(TestCase):
    """Pruebas para el generador de reportes de ventas
    
    Verifica la generación de reportes de ventas, incluyendo
    resúmenes diarios, mensuales y análisis de tendencias.
    """

    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.reporter = VentasReporter()
        
        # Crear pagos de prueba
        self.fecha_base = timezone.now()
        
        # Pagos generales
        Pago.objects.create(
            monto=Decimal('100.00'),
            moneda='USD',
            estado='completado',
            metodo_pago='tarjeta',
            fecha_creacion=self.fecha_base,
            referencia='PAY001'
        )
        
        Pago.objects.create(
            monto=Decimal('150.00'),
            moneda='USD',
            estado='completado',
            metodo_pago='paypal',
            fecha_creacion=self.fecha_base - timedelta(days=1),
            referencia='PAY002'
        )
        
        # Pagos de inscripción
        PagoInscripcion.objects.create(
            monto=Decimal('200.00'),
            moneda='USD',
            estado='completado',
            metodo_pago='tarjeta',
            fecha_creacion=self.fecha_base,
            referencia='INS001',
            estudiante_id=1
        )
        
        # Donaciones
        Donacion.objects.create(
            monto=Decimal('50.00'),
            moneda='USD',
            estado='completado',
            metodo_pago='transferencia',
            fecha_creacion=self.fecha_base,
            referencia='DON001',
            donante_email='donante@test.com'
        )

    def test_reporte_diario(self):
        """Prueba la generación del reporte diario de ventas"""
        reporte = self.reporter.generar_reporte_diario(self.fecha_base.date())
        
        self.assertEqual(reporte['total_ventas'], Decimal('350.00'))
        self.assertEqual(reporte['total_transacciones'], 3)
        self.assertEqual(reporte['promedio_venta'], Decimal('116.67'))
        
        # Verificar desglose por tipo
        self.assertEqual(reporte['desglose']['pagos'], Decimal('100.00'))
        self.assertEqual(reporte['desglose']['inscripciones'], Decimal('200.00'))
        self.assertEqual(reporte['desglose']['donaciones'], Decimal('50.00'))

    def test_reporte_mensual(self):
        """Prueba la generación del reporte mensual"""
        reporte = self.reporter.generar_reporte_mensual(
            self.fecha_base.year,
            self.fecha_base.month
        )
        
        self.assertEqual(reporte['total_ventas'], Decimal('500.00'))
        self.assertEqual(reporte['total_transacciones'], 4)
        
        # Verificar tendencias diarias
        self.assertIn('tendencia_diaria', reporte)
        self.assertEqual(len(reporte['tendencia_diaria']), 2)

    def test_reporte_por_metodo_pago(self):
        """Prueba el análisis por método de pago"""
        reporte = self.reporter.analizar_metodos_pago(
            self.fecha_base.date(),
            self.fecha_base.date()
        )
        
        self.assertEqual(reporte['tarjeta']['total'], Decimal('300.00'))
        self.assertEqual(reporte['paypal']['total'], Decimal('150.00'))
        self.assertEqual(reporte['transferencia']['total'], Decimal('50.00'))

    def test_reporte_conversion_moneda(self):
        """Prueba la conversión de monedas en reportes"""
        # Crear pago en otra moneda
        Pago.objects.create(
            monto=Decimal('50000.00'),
            moneda='CRC',
            estado='completado',
            metodo_pago='tarjeta',
            fecha_creacion=self.fecha_base,
            referencia='PAY003'
        )
        
        reporte = self.reporter.generar_reporte_diario(
            self.fecha_base.date(),
            moneda_base='USD'
        )
        
        # Asumiendo tasa de conversión aproximada
        self.assertGreater(reporte['total_ventas'], Decimal('350.00'))

    def test_reporte_tendencias(self):
        """Prueba el análisis de tendencias"""
        tendencias = self.reporter.analizar_tendencias(
            fecha_inicio=self.fecha_base - timedelta(days=30),
            fecha_fin=self.fecha_base
        )
        
        self.assertIn('crecimiento_mensual', tendencias)
        self.assertIn('dia_mas_ventas', tendencias)
        self.assertIn('metodo_pago_preferido', tendencias)

    def test_reporte_estadisticas(self):
        """Prueba el cálculo de estadísticas avanzadas"""
        stats = self.reporter.calcular_estadisticas(
            fecha_inicio=self.fecha_base - timedelta(days=7),
            fecha_fin=self.fecha_base
        )
        
        self.assertIn('promedio_diario', stats)
        self.assertIn('desviacion_estandar', stats)
        self.assertIn('mediana', stats)

    def test_reporte_vacio(self):
        """Prueba la generación de reportes sin datos"""
        fecha_futura = self.fecha_base + timedelta(days=30)
        reporte = self.reporter.generar_reporte_diario(fecha_futura.date())
        
        self.assertEqual(reporte['total_ventas'], Decimal('0'))
        self.assertEqual(reporte['total_transacciones'], 0)

    def test_reporte_comparativo(self):
        """Prueba la generación de reportes comparativos"""
        comparacion = self.reporter.generar_comparativo(
            fecha_inicio=self.fecha_base - timedelta(days=30),
            fecha_fin=self.fecha_base,
            periodo_anterior=30
        )
        
        self.assertIn('variacion_porcentual', comparacion)
        self.assertIn('tendencia', comparacion)

    def test_filtros_reporte(self):
        """Prueba los filtros en la generación de reportes"""
        reporte = self.reporter.generar_reporte_diario(
            self.fecha_base.date(),
            metodo_pago='tarjeta',
            tipo_transaccion='inscripcion'
        )
        
        self.assertEqual(reporte['total_ventas'], Decimal('200.00'))
        self.assertEqual(reporte['total_transacciones'], 1)