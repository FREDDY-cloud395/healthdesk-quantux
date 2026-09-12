# QUANTUX SALUD • HEALTHDESK
## DOC-UM-005: MANUAL OPERATIVO Y GUÍA DE USUARIO
### GUÍA DE USO PARA PROFESIONALES DE SALUD, OPERADORES ITIL Y ADMINISTRADORES

---

### METADATOS Y CONTROL DOCUMENTAL
* **Código Documental:** DOC-UM-005
* **Versión Oficial:** v3.2.0-UAT
* **Fecha de Emisión:** Septiembre 2026
* **Autor / Solution Owner:** Freddy Cortés
* **Audiencia:** Solicitantes Asistenciales, Operadores Soporte N1/N2/N3, Administradores TI

---

## 1. GUÍA RÁPIDA POR PERFIL OPERATIVO

### 1.1. Perfil Solicitante Asistencial (Médicos, Enfermeros, Secretarios)
1. **Acceso al Cockpit:** Ingrese con usuario `solicitante` y contraseña `quantux123`.
2. **Creación de Solicitud:**
   * Presione el botón azul **"Nuevo Ticket"**.
   * Seleccione la **Plataforma Clínica** afectada (ej: *Receta Digital* o *Telemedicina*).
   * Seleccione su **Institución Sanitaria** (ej: *OSDE* o *Sanatorio Mater Dei*).
   * Indique el **Impacto** y la **Urgencia** (el sistema calculará automáticamente la prioridad ITIL).
   * Adjunte una captura de pantalla si corresponde y presione **"Crear Solicitud"**.
3. **Seguimiento y Cierre:**
   * Consulte el estado en tiempo real en la bandeja.
   * Cuando el soporte resuelva el ticket, ingrese a la solicitud, valide la solución y presione **"Cerrar con Conformidad"**.

### 1.2. Perfil Operador de Soporte (Nivel N1 / N2 / N3)
1. **Acceso y Triage:** Ingrese con usuario `soporte` o `cpaez` y contraseña `quantux123`.
2. **Tomar Ticket:** En la bandeja, seleccione un ticket en estado `NUEVO` y presione **"Tomar Ticket"**.
3. **Gestión Operativa:**
   * Para iniciar diagnóstico, transicione a **"EN CURSO"**.
   * Si requiere datos externos, presione **"Pausar / En Espera"**.
   * Si requiere notas técnicas privadas no visibles para el médico, marque la casilla **"Nota Interna"**.
4. **Escalamiento:** Si el incidente supera el nivel asignado, presione **"Escalar"** y seleccione N2 o N3 indicando el motivo técnico.
5. **Resolución:** Ingrese la solución técnica obligatoria (mínimo 8 caracteres), marque si fue un *Workaround* y presione **"Resolver Ticket"**.

### 1.3. Perfil Administrador
1. **Acceso:** Ingrese con usuario `admin` y contraseña `quantux123`.
2. **Supervisión de Mesas:** Acceda al panel de **Mesas de Ayuda** para ver la dotación y carga en N1, N2 y N3.
3. **Gestión de Base de Conocimiento:** Cree y apruebe nuevas guías clínicas con versionado `v1.0` y `v1.1`.
4. **Exportación Forense:** Presione **"Exportar CSV"** para descargar el registro completo de auditoría y tickets para análisis gerencial.

---

## 2. GUÍA DE USO SEGURO DE HERRAMIENTAS ASISTIDAS POR IA

> [!IMPORTANT]
> **Guardrail Asistencial Obligatorio:**
> Los módulos asistidos por IA dentro de Quantux HealthDesk tienen como única finalidad la sugerencia de protocolos técnicos y la aceleración de documentación.
> **Está estrictamente prohibido que un operador aplique una sugerencia clínica sin previa verificación con el especialista facultativo responsable.**

---

### APROBACIÓN DOCUMENTAL
* **Solution Owner:** *Freddy Cortés*
* **Versión:** `v3.2.0-UAT` • Septiembre 2026
