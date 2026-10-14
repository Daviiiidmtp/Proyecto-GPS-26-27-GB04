# Revisión inicial de planificación — El Hogar del Hobbit

## 1. Metadatos de la ejecución

- **Proyecto:** El Hogar del Hobbit.
- **Modo:** READINESS.
- **Idioma:** Español.
- **Baseline revisado:** `Versión Inicial`, declarada en las siete especificaciones de épica.
- **Alcance revisado:** Historias `US-01` a `US-17`, correspondientes a `EP-01` a `EP-07`.
- **Horizonte declarado:** 3 sprints de 1 semana, 5 días por sprint.
- **Capacidad declarada:** 90 horas efectivas netas en los 3 sprints, según `docs/project/viabilidad.md`.
- **Fecha de revisión:** 2026-10-14.
- **Versión del informe:** `initial-planning-review-v02.md`.
- **Informe previo:** `docs/project/reviews/initial-planning/initial-planning-review-v01.md`.
- **Disposición humana comunicada:** Los hallazgos `RR-001` a `RR-009` se consideran procesados y justificados por el equipo.
- **Asignación temporal comunicada:** La distribución de las 17 historias se gestiona externamente en el Excel del equipo y respeta los `Predecessors`; el Excel no fue aportado para esta revisión.
- **Fuentes revisadas:**
  - `specs/EP-01-catalogo/spec.md`
  - `specs/EP-02-eventos/spec.md`
  - `specs/EP-03-foro/spec.md`
  - `specs/EP-04-usuarios/spec.md`
  - `specs/EP-05-notificaciones/spec.md`
  - `specs/EP-06-inventario/spec.md`
  - `specs/EP-07-soporte/spec.md`
  - `specs/product/goals.md`
  - `specs/product/mission.md`
  - `docs/project/viabilidad.md`
  - `docs/quality/definition-of-ready.md`
  - `docs/quality/definition-of-done.md`
- **Fuente de trazabilidad de `RR-001` a `RR-009`:** No identificada como archivo local en la ruta revisada; se acepta la disposición comunicada por el equipo para esta ejecución, sin volver a evaluar esos hallazgos.
- **Commit revisado:** No proporcionado.

## 2. Resumen

**Resultado consultivo: NOT_READY.**

La capacidad efectiva declarada es de 90 horas netas para los tres sprints. La suma de las estimaciones de las 17 historias extraídas de las especificaciones es **25,5 horas-persona**, por lo que el margen agregado nominal sería de **64,5 horas**, si ambas magnitudes son comparables.

La documentación local no es coherente con esa cifra única de carga:

- Las 17 especificaciones suman **25,5 h-p**.
- La tabla de distribución por sprint de `viabilidad.md` suma **26,5 h** (`9 + 9 + 8,5`).
- La misma sección de `viabilidad.md` declara después **22,5 horas** y un margen de **67,5 horas**.
- El mensaje del equipo comunica **25,5 h** como carga corregida, pero esa corrección no aparece reflejada de forma consistente en `viabilidad.md`.

La secuencia de `Predecessors` no presenta ciclos evidentes. La asignación externa se acepta como supuesto comunicado, pero no puede verificarse sin el Excel. El cálculo de costes de **1.322,50 €/semana** y **3.967,50 € en tres sprints** sí es aritméticamente reproducible según las tarifas y horas de gestión/desarrollo documentadas. Debe aclararse, no obstante, su relación con las 30 horas netas de capacidad semanal.

**Bloqueos:** carga oficial no reconciliada; asignación temporal externa no verificable; relación entre capacidad neta y horas costeadas no explicitada.

## 3. Inventario de evidencias y matriz de compatibilidad

| Dimensión | Estado | Evidencia | Límite |
|---|---|---|---|
| Baseline y alcance | Verificable | Las siete épicas declaran `Versión Inicial`; las especificaciones cubren `US-01` a `US-17` | No se aportó un manifiesto formal |
| Requisitos y disposición previa | Parcialmente verificable | El equipo comunica que `RR-001` a `RR-009` están resueltos | No se identificó el archivo de trazabilidad local |
| Identificación de historias | Verificable | Se identifican 17 historias con estimación y `Predecessors` | El Excel de asignación no está disponible |
| Carga de especificaciones | Verificable | La suma de las 17 historias es 25,5 h-p | No coincide con los totales de `viabilidad.md` |
| Distribución por sprint | Parcialmente verificable | `viabilidad.md` registra Sprint 1: 9 h, Sprint 2: 9 h, Sprint 3: 8,5 h | La suma es 26,5 h y no se muestran historias asociadas |
| Capacidad agregada | Verificable | 6 h/día, 30 h/sprint y 90 h en tres sprints | Debe distinguirse capacidad neta de horas costeadas |
| Capacidad individual | Parcialmente verificable | La tabla declara 1, 2, 1, 1 y 1 h/día por miembro | No hay asignación de historias por persona |
| Horizonte temporal | Parcialmente verificable | Se declaran 3 sprints de 1 semana | El Excel externo no permite comprobar la asignación exacta |
| Dependencias | Parcialmente verificable | `Predecessors` está presente y no muestra ciclos evidentes | No se puede comprobar su materialización temporal |
| Costes | Parcialmente verificable | Roles, horas, tarifas y fórmula están en `viabilidad.md` | La base de horas costeadas frente a capacidad neta requiere aclaración |
| DoR y DoD | Parcialmente verificable | Existen definiciones documentadas | La cobertura del DoD en las estimaciones no está explicitada |
| Viabilidad global | No preparada | Existe margen frente a 90 h bajo cualquiera de las cargas, pero las cargas difieren | No puede fijarse una carga oficial única |

## 4. Hallazgos

### IPR-v02-001 — Tres cifras incompatibles para la carga total

- **Categoría:** Estimación y alcance.
- **Severidad:** CRITICAL.
- **Bloqueante:** YES.
- **Fuente/ID:** Estimaciones de `US-01` a `US-17`; `docs/project/viabilidad.md`, sección «Estimación del Proyecto y Viabilidad»; disposición comunicada de 25,5 h.
- **Evidencia observada:** Las especificaciones suman 25,5 h-p. La distribución por sprint de `viabilidad.md` suma 26,5 h. La conclusión de la misma sección usa 22,5 h. El mensaje del equipo identifica 25,5 h como cifra de carga.
- **Impacto:** No existe una carga base única para evaluar el margen, comprobar el Excel o relacionar el esfuerzo con el presupuesto.
- **Acción recomendada:** Actualizar o complementar la fuente oficial con una tabla historia por historia que reconcilie las 17 estimaciones y los totales por sprint.
- **Pregunta o decisión requerida:** ¿La carga oficial es 25,5 h-p? Si lo es, ¿qué dos cifras de `viabilidad.md` deben corregirse y qué historias componen los 9, 9 y 8,5 h?
- **Propietario sugerido:** Product Owner y responsable de estimación.

### IPR-v02-002 — Distribución temporal no verificable contra el Excel externo

- **Categoría:** Horizonte y planificación temporal.
- **Severidad:** MAJOR.
- **Bloqueante:** YES.
- **Fuente/ID:** Comunicación sobre el Excel externo; `Predecessors` de las especificaciones; tabla de sprints de `viabilidad.md`.
- **Evidencia observada:** Se afirma que el Excel distribuye las 17 historias en tres sprints y respeta las predecesoras, pero el archivo no está disponible. `viabilidad.md` aporta totales por sprint, no el detalle de historias, roles ni personas.
- **Impacto:** No se puede comprobar la carga por sprint, la terminación de predecesoras, la carga individual ni la ausencia de cuellos de botella.
- **Acción recomendada:** Aportar un extracto versionado del Excel con historia, sprint, estimación usada, responsable o rol y comprobación de predecesoras.
- **Pregunta o decisión requerida:** ¿Qué versión del Excel constituye la asignación revisada y qué regla determina que una predecesora está terminada?
- **Propietario sugerido:** Scrum Master y responsable de planificación.

### IPR-v02-003 — Capacidad agregada suficiente solo después de reconciliar la carga

- **Categoría:** Capacidad y viabilidad.
- **Severidad:** MINOR.
- **Bloqueante:** NO, una vez resuelto `IPR-v02-001`.
- **Fuente/ID:** `docs/project/viabilidad.md`, tabla de capacidad.
- **Evidencia observada:** La capacidad neta es 6 h/día, 30 h/sprint y 90 h en tres sprints. Los márgenes nominales serían 64,5 h frente a 25,5 h, 63,5 h frente a 26,5 h o 67,5 h frente a 22,5 h.
- **Impacto:** Todos los escenarios agregados quedan por debajo de 90 h, pero el equipo no ha establecido cuál es la carga oficial ni se ha comprobado la distribución individual.
- **Acción recomendada:** Usar una única cifra aprobada y validarla contra el Excel y la cobertura del DoD.
- **Pregunta o decisión requerida:** ¿Las estimaciones de las historias incluyen pruebas, regresión, integración, documentación y revisión?
- **Propietario sugerido:** Equipo técnico y responsable de estimación.

### IPR-v02-004 — Diferencia no explicada entre capacidad neta y horas costeadas

- **Categoría:** Capacidad y costes.
- **Severidad:** MAJOR.
- **Bloqueante:** YES para una lectura conjunta de viabilidad y presupuesto.
- **Fuente/ID:** Tablas de capacidad y costes de `docs/project/viabilidad.md`.
- **Evidencia observada:** La capacidad neta suma 6 h/día, es decir, 30 h/semana. Las horas de gestión y desarrollo utilizadas en el cálculo económico suman 10,5 h/día, es decir, 52,5 h/semana.
- **Impacto:** No está definido si las 52,5 horas son horas económicas contratadas, horas brutas de participación o una base distinta de las 30 horas netas de ejecución. No puede relacionarse directamente el coste con la carga de historias.
- **Acción recomendada:** Documentar la relación entre horas base, deducciones, capacidad neta, horas de gestión, horas de desarrollo y horas facturadas.
- **Pregunta o decisión requerida:** ¿Las 52,5 horas costeadas son una base económica fija del equipo durante el sprint, independiente de las 30 horas netas de ejecución?
- **Propietario sugerido:** Responsable financiero y Scrum Master.

### IPR-v02-005 — Coste semanal y total con soporte aritmético

- **Categoría:** Costes.
- **Severidad:** MINOR.
- **Bloqueante:** NO para la aritmética; YES para relacionarlo con la carga oficial.
- **Fuente/ID:** Tabla de costes y fórmula de `docs/project/viabilidad.md`.
- **Evidencia observada:** PO: `5 × (0,5 + 2) × 27 = 337,50 €`; SM: `5 × (0,5 + 1) × 23 = 172,50 €`; Lead Tech: `5 × (1 + 1) × 35 = 350,00 €`; QA/DevOps: `5 × (1 + 1) × 29 = 290,00 €`; Dev: `5 × (0,5 + 1) × 23 = 172,50 €`. La suma es `1.322,50 €` y por tres sprints `3.967,50 €`.
- **Impacto:** El importe es reproducible con la fórmula declarada, pero no se demuestra que el coste sea variable con las 25,5 h-p ni que esté distribuido por historia.
- **Acción recomendada:** Declarar si el importe es un coste fijo de mantener el equipo durante tres sprints o un coste imputado al esfuerzo de historias.
- **Pregunta o decisión requerida:** ¿El presupuesto de 3.967,50 € cubre el calendario completo aunque la carga de historias sea inferior a la capacidad?
- **Propietario sugerido:** Responsable financiero.

## 5. Aritmética y observaciones de capacidad/recursos

### 5.1. Carga extraída de las especificaciones

| Prioridad | Historias | Total |
|---|---|---:|
| Must | `US-01`, `US-02`, `US-04`, `US-05`, `US-06`, `US-09`, `US-10`, `US-12`, `US-13`, `US-17` | 17,0 h-p |
| Should | `US-03`, `US-07`, `US-08`, `US-14`, `US-15`, `US-16` | 8,0 h-p |
| Could | `US-11` | 1,5 h-p |
| **Total** | **17 historias** | **25,5 h-p** |

Esta es la suma historia por historia de las estimaciones visibles en `specs/`.

### 5.2. Capacidad efectiva

Según `viabilidad.md`:

- Scrum Master: 1 h/día.
- Product Owner: 2 h/día.
- DevOps/QA: 1 h/día.
- Lead Tech: 1 h/día.
- Developer: 1 h/día.
- Total: 6 h/día.
- Sprint de 5 días: `6 × 5 = 30 h`.
- Tres sprints: `3 × 30 = 90 h`.

Comparaciones posibles, manteniendo sus fuentes separadas:

| Carga de referencia | Cálculo | Margen nominal frente a 90 h |
|---:|---:|---:|
| 25,5 h-p | `90 - 25,5` | 64,5 h |
| 26,5 h | `90 - 26,5` | 63,5 h |
| 22,5 h | `90 - 22,5` | 67,5 h |

No es válido presentar uno de estos márgenes como resultado oficial hasta que el equipo reconcilie las tres cifras.

### 5.3. Límites

- La capacidad agregada no demuestra capacidad por persona, rol o sprint.
- No se aporta el Excel para verificar la asignación individual.
- No se sabe si las estimaciones incluyen todas las actividades del DoD.
- Las horas de coste no son automáticamente horas netas de ejecución.
- No se añade ningún factor de foco o reserva no declarado.

## 6. Dependencias y observaciones de capacidades

### 6.1. Dependencias

Las relaciones principales observadas son:

- `US-01 → US-02`, `US-03`, `US-16` y `US-17`.
- `US-12 → US-13 → US-17`.
- `US-04` y `US-09` → `US-05`.
- `US-04` y `US-06` → `US-11`.
- `US-09 → US-07`.
- `US-07` y `US-09` → `US-08`.
- `US-07 → US-10`.

No se observan ciclos en el grafo de `Predecessors`. La dirección `US-12 → US-13 → US-17` es coherente con que la compra dependa de la capacidad de modificar stock.

Se acepta como supuesto comunicado que el Excel respeta estas dependencias. No se verifica la fecha de terminación de cada predecesora ni la regla de solapamiento dentro de un sprint.

### 6.2. Horizonte

Tres sprints de una semana son compatibles con los 90 h de capacidad declarada en términos agregados. La tabla local de `viabilidad.md` propone 9, 9 y 8,5 h, pero esos totales suman 26,5 h y no están trazados a las historias. Por ello, la duración es conocida, pero la viabilidad temporal de la asignación no está demostrada.

No se crea una asignación alternativa ni se decide qué historias pertenecen a cada sprint.

### 6.3. Capacidades y posibles cuellos de botella

Las historias requieren autenticación y autorización, catálogo, inventario, stock, compra simulada, eventos y aforo, foro y moderación, notificaciones, pruebas y verificación de NFR. `viabilidad.md` define los roles PO, SM, Lead Tech, DevOps/QA y Developer, pero no aporta la asignación de cada capacidad a cada historia. Debe verificarse en el Excel.

## 7. Resultado de costes

- **Resultado aritmético:** Soportado para el coste del equipo durante tres sprints.
- **Coste semanal:** `1.322,50 €`.
- **Coste total:** `3.967,50 €`.
- **Roles y tarifas:** PO `27 €/h`, SM `23 €/h`, Lead Tech `35 €/h`, QA/DevOps `29 €/h`, Developer `23 €/h`.
- **Fórmula:** `5 días × (horas de gestión + horas de desarrollo) × tarifa`.
- **Comprobación:** La suma de los cinco costes semanales es `1.322,50 €`; `3 × 1.322,50 € = 3.967,50 €`.
- **Presupuesto:** No se proporciona un límite presupuestario independiente.
- **Supuesto:** El importe es el coste del equipo durante tres semanas usando las horas económicas documentadas.
- **Desconocido:** No se explica la relación entre las 52,5 horas semanales costeadas y las 30 horas semanales netas de capacidad.
- **Conclusión:** El cálculo de costes tiene soporte aritmético según los roles definidos, pero su relación con la carga de las historias y con la capacidad neta requiere aclaración.

## 8. Preguntas y próximas acciones sugeridas

| Acción o pregunta | Propietario sugerido | Disparador de validación | Bloqueante |
|---|---|---|---|
| Reconciliar 25,5 h-p, 26,5 h y 22,5 h | Product Owner y responsable de estimación | Fuente única con suma por historia y por sprint | Sí |
| Aportar la versión del Excel | Scrum Master | Extracto con historia, sprint, esfuerzo y predecesoras | Sí |
| Confirmar la regla de finalización de predecesoras | Equipo técnico | Regla documentada de orden o solapamiento | Sí para validar secuencia |
| Explicar 30 h netas frente a 52,5 h costeadas | Responsable financiero y Scrum Master | Unidades y fórmula relacionadas | Sí para viabilidad conjunta |
| Confirmar cobertura del DoD en la carga | Equipo técnico y QA | Estimaciones revisadas por actividad | No inicialmente |
| Confirmar si el coste es fijo por calendario | Responsable financiero | Decisión presupuestaria registrada | No para la aritmética |
| Mantener como resueltos `RR-001` a `RR-009` | Equipo de requisitos | Referencia al archivo de trazabilidad | No, según la disposición comunicada |

## 9. Disposición RECHECK

Esta ejecución no es un `RECHECK` formal: el modo solicitado es `READINESS`. No obstante, se registra la evolución respecto de `initial-planning-review-v01.md` porque la revisión actual aporta evidencia local actualizada.

| Hallazgo previo | Decisión humana | Evidencia modificada | Estado verificado | Impacto restante |
|---|---|---|---|---|
| `IPR-v01-001` | El equipo comunica 25,5 h como carga | `viabilidad.md` sigue mostrando 26,5 h por sprint y 22,5 h en la conclusión | No verificado como resuelto | Reaparece como `IPR-v02-001` |
| `IPR-v01-002` | La distribución está en un Excel externo y respeta predecesoras | No se aporta el Excel | Aceptado como supuesto, no verificado | Reaparece como `IPR-v02-002` |
| `IPR-v01-004` | Se aportó `viabilidad.md` con roles y tarifas | Tabla de costes y fórmula disponibles | Aritmética verificada; relación con capacidad pendiente | Reaparece acotado como `IPR-v02-004` y `IPR-v02-005` |
| `RR-001` a `RR-009` | El equipo comunica que fueron procesados y justificados | No se aporta el archivo de trazabilidad | Aceptados como resueltos para esta revisión | Sin impacto adicional en este informe |

## 10. Consejo final y declaración de límites

El resultado es **NOT_READY** para declarar preparados, sin aclaraciones adicionales, los insumos de una hipótesis de planificación de las 17 historias en tres sprints.

La evidencia permite afirmar que:

1. La capacidad efectiva neta declarada es de 90 horas en tres sprints.
2. Las especificaciones suman 25,5 h-p, inferior a 90 h en términos agregados.
3. `viabilidad.md` contiene dos totales incompatibles: 26,5 h en la distribución por sprint y 22,5 h en la conclusión.
4. El mensaje del equipo indica 25,5 h como carga, pero esa cifra no está reflejada de forma coherente en `viabilidad.md`.
5. Los `Predecessors` no muestran ciclos evidentes.
6. El coste semanal de 1.322,50 € y el total de 3.967,50 € están correctamente calculados con la fórmula y tarifas documentadas.
7. La asignación del Excel se acepta como supuesto comunicado, pero no se ha verificado directamente.

Para alcanzar `READY` o `READY_WITH_NON_BLOCKING_QUESTIONS`, el equipo debe reconciliar las tres cargas, hacer verificable la asignación temporal y aclarar las unidades de capacidad y coste. Esta revisión no selecciona historias, no asigna recursos, no crea un calendario ni aprueba un compromiso.

Las fuentes existentes no han sido modificadas. Solo se ha creado este nuevo informe en `docs/project/reviews/initial-planning/initial-planning-review-v02.md`. No se aprueba ningún plan, baseline, presupuesto, asignación de recursos ni criterio de calidad.
