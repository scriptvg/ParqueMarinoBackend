from django.contrib import admin
from .models import (
    ServiciosEducativos, ServiciosEducativosImage, ServiciosEducativosFacts,
    ServiciosEducativosDescription, ServiciosEducativosButtons,
    ProgramaEducativo, ProgramaItem,
    Instructor, Programa, Horario, Inscripcion
)

# Configuración para Servicios Educativos
@admin.register(ServiciosEducativos)
class ServiciosEducativosAdmin(admin.ModelAdmin):
    list_display = ('value', 'label', 'title')
    search_fields = ('value', 'label', 'title')

@admin.register(ServiciosEducativosImage)
class ServiciosEducativosImageAdmin(admin.ModelAdmin):
    list_display = ('servicios_educativos', 'image', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')

@admin.register(ServiciosEducativosFacts)
class ServiciosEducativosFactsAdmin(admin.ModelAdmin):
    list_display = ('servicios_educativos', 'fact')
    search_fields = ('fact',)

@admin.register(ServiciosEducativosDescription)
class ServiciosEducativosDescriptionAdmin(admin.ModelAdmin):
    list_display = ('servicios_educativos', 'description')
    search_fields = ('description',)

@admin.register(ServiciosEducativosButtons)
class ServiciosEducativosButtonsAdmin(admin.ModelAdmin):
    list_display = ('servicios_educativos', 'label', 'link')
    search_fields = ('label', 'link')

# Configuración para Programas Educativos
@admin.register(ProgramaEducativo)
class ProgramaEducativoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')

@admin.register(ProgramaItem)
class ProgramaItemAdmin(admin.ModelAdmin):
    list_display = ('programa', 'text')
    search_fields = ('text', 'programa__title')
    list_filter = ('programa',)

# Configuración para Instructor
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'especialidad', 'experiencia_years', 'activo')
    list_filter = ('activo', 'especialidad')
    search_fields = ('user__username', 'user__email', 'especialidad')
    list_editable = ('activo',)

# Configuración para Programa
@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'duracion_horas', 'capacidad_min', 'capacidad_max', 'precio', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
    list_editable = ('activo', 'precio')

# Configuración para Horario
@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('programa', 'instructor', 'fecha_inicio', 'fecha_fin', 'cupos_disponibles', 'estado')
    list_filter = ('estado', 'programa', 'instructor')
    search_fields = ('programa__nombre', 'instructor__user__username')
    list_editable = ('estado',)

# Configuración para Inscripcion
@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('horario', 'usuario', 'nombre_participante', 'edad_participante', 'fecha_inscripcion', 'estado_pago')
    list_filter = ('estado_pago', 'horario__programa')
    search_fields = ('usuario__username', 'nombre_participante')
    list_editable = ('estado_pago',)
