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
- **Versión del informe:** `initial-planning-review-v03.md`.
- **Informe previo:** `docs/project/reviews/initial-planning/initial-planning-review-v02.md`.
- **Disposición humana comunicada:** Los hallazgos `RR-001` a `RR-009` se consideran procesados y justificados por el equipo.
- **Asignación temporal comunicada:** La distribución de las 17 historias se gestiona externamente en el Excel del equipo y respeta los `Predecessors`; el Excel no fue aportado para esta revisión.
- **Fuentes revisadas:** Las siete especificaciones de `specs/`, `specs/product/goals.md`, `specs/product/mission.md`, `docs/project/viabilidad.md`, `docs/quality/definition-of-ready.md` y `docs/quality/definition-of-done.md`.
- **Fuente de trazabilidad de `RR-001` a `RR-009`:** No identificada como archivo local en la ruta revisada; se acepta la disposición comunicada por el equipo para esta ejecución, sin volver a evaluar esos hallazgos.
- **Commit revisado:** No proporcionado.

## 2. Resumen

**Resultado consultivo: NOT_READY.**

La capacidad efectiva declarada es de 90 horas netas para los tres sprints. Las 17 especificaciones suman **25,5 horas-persona**, que dejarían un margen nominal de **64,5 horas** frente a la capacidad agregada.

La evidencia local sigue conteniendo una inconsistencia de carga:

- Las especificaciones suman **25,5 h-p**.
- La tabla de distribución temporal de `viabilidad.md` suma **26,5 h** (`9 + 9 + 8,5`).
- El mensaje del equipo comunica **25,5 h** como carga de referencia.

Además, `viabilidad.md` contiene un error aritmético interno: declara un esfuerzo de **26,5 horas** y un margen de **63,5 horas**, pero su conclusión afirma un colchón de **67,5 horas**, que solo correspondería a una carga de 22,5 horas.

El grafo de `Predecessors` no presenta ciclos evidentes. La distribución del Excel se acepta como supuesto comunicado, pero no se verifica al no estar disponible. El coste de **1.322,50 €/semana** y **3.967,50 € en tres sprints** tiene soporte aritmético según los roles y tarifas documentados, aunque debe aclararse su relación con las 30 horas netas semanales.

**Bloqueos:** carga oficial no reconciliada; error de margen en la fuente de viabilidad; asignación externa no verificable; relación no explicitada entre capacidad neta y horas costeadas.

## 3. Inventario de evidencias y matriz de compatibilidad

| Dimensión | Estado | Evidencia | Límite |
|---|---|---|---|
| Baseline y alcance | Verificable | Las siete épicas declaran `Versión Inicial`; se cubren `US-01` a `US-17` | No se aportó un manifiesto formal |
| Requisitos y disposición previa | Parcialmente verificable | El equipo comunica que `RR-001` a `RR-009` están resueltos | No se identificó el archivo de trazabilidad local |
| Identificación de historias | Verificable | Se identifican 17 historias con estimación y `Predecessors` | El Excel no está disponible |
| Carga de especificaciones | Verificable | La suma de las historias es 25,5 h-p | No coincide con el total por sprint local |
| Distribución por sprint | Parcialmente verificable | `viabilidad.md` registra 9, 9 y 8,5 h | Suma 26,5 h y no muestra historias asociadas |
| Capacidad agregada | Verificable | 6 h/día, 30 h/sprint y 90 h en tres sprints | Debe separarse de las horas costeadas |
| Capacidad individual | Parcialmente verificable | La tabla declara 1, 2, 1, 1 y 1 h/día por miembro | No hay asignación de historias por persona |
| Horizonte temporal | Parcialmente verificable | Se declaran 3 sprints de 1 semana | No se comprueba la asignación exacta del Excel |
| Dependencias | Parcialmente verificable | `Predecessors` está presente y no muestra ciclos evidentes | No se verifica su materialización temporal |
| Costes | Parcialmente verificable | Roles, horas, tarifas y fórmula están documentados | La relación con capacidad neta requiere aclaración |
| DoR y DoD | Parcialmente verificable | Existen definiciones documentadas | No se explicita la cobertura del DoD en las estimaciones |
| Viabilidad global | No preparada | Hay margen agregado, pero las cargas y el margen publicado no son coherentes | Falta una base numérica única |

## 4. Hallazgos

### IPR-v03-001 — Carga oficial no reconciliada entre especificaciones y viabilidad

- **Categoría:** Estimación y alcance.
- **Severidad:** CRITICAL.
- **Bloqueante:** YES.
- **Fuente/ID:** Estimaciones de `US-01` a `US-17`; tabla de sprints de `docs/project/viabilidad.md`; disposición comunicada de 25,5 h.
- **Evidencia observada:** Las especificaciones suman 25,5 h-p, mientras que `viabilidad.md` suma 26,5 h en los tres sprints. El equipo comunica 25,5 h como carga, pero no se muestra la reconciliación historia por historia.
- **Impacto:** No existe una carga base única para evaluar el margen, la asignación temporal y la relación entre esfuerzo y coste.
- **Acción recomendada:** Crear una tabla oficial que relacione cada historia con su estimación y sprint, y que concilie el total de historias con los subtotales de sprint.
- **Pregunta o decisión requerida:** ¿La carga oficial de las 17 historias es 25,5 h-p o 26,5 h? Si es 26,5 h, ¿qué 1 hora adicional se está incluyendo?
- **Propietario sugerido:** Product Owner y responsable de estimación.

### IPR-v03-002 — Margen aritmético incorrecto en la conclusión de viabilidad

- **Categoría:** Aritmética y capacidad.
- **Severidad:** MAJOR.
- **Bloqueante:** YES.
- **Fuente/ID:** `docs/project/viabilidad.md`, sección «Estimación del Proyecto y Viabilidad».
- **Evidencia observada:** El documento declara `26,5 h` de esfuerzo, `90,0 h` de capacidad y `63,5 h` de margen, que es correcto. Sin embargo, la conclusión afirma un colchón de `67,5 h`.
- **Impacto:** La conclusión presenta una cifra que no corresponde al esfuerzo declarado y puede inducir a una evaluación incorrecta del margen.
- **Acción recomendada:** Corregir la conclusión para que use 63,5 h, o corregir simultáneamente el esfuerzo si la cifra oficial fuese otra.
- **Pregunta o decisión requerida:** ¿Debe considerarse oficial el margen de 63,5 h asociado a 26,5 h, o debe cambiarse también la carga oficial?
- **Propietario sugerido:** Responsable de planificación.

### IPR-v03-003 — Asignación temporal externa no verificable

- **Categoría:** Horizonte y planificación temporal.
- **Severidad:** MAJOR.
- **Bloqueante:** YES.
- **Fuente/ID:** Comunicación sobre el Excel externo; `Predecessors` de las especificaciones.
- **Evidencia observada:** Se afirma que el Excel distribuye las 17 historias en tres sprints y respeta las predecesoras, pero el archivo no está disponible. `viabilidad.md` solo muestra totales por sprint.
- **Impacto:** No puede comprobarse la carga por sprint, la terminación de predecesoras, la carga individual ni la ausencia de cuellos de botella.
- **Acción recomendada:** Aportar un extracto versionado con historia, sprint, estimación, rol o responsable y verificación de predecesoras.
- **Pregunta o decisión requerida:** ¿Qué versión del Excel constituye la asignación revisada y qué regla determina que una predecesora está terminada?
- **Propietario sugerido:** Scrum Master y responsable de planificación.

### IPR-v03-004 — Diferencia no explicada entre capacidad neta y horas costeadas

- **Categoría:** Capacidad y costes.
- **Severidad:** MAJOR.
- **Bloqueante:** YES para una lectura conjunta de viabilidad y presupuesto.
- **Fuente/ID:** Tablas de capacidad y costes de `docs/project/viabilidad.md`.
- **Evidencia observada:** La capacidad neta es 6 h/día, o 30 h/semana. Las horas de gestión y desarrollo utilizadas para el coste suman 10,5 h/día, o 52,5 h/semana.
- **Impacto:** No se sabe si las 52,5 horas son una base económica bruta, horas contratadas o una magnitud distinta de la capacidad neta de ejecución.
- **Acción recomendada:** Documentar la relación entre horas base, deducciones, capacidad neta, horas de gestión, horas de desarrollo y horas facturadas.
- **Pregunta o decisión requerida:** ¿Las 52,5 horas costeadas son un coste fijo del equipo durante el sprint, independiente de las 30 horas netas?
- **Propietario sugerido:** Responsable financiero y Scrum Master.

### IPR-v03-005 — Coste semanal y total con soporte aritmético

- **Categoría:** Costes.
- **Severidad:** MINOR.
- **Bloqueante:** NO para la aritmética; YES para relacionarlo con la carga oficial.
- **Fuente/ID:** Tabla de costes y fórmula de `docs/project/viabilidad.md`.
- **Evidencia observada:** PO `337,50 €`, SM `172,50 €`, Lead Tech `350,00 €`, QA/DevOps `290,00 €` y Dev `172,50 €`; la suma es `1.322,50 €`, y `3 × 1.322,50 € = 3.967,50 €`.
- **Impacto:** El importe es reproducible, pero no se demuestra que esté imputado a las 25,5 h-p o a las 26,5 h de la tabla por sprint.
- **Acción recomendada:** Declarar si el presupuesto es fijo por calendario o variable según horas asignadas a historias.
- **Pregunta o decisión requerida:** ¿El presupuesto de 3.967,50 € cubre el mantenimiento del equipo durante tres sprints con independencia de la carga de historias?
- **Propietario sugerido:** Responsable financiero.

## 5. Aritmética y observaciones de capacidad/recursos

### 5.1. Carga extraída de las especificaciones

| Prioridad | Historias | Total |
|---|---|---:|
| Must | `US-01`, `US-02`, `US-04`, `US-05`, `US-06`, `US-09`, `US-10`, `US-12`, `US-13`, `US-17` | 17,0 h-p |
| Should | `US-03`, `US-07`, `US-08`, `US-14`, `US-15`, `US-16` | 8,0 h-p |
| Could | `US-11` | 1,5 h-p |
| **Total** | **17 historias** | **25,5 h-p** |

### 5.2. Capacidad efectiva declarada

Según `viabilidad.md`, la capacidad diaria neta es:

- Scrum Master: 1 h/día.
- Product Owner: 2 h/día.
- DevOps/QA: 1 h/día.
- Lead Tech: 1 h/día.
- Developer: 1 h/día.
- **Total:** 6 h/día.
- **Por sprint:** `6 × 5 = 30 h`.
- **Tres sprints:** `3 × 30 = 90 h`.

Comparaciones numéricas, manteniendo sus fuentes separadas:

| Carga de referencia | Cálculo | Margen nominal frente a 90 h |
|---:|---:|---:|
| 25,5 h-p | `90 - 25,5` | 64,5 h |
| 26,5 h | `90 - 26,5` | 63,5 h |

La cifra de 67,5 h no es compatible con una carga de 26,5 h; solo resulta de `90 - 22,5`.

### 5.3. Límites

- La comparación agregada no demuestra capacidad por persona, rol o sprint.
- El Excel no está disponible para verificar asignaciones individuales.
- No se sabe si las estimaciones incluyen pruebas, regresión, integración, documentación y revisión del DoD.
- Las horas costeadas no son automáticamente horas netas de ejecución.
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

No se observan ciclos en el grafo de `Predecessors`. Se acepta como supuesto comunicado que el Excel respeta estas dependencias, pero no se verifica el momento de terminación de cada predecesora ni la regla de solapamiento dentro de un sprint.

### 6.2. Horizonte temporal

Tres sprints de una semana son compatibles con los 90 h de capacidad declarada en términos agregados. La distribución local propone 9, 9 y 8,5 h, que suma 26,5 h; no se dispone de la trazabilidad de esas cifras a historias. Por ello, la duración es conocida, pero la viabilidad temporal de la asignación no está demostrada.

No se crea una asignación alternativa ni se decide qué historias pertenecen a cada sprint.

### 6.3. Capacidades y posibles cuellos de botella

Las historias requieren autenticación y autorización, catálogo, inventario, stock, compra simulada, eventos y aforo, foro y moderación, notificaciones, pruebas y verificación de NFR. `viabilidad.md` define PO, SM, Lead Tech, DevOps/QA y Developer, pero no asigna cada capacidad a cada historia. Esa relación debe verificarse en el Excel.

## 7. Resultado de costes

- **Resultado aritmético:** Soportado para el coste del equipo durante tres sprints.
- **Coste semanal:** `1.322,50 €`.
- **Coste total:** `3.967,50 €`.
- **Roles y tarifas:** PO `27 €/h`, SM `23 €/h`, Lead Tech `35 €/h`, QA/DevOps `29 €/h`, Developer `23 €/h`.
- **Fórmula:** `5 días × (horas de gestión + horas de desarrollo) × tarifa`.
- **Comprobación:** La suma de los cinco costes semanales es `1.322,50 €`; `3 × 1.322,50 € = 3.967,50 €`.
- **Presupuesto:** No se proporciona un límite presupuestario independiente.
- **Supuesto:** El importe representa el coste del equipo durante tres semanas usando las horas económicas documentadas.
- **Desconocido:** No se explica la relación entre las 52,5 horas semanales costeadas y las 30 horas semanales netas de capacidad.
- **Conclusión:** El cálculo de costes tiene soporte aritmético según los roles definidos, pero su relación con la carga oficial y la capacidad neta requiere aclaración.

## 8. Preguntas y próximas acciones sugeridas

| Acción o pregunta | Propietario sugerido | Disparador de validación | Bloqueante |
|---|---|---|---|
| Reconciliar 25,5 h-p y 26,5 h | Product Owner y responsable de estimación | Fuente única con suma por historia y por sprint | Sí |
| Corregir el margen 67,5/63,5 h | Responsable de planificación | Conclusión coherente con la carga oficial | Sí |
| Aportar la versión del Excel | Scrum Master | Extracto con historia, sprint, esfuerzo y predecesoras | Sí |
| Explicar 30 h netas frente a 52,5 h costeadas | Responsable financiero y Scrum Master | Unidades y fórmula relacionadas | Sí |
| Confirmar cobertura del DoD en la carga | Equipo técnico y QA | Estimaciones revisadas por actividad | No inicialmente |
| Confirmar si el coste es fijo por calendario | Responsable financiero | Decisión presupuestaria registrada | No para la aritmética |
| Mantener como resueltos `RR-001` a `RR-009` | Equipo de requisitos | Referencia al archivo de trazabilidad | No, según la disposición comunicada |

## 9. Disposición RECHECK

Esta ejecución no es un `RECHECK` formal: el modo solicitado es `READINESS`. Se registra la evolución respecto de `initial-planning-review-v02.md` porque la fuente local fue revisada nuevamente.

| Hallazgo previo | Decisión humana | Evidencia modificada | Estado verificado | Impacto restante |
|---|---|---|---|---|
| `IPR-v02-001` | El equipo comunica 25,5 h como carga | `viabilidad.md` mantiene 26,5 h por sprint | No resuelto documentalmente | Reaparece como `IPR-v03-001` |
| `IPR-v02-002` | La distribución está en un Excel externo y respeta predecesoras | El Excel no se aporta | Aceptado como supuesto, no verificado | Reaparece como `IPR-v03-003` |
| `IPR-v02-004` | Se mantiene la fuente de capacidad y costes | Siguen siendo 30 h netas y 52,5 h costeadas por semana | Relación pendiente | Reaparece como `IPR-v03-004` |
| `IPR-v02-005` | Se mantienen roles, tarifas y fórmula | El importe sigue siendo reproducible | Verificado aritméticamente | Reaparece acotado como `IPR-v03-005` |
| `RR-001` a `RR-009` | El equipo comunica que fueron procesados y justificados | No se aporta el archivo de trazabilidad | Aceptados como resueltos para esta revisión | Sin impacto adicional en este informe |

## 10. Consejo final y declaración de límites

El resultado es **NOT_READY** para declarar preparados, sin aclaraciones adicionales, los insumos de una hipótesis de planificación de las 17 historias en tres sprints.

La evidencia permite afirmar que:

1. La capacidad efectiva neta declarada es de 90 horas en tres sprints.
2. Las especificaciones suman 25,5 h-p, inferior a 90 h en términos agregados.
3. La tabla de sprints de `viabilidad.md` suma 26,5 h.
4. La conclusión de `viabilidad.md` contiene un margen incorrecto de 67,5 h para una carga declarada de 26,5 h; el margen correspondiente es 63,5 h.
5. Los `Predecessors` no muestran ciclos evidentes.
6. El coste semanal de 1.322,50 € y el total de 3.967,50 € están correctamente calculados con la fórmula y tarifas documentadas.
7. La asignación del Excel se acepta como supuesto comunicado, pero no se ha verificado directamente.

Para alcanzar `READY` o `READY_WITH_NON_BLOCKING_QUESTIONS`, el equipo debe reconciliar las cargas, corregir el margen publicado, hacer verificable la asignación temporal y aclarar las unidades de capacidad y coste. Esta revisión no selecciona historias, no asigna recursos, no crea un calendario ni aprueba un compromiso.

Las fuentes existentes no han sido modificadas. Solo se ha creado este nuevo informe en `docs/project/reviews/initial-planning/initial-planning-review-v03.md`. No se aprueba ningún plan, baseline, presupuesto, asignación de recursos ni criterio de calidad.
