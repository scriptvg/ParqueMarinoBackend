from django.contrib import admin
from .models import Pago, PagoInscripcion, Donacion

# Configuración del administrador para el modelo Pago
@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'referencia_transaccion', 'monto', 'fecha_pago', 'estado')
    list_filter = ('estado', 'fecha_pago', 'metodo_pago')
    search_fields = ('referencia_transaccion', 'notas')
    ordering = ('-fecha_pago',)

# Configuración del administrador para el modelo PagoInscripcion
@admin.register(PagoInscripcion)
class PagoInscripcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'referencia_transaccion', 'monto', 'fecha_pago', 'estado', 'inscripcion')
    list_filter = ('estado', 'fecha_pago', 'metodo_pago')
    search_fields = ('referencia_transaccion', 'inscripcion__id')
    ordering = ('-fecha_pago',)

# Configuración del administrador para el modelo Donacion
@admin.register(Donacion)
class DonacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_donante', 'monto', 'fecha_creacion', 'estado')
    list_filter = ('estado', 'metodo_pago')
    search_fields = ('nombre_donante', 'email_donante', 'referencia_transaccion')
    ordering = ('-id',)
