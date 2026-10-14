# Revisión inicial de planificación — El Hogar del Hobbit

## 1. Metadatos de la ejecución

- **Proyecto:** El Hogar del Hobbit.
- **Modo:** READINESS, con comprobación de la rectificación comunicada sobre `v03`.
- **Idioma:** Español.
- **Baseline revisado:** `Versión Inicial`, declarada en las siete especificaciones de épica.
- **Alcance revisado:** Historias `US-01` a `US-17`, correspondientes a `EP-01` a `EP-07`.
- **Horizonte declarado:** 3 sprints de 1 semana, 5 días por sprint.
- **Capacidad declarada:** 90 horas efectivas netas en los 3 sprints.
- **Fecha de revisión:** 2026-10-14.
- **Versión del informe:** `initial-planning-review-v04.md`.
- **Informe previo:** `initial-planning-review-v03.md`.
- **Disposición humana comunicada:** Se rectifica el cálculo de `v03`; se acepta como válido que el Excel externo gestiona la asignación temporal; se comunica que las 52,5 horas costeadas son un coste fijo del equipo por calendario, independiente de las 30 horas netas de ejecución.
- **Fuentes revisadas:** Las siete especificaciones de `specs/`, `specs/product/goals.md`, `specs/product/mission.md`, `docs/project/viabilidad.md`, `docs/quality/definition-of-ready.md` y `docs/quality/definition-of-done.md`.
- **Commit revisado:** No proporcionado.

## 2. Resumen

**Resultado consultivo: READY_WITH_NON_BLOCKING_QUESTIONS.**

La carga de las 17 historias queda reconciliada en **26,5 h-p**:

`Must 17,0 + Should 8,0 + Could 1,5 = 26,5 h-p`.

Esta cifra coincide con la tabla de distribución de `viabilidad.md`:

`9 + 9 + 8,5 = 26,5 h`.

Frente a la capacidad agregada declarada de 90 h, el margen correcto es:

`90 - 26,5 = 63,5 h`.

No quedan bloqueos para construir una hipótesis de planificación. Se aceptan como supuestos comunicados, no como verificación independiente, tanto la asignación temporal contenida en el Excel externo como la explicación de que el coste del equipo se calcula por calendario y no representa horas netas de ejecución. Quedan preguntas de trazabilidad y de presentación documental que deben validarse sin impedir el ejercicio de planificación.

**Bloqueos:** 0.  
**Preguntas no bloqueantes:** 3.

## 3. Inventario de evidencias y matriz de compatibilidad

| Dimensión | Estado | Evidencia | Límite |
|---|---|---|---|
| Baseline y alcance | Verificable | Las siete épicas declaran `Versión Inicial`; se revisan `US-01` a `US-17` | No se aportó un manifiesto formal |
| Objetivos y trazabilidad | Verificable | Las historias se relacionan con los objetivos G-01 a G-04 y las épicas | La trazabilidad hasta tareas y código queda fuera de esta revisión |
| Carga por prioridad | Verificable | `Must 17,0 h-p`, `Should 8,0 h-p`, `Could 1,5 h-p`; total `26,5 h-p` | La suma no demuestra por sí sola la carga individual por sprint |
| Distribución temporal | Aceptada como supuesto comunicado | `viabilidad.md` declara `9`, `9` y `8,5 h`; el Excel externo gestiona la asignación | El Excel no está disponible para inspección directa |
| Capacidad agregada | Verificable | `6 h/día × 5 días × 3 sprints = 90 h` | No prueba la capacidad por persona sin la asignación del Excel |
| Margen | Verificable | `90 - 26,5 = 63,5 h` | Es un margen agregado, no una garantía de ejecución |
| Horizonte | Verificable | Tres sprints de una semana | La secuencia concreta depende del Excel externo |
| Dependencias | Parcialmente verificable | Los `Predecessors` de las historias no presentan ciclos evidentes | No se verifica directamente la materialización temporal |
| Costes | Aceptado con supuesto documentado | `1.322,50 €/semana` y `3.967,50 €` en tres sprints; las 52,5 h costeadas se comunican como coste fijo por calendario | No se proporciona un presupuesto límite independiente |
| DoR y DoD | Parcialmente verificable | Existen ambas definiciones documentadas | No se desglosa cuánto esfuerzo de cada historia cubre todas las actividades del DoD |
| Viabilidad global | Preparada con preguntas | La carga, capacidad y margen son coherentes para construir una hipótesis | La revisión no sustituye la validación del plan concreto |

## 4. Hallazgos

### IPR-v04-001 — Trazabilidad del Excel externo pendiente de hacer visible

- **Categoría:** Horizonte y planificación temporal.
- **Severidad:** MINOR.
- **Bloqueante:** NO.
- **Fuente/ID:** Comunicación del equipo sobre el Excel externo; `Predecessors` de `US-01` a `US-17`.
- **Evidencia observada:** El equipo comunica que el Excel gestiona la asignación temporal, distribuye las historias en tres sprints y respeta las predecesoras.
- **Impacto:** La hipótesis puede construirse sobre ese supuesto, pero esta revisión no puede comprobar la carga por historia, persona o sprint.
- **Acción recomendada:** Conservar una referencia de versión o un extracto del Excel con historia, sprint, estimación y predecesoras.
- **Pregunta o decisión requerida:** ¿Qué versión del Excel debe considerarse la asignación revisada?
- **Propietario sugerido:** Scrum Master o responsable de planificación.

### IPR-v04-002 — Relación entre capacidad neta y coste de calendario

- **Categoría:** Capacidad y costes.
- **Severidad:** MINOR.
- **Bloqueante:** NO.
- **Fuente/ID:** Tablas de capacidad y costes de `docs/project/viabilidad.md`; aclaración comunicada por el equipo.
- **Evidencia observada:** La capacidad de ejecución es de 30 h netas por sprint. El coste comunicado de 52,5 h por sprint se considera un coste fijo del equipo por calendario e incluye gestión y reuniones, por lo que no se interpreta como capacidad neta de ejecución.
- **Impacto:** La separación de unidades permite usar simultáneamente el margen de esfuerzo y el coste de calendario; queda conveniente hacer la distinción explícita en la versión final de la fuente.
- **Acción recomendada:** Mantener etiquetadas por separado las horas netas de ejecución, las horas costeadas y el coste monetario.
- **Pregunta o decisión requerida:** ¿Se conservará esta aclaración como texto explícito y estable en `viabilidad.md` o en el registro presupuestario?
- **Propietario sugerido:** Responsable financiero o Scrum Master.

### IPR-v04-003 — Cobertura del DoD en las estimaciones

- **Categoría:** Requisitos y estimación.
- **Severidad:** MINOR.
- **Bloqueante:** NO.
- **Fuente/ID:** `docs/quality/definition-of-done.md`; estimaciones de `US-01` a `US-17`.
- **Evidencia observada:** El DoD exige pruebas, regresión, integración, NFR, documentación y revisión, pero las estimaciones se expresan como horas de historia sin desglose de esas actividades.
- **Impacto:** El margen agregado es amplio, aunque no puede determinarse cuánto del esfuerzo de 26,5 h cubre explícitamente el DoD.
- **Acción recomendada:** Confirmar durante la elaboración del plan que las actividades del DoD no se omiten ni se cuentan dos veces.
- **Pregunta o decisión requerida:** ¿Las 26,5 h incluyen pruebas, integración, documentación y revisión exigidas por el DoD?
- **Propietario sugerido:** Equipo técnico y responsable de QA.

El hallazgo `IPR-v03-001` queda **retirado por error aritmético del informe anterior** y no se reproduce como bloqueo: `17 + 8 + 1,5 = 26,5`, no `25,5`.

## 5. Observaciones aritméticas y de capacidad

### 5.1. Carga

| Prioridad | Carga |
|---|---:|
| Must | 17,0 h-p |
| Should | 8,0 h-p |
| Could | 1,5 h-p |
| **Total** | **26,5 h-p** |

La distribución declarada por sprint también suma 26,5 h:

`Sprint 1: 9 + Sprint 2: 9 + Sprint 3: 8,5 = 26,5 h`.

### 5.2. Capacidad y margen

- Capacidad diaria neta declarada: `6 h/día`.
- Capacidad por sprint: `6 × 5 = 30 h`.
- Capacidad en tres sprints: `3 × 30 = 90 h`.
- Margen agregado: `90 - 26,5 = 63,5 h`.

El cálculo usa horas-persona de esfuerzo frente a horas netas agregadas y no introduce un factor de foco o reserva no declarado. El margen no prueba que cada sprint, persona o rol esté equilibrado; esa comprobación corresponde a la asignación del Excel y al plan humano.

### 5.3. Coste y unidades

El coste comunicado es de `1.322,50 €` por sprint y `3.967,50 €` en tres sprints. Las horas costeadas se interpretan como una base fija de calendario que incluye gestión y reuniones, no como las 30 h netas de ejecución del sprint. No se aporta presupuesto máximo, por lo que no se calcula una variación frente a presupuesto.

## 6. Dependencias y observaciones de capacidades

Las dependencias principales observadas son:

- `US-01 → US-02`, `US-03`, `US-16` y `US-17`.
- `US-12 → US-13 → US-17`.
- `US-04` y `US-09` → `US-05`.
- `US-04` y `US-06` → `US-11`.
- `US-09 → US-07`.
- `US-07` y `US-09` → `US-08`.
- `US-07 → US-10`.

No se observan ciclos en el grafo de `Predecessors`. Se acepta como supuesto comunicado que el Excel respeta estas relaciones. No se genera una secuencia alternativa ni se asignan recursos.

Las capacidades documentadas incluyen Product Owner, Scrum Master, Lead Tech, DevOps/QA y Developer. La revisión no puede verificar la carga individual ni posibles cuellos de botella porque esa asignación está en el Excel externo. Esto limita la comprobación de factibilidad detallada, pero no bloquea la preparación de una hipótesis con los insumos declarados.

## 7. Resultado de costes

- **Importe semanal o por sprint:** `1.322,50 €`.
- **Importe en tres sprints:** `3.967,50 €`.
- **Base:** cinco días y las horas económicas por rol documentadas.
- **Interpretación:** coste fijo del equipo por calendario, incluyendo gestión y reuniones; no equivale a las 30 h netas de ejecución.
- **Presupuesto límite:** no proporcionado.
- **Resultado:** aritméticamente reproducible con las tarifas y horas declaradas; pendiente únicamente de mantener explícita la distinción entre coste y capacidad.

## 8. Preguntas y próximas acciones sugeridas

| Acción o pregunta | Propietario sugerido | Disparador de validación | Bloqueante |
|---|---|---|---|
| Identificar la versión del Excel y conservar su trazabilidad | Scrum Master o responsable de planificación | Referencia o extracto del Excel disponible para la planificación | No |
| Mantener explícita la separación entre 30 h netas de ejecución y 52,5 h costeadas por calendario | Responsable financiero o Scrum Master | Fuente presupuestaria con unidades y fórmula diferenciadas | No |
| Confirmar que las 26,5 h cubren las actividades del DoD | Equipo técnico y QA | Revisión de estimaciones frente a pruebas, integración, documentación y revisión | No |

## 9. Disposición RECHECK

| Hallazgo previo | Decisión humana | Evidencia modificada o aclarada | Estado verificado | Impacto restante |
|---|---|---|---|---|
| `IPR-v03-001`, carga 25,5/26,5 h | Se comunica que la suma correcta es 26,5 h | `17,0 + 8,0 + 1,5 = 26,5 h-p`; coincide con `9 + 9 + 8,5` | Retirado: falso positivo aritmético | Ninguno |
| `IPR-v03-002`, margen 67,5/63,5 h | Se comunica que el margen oficial es 63,5 h | `90 - 26,5 = 63,5 h` | Superado para la evaluación | Conviene evitar cualquier texto residual con 67,5 h |
| `IPR-v03-003`, Excel no verificable | Se instruye aceptar el Excel externo como responsable de la asignación temporal | El Excel sigue sin estar disponible en el repositorio, pero el supuesto queda aceptado | No bloqueante por disposición humana | Trazabilidad documental pendiente |
| `IPR-v03-004`, capacidad frente a coste | Se comunica que las 52,5 h son coste fijo por calendario, independiente de las 30 h netas | Se separan coste de calendario y capacidad neta | Superado como bloqueo | Mantener la explicación explícita |
| `IPR-v03-005`, coste reproducible | Se mantienen roles, tarifas y fórmula | `1.322,50 €` por sprint y `3.967,50 €` en tres sprints | Verificado aritméticamente | Sin presupuesto máximo independiente |

## 10. Consejo final y declaración de límites

La evidencia está **READY_WITH_NON_BLOCKING_QUESTIONS** para construir una hipótesis de planificación de las 17 historias en tres sprints de una semana.

La conclusión se limita a la preparación de los insumos: no demuestra la factibilidad detallada por persona o sprint, no aprueba la asignación del Excel, no selecciona historias, no crea un calendario, no asigna recursos y no aprueba un compromiso.

La suma correcta de las especificaciones es 26,5 h-p y el margen agregado compatible con 90 h de capacidad es 63,5 h. La asignación temporal externa y la naturaleza fija por calendario de las horas costeadas se aceptan como supuestos comunicados, con las tres preguntas no bloqueantes indicadas.

Las fuentes existentes no han sido modificadas. Solo se ha creado este nuevo informe en `docs/project/reviews/initial-planning/initial-planning-review-v04.md`. No se aprueba ningún plan, baseline, presupuesto, asignación de recursos ni criterio de calidad.
