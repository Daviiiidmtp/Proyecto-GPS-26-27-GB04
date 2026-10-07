# Requirements review v01

## 1. Run metadata

- **Baseline/snapshot:** `Versión Inicial`, según las siete especificaciones revisadas.
- **Supplied commit:** No proporcionado.
- **Fecha/hora de revisión:** 2026-10-07; hora exacta de inicio no registrada.
- **Agente:** `requirements-reviewer.agent.md`.
- **Modelo/herramienta:** No proporcionado.
- **Modo:** `INITIAL`.
- **Alcance:** Épicas `EP-01` a `EP-07` y sus historias `US-01` a `US-15` en `specs/`; Definition of Ready, Definition of Done y constitución del proyecto.
- **Idioma:** Español.
- **Precedencia aplicada:** Las especificaciones de `specs/` son la fuente detallada confirmada por el equipo. El DoR, el DoD y la constitución se usan como reglas transversales. No se encontró una misión de producto independiente para validar la cobertura de objetivos.

## 2. Source manifest and limitations

### Fuentes leídas

| Fuente | Rol | Baseline/versión | Secciones revisadas |
|---|---|---|---|
| `specs/EP-01-catalogo/spec.md` | Especificación de catálogo | Versión Inicial | Objetivo, resultado, US-01 a US-03, criterios, reglas, casos límite y restricciones |
| `specs/EP-02-eventos/spec.md` | Especificación de eventos | Versión Inicial | Objetivo, resultado, US-04 a US-06, criterios, reglas, casos límite y restricciones |
| `specs/EP-03-foro/spec.md` | Especificación de foro | Versión Inicial | Objetivo, resultado, US-07 y US-08, criterios y boundary |
| `specs/EP-04-usuarios/spec.md` | Especificación de usuarios | Versión Inicial | Objetivo, resultado, US-09 y US-10, criterios, reglas, casos límite y restricciones |
| `specs/EP-05-notificaciones/spec.md` | Especificación de notificaciones | Versión Inicial | Objetivo, resultado, US-11, criterios y boundary |
| `specs/EP-06-inventario/spec.md` | Especificación de inventario | Versión Inicial | Objetivo, resultado, US-12 y US-13, criterios, reglas, casos límite y restricciones |
| `specs/EP-07-soporte/spec.md` | Especificación de soporte | Versión Inicial | Objetivo, resultado, US-14 y US-15, criterios y boundary |
| `docs/quality/definition-of-ready.md` | Criterio transversal de preparación | No indicado | Todos los criterios de identificación, valor, aceptación, planificación, restricciones y cuestiones pendientes |
| `docs/quality/definition-of-done.md` | Criterio transversal de finalización | No indicado | Implementación, aceptación, pruebas, integración, NFR, documentación y revisión |
| `.specify/memory/constitution.md` | Gobierno y principios | No indicado | Especificación previa, calidad verificable, privacidad, usabilidad/accesibilidad y artefactos |

### Fuentes no accesibles o no encontradas

- No se encontró `.specify/specs/`; se utilizó `specs/` por confirmación explícita del equipo.
- No se encontró una misión de producto, catálogo de objetivos o documento de stakeholders en las rutas inspeccionadas. La cobertura respecto a una misión completa queda **NOT_ASSESSABLE**.
- No se proporcionaron decisiones humanas, informe previo ni log de decisiones; no aplican comprobaciones de `RECHECK`.
- No se inspeccionó código ni se ejecutaron pruebas. Este informe evalúa requisitos, no conformidad de implementación con el DoD.

## 3. Scoped assessment

**Recomendación: NEEDS_REFINEMENT.**

El alcance revisado comprende las 15 historias `US-01`–`US-15`. Hay hallazgos bloqueantes para una planificación fiable: una dependencia circular en el flujo del foro, autorización administrativa insuficientemente especificada, reserva concurrente sin comportamiento transaccional verificable, y varios criterios de aceptación incompletos para errores, estados vacíos y límites. Las historias tienen identificadores, épicas, objetivos, prioridades y estimaciones, pero no todas están listas conforme al DoR.

Esto no es una aprobación de la línea base ni del gate. La recomendación se limita al contenido revisado y no determina si el producto cubre una misión no suministrada.

## 4. Coverage matrix

| Dimensión | IDs inspeccionados | Resultado | Hallazgos |
|---|---|---|---|
| Claridad y consistencia | `US-01`–`US-15`, referencias cruzadas | **NO MET** | `RR-001`, `RR-002`, `RR-003`, `RR-004` |
| Cobertura y alcance | `EP-01`–`EP-07`, `US-01`–`US-15` | **NOT_ASSESSABLE / NO MET** | `RR-005`, `RR-006`; falta misión y stakeholders completos |
| Elementos de especificación | Todas las historias y NFR declarados | **NO MET** | `RR-003`, `RR-004`, `RR-005`, `RR-007` |
| Granularidad | `US-05`, `US-10`, `US-12`, `US-14` principalmente | **NO MET** | `RR-008` |
| Aceptación y DoR | `US-01`–`US-15` frente a DoR | **NO MET** | `RR-003`, `RR-004`, `RR-007`; matriz de §6 |
| Dependencias y supuestos | Todos los campos `Predecessors`, boundaries y reglas | **NO MET** | `RR-001`, `RR-002`, `RR-009` |

## 5. Findings

### 5.1 Compact index

| ID | Severidad | Confianza | Estado | Categoría | Afectación |
|---|---|---|---|---|---|
| `RR-001` | CRITICAL | HIGH | Bloqueante | Dependencia/consistencia | `US-07`, `US-08`, `US-10` |
| `RR-002` | MAJOR | HIGH | Bloqueante | Autorización y alcance | `US-06`, `US-10`, `US-12`, `US-13` |
| `RR-003` | MAJOR | HIGH | Bloqueante | Aceptación insuficiente | `US-02`, `US-03`, `US-04`, `US-06`, `US-09`, `US-11`, `US-13`, `US-14` |
| `RR-004` | MAJOR | HIGH | Bloqueante | Concurrencia e integridad | `US-05`, `US-13` |
| `RR-005` | MAJOR | MEDIUM | Bloqueante por cobertura | NFR y verificabilidad | `US-01`, `US-04`, `US-09`, constitución |
| `RR-006` | QUESTION | MEDIUM | No confirmado | Alcance/misión | `EP-01`–`EP-07` |
| `RR-007` | MAJOR | HIGH | Bloqueante | Casos de error y seguridad | `US-01`–`US-15`, especialmente `US-09`, `US-14` |
| `RR-008` | MAJOR | HIGH | Bloqueante de planificación | Granularidad | `US-05`, `US-10`, `US-12`, `US-14` |
| `RR-009` | MAJOR | HIGH | Bloqueante | Modelo de dominio/dependencias | `US-04`–`US-06`, `US-11`, `US-12` |

### 5.2 Detailed evidence records

#### RR-001 — Dependencia circular del foro

- **Categoría:** Dependencias y consistencia.
- **Fuente y extracto:** `specs/EP-03-foro/spec.md`, `US-07`, `Predecessors: US-09`; `specs/EP-04-usuarios/spec.md`, `US-10`, `Predecessors: US-07, US-09`.
- **Observación:** `US-07` necesita registro, mientras `US-10` necesita que exista el foro y sus mensajes. Si el plan interpreta `US-10` como prerrequisito de la capacidad completa del foro, queda una secuencia circular; además, no se declara explícitamente si leer es anónimo y escribir exige autenticación.
- **Impacto:** Impide ordenar el trabajo y puede dejar sin definición el flujo mínimo que permite probar moderación.
- **Acción sugerida:** Separar autenticación como prerrequisito explícito; declarar `US-07` como dependiente de `US-09` y `US-10` como dependiente de la publicación/respuesta que realmente modera, no al revés. Definir permisos de lectura, creación, respuesta y moderación.
- **Confianza:** HIGH, porque las dos dependencias aparecen literalmente.
- **Bloqueante:** Sí.

#### RR-002 — Autorización administrativa incompleta

- **Categoría:** Seguridad y alcance.
- **Fuente y extracto:** `US-06-AC-01`: “Los administradores tienen un formulario”; `US-10-AC-01`: “Si entras con cuenta de administrador”; `US-12-AC-01`: “panel privado de administrador”.
- **Observación:** Se describe la interfaz para administradores, pero no el comportamiento ante usuario no autenticado, usuario normal, sesión caducada o cuenta bloqueada. `US-10` solo menciona bloqueo de cuentas sin definir quién puede bloquear/desbloquear ni cómo se aplica a sesiones activas.
- **Impacto:** No se puede verificar el control de acceso ni planificar una frontera de seguridad coherente.
- **Acción sugerida:** Añadir criterios negativos por rol y sesión para cada operación administrativa, más reglas para bloqueo, desbloqueo, sesiones activas y respuesta esperada ante acceso denegado.
- **Confianza:** HIGH.
- **Bloqueante:** Sí.

#### RR-003 — Criterios de aceptación incompletos en búsquedas, eventos, registro y notificaciones

- **Categoría:** Claridad y aceptación.
- **Fuente y extracto:** `US-02-AC-02` solo indica coincidencia parcial; `US-03-AC-02` solo indica mostrar la categoría; `US-04-AC-03` solo excluye eventos pasados; `US-09-AC-01`–`US-09-AC-03` no describen campos vacíos o duplicados; `US-11-AC-01`–`US-11-AC-03` no define lectura.
- **Observación:** Faltan estados sin resultados, búsqueda vacía, mayúsculas/espacios, combinación de filtros, categorías sin productos, eventos llenos/cancelados, fechas inválidas, email duplicado, contraseñas no coincidentes y transición de notificación no leída a leída.
- **Impacto:** Dos implementaciones razonables podrían comportarse de forma distinta y no habría una prueba objetiva común.
- **Acción sugerida:** Añadir escenarios Given/When/Then para entradas válidas, inválidas, vacías, duplicadas y sin resultados, incluyendo el estado visible y la posibilidad de reintento.
- **Confianza:** HIGH.
- **Bloqueante:** Sí para planificación detallada.

#### RR-004 — Reserva y stock sin garantía de integridad concurrente

- **Categoría:** Reglas de negocio y concurrencia.
- **Fuente y extracto:** `US-05` indica que dos personas pueden intentar tomar la última plaza; `US-05-AC-02` exige decrementar plazas; `US-13-AC-01` permite sumar o restar stock.
- **Observación:** Se expresa el resultado deseado en una carrera, pero no se especifica la invariante que nunca debe romperse, qué ocurre si se reintenta la misma petición, ni cómo se resuelve un fallo parcial. En stock tampoco se prohíbe explícitamente quedar por debajo de cero.
- **Impacto:** Puede haber sobre-reservas, plazas negativas, doble inscripción o pérdida de actualizaciones.
- **Acción sugerida:** Definir una única operación atómica de reserva/actualización, unicidad por cuenta-evento, respuesta para solicitud repetida, error de evento lleno y regla `stock >= 0`; añadir escenarios de dos solicitudes simultáneas.
- **Confianza:** HIGH.
- **Bloqueante:** Sí.

#### RR-005 — NFR declarados sin umbral ni método de verificación

- **Categoría:** Requisitos no funcionales.
- **Fuente y extracto:** `US-01`: “La página principal tiene que cargar rápido”; `US-04`: “debe verse bien ... en ordenador como en móvil”; `EP-01` boundary y `constitution.md`: “calidad y comportamiento verificable”, “usabilidad y accesibilidad”.
- **Observación:** Rendimiento, responsive, accesibilidad y seguridad se mencionan como intención, pero no tienen métrica, contexto de prueba, prioridad ni evidencia requerida.
- **Impacto:** El DoR y el DoD exigen comprobar NFR, pero el equipo no puede saber qué resultado satisface el requisito.
- **Acción sugerida:** Acordar para cada NFR el alcance, métrica o checklist verificable, dispositivos/contextos aplicables y criterio de aprobación. No se propone un valor numérico sin decisión del equipo.
- **Confianza:** HIGH para la falta de verificabilidad; MEDIUM para el impacto exacto por ausencia de misión.
- **Bloqueante:** Sí para historias afectadas.

#### RR-006 — Cobertura respecto a misión y stakeholders no evaluable

- **Categoría:** Cobertura y trazabilidad.
- **Fuente y extracto:** Cada épica declara solo `Goals: G-01` o `G-02`; no existe fuente revisada que defina el contenido de esos objetivos ni el conjunto de stakeholders.
- **Observación:** Se puede comprobar la trazabilidad formal de cada historia a un objetivo declarado, pero no si los objetivos son completos ni si faltan capacidades como compra, pago, cancelación, recuperación de cuenta o gestión de contenidos.
- **Impacto:** La planificación puede cubrir correctamente las especificaciones existentes y aun así omitir resultados de producto.
- **Acción sugerida:** Proporcionar la misión/catálogo de objetivos y stakeholders, o confirmar explícitamente esas capacidades como fuera de alcance.
- **Confianza:** MEDIUM, porque la ausencia se limita a las fuentes revisadas.
- **Bloqueante:** Sí para una evaluación global; no bloquea la refinación local.

#### RR-007 — Falta de flujos de error y seguridad transversal

- **Categoría:** Aceptación, privacidad y robustez.
- **Fuente y extracto:** `US-14-AC-03` afirma éxito al enviar, pero no define fallo; `US-09` solo exige ocho caracteres y “algoritmos de encriptación”; `EP-03` excluye archivos, pero no define moderación de texto.
- **Observación:** Varias historias solo especifican el camino feliz. No se define qué se muestra ante fallo de persistencia, entrada inválida, pérdida de conexión, contenido vacío, sesión expirada o envío duplicado. “Encriptadas” es impreciso para contraseñas y no define gestión de secretos.
- **Impacto:** Los criterios no cubren seguridad mínima, privacidad ni recuperación del usuario ante fallos.
- **Acción sugerida:** Añadir criterios de error y reintento donde aplique, política de validación y mensajes no sensibles; precisar que las contraseñas se almacenan mediante un mecanismo de hash adecuado, sin imponer una tecnología concreta si no está decidida.
- **Confianza:** HIGH.
- **Bloqueante:** Sí para registro, contacto, administración y foro.

#### RR-008 — Historias con varios outcomes independientes

- **Categoría:** Granularidad/INVEST.
- **Fuente y extracto:** `US-10` combina “eliminar mensajes” y “bloquear cuentas”; `US-12` combina panel, formulario, validaciones, imagen por defecto y publicación; `US-14` combina navegación, formulario y entrega de incidencias; `US-05` combina elegibilidad, reserva, decremento y concurrencia.
- **Observación:** Cada historia puede producir varios verticales con reglas, permisos y pruebas diferentes. Las estimaciones de 1–2 h-p no reflejan explícitamente esos outcomes ni la incertidumbre asociada.
- **Impacto:** Riesgo de tareas no planificables, aceptación parcial ambigua y falsa sensación de progreso.
- **Acción sugerida:** Considerar dividir por outcome vertical: moderar mensajes / bloquear cuentas; alta de producto / imagen por defecto / publicación; formulario / persistencia o entrega; reservar plaza / impedir duplicado / carrera de última plaza. Mantener dependencias reales, no dividir solo por capas técnicas.
- **Confianza:** HIGH.
- **Bloqueante:** Sí para planificación de esas historias.

#### RR-009 — Modelo de dominio y estados compartidos no definidos

- **Categoría:** Dependencias y supuestos.
- **Fuente y extracto:** `US-04` muestra plazas, `US-05` las consume, `US-06` crea eventos y `US-11` notifica nuevos eventos; `US-12` publica productos y `US-01` solo muestra productos “Activos”; `US-13` usa “Agotado”.
- **Observación:** No se define el ciclo de estados de eventos y productos, ni quién puede cambiarlo, ni si una baja de stock cambia `Activo`, `Agotado` u otro estado. Tampoco se especifica qué evento genera una notificación ni si se notifican cambios posteriores.
- **Impacto:** Las historias no comparten un contrato de datos verificable y pueden producir inconsistencias entre panel, catálogo, calendario y notificaciones.
- **Acción sugerida:** Documentar entidades, estados, transiciones, campos obligatorios, relaciones y eventos de dominio mínimos, incluyendo cancelación/edición si están dentro del alcance.
- **Confianza:** HIGH.
- **Bloqueante:** Sí para integrar estas épicas.

## 6. DoR matrix

**Códigos de criterio del DoR:** D1 identificador; D2 épica; D3 objetivo; D4 usuario/stakeholder; D5 capacidad; D6 valor; D7 límites; D8 criterios de aceptación; D9 comportamiento observable; D10 independencia de implementación; D11 casos límite; D12 prioridad; D13 estimación; D14 incertidumbre; D15 dependencias; D16 NFR; D17 restricciones; D18 dudas bloqueantes resueltas; D19 supuestos documentados.

**Estados:** `MET`, `NOT_MET`, `NOT_ASSESSABLE`, `NOT_APPLICABLE`. `NOT_MET` indica evidencia insuficiente o incumplimiento; `NOT_ASSESSABLE` indica que falta una fuente o decisión necesaria; `NOT_APPLICABLE` solo se usa cuando el criterio no corresponde.

| Historia | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 | D13 | D14 | D15 | D16 | D17 | D18 | D19 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `US-01` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-02` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_APPLICABLE | NOT_MET | NOT_MET |
| `US-03` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_APPLICABLE | NOT_MET | NOT_MET |
| `US-04` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-05` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-06` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | NOT_MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-07` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | NOT_MET | MET | MET | NOT_MET | NOT_MET |
| `US-08` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | NOT_MET | MET | MET | NOT_MET | NOT_MET |
| `US-09` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-10` | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-11` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-12` | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-13` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-14` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | NOT_MET | NOT_MET | NOT_APPLICABLE | NOT_MET | NOT_MET |
| `US-15` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | NOT_MET | NOT_APPLICABLE | NOT_APPLICABLE | NOT_MET | NOT_MET |

### Interpretación de la matriz

- Todas las historias tienen ID, épica, objetivo, rol, capacidad, beneficio, prioridad y estimación explícitos.
- Las incertidumbres están ausentes en `US-02`, `US-03`, `US-06`–`US-08`, `US-10`–`US-15`; por ello D14 no está satisfecho en esas historias.
- D11 falla donde no hay casos alternativos o de error documentados; la excepción principal es `US-05`, que sí documenta la carrera de la última plaza, aunque aún necesita criterios observables.
- D16 no está satisfecho cuando la historia depende de rendimiento, responsive, seguridad, accesibilidad o robustez sin requisito verificable. `NOT_APPLICABLE` se reserva para historias sin NFR específico declarado, no implica que estén exentas de NFR transversales del DoD.
- D18 y D19 se mantienen como `NOT_MET` cuando no hay evidencia de preguntas resueltas o supuestos documentados; no se presume que la ausencia de una sección equivalga a una decisión.

### Elementos diferidos

Se consideran **diferidos, no satisfechos** hasta decisión del equipo: umbrales de rendimiento y responsive (`RR-005`), misión y stakeholders (`RR-006`), política de notificaciones (`RR-003`/`RR-009`), comportamiento de bloqueo de sesiones (`RR-002`) y almacenamiento/entrega de contacto (`RR-007`). Aceptar una propuesta no sustituye actualizar la fuente.

## 7. Candidate omissions, missing stakeholder questions and OUT_OF_SCOPE suggestions

Estas son preguntas o candidatos, no defectos confirmados. La clasificación depende de la misión no suministrada.

### IN_SCOPE_CANDIDATE

- **Cancelación o modificación de eventos:** racional: `US-04`/`US-05` gestionan plazas, pero no describen qué ocurre con un evento cancelado o modificado. Pregunta: ¿el administrador puede cancelar/editar y cómo se liberan las plazas?
- **Recuperación de cuenta y gestión de sesión:** racional: `US-09` crea cuentas y `US-10` bloquea cuentas. Pregunta: ¿la versión inicial necesita cerrar sesión, recuperar contraseña y gestionar sesiones bloqueadas?
- **Estado de entrega de contacto:** racional: `US-14` confirma envío sin destinatario ni bandeja. Pregunta: ¿el mensaje se almacena en un panel, se entrega a un canal interno o solo se simula?
- **Estado leído de notificaciones:** racional: `US-11` habla de no leídas. Pregunta: ¿cuándo se marca una notificación como leída y se conserva para futuras sesiones?

### SCOPE_UNCLEAR

- **Compra, carrito, pagos y reservas de productos:** `EP-01` usa “a la venta”, pero no hay historias de compra. Pregunta: ¿el catálogo es únicamente informativo en esta versión?
- **Gestión de categorías y contenido de FAQs:** `US-03` y `US-15` consumen categorías/FAQs, pero no se define quién las mantiene. Pregunta: ¿son datos fijos ficticios o existe administración?
- **Moderación del contenido del foro:** `US-10` elimina mensajes, pero no hay normas, auditoría ni restauración. Pregunta: ¿qué mínimo de moderación entra en la versión inicial?

### OUT_OF_SCOPE candidate

- **Correo electrónico real:** el boundary de `EP-05` lo excluye explícitamente. Debe permanecer fuera salvo decisión posterior.
- **Subida de fotos/archivos en el foro:** el boundary de `EP-03` lo excluye explícitamente.
- **Datos bancarios reales:** el boundary de `EP-04` lo excluye explícitamente.

## 8. Dependencies, assumptions and traceability gaps

### Dependencias explícitas y problemas

- `US-02` y `US-03` dependen de `US-01`; son dependencias funcionales razonables, pero los filtros y búsqueda deberían compartir el contrato de producto y el estado sin resultados.
- `US-05` depende de `US-04`; también necesita identidad de `US-09`, aunque no aparece en `Predecessors`.
- `US-07` depende de `US-09`; `US-08` depende de `US-07`; `US-10` depende de `US-07` y `US-09`. La secuencia debe corregirse y distinguir capacidad de foro de capacidad de moderación (`RR-001`).
- `US-11` depende de `US-04`, pero la publicación nace en `US-06`; falta la dependencia/contrato entre creación de evento y generación de notificación.
- `US-12` hace aparecer productos en `US-01`; requiere contrato de estado `Activo`, pero no está declarado como dependencia.
- `US-13` cambia stock y puede afectar la visibilidad/estado del producto; ese vínculo no está especificado.

### Supuestos no documentados

- Qué significa “local” en la zona horaria de eventos.
- Si los usuarios anónimos pueden ver catálogo, eventos, foro y FAQs.
- Si “cliente” y “usuario” son el mismo rol, y si el administrador también puede realizar acciones de cliente.
- Qué datos ficticios existen al iniciar el sistema y cómo se carga el catálogo vacío.
- Qué canal recibe los mensajes de contacto.
- Qué contenidos y categorías existen y quién los mantiene.

### Trazabilidad

La trazabilidad historia → épica → `G-01`/`G-02` está presente formalmente. No puede validarse objetivo → misión, historia → stakeholder completo ni historia → evidencia de pruebas porque no se suministraron esas fuentes.

## 9. Questions for humans

### Prioridad alta — resolver antes de planificar

1. ¿Cuál es la secuencia correcta entre registro, foro, publicación/respuesta y moderación? ¿Leer el foro es anónimo?
2. ¿Qué operaciones son exclusivamente administrativas y qué respuesta recibe cada rol no autorizado?
3. ¿Cómo se garantiza la atomicidad de una inscripción y del cambio de stock? ¿Se permite una única inscripción por cuenta y evento como regla de datos?
4. ¿Qué estados tienen los eventos y productos (`activo`, `agotado`, `cancelado`, etc.) y qué transiciones puede ejecutar cada rol?
5. ¿Qué comportamiento debe observarse ante campos vacíos, entradas inválidas, duplicados, errores de red, sesión expirada y reintentos?
6. ¿Qué misión, stakeholders y capacidades están fuera de alcance? En particular, ¿el catálogo permite comprar o solo consultar?

### Prioridad media

7. ¿Qué umbrales o pruebas verifican “cargar rápido”, responsive, accesibilidad y seguridad?
8. ¿Qué significa exactamente “encriptar” contraseñas y qué política de sesión/recuperación se desea?
9. ¿A dónde se entrega o almacena el formulario de contacto?
10. ¿Cuándo se marca una notificación como leída y qué ocurre con usuarios desconectados?
11. ¿Quién mantiene categorías y FAQs?
12. ¿Qué reglas de edición/cancelación existen para eventos y qué ocurre con las plazas reservadas?

## 10. RECHECK crosswalk

No aplica: esta es una revisión `INITIAL`; no se proporcionaron informe previo, log de decisiones ni fuentes revisadas posteriores.

## 11. Explicit closure

**This is an advisory review. No source requirement, priority, estimate, plan or human decision was changed. No baseline or gate was approved.**
