# QUANTUX SALUD • HEALTHDESK
## DOC-MAN-005: MANUAL DE USUARIO Y GUÍA OPERATIVA FÁCIL

---

**Código Documental:** DOC-MAN-005  
**Versión:** 3.0 (Edición Amigable para Usuarios y Equipos de Salud)  
**Fecha de Publicación:** Agosto 2026  
**Líder Funcional / Solution Owner:** Freddy Cortés  
**Facilitador Técnico:** Diego Martínez  
**Comité Evaluador:** Paula Sbarbati (Calidad Asistencial), Diego Martínez (Arquitectura Técnica), Carolina Brizuela (Operaciones Hospitalarias), Nicolás Sánchez (Seguridad y Gobernanza)  
**Estado:** VIGENTE / DISTRIBUCIÓN GENERAL  

---

## 1. BIENVENIDA Y CONCEPTOS BÁSICOS

Bienvenido a **HealthDesk Quantux**, la mesa de ayuda unificada diseñada para hacer simple, ágil y transparente la atención de requerimientos e incidencias tecnológicas en tu institución de salud.

Esta plataforma es utilizada por profesionales y personal de múltiples áreas: **asistencia a pacientes, enfermería, administración, secretaría, farmacia, laboratorio, diagnóstico por imágenes, facturación y dirección**.

### 💡 ¿Para qué sirve este sistema?
* **Pedir asistencia técnica en menos de 1 minuto** ante cualquier inconveniente en tus sistemas habituales (Receta Digital, Telemedicina, Portal de Pacientes, Historia Clínica, Turnos, Laboratorio, etc.).
* **Conocer en todo momento quién está trabajando en tu solicitud** y el tiempo estimado de respuesta.
* **Tener la última palabra:** El equipo técnico soluciona el inconveniente, pero **tú confirmas que todo funciona correctamente** en tu puesto de trabajo antes del cierre definitivo.

---

### 👥 ¿Quiénes usan el sistema y qué puede hacer cada rol?

Para asegurar una operación libre de saturación y fatiga, cada rol tiene una interfaz adaptada a su función directa:

| Perfil de Usuario | ¿Quiénes son? | ¿Qué pueden hacer en el sistema? |
| :--- | :--- | :--- |
| **👤 Usuario Solicitante** | Personal operativo, administrativo, profesionales o jefaturas de las instituciones cliente. | • Crear nuevas solicitudes en menos de 30 segundos.<br>• Ver y dar seguimiento a sus solicitudes abiertas.<br>• Responder mensajes del equipo de soporte.<br>• **Confirmar la solución y cerrar el ticket con calificación CSAT (1-5★ y Kudos).** |
| **🎧 Analista de Soporte (N1/N2/N3)** | Operadores y especialistas técnicos de la mesa de ayuda. | • Atender la bandeja general con filtros rápidos y vista Zen.<br>• Diagnosticar con notas privadas (🔒) y escalar a especialistas.<br>• Aplicar y documentar la solución técnica.<br>• **Marcar el ticket como RESUELTO.** |
| **🎯 Líder de Equipo (Team Leader)** | Supervisores de turno y coordinadores operativos de soporte. | • **Torre de Control en vivo:** monitorear colas y balance de carga de analistas.<br>• **Rebalanceo de tickets:** reasignar casos entre operadores con 1 clic.<br>• **Mesa de Rescate al Cliente:** intervenir de inmediato ante notas bajas (1 o 2 estrellas).<br>• Monitorear incidentes críticos P1 y tiempos de SLA. |
| **👑 Administrador (Admin)** | Responsables de sistemas, gobierno y plataforma. | • Gestión de altas, bajas y permisos de usuarios y roles.<br>• Configuración del catálogo de Instituciones y Plataformas.<br>• Despliegue de Releases de Software a Producción (resolución en cascada).<br>• Pistas de auditoría forense inmutables y exportación de reportes. |

---

## 2. GUÍA RÁPIDA: CÓMO USAR LA PANTALLA PRINCIPAL

La pantalla principal está organizada de forma limpia en **3 secciones sencillas**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  🩺 QUANTUX SALUD • MESA DE AYUDA      [Barra de Turno: Solicitudes Activas y Resueltas] │
│  [➕ Nueva Solicitud]   [👥 Mi Cuenta / Usuarios]   [🔍 Buscar...]   [Filtros Rápidos]  │
├──────────────────────────┬─────────────────────────────────┬───────────────────────────┤
│    1. PANEL IZQUIERDO    │       2. PANEL CENTRAL          │     3. PANEL DERECHO      │
│  • Listado de solicitudes│  • Título y detalle de tu caso  │  • Estado actual del caso │
│  • Búsqueda por palabra  │  • Historial de conversación    │  • Operador asignado      │
│  • Filtro por servicio   │  • Pestañas: Chat / Historial   │  • Botón para dar tu      │
│  • [📊 Descargar Excel]  │  • Escribir mensaje a soporte   │    Conformidad y Cierre   │
└──────────────────────────┴─────────────────────────────────┴───────────────────────────┘
```

* **Barra Superior:** Acceso rápido para crear una nueva solicitud y ver el estado general del turno.
* **Panel Izquierdo (Tus Solicitudes):** Lista ordenada de solicitudes. Puedes buscar cualquier caso por palabra clave o número.
* **Panel Central (Conversación y Detalle):** Muestra qué se solicitó y los mensajes intercambiados con el equipo de soporte.
* **Panel Derecho (Acciones y Estado):** Te muestra en qué etapa está tu caso y contiene el botón para validar y finalizar la atención.

---

## 3. PASO A PASO: CÓMO PEDIR AYUDA (USUARIO SOLICITANTE)

### ⏱️ Paso 1: Crear una Solicitud (Menos de 30 segundos)
1. Haz clic en el botón verde **"➕ Nueva Solicitud"** en la barra superior.
2. Completa los campos guiados:
   * **Plataforma / Sistema:** Elige el sistema afectado (ej. *Receta Digital*, *Telemedicina*, *Historia Clínica*, *Portal de Pacientes*).
   * **Institución o Sede:** Selecciona tu sanatorio, hospital u obra social.
   * **¿Cuánto afecta tu trabajo?:**
     * *Crítico:* Detención total de la atención urgente (ej. Bloqueo total en servicio en producción o quirófano).
     * *Alto:* Falla importante pero puedes usar una alternativa temporal.
     * *Medio:* Inconveniente puntual en tu puesto sin frenar la atención general.
     * *Bajo:* Consulta, duda operativa o solicitud de un nuevo permiso.
3. Escribe un **Título claro** y una **Descripción breve** de lo que ocurre (ej. "Mensaje de error al guardar historia clínica en consultorio 4").
4. Presiona **"Confirmar y Enviar Solicitud"**.
   > 📧 **Aviso por Email:** Recibirás de inmediato un correo electrónico con el número de tu solicitud y el tiempo comprometido de respuesta.

### 💬 Paso 2: Seguimiento y Comunicación con el Operador
* Abre tu solicitud desde el panel izquierdo.
* En el panel central podrás leer las respuestas y consejos del equipo técnico.
* Puedes escribir nuevos mensajes si tienes más detalles o capturas de pantalla para aportar.

### ✅ Paso 3: Confirmación y Cierre (Tu Validación Final)
* Cuando el equipo de soporte resuelva el problema, tu solicitud pasará al estado **"Solucionado"**.
* Verifica en tu computadora o dispositivo que el sistema funcione con normalidad.
* En el panel derecho aparecerá un cuadro destacado con el botón **"Confirmar Solución y Cerrar"**.
* Al hacer clic, el caso queda formalmente cerrado y archivado de manera segura.

---

## 4. GUÍA PARA EL EQUIPO DE SOPORTE TÉCNICO

### 🔄 El Camino de la Solicitud (Estados Simples)
`NUEVA` ➔ *(Tomar caso)* ➔ `ASIGNADA` ➔ *(Iniciar trabajo)* ➔ `EN TRABAJO` ➔ *(Resolver)* ➔ `SOLUCIONADA` ➔ *(Validación del Solicitante)* ➔ `CERRADA`

### 🛠️ Tareas Clave del Operador
1. **Tomar Caso:** En solicitudes nuevas, presiona **"🙋‍♂️ Tomar Yo"** para asignártela en 1 clic.
2. **Derivar a Especialista:** Si el caso requiere intervención de infraestructura o desarrollo, selecciona al especialista y el nivel (N2 / N3) y guarda.
3. **Notas Privadas de Soporte (🔒):** Si necesitas registrar comandos técnicos o notas internas sin confundir al usuario solicitante, marca la casilla **"🔒 Nota Privada Interna"**.
4. **Registrar Solución Clara:** Explica la solución aplicada con al menos 8 caracteres (ej. "Se reinició el servicio de autenticación y se renovó la sesión"). Si aplicaste una solución temporal, marca **"⚠️ Solución Provisoria"**.

---

## 5. PREGUNTAS FRECUENTES (FAQ) Y CONTACTO DE PRODUCCIÓN

* **¿Qué hago ante una emergencia total en servicio en producción o quirófano?**  
  Registra la solicitud con impacto *Crítico*. El sistema la marcará como **P1** (prioridad máxima con alarma visual y SLA de 1 hora) y notificará de inmediato a la servicio en producción técnica 24/7.
* **¿Por qué mi solicitud sigue en estado 'Solucionada'?**  
  Porque el sistema espera tu confirmación. Revisa tu sistema y presiona *"Confirmar Solución y Cerrar"* para finalizar el circuito.
* **¿Puedo descargar todas las solicitudes de mi servicio a Excel?**  
  Sí, usando el botón *"📊 Exportar Bandeja a CSV"* en el panel izquierdo.

---

### 📋 Aprobación Oficial del Comité Evaluador

| Paula Sbarbati | Diego Martínez | Carolina Brizuela | Nicolás Sánchez |
| :---: | :---: | :---: | :---: |
| Calidad Asistencial | Arquitectura Técnica | Operaciones de Salud | Seguridad y Gobernanza |
