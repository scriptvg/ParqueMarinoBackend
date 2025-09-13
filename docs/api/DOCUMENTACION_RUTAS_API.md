# Parque Marino Backend - Documentación de Rutas de la API

Este documento proporciona una descripción general completa de todos los puntos finales de la API disponibles en el sistema Parque Marino Backend, organizados por módulo.

## Versionado de la API

Todos los puntos finales son accesibles bajo dos rutas base:
- `/api/v1/` - Versión 1 explícita
- `/api/` - Por defecto a la versión 1 (compatibilidad hacia atrás)

## Autenticación

La mayoría de los puntos finales requieren autenticación mediante tokens JWT. Incluya el token en el encabezado de Autorización:
```
Authorization: Bearer <token>
```

## Rutas Principales de la API

### Puntos finales de Autenticación
- `POST /api/auth/token/` - Obtener token JWT
- `POST /api/auth/token/refresh/` - Refrescar token JWT
- `POST /api/auth/login/` - Inicio de sesión de usuario
- `POST /api/auth/logout/` - Cierre de sesión de usuario
- `POST /api/auth/register/` - Registro de usuario
- `POST /api/auth/forgot-password/` - Solicitar restablecimiento de contraseña
- `POST /api/auth/reset-password-confirm/` - Confirmar restablecimiento de contraseña

### Puntos finales de Mensajería
- `POST /api/messaging/send-otp/` - Enviar mensaje OTP
- `POST /api/messaging/verify-otp/` - Verificar código OTP
- `GET /api/messaging/test-twilio/` - Probar integración de Twilio

## Módulos de Negocio

### Módulo de Vida Silvestre

#### Animales
- `GET /api/wildlife/animals/` - Listar todos los animales
- `POST /api/wildlife/animals/create/` - Crear nuevo animal
- `GET /api/wildlife/animals/{id}/` - Obtener detalles del animal
- `PUT/PATCH /api/wildlife/animals/{id}/update/` - Actualizar animal
- `DELETE /api/wildlife/animals/{id}/delete/` - Eliminar animal

#### Especies
- `GET /api/wildlife/species/` - Listar todas las especies
- `POST /api/wildlife/species/create/` - Crear nueva especie
- `GET /api/wildlife/species/{id}/` - Obtener detalles de la especie
- `PUT/PATCH /api/wildlife/species/{id}/update/` - Actualizar especie
- `DELETE /api/wildlife/species/{id}/delete/` - Eliminar especie

#### Estado de Conservación
- `GET /api/wildlife/conservation-status/` - Listar todos los estados de conservación
- `POST /api/wildlife/conservation-status/create/` - Crear nuevo estado de conservación
- `GET /api/wildlife/conservation-status/{id}/` - Obtener detalles del estado de conservación
- `PUT/PATCH /api/wildlife/conservation-status/{id}/update/` - Actualizar estado de conservación
- `DELETE /api/wildlife/conservation-status/{id}/delete/` - Eliminar estado de conservación

#### Hábitats
- `GET /api/wildlife/habitats/` - Listar todos los hábitats
- `POST /api/wildlife/habitats/create/` - Crear nuevo hábitat
- `GET /api/wildlife/habitats/{id}/` - Obtener detalles del hábitat
- `PUT/PATCH /api/wildlife/habitats/{id}/update/` - Actualizar hábitat
- `DELETE /api/wildlife/habitats/{id}/delete/` - Eliminar hábitat

### Módulo de Exhibiciones

#### Exhibiciones
- `GET /api/exhibitions/exhibiciones/` - Listar todas las exhibiciones
- `POST /api/exhibitions/exhibiciones/create/` - Crear nueva exhibición
- `GET /api/exhibitions/exhibiciones/{id}/` - Obtener detalles de la exhibición
- `GET /api/exhibitions/exhibiciones/{id}/full_details/` - Obtener detalles completos de la exhibición
- `PUT/PATCH /api/exhibitions/exhibiciones/{id}/update/` - Actualizar exhibición
- `DELETE /api/exhibitions/exhibiciones/{id}/delete/` - Eliminar exhibición

#### Imágenes de Exhibiciones
- `GET /api/exhibitions/exhibicion-images/` - Listar todas las imágenes de exhibiciones
- `POST /api/exhibitions/exhibicion-images/create/` - Crear nueva imagen de exhibición
- `GET /api/exhibitions/exhibicion-images/{id}/` - Obtener detalles de la imagen de exhibición
- `PUT/PATCH /api/exhibitions/exhibicion-images/{id}/update/` - Actualizar imagen de exhibición
- `DELETE /api/exhibitions/exhibicion-images/{id}/delete/` - Eliminar imagen de exhibición

#### Descripciones de Exhibiciones
- `GET /api/exhibitions/exhibicion-descriptions/` - Listar todas las descripciones de exhibiciones
- `POST /api/exhibitions/exhibicion-descriptions/create/` - Crear nueva descripción de exhibición
- `GET /api/exhibitions/exhibicion-descriptions/{id}/` - Obtener detalles de la descripción de exhibición
- `PUT/PATCH /api/exhibitions/exhibicion-descriptions/{id}/update/` - Actualizar descripción de exhibición
- `DELETE /api/exhibitions/exhibicion-descriptions/{id}/delete/` - Eliminar descripción de exhibición

#### Hechos de Exhibiciones
- `GET /api/exhibitions/exhibicion-facts/` - Listar todos los hechos de exhibiciones
- `POST /api/exhibitions/exhibicion-facts/create/` - Crear nuevo hecho de exhibición
- `GET /api/exhibitions/exhibicion-facts/{id}/` - Obtener detalles del hecho de exhibición
- `PUT/PATCH /api/exhibitions/exhibicion-facts/{id}/update/` - Actualizar hecho de exhibición
- `DELETE /api/exhibitions/exhibicion-facts/{id}/delete/` - Eliminar hecho de exhibición

#### Botones de Exhibiciones
- `GET /api/exhibitions/exhibicion-buttons/` - Listar todos los botones de exhibiciones
- `POST /api/exhibitions/exhibicion-buttons/create/` - Crear nuevo botón de exhibición
- `GET /api/exhibitions/exhibicion-buttons/{id}/` - Obtener detalles del botón de exhibición
- `PUT/PATCH /api/exhibitions/exhibicion-buttons/{id}/update/` - Actualizar botón de exhibición
- `DELETE /api/exhibitions/exhibicion-buttons/{id}/delete/` - Eliminar botón de exhibición

### Módulo de Educación

#### Programas Educativos
- `GET /api/education/programas-educativos/` - Listar todos los programas educativos
- `POST /api/education/programas-educativos/create/` - Crear nuevo programa educativo
- `GET /api/education/programas-educativos/{id}/` - Obtener detalles del programa educativo
- `PUT/PATCH /api/education/programas-educativos/{id}/update/` - Actualizar programa educativo
- `DELETE /api/education/programas-educativos/{id}/delete/` - Eliminar programa educativo

#### Servicios Educativos
- `GET /api/education/servicios-educativos/` - Listar todos los servicios educativos
- `POST /api/education/servicios-educativos/create/` - Crear nuevo servicio educativo
- `GET /api/education/servicios-educativos/{id}/` - Obtener detalles del servicio educativo
- `PUT/PATCH /api/education/servicios-educativos/{id}/update/` - Actualizar servicio educativo
- `DELETE /api/education/servicios-educativos/{id}/delete/` - Eliminar servicio educativo

#### Imágenes de Servicios Educativos
- `GET /api/education/servicios-educativos-images/` - Listar todas las imágenes de servicios educativos
- `POST /api/education/servicios-educativos-images/create/` - Crear nueva imagen de servicio educativo
- `GET /api/education/servicios-educativos-images/{id}/` - Obtener detalles de la imagen de servicio educativo
- `PUT/PATCH /api/education/servicios-educativos-images/{id}/update/` - Actualizar imagen de servicio educativo
- `DELETE /api/education/servicios-educativos-images/{id}/delete/` - Eliminar imagen de servicio educativo

#### Descripciones de Servicios Educativos
- `GET /api/education/servicios-educativos-descriptions/` - Listar todas las descripciones de servicios educativos
- `POST /api/education/servicios-educativos-descriptions/create/` - Crear nueva descripción de servicio educativo
- `GET /api/education/servicios-educativos-descriptions/{id}/` - Obtener detalles de la descripción de servicio educativo
- `PUT/PATCH /api/education/servicios-educativos-descriptions/{id}/update/` - Actualizar descripción de servicio educativo
- `DELETE /api/education/servicios-educativos-descriptions/{id}/delete/` - Eliminar descripción de servicio educativo

#### Hechos de Servicios Educativos
- `GET /api/education/servicios-educativos-facts/` - Listar todos los hechos de servicios educativos
- `POST /api/education/servicios-educativos-facts/create/` - Crear nuevo hecho de servicio educativo
- `GET /api/education/servicios-educativos-facts/{id}/` - Obtener detalles del hecho de servicio educativo
- `PUT/PATCH /api/education/servicios-educativos-facts/{id}/update/` - Actualizar hecho de servicio educativo
- `DELETE /api/education/servicios-educativos-facts/{id}/delete/` - Eliminar hecho de servicio educativo

#### Botones de Servicios Educativos
- `GET /api/education/servicios-educativos-buttons/` - Listar todos los botones de servicios educativos
- `POST /api/education/servicios-educativos-buttons/create/` - Crear nuevo botón de servicio educativo
- `GET /api/education/servicios-educativos-buttons/{id}/` - Obtener detalles del botón de servicio educativo
- `PUT/PATCH /api/education/servicios-educativos-buttons/{id}/update/` - Actualizar botón de servicio educativo
- `DELETE /api/education/servicios-educativos-buttons/{id}/delete/` - Eliminar botón de servicio educativo

#### Instructores
- `GET /api/education/instructores/` - Listar todos los instructores
- `POST /api/education/instructores/create/` - Crear nuevo instructor
- `GET /api/education/instructores/{id}/` - Obtener detalles del instructor
- `PUT/PATCH /api/education/instructores/{id}/update/` - Actualizar instructor
- `DELETE /api/education/instructores/{id}/delete/` - Eliminar instructor

#### Horarios
- `GET /api/education/horarios/` - Listar todos los horarios
- `POST /api/education/horarios/create/` - Crear nuevo horario
- `GET /api/education/horarios/{id}/` - Obtener detalles del horario
- `PUT/PATCH /api/education/horarios/{id}/update/` - Actualizar horario
- `DELETE /api/education/horarios/{id}/delete/` - Eliminar horario

#### Inscripciones
- `GET /api/education/inscripciones/` - Listar todas las inscripciones
- `POST /api/education/inscripciones/create/` - Crear nueva inscripción
- `GET /api/education/inscripciones/{id}/` - Obtener detalles de la inscripción
- `PUT/PATCH /api/education/inscripciones/{id}/update/` - Actualizar inscripción
- `DELETE /api/education/inscripciones/{id}/delete/` - Eliminar inscripción

#### Elementos de Programa
- `GET /api/education/programa-items/` - Listar todos los elementos de programa
- `POST /api/education/programa-items/create/` - Crear nuevo elemento de programa
- `GET /api/education/programa-items/{id}/` - Obtener detalles del elemento de programa
- `PUT/PATCH /api/education/programa-items/{id}/update/` - Actualizar elemento de programa
- `DELETE /api/education/programa-items/{id}/delete/` - Eliminar elemento de programa

### Módulo de Pagos

#### Pagos
- `GET /api/payments/pagos/` - Listar todos los pagos
- `POST /api/payments/pagos/create/` - Crear nuevo pago
- `GET /api/payments/pagos/{id}/` - Obtener detalles del pago
- `POST /api/payments/pagos/{id}/procesar_pago/` - Procesar pago con Stripe
- `PUT/PATCH /api/payments/pagos/{id}/update/` - Actualizar pago
- `DELETE /api/payments/pagos/{id}/delete/` - Eliminar pago

#### Pagos de Inscripción
- `GET /api/payments/pagos-inscripcion/` - Listar todos los pagos de inscripción
- `POST /api/payments/pagos-inscripcion/create/` - Crear nuevo pago de inscripción
- `GET /api/payments/pagos-inscripcion/{id}/` - Obtener detalles del pago de inscripción
- `POST /api/payments/pagos-inscripcion/{id}/procesar_pago_inscripcion/` - Procesar pago de inscripción
- `PUT/PATCH /api/payments/pagos-inscripcion/{id}/update/` - Actualizar pago de inscripción
- `DELETE /api/payments/pagos-inscripcion/{id}/delete/` - Eliminar pago de inscripción

#### Donaciones
- `GET /api/payments/donaciones/` - Listar todas las donaciones
- `POST /api/payments/donaciones/create/` - Crear nueva donación
- `GET /api/payments/donaciones/{id}/` - Obtener detalles de la donación
- `POST /api/payments/donaciones/{id}/procesar_donacion/` - Procesar donación con Stripe
- `PUT/PATCH /api/payments/donaciones/{id}/update/` - Actualizar donación
- `DELETE /api/payments/donaciones/{id}/delete/` - Eliminar donación

#### Pagos de Administración
- `GET /api/payments/admin-pagos/` - Listar todos los pagos de administración
- `POST /api/payments/admin-pagos/create/` - Crear nuevo pago de administración
- `GET /api/payments/admin-pagos/{id}/` - Obtener detalles del pago de administración
- `POST /api/payments/admin-pagos/{id}/procesar_pago_admin/` - Procesar pago de administración
- `PUT/PATCH /api/payments/admin-pagos/{id}/update/` - Actualizar pago de administración
- `DELETE /api/payments/admin-pagos/{id}/delete/` - Eliminar pago de administración

#### Pagos de Inscripción de Administración
- `GET /api/payments/admin-pagos-inscripcion/` - Listar todos los pagos de inscripción de administración
- `POST /api/payments/admin-pagos-inscripcion/create/` - Crear nuevo pago de inscripción de administración
- `GET /api/payments/admin-pagos-inscripcion/{id}/` - Obtener detalles del pago de inscripción de administración
- `POST /api/payments/admin-pagos-inscripcion/{id}/procesar_pago_inscripcion_admin/` - Procesar pago de inscripción de administración
- `PUT/PATCH /api/payments/admin-pagos-inscripcion/{id}/update/` - Actualizar pago de inscripción de administración
- `DELETE /api/payments/admin-pagos-inscripcion/{id}/delete/` - Eliminar pago de inscripción de administración

#### Donaciones de Administración
- `GET /api/payments/admin-donaciones/` - Listar todas las donaciones de administración
- `POST /api/payments/admin-donaciones/create/` - Crear nueva donación de administración
- `GET /api/payments/admin-donaciones/{id}/` - Obtener detalles de la donación de administración
- `POST /api/payments/admin-donaciones/{id}/procesar_donacion_admin/` - Procesar donación de administración
- `PUT/PATCH /api/payments/admin-donaciones/{id}/update/` - Actualizar donación de administración
- `DELETE /api/payments/admin-donaciones/{id}/delete/` - Eliminar donación de administración

### Módulo de Tickets

#### Tickets
- `GET /api/tickets/tickets/` - Listar todos los tickets
- `POST /api/tickets/tickets/create/` - Crear nuevo ticket
- `GET /api/tickets/tickets/{id}/` - Obtener detalles del ticket
- `POST /api/tickets/tickets/{id}/check_availability/` - Verificar disponibilidad del ticket
- `PUT/PATCH /api/tickets/tickets/{id}/update/` - Actualizar ticket
- `DELETE /api/tickets/tickets/{id}/delete/` - Eliminar ticket

#### Visitas
- `GET /api/tickets/visits/` - Listar todas las visitas
- `POST /api/tickets/visits/create/` - Crear nueva visita
- `GET /api/tickets/visits/{id}/` - Obtener detalles de la visita
- `PUT/PATCH /api/tickets/visits/{id}/update/` - Actualizar visita
- `DELETE /api/tickets/visits/{id}/delete/` - Eliminar visita

### Módulo de Infraestructura

#### Secciones
- `GET /api/infrastructure/sections/` - Listar todas las secciones
- `POST /api/infrastructure/sections/create/` - Crear nueva sección
- `GET /api/infrastructure/sections/{id}/` - Obtener detalles de la sección
- `PUT/PATCH /api/infrastructure/sections/{id}/update/` - Actualizar sección
- `DELETE /api/infrastructure/sections/{id}/delete/` - Eliminar sección

#### Hábitats de Infraestructura
- `GET /api/infrastructure/habitats/` - Listar todos los hábitats de infraestructura
- `POST /api/infrastructure/habitats/create/` - Crear nuevo hábitat de infraestructura
- `GET /api/infrastructure/habitats/{id}/` - Obtener detalles del hábitat de infraestructura
- `PUT/PATCH /api/infrastructure/habitats/{id}/update/` - Actualizar hábitat de infraestructura
- `DELETE /api/infrastructure/habitats/{id}/delete/` - Eliminar hábitat de infraestructura

### Módulo de Documentos

#### Documentos
- `GET /api/documents/documentos/` - Listar todos los documentos
- `POST /api/documents/documentos/create/` - Crear nuevo documento
- `GET /api/documents/documentos/{id}/` - Obtener detalles del documento
- `PUT/PATCH /api/documents/documentos/{id}/update/` - Actualizar documento
- `DELETE /api/documents/documentos/{id}/delete/` - Eliminar documento

#### Historial de Documentos
- `GET /api/documents/historial-documentos/` - Listar todos los registros del historial de documentos
- `GET /api/documents/historial-documentos/{id}/` - Obtener detalles del registro del historial de documentos

### Módulos de Soporte

#### Auditoría
- `GET /api/audit/audit-logs/` - Listar todos los registros de auditoría
- `GET /api/audit/audit-logs/{id}/` - Obtener detalles del registro de auditoría

#### Seguridad

##### Usuarios
- `GET /api/auth/users/` - Listar todos los usuarios
- `POST /api/auth/users/create/` - Crear nuevo usuario
- `GET /api/auth/users/{id}/` - Obtener detalles del usuario
- `PUT/PATCH /api/auth/users/{id}/update/` - Actualizar usuario
- `DELETE /api/auth/users/{id}/delete/` - Eliminar usuario

##### Perfiles de Usuario
- `GET /api/auth/user-profiles/` - Listar todos los perfiles de usuario
- `POST /api/auth/user-profiles/create/` - Crear nuevo perfil de usuario
- `GET /api/auth/user-profiles/{id}/` - Obtener detalles del perfil de usuario
- `PUT/PATCH /api/auth/user-profiles/{id}/update/` - Actualizar perfil de usuario
- `DELETE /api/auth/user-profiles/{id}/delete/` - Eliminar perfil de usuario

##### Roles
- `GET /api/auth/roles/` - Listar todos los roles
- `GET /api/auth/roles/{id}/` - Obtener detalles del rol

##### Permisos
- `GET /api/auth/permissions/` - Listar todos los permisos
- `GET /api/auth/permissions/{id}/` - Obtener detalles del permiso

## Formato de Respuesta

Todas las respuestas de la API siguen un formato JSON consistente:

```json
{
  "status": "success|error",
  "data": {...},
  "message": "Descripción de la respuesta"
}
```

## Manejo de Errores

Los errores se devuelven con códigos de estado HTTP apropiados y una respuesta JSON que contiene detalles del error:

```json
{
  "status": "error",
  "error": "Código de error",
  "message": "Mensaje de error legible por humanos"
}
```

## Limitación de Tasa

La API implementa limitación de tasa para prevenir abusos. Exceder el límite resultará en una respuesta 429 (Demasiadas Solicitudes).