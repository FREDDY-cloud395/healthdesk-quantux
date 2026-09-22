import sqlite3
import datetime

conn = sqlite3.connect('backend/healthdesk.db')
cursor = conn.cursor()
now = datetime.datetime.now(datetime.timezone.utc).isoformat()

article = {
    "title": "Bitácora Operativa de Soporte CD2: Casuística Real, Queries de Contingencia y Reglas de Campo",
    "category": "Casuística Real & Soporte CD2",
    "tags": "casuistica real, chat soporte, consultas frecuentes, queries mongo, sisa, crm, jitsi, matriculas, nutricion, registración",
    "space_name": "Soporte N1/N2/N3 & Operaciones",
    "content": """# Bitácora Operativa de Soporte CD2: Casuística Real y Reglas de Campo

Guía de resolución práctica basada en los casos reales resueltos por el equipo de soporte e ingeniería de Consultorio Digital 2 (Hugo Muñoz, Jessica González, Damián Cofán, Camila Roldán y Freddy Cortés).

---

## 1. Gestión de Matrículas en Base de Datos (Scripts MongoDB de Contingencia)

### A. Prestador con 1 sola matrícula que figura inhabilitada
* **Síntoma:** El profesional tiene una sola matrícula activa en SISA, pero la interfaz de CD2 la muestra inhabilitada y bloquea las opciones de prescripción.
* **Causa:** Inconsistencia temporal entre la matrícula por defecto y el arreglo de matrículas activas.
* **Query MongoDB de Contingencia (Ticket de Implementación):**
```javascript
// Opción 1: Habilitación por ID de usuario
db.users.updateOne(
  { _id: ObjectId("6a0347bfa6ed2811cfe3acba") },
  {
    $set: {
      "defaultMatricula.habilitado": true,
      "defaultMatricula.especialidad": ObjectId("694531791f58654511912856")
    }
  }
);

// Opción 2: Asignación directa desde el arreglo matriculasSisa por IC
db.users.updateOne(
  { icPractitioner: "2000177203" },
  [
    {
      $set: {
        defaultMatricula: { $arrayElemAt: ["$matriculasSisa", 0] }
      }
    }
  ]
);
```

### B. Matrícula única habilitada (Comportamiento del Menú Select)
* **Regla:** Si el médico tiene una sola matrícula habilitada, el sistema la selecciona por defecto automáticamente y **no despliega menú de opciones** (porque no hay otra para alternar). Si no aparece el cartel rojo de advertencia, la matrícula está lista para prescribir.
* **Confusión recurrente:** Si el médico dice que no puede finalizar la consulta, verificar si cargó el **Diagnóstico Obligatorio**.

### C. Cuándo impacta una nueva matrícula dada de alta en SISA o unificada en CRM
* **Regla de Oro:** La actualización **NO impacta de forma instantánea**. El cambio se sincroniza en CD2 **únicamente cuando el profesional vuelve a iniciar sesión (hace login nuevamente)** en la plataforma.

### D. Matrícula con formato especial o barra (ej. "04971/1")
* Si en la base de CD2 y en el padrón SISA figura con `/1`, la plataforma envía el dato fidedigno del origen. El profesional debe regularizar la inscripción directamente ante el Ministerio de Salud (SISA).

---

## 2. Reglas de Validación: Medios de Registración (CRM -> Consultorio Digital)
Para que Consultorio Digital pueda sincronizar Operador y Terminal desde el CRM, se exige una coincidencia estricta del 100% en 4 variables:
1. **Efector** (ej. `6001127106`)
2. **Filial**
3. **Región** (ej. detectar discrepancias entre región de residencia y de atención como Neuquén 20 vs Río Negro 22)
4. **Estado**
* **Flujo de Soporte:** Si faltan Operador o Terminal o el botón de registro está bloqueado, cruzar estas 4 variables. Si no coinciden, gestionar la corrección o alta de la región en CRM.

---

## 3. Módulo de Registración de CD2 (Virtuales vs Presenciales)
* **Atenciones Virtuales:** Solo se pueden reintentar registraciones para consultas virtuales que hayan quedado sin registración o en estado rechazado.
* **Atenciones Presenciales:** Si una prestación presencial quedó rechazada, **NO se puede reintentar registrar desde el módulo de CD2** (debe gestionarse por diferido o vía validador externo).
* **Múltiples Prestaciones en Presencial:** En atenciones presenciales se pueden cargar múltiples prestaciones en el carrito clínico (ej. consulta `420101` y práctica complementaria `140101`). En el resumen de atenciones finalizadas se muestra la última registrada.
* **Plataformas Externas:** Cualquier registración o anulación realizada fuera de CD (ej. Extranet o validador directo) **no se reflejará** en el módulo de CD2.

---

## 4. Búsqueda de Obras Sociales: Caso OSDEPYM
* **Problema:** El prestador no encuentra "OSDEPYM" al editar la cobertura del paciente.
* **Motivo:** En los padrones oficiales figuraba como *"OBRA SOCIAL DE DIRECTIVOS Y EMPRESARIOS PEQUEÑOS Y MEDIANOS"* y posteriormente cambió su razón social a *"Obra Social de Empresarios, Profesionales y Monotributistas de Argentina"*.
* **Resolución:** El nomenclador de CD2 fue actualizado para permitir la búsqueda por la sigla abreviada **OSDEPYM**.

---

## 5. Videoconsulta Jitsi: Auto-visualización (Self-View)
* **Incidencia:** Al maximizar la pantalla de videoconsulta, no se ve la miniatura propia del médico en la esquina superior derecha.
* **Causa/Solución:** Atributo faltante en la etiqueta `iframe` de Jitsi, corregido para mantener activa la miniatura durante la llamada.

---

## 6. Procedimiento de Baja de Prestador por Modificación de CUIT/IC
Para revocar el acceso de un prestador manteniendo la integridad de auditoría histórica:
```javascript
db.users.updateOne(
  { icPractitioner: "2002643140" },
  { $set: { icPractitioner: "10002002643140" } }
);
```

---

## 7. Incidencia Nutrición (Prestaciones 190173 vs 420296)
* Al finalizar nutrición, si impacta la prestación `190173` y es rechazada: solicitar al profesional recargar la pantalla (F5) para aplicar el fix desplegado y reintentar desde el módulo de registración para turnos virtuales. Como paliativo de honorarios, registrar en diferido la `420296` por fuera de CD.
"""
}

cursor.execute("SELECT id FROM kb_articles WHERE title = ?", (article["title"],))
row = cursor.fetchone()
if row:
    cursor.execute("""
        UPDATE kb_articles
        SET category = ?, tags = ?, space_name = ?, content = ?, updated_at = ?
        WHERE id = ?
    """, (article["category"], article["tags"], article["space_name"], article["content"], now, row[0]))
else:
    cursor.execute("""
        INSERT INTO kb_articles (
            title, category, content, author_username, tags, version,
            changelog, view_count, requests_deflected, helpful_score,
            space_name, is_published, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        article["title"], article["category"], article["content"], "admin", article["tags"],
        "v2.0", "Carga oficial Bitácora de Soporte CD2 basada en chat real",
        0, 0, 100, article["space_name"], 1, now, now
    ))

conn.commit()
cursor.execute("SELECT COUNT(*) FROM kb_articles")
total = cursor.fetchone()[0]
conn.close()
print(f"Bitacora cargada con exito. Total articulos en KB: {total}")
