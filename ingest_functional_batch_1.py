# -*- coding: utf-8 -*-
"""
Script de ingesta oficial: Lote 1 de Documentos Funcionales CD2
Inserta 9 artículos canónicos en SQLite kb_articles (IDs 39 a 47).
"""
import sqlite3
from datetime import datetime

DB_PATH = "backend/healthdesk.db"

ARTICLES = [
    {
        "id": 39,
        "title": "CD2-DW-001: Adecuación de Vistas DW - Desacople de Consultorio (institution) y Turno (appointment) para Filial y Contrato",
        "category": "Data Warehouse / Vistas",
        "tags": "DW, Data Warehouse, institution, appointment, desacople, filial, contrato, atencion modular, recetas, indicaciones, evoluciones, Freddy Cortes",
        "content": """### CD2-DW-001: Adecuación de Vistas DW - Desacople de Consultorio (institution) y Turno (appointment) para Filial y Contrato

* **Módulo / Subsistema:** Vistas de Explotación DW / Consultorio Digital / Core API
* **Categoría:** Data Warehouse / Vistas
* **Autoría Funcional:** Freddy Cortés (FeroSistemas) - Versión 1.2

#### 1. Síntoma Reportado (Lenguaje de DW y Soporte Funcional)
"En el Data Warehouse no se puede calcular ni liquidar el Contrato ni la Filial para atenciones modulares o prescripciones fuera de consulta. El campo institution viene nulo o no se encuentra cuando appointment es null."

#### 2. Diagnóstico y Causa Raíz
Históricamente, el nodo `institution` se encontraba incorrectamente anidado dentro del nodo `appointment` (`appointment.institution`). En las atenciones modulares o prescripciones emitidas fuera de consulta, el valor de `appointment` es nulo (`appointment: null`), provocando que DW pierda por completo los datos del consultorio (`_id` e `id`).

#### 3. Procedimiento de Resolución y Regla de Negocio Homologada
1. Desacoplar estructuralmente `institution` del nodo `appointment` en las vistas de **Recetas, Indicaciones y Evoluciones**.
2. Exponer `appointment.identifier` **únicamente** cuando exista una atención con turno agendado asociada.
3. Exponer el nodo `institution` como nodo independiente de primer nivel para **todos los registros**, conteniendo de forma obligatoria:
   - `institution._id`: OID del consultorio en base de datos.
   - `institution.id`: ID externo del consultorio.
4. Con esta estructura, DW reconstruye Filial y Contrato con independencia de si la atención tuvo turno previo o fue modular.

```json
{
  "institution": {
    "_id": "<oid_consultorio>",
    "id": "<id_consultorio_externo>"
  }
}
```"""
    },
    {
        "id": 40,
        "title": "CD2-DW-002: Adecuación de Vistas DW - Construcción de Vista Atenciones e Indicadores de Demanda Espontánea y Fuera de Consulta",
        "category": "Data Warehouse / Vistas",
        "tags": "DW, Vista Atenciones, indicadores, socios unicos, fuera de consulta, demanda espontanea, medicationRequest, imageServiceRequest, practiceServiceRequest, labServiceRequest, note, certificate, Freddy Cortes",
        "content": """### CD2-DW-002: Adecuación de Vistas DW - Construcción de Vista Atenciones e Indicadores de Demanda Espontánea y Fuera de Consulta

* **Módulo / Subsistema:** Data Warehouse / Colecciones Atenciones e Institutions
* **Categoría:** Data Warehouse / Vistas
* **Autoría Funcional:** Freddy Cortés (FeroSistemas) - Versión 1.2

#### 1. Síntoma Reportado (Lenguaje de DW y Analistas de Negocio)
"Discrepancias en el cómputo de socios únicos atendidos en el período y falta de segregación entre atenciones con turno versus atenciones modulares o prescripciones fuera de consulta."

#### 2. Diagnóstico y Causa Raíz
Se requería la creación de una vista consolidada construida a partir de las collections de MongoDB `Atenciones` e `Institutions` que unifique todas las prestaciones y exponga los atributos necesarios para el cálculo de indicadores de Consultorio Digital.

#### 3. Procedimiento de Resolución y Mapeo Oficial de Indicadores
La vista expone el universo completo de atenciones (con turno y modulares) mapeando los siguientes campos a métricas:
- `socioNumber`:
  - *Socios únicos atendidos:* Conteo de `socioNumber` únicos con al menos una atención en el período.
  - *Socios únicos atendidos o con prescripción fuera de consulta:* Registros con `appointment: null` y `socioNumber` informado.
- `clinicalEvolution` + `appointment`: Métrica de evoluciones formales completadas.
- Solicitudes Clínicas Fuera de Consulta (conteo en el período donde `appointment` es null):
  - `medicationRequest`: Medicamentos fuera de consulta.
  - `imageServiceRequest`: Estudios de imágenes fuera de consulta.
  - `practiceServiceRequest`: Prácticas médicas fuera de consulta.
  - `labServiceRequest`: Determinaciones de laboratorio fuera de consulta.
  - `note`: Notas médicas emitidas fuera de consulta.
  - `certificate`: Certificados emitidos fuera de consulta.
- Especialidades en Vista Prestadores: Exposición obligatoria de flags `prescription` (boolean) y `psicopatology` (boolean)."""
    },
    {
        "id": 41,
        "title": "CD2-SISA-001: Restricción Regulatoria de Matrículas SISA - Baja de CRM, Bloqueo de Prescripción (01/06) y 8 Escenarios del Selector",
        "category": "Matrículas / SISA",
        "tags": "SISA, matriculas CRM, bloqueo prescripcion, 01/06, selector matricula, vencida, inhabilitada, refeps, Jessica Gonzalez",
        "content": """### CD2-SISA-001: Restricción Regulatoria de Matrículas SISA - Baja de CRM, Bloqueo de Prescripción (01/06) y 8 Escenarios del Selector

* **Módulo / Subsistema:** Matrículas Médicas / SISA REFEPS / Prescripción
* **Categoría:** Matrículas / SISA
* **Autoría Funcional:** Jessica González (Quantux) - Versión V1

#### 1. Síntoma Reportado (Lenguaje del Médico / Soporte)
"El médico no puede prescribir medicamentos, las opciones de prescripción y recetas están grisadas con una advertencia en pantalla, o no visualiza su matrícula histórica de CRM en el perfil."

#### 2. Diagnóstico y Causa Raíz
Por adecuación regulatoria obligatoria:
- **Solo las matrículas provenientes de SISA habilitadas/vigentes** pueden ser utilizadas para prescribir.
- **Las matrículas de CRM dejan de ser válidas**, no se consultan al servicio de CRM y se eliminan del perfil del prestador.
- Las matrículas SISA vencidas o inhabilitadas se muestran grisadas, no son seleccionables y **nunca** se asignan por defecto.
- A partir del **01/06**, el sistema bloquea de forma total las prescripciones a prestadores que no posean al menos una matrícula SISA habilitada.

#### 3. Procedimiento de Resolución y Reglas de los 8 Escenarios
1. **1 sola matrícula SISA habilitada:** Se asigna automáticamente por defecto. Prescribe normalmente.
2. **Múltiples matrículas SISA habilitadas:** Prioridad M.P. (Provincia) vs M.N. (Filial 60 CABA). Seleccionable en Perfil.
3. **1 o varias SISA pero todas vencidas:** No se asignan por defecto, prescripción bloqueada.
4. **Matrículas CRM sin SISA:** CRM eliminadas. Prescripción bloqueada. Warnings activos.
5. **Matrícula por defecto vencida o CRM teniendo otra SISA habilitada:** **El sistema NUNCA cambia automáticamente de matrícula.** El profesional debe ingresar a Perfil y seleccionar manualmente la SISA vigente para levantar el warning.
6. **Qué se bloquea:** Prescripción de fármacos, repetición de recetas, órdenes de estudios, certificados y notas.
7. **Qué NO se bloquea:** Diagnóstico, evolución médica, atenciones presenciales y psicopatología virtual.
8. **Canal de regularización ante REF-EPS:** Enviar email a `refeps@msal.gov.ar`."""
    },
    {
        "id": 42,
        "title": "CD2-ALTA-001: Optimización del Flujo de Alta de Prestador en CD - Menú Lateral, Justificación Celular/Email y Transición de Sala de Espera",
        "category": "Onboarding / Alta Prestador",
        "tags": "alta prestador, menu lateral, celular whatsapp, email bienvenida, sala de espera, consultorio digital, cartillas, Jessica Gonzalez",
        "content": """### CD2-ALTA-001: Optimización del Flujo de Alta de Prestador en CD - Menú Lateral, Justificación Celular/Email y Transición de Sala de Espera

* **Módulo / Subsistema:** Onboarding de Prestadores / Navegación y UI
* **Categoría:** Onboarding / Alta Prestador
* **Autoría Funcional:** Jessica González (Quantux) - Versión V1

#### 1. Síntoma Reportado (Lenguaje del Prestador)
"Soy un prestador nuevo y no encuentro la opción 'Mis datos' en el menú de la tuerca, o no entiendo por qué me exigen un celular personal y un correo no compartido."

#### 2. Diagnóstico y Causa Raíz
Se rediseñó el flujo de ingreso de nuevos prestadores para optimizar la usabilidad:
- Se eliminó la opción "Mis datos" del menú desplegable del engranaje/tuerca superior derecha.
- Se incorporó el acceso directo destacado **"Alta Consultorio Digital"** en el menú lateral izquierdo.
- Justificación estricta de datos: Celular requerido exclusivamente para soporte personalizado por WhatsApp. Correo requerido estrictamente personal y no compartido para recibir el enlace único de bienvenida del primer login.

#### 3. Procedimiento de Resolución y Ciclo de Vida del Menú
1. El prestador nuevo ingresa a **"Alta Consultorio Digital"** en el menú lateral.
2. Completa Celular y Email. El botón *"Iniciar alta"* se habilita solo cuando ambos tengan formato válido.
3. Al presionar *"Iniciar alta"*, se despliega el modal de éxito con el botón *"Entendido"*.
4. **Estado En Trámite:** El prestador puede consultar sus datos en modo lectura desde el menú lateral, pero no modificarlos directamente.
5. **Activación:** El prestador hace su primer login mediante el enlace de bienvenida y el equipo de **Cartillas** registra la fecha oficial de inicio de operación en el backoffice.
6. **Transición Automática:** La opción *"Alta Consultorio Digital"* desaparece del menú y *"Sala de Espera"* pasa a denominarse oficialmente **"Consultorio Digital"**."""
    },
    {
        "id": 43,
        "title": "CD2-NOSOC-001: Pacientes No Socios en CD - Atención Integral, Branding Neutro, Bloqueo Filiatorio Obligatorio y Restricciones",
        "category": "Pacientes No Socios",
        "tags": "no socios, no osde, branding neutro, datos filiatorios, bloqueo primera atencion, otra cobertura, psicopatologia, nutricion, fonoaudiologia, Freddy Cortes, Jessica Gonzalez",
        "content": """### CD2-NOSOC-001: Pacientes No Socios en CD - Atención Integral, Branding Neutro, Bloqueo Filiatorio Obligatorio y Restricciones

* **Módulo / Subsistema:** Atención Asistencial / Pacientes No OSDE
* **Categoría:** Pacientes No Socios
* **Autoría Funcional:** Freddy Cortés, Jessica González, Alan Tapia (Quantux) - Versión V4

#### 1. Síntoma Reportado (Lenguaje del Médico)
"Atiendo a un paciente particular / No Socio y los botones de prescripción, órdenes y certificados aparecen deshabilitados. En la sala de espera figura como 'Otra cobertura'."

#### 2. Diagnóstico y Causa Raíz
En la atención de pacientes No OSDE rigen reglas específicas de identificación y confidencialidad:
- **Sala de Espera:** Figuran con la etiqueta *"Otra cobertura"* hasta que se abre el turno y se consultan sus datos en la base externa.
- **Bloqueo Filiatorio en Primera Atención:** Es **obligatorio** completar o actualizar los datos filiatorios del paciente No Socio antes de prescribir. Si no están completos, los botones de recetas, estudios y certificados permanecen deshabilitados.
- Se accede a la carga mediante el enlace *"desde acá"* en el mensaje o *"Editar datos"* en la cabecera.

#### 3. Procedimiento de Resolución y Reglas de Especialidad
1. Completar todos los datos filiatorios requeridos y presionar *"Guardar"*; inmediatamente se habilitan las opciones clínicas.
2. **Branding Neutro Obligatorio:** Toda la documentación (órdenes de estudio, prácticas, certificados y notas) se genera y envía con branding neutro, sin logos ni menciones a OSDE.
3. **Evolución:** Se registra en la historia clínica pero **nunca se envía al paciente**.
4. **Restricciones en Psicopatología, Nutrición y Fonoaudiología:**
   - Prohibida la prescripción de medicamentos.
   - Prohibida la prescripción de laboratorio, imágenes y prácticas.
   - Únicamente habilitada la Evolución y la emisión de notas y certificados."""
    },
    {
        "id": 44,
        "title": "CD2-NOSOC-002: Pacientes No Socios en CD - Arquitectura Dual, Recetas INNOVAMED sin Diagnóstico, API Render y MongoDB Atlas",
        "category": "Pacientes No Socios / Arquitectura",
        "tags": "no socios, arquitectura, INNOVAMED, recetas sin diagnostico, MongoDB Atlas, Render API, Jitsi OSDE, Jitsi Quantux, Alan Tapia",
        "content": """### CD2-NOSOC-002: Pacientes No Socios en CD - Arquitectura Dual, Recetas INNOVAMED sin Diagnóstico, API Render y MongoDB Atlas

* **Módulo / Subsistema:** Arquitectura Técnica / Integraciones Externas / Seguridad
* **Categoría:** Pacientes No Socios / Arquitectura
* **Autoría Funcional:** Alan Tapia, Freddy Cortés, Jessica González - Versión V4

#### 1. Síntoma Reportado (Lenguaje de Ingeniería y Soporte N3)
"Consultas sobre el repositorio de recetas de No Socios, ausencia de diagnóstico en la constancia de receta PDF o funcionamiento de la API externa en Render y MongoDB Atlas."

#### 2. Diagnóstico y Causa Raíz
Para aislar el riesgo legal y operativo entre afiliados OSDE y pacientes particulares, se implementó una arquitectura completamente desacoplada con componentes independientes.

#### 3. Procedimiento y Especificaciones Técnicas
1. **Circuito de Medicamentos INNOVAMED:**
   - Las recetas de medicamentos de No Socios son procesadas por **INNOVAMED**.
   - **Ofuscación de Diagnóstico:** INNOVAMED ofusca diagnósticos sensibles; **en el PDF de la receta nunca se muestra el diagnóstico**.
   - **No Persistencia en OSDE:** Las recetas de No Socios **no se guardan** en repositorios OSDE.
2. **Infraestructura de Backend:**
   - **API No Socios:** Hospedada en **Render** (auto-recovery en fallas OOM/crash, reemplazo tras 60s de inactividad, validación estricta de token IAM en middleware).
   - **Base de Datos:** **MongoDB Atlas** (Replica Set, conexión `mongodb+srv` con TLS 1.3 forzado y static outbound IPs).
3. **Registro de Salud Unificado:**
   - *Etapa 1:* Petición concurrente (GET) a API OSDE y API No Socios -> Merge y ordenamiento en cliente.
   - *Etapa 2:* Consulta directa a base externa tras migración de historial clínico.
4. **Videoconsultas:** Jitsi OSDE en Etapa 1; Jitsi Quantux en Etapa 2."""
    },
    {
        "id": 45,
        "title": "CD2-REG-001: Módulo Registraciones - Exposición Multirregistro OK, Consolidación de Rechazos, Estado 'Sin registraciones' y Regla Virtual",
        "category": "Registración de Prestaciones",
        "tags": "modulo registraciones, registrado ok, consolidacion rechazos, esta atencion no tiene registraciones asociadas, anular prestacion, prestaciones virtuales, Jessica Gonzalez",
        "content": """### CD2-REG-001: Módulo Registraciones - Exposición Multirregistro OK, Consolidación de Rechazos, Estado 'Sin registraciones' y Regla Virtual

* **Módulo / Subsistema:** Módulo de Registración de Prestaciones Médicas
* **Categoría:** Registración de Prestaciones
* **Autoría Funcional:** Jessica González (Quantux) - Versión V1.0

#### 1. Síntoma Reportado (Lenguaje del Médico / Facturación)
"Solo se visualiza la última prestación registrada en la atención pisando a las anteriores, o la pantalla muestra decenas de filas repetidas para un mismo rechazo, o figura un estado confuso 'Validado OK'."

#### 2. Diagnóstico y Causa Raíz
El módulo de Registraciones limitaba la exposición al último ítem procesado y multiplicaba los registros por cada intento fallido. Además, utilizaba erróneamente la etiqueta "Validado OK" para atenciones validadas pero sin registración efectiva.

#### 3. Procedimiento de Resolución y Reglas Oficiales
1. **Prestaciones Registradas OK (Multirregistro):** Se visualizan **todas las prestaciones registradas correctamente** de manera individual con su opción correspondiente de *"Anular"*.
2. **Consolidación de Prestaciones Rechazadas:** Los intentos fallidos se agrupan por código. Si la prestación `420296` tuvo 20 intentos rechazados, el listado muestra **un único renglón**: `Prestación 420296 — Rechazada`.
3. **Anulación Individual e Idempotente:** Al anular una prestación, solo ese registro muta a *"Anulada"*; el resto de las prestaciones de la atención conserva su estado.
4. **Fix Terminológico:** Se erradica "Validado OK". Si la prestación fue validada pero no registrada, el estado oficial a mostrar es:  
   **`"Esta atención no tiene registraciones asociadas"`**.
5. **Modalidad Presencial vs Virtual:**
   - *Presenciales:* Permite anular, pero no permite nueva registración desde esta vista.
   - *Virtuales:* Permite anular. Si existe al menos una registración en *"Registrado OK"*, **se bloquea cualquier nueva registración** (máximo 1 activa)."""
    },
    {
        "id": 46,
        "title": "CD2-MED-001: Manejo de Errores del Repositorio de Medicamentos - Clasificación en 3 Categorías, Reenvío 5xx vs Reemisión de Receta",
        "category": "Prescripción / Repositorio Medicamentos",
        "tags": "repositorio medicamentos, receta rechazada, error 500, error 599, credencial 11 caracteres, socio inexistente, atenciones realizadas, seccion medicamentos, Freddy Cortes, Jessica Gonzalez",
        "content": """### CD2-MED-001: Manejo de Errores del Repositorio de Medicamentos - Clasificación en 3 Categorías, Reenvío 5xx vs Reemisión de Receta

* **Módulo / Subsistema:** Repositorio de Medicamentos / Receta Electrónica / Notificaciones
* **Categoría:** Prescripción / Repositorio Medicamentos
* **Autoría Funcional:** Freddy Cortés, Jessica González (Ferosistemas) - Versión 1.2

#### 1. Síntoma Reportado (Lenguaje del Prestador)
"El médico recibe un correo con el asunto 'Receta no generada - Paciente {{Nombre}}' y no sabe si debe reenviar la receta desde la atención o confeccionar una nueva."

#### 2. Diagnóstico y Causa Raíz
Se superó el modelo anterior de error genérico 422 para clasificar los rechazos en categorías específicas con instrucciones de acción diferenciadas según el tipo de falla.

#### 3. Procedimiento de Resolución y Matriz de Acciones
1. **Categoría Errores de Datos del Paciente:**
   - *Errores:* Credencial excede o tiene longitud menor a 11 caracteres, Socio inexistente, Credencial incorrecta, Falta indicar número de credencial.
   - *Acción médica obligatoria:* **No intentar reenviar.** Debe emitir una nueva receta electrónica fuera de la atención desde la sección *Medicamentos* de la plataforma corrigiendo los datos del afiliado.
2. **Categoría Error Interno del Servicio (HTTP 500 al 599):**
   - *Causa:* Inconveniente técnico o timeout en el último reintento de envío al repositorio.
   - *Acción médica:* **SÍ puede reenviar la receta** directamente desde la sección *Atenciones realizadas*, o emitir una nueva desde *Medicamentos*.
3. **Categoría Estándar UX:** Para rechazos no contemplados en la etapa 1, se instruye la emisión de una nueva receta desde *Medicamentos*.
4. **Roadmap Etapa 2:** Incorporación de mensajes específicos para código Alfabeta no encontrado y falta de comerciales para monodroga."""
    },
    {
        "id": 47,
        "title": "CD2-PSICO-001: Registro de Prestaciones en Psicopatología Virtual - Restricción a Lista Cerrada (330384, 330385, 330386)",
        "category": "Psicopatología / Prestaciones Virtuales",
        "tags": "psicopatologia virtual, prestaciones permitidas, 330384, 330385, 330386, entrevista de orientacion on line, terapia individual on line, control farmacologico on line, Jessica Gonzalez",
        "content": """### CD2-PSICO-001: Registro de Prestaciones en Psicopatología Virtual - Restricción a Lista Cerrada (330384, 330385, 330386)

* **Módulo / Subsistema:** Registro de Prestaciones / Psicopatología / Telemedicina
* **Categoría:** Psicopatología / Prestaciones Virtuales
* **Autoría Funcional:** Jessica González (Quantux) - Versión V1

#### 1. Síntoma Reportado (Lenguaje del Profesional de Salud Mental)
"En una videoconsulta de Psicopatología, al ingresar al registro de prestación solo aparecen tres opciones disponibles y no encuentro los códigos presenciales habituales."

#### 2. Diagnóstico y Causa Raíz
Por definición funcional regulatoria para Consultorio Digital, los turnos virtuales de Psicopatología tienen restringida la oferta de prestaciones para evitar la carga de códigos no homologados en telemedicina.

#### 3. Procedimiento de Resolución y Catálogo Oficial Permitido
Cuando el sistema valida `Especialidad = Psicopatología` y `Modalidad = Virtual`:
1. El selector de prestaciones carga **exclusivamente** la siguiente lista cerrada de 3 códigos:
   - **`330384` — ENTREVISTA DE ORIENTACION ON LINE**
   - **`330385` — TERAPIA INDIVIDUAL ON LINE**
   - **`330386` — CONTROL FARMACOLÓGICO ON LINE**
2. **Ninguna otra prestación** del maestro general puede visualizarse ni seleccionarse.
3. **Límites del Alcance:** Esta restricción no altera las prestaciones habilitadas para Psicopatología presencial ni para las restantes especialidades médicas."""
    }
]

def run_ingest():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"Iniciando ingesta del Lote 1 de Documentos Funcionales en {DB_PATH}...")
    inserted = 0
    updated = 0

    for art in ARTICLES:
        cursor.execute("SELECT id FROM kb_articles WHERE id = ?", (art["id"],))
        exists = cursor.fetchone()
        if exists:
            cursor.execute("""
                UPDATE kb_articles 
                SET title = ?, category = ?, tags = ?, content = ?, updated_at = ?, version = 'v1.0-lote1'
                WHERE id = ?
            """, (art["title"], art["category"], art["tags"], art["content"], now_str, art["id"]))
            updated += 1
            print(f"[UPDATED] {art['id']}: {art['title'][:65]}...")
        else:
            cursor.execute("""
                INSERT INTO kb_articles (
                    id, title, category, content, author_username, tags, 
                    is_published, created_at, updated_at, version, changelog, 
                    view_count, requests_deflected, helpful_score, space_name
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                art["id"], art["title"], art["category"], art["content"], 
                "admin", art["tags"], 1, now_str, now_str, "v1.0-lote1", 
                "Ingesta oficial Lote 1 Funcional CD2", 0, 0, 5, "consultorio-digital"
            ))
            inserted += 1
            print(f"[INSERTED] {art['id']}: {art['title'][:65]}...")

    conn.commit()
    cursor.execute("SELECT count(*) FROM kb_articles")
    total = cursor.fetchone()[0]
    conn.close()
    print(f"\nIngesta finalizada: {inserted} insertados, {updated} actualizados. Total artículos en KB: {total}")

if __name__ == "__main__":
    run_ingest()
