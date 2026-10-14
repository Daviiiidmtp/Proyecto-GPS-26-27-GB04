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
- **Versión del informe:** `initial-planning-review-v01.md`.
- **Informe previo:** `docs/reports/requirements-report-v01.md`, revisión de requisitos `v01`.
- **Disposición humana comunicada:** Los hallazgos `RR-001` a `RR-009` se consideran procesados y justificados por el equipo.
- **Asignación temporal:** Se comunica que la distribución de las 17 historias se gestiona externamente en el Excel del equipo y respeta los `Predecessors`; el Excel no fue aportado para esta revisión.
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

La capacidad efectiva declarada es de 90 horas netas para los tres sprints. La suma de las estimaciones de las 17 historias extraídas de `specs/` es **25,5 horas-persona**, por lo que, tomando ambas magnitudes como comparables, existe un margen agregado nominal de **64,5 horas**.

No obstante, `docs/project/viabilidad.md` utiliza **22,5 horas** como carga total y calcula un margen de **67,5 horas**. La diferencia de **3 horas** no está explicada. Esta contradicción afecta a la carga base de la planificación y es bloqueante hasta que el equipo confirme qué historias o estimaciones componen el total de 22,5 horas.

La secuencia declarada de `Predecessors` no presenta ciclos evidentes y la distribución externa se acepta como supuesto de trabajo. Sin el Excel no puede verificarse la asignación por sprint, la carga individual ni el orden temporal concreto.

El cálculo monetario semanal de **1.322,50 €** y el total de **3.967,50 €** sí tienen soporte aritmético con las horas de gestión y desarrollo y las tarifas por rol de `viabilidad.md`. Sin embargo, esas horas facturadas suman 52,5 horas por semana, mientras que la capacidad efectiva neta indicada es de 30 horas por semana. La relación entre ambas unidades y el alcance que se costea debe quedar explícita.

**Bloqueos:** inconsistencia entre 25,5 h-p y 22,5 h; falta de verificación documental del Excel externo; relación no explicitada entre capacidad neta, horas de desarrollo, horas de gestión y horas costeadas.

## 3. Inventario de evidencias y matriz de compatibilidad

| Dimensión | Estado | Evidencia | Límite |
|---|---|---|---|
| Baseline y alcance | Verificable | Las siete épicas declaran `Versión Inicial`; las especificaciones cubren `US-01` a `US-17` | No se aportó un manifiesto formal |
| Requisitos y disposición previa | Parcialmente verificable | El equipo comunica que `RR-001` a `RR-009` están resueltos | No se identificó el archivo de trazabilidad local |
| Identificación de historias | Verificable | Se identifican 17 historias con estimación y `Predecessors` | La asignación de sprints está fuera de las especificaciones |
| Estimación de carga | No compatible | Las especificaciones suman 25,5 h-p; `viabilidad.md` declara 22,5 h | Falta la reconciliación de 3 horas |
| Capacidad agregada | Verificable | La tabla de capacidad declara 6 h/día y 30 h/sprint; 3 sprints dan 90 h | Debe distinguirse capacidad neta de horas costeadas |
| Capacidad individual | Parcialmente verificable | La tabla declara 1, 2, 1, 1 y 1 h/día por miembro | No hay asignación de historias por persona |
| Horizonte temporal | Parcialmente verificable | Se declara un horizonte de 3 sprints de 1 semana | El Excel externo no está disponible para comprobar cargas y orden |
| Dependencias | Parcialmente verificable | `Predecessors` está presente en las historias y no muestra ciclos evidentes | No se puede comprobar su materialización temporal |
| Costes | Parcialmente verificable | Roles, horas diarias, tarifas y fórmulas están en `viabilidad.md` | La base de horas costeadas frente a capacidad neta requiere aclaración |
| DoR y DoD | Parcialmente verificable | Existen DoR y DoD documentados | La cobertura de actividades en las estimaciones no está explicitada |
| Viabilidad global | No preparada | Hay margen agregado si se usa 25,5 h frente a 90 h | La inconsistencia de carga impide una conclusión limpia |

## 4. Hallazgos

### IPR-v01-001 — Inconsistencia entre la carga de las especificaciones y la carga de viabilidad

- **Categoría:** Estimación y alcance.
- **Severidad:** CRITICAL.
- **Bloqueante:** YES.
- **Fuente/ID:** `US-01` a `US-17` en `specs/`; `docs/project/viabilidad.md`, sección «Estimación del Proyecto y Viabilidad».
- **Evidencia observada:** La suma de las 17 estimaciones declaradas en las especificaciones es 25,5 h-p. `viabilidad.md` declara 22,5 horas y calcula el margen con esa cifra.
- **Impacto:** La carga de referencia para la planificación no es única. El margen comunicado puede estar sobreestimado en 3 horas y no puede saberse si falta una historia, una estimación o una decisión de alcance.
- **Acción recomendada:** Reconciliar la suma historia por historia con la tabla de viabilidad y registrar la cifra aprobada y su alcance exacto.
- **Pregunta o decisión requerida:** ¿La carga oficial de las 17 historias es 25,5 h-p o 22,5 h? Si son 22,5 h, ¿qué 3 horas se excluyen y por qué?
- **Propietario sugerido:** Product Owner y responsable de estimación.

### IPR-v01-002 — La asignación temporal externa no es verificable en esta revisión

- **Categoría:** Horizonte y planificación temporal.
- **Severidad:** MAJOR.
- **Bloqueante:** YES.
- **Fuente/ID:** Comunicación del equipo sobre el Excel externo; `Predecessors` en `specs/`.
- **Evidencia observada:** Se afirma que las 17 historias están distribuidas en tres sprints respetando sus predecesoras, pero el Excel no está disponible entre las fuentes revisadas.
- **Impacto:** No puede comprobarse la carga de cada sprint, la precedencia efectiva, la ausencia de sobreasignación individual ni el cumplimiento de las tres semanas.
- **Acción recomendada:** Aportar el extracto versionado del Excel con historia, sprint, estimación, rol o responsable y comprobación de predecesoras; no se genera una asignación alternativa en esta revisión.
- **Pregunta o decisión requerida:** ¿Qué versión del Excel constituye la asignación temporal revisada y qué regla determina que una predecesora está terminada?
- **Propietario sugerido:** Scrum Master y responsable de planificación.

### IPR-v01-003 — Capacidad efectiva agregada suficiente bajo la cifra reconciliada

- **Categoría:** Capacidad.
- **Severidad:** MINOR.
- **Bloqueante:** NO, una vez resuelto `IPR-v01-001`.
- **Fuente/ID:** `docs/project/viabilidad.md`, tabla de capacidad.
- **Evidencia observada:** La capacidad neta es 6 h/día de equipo, 30 h por sprint y 90 h en tres sprints. Frente a 25,5 h-p, el margen nominal sería 64,5 h; frente a 22,5 h, 67,5 h.
- **Impacto:** El total agregado no parece saturar al equipo, pero no prueba la viabilidad por persona, rol o sprint ni la inclusión de todo el trabajo del DoD.
- **Acción recomendada:** Mantener el cálculo como comprobación agregada y validarlo contra la asignación externa y la cobertura de actividades.
- **Pregunta o decisión requerida:** ¿Las estimaciones de historias incluyen pruebas, regresión, integración, documentación y revisión, o esas actividades consumen parte de las 90 horas?
- **Propietario sugerido:** Equipo técnico y responsable de estimación.

### IPR-v01-004 — Diferencia no explicada entre capacidad neta y horas costeadas

- **Categoría:** Capacidad y costes.
- **Severidad:** MAJOR.
- **Bloqueante:** YES para una lectura conjunta de viabilidad y presupuesto.
- **Fuente/ID:** `docs/project/viabilidad.md`, tablas «Cálculo de la Capacidad» y «Presupuesto y Costes por Rol».
- **Evidencia observada:** La capacidad efectiva suma 6 h/día, es decir, 30 h por semana. La tabla de costes usa horas de gestión y desarrollo que suman 10,5 h/día y 52,5 h por semana.
- **Impacto:** No está explícito si las 52,5 horas son horas contratadas/valoradas, disponibilidad bruta, o una base económica distinta de las 30 horas netas de ejecución. Sin esa distinción, no puede relacionarse directamente el presupuesto con el esfuerzo del alcance.
- **Acción recomendada:** Documentar la relación entre horas base, horas descontadas, capacidad neta, horas de gestión, horas de desarrollo y horas facturadas; indicar qué magnitud se usa para costear el proyecto.
- **Pregunta o decisión requerida:** ¿Las 52,5 horas semanales costeadas representan disponibilidad económica del equipo aunque solo 30 sean horas netas de ejecución, o existe doble contabilización?
- **Propietario sugerido:** Responsable financiero y Scrum Master.

### IPR-v01-005 — Coste semanal y total con soporte aritmético condicionado al alcance

- **Categoría:** Costes.
- **Severidad:** MINOR.
- **Bloqueante:** NO para la aritmética; YES para su interpretación como coste de la carga de 17 historias.
- **Fuente/ID:** `docs/project/viabilidad.md`, tabla de tarifas y fórmula de coste.
- **Evidencia observada:** Se verifica:
  - Product Owner: `5 × (0,5 + 2) × 27 € = 337,50 €`.
  - Scrum Master: `5 × (0,5 + 1) × 23 € = 172,50 €`.
  - Lead Tech: `5 × (1 + 1) × 35 € = 350,00 €`.
  - DevOps/QA: `5 × (1 + 1) × 29 € = 290,00 €`.
  - Developer: `5 × (0,5 + 1) × 23 € = 172,50 €`.
  - Total semanal: `1.322,50 €`.
  - Total de tres sprints: `3 × 1.322,50 € = 3.967,50 €`.
- **Impacto:** La aritmética del presupuesto es consistente con la fórmula declarada, pero no puede confirmarse que la base de horas corresponda exactamente a la carga aprobada de 25,5 h-p.
- **Acción recomendada:** Conservar el cálculo como coste del equipo durante tres semanas y añadir su relación con el esfuerzo de historias y con la capacidad neta.
- **Pregunta o decisión requerida:** ¿El presupuesto cubre el coste fijo del equipo durante los tres sprints independientemente de la carga de historias?
- **Propietario sugerido:** Responsable financiero.

## 5. Aritmética y observaciones de capacidad/recursos

### 5.1. Carga extraída de las 17 historias

| Prioridad | Historias | Total |
|---|---|---:|
| Must | `US-01`, `US-02`, `US-04`, `US-05`, `US-06`, `US-09`, `US-10`, `US-12`, `US-13`, `US-17` | 17,0 h-p |
| Should | `US-03`, `US-07`, `US-08`, `US-14`, `US-15`, `US-16` | 8,0 h-p |
| Could | `US-11` | 1,5 h-p |
| **Total** | **17 historias** | **25,5 h-p** |

La suma se obtiene de las estimaciones individuales declaradas en las especificaciones. Todas las unidades de esta tabla son horas-persona.

### 5.2. Capacidad efectiva declarada

Según `viabilidad.md`:

- Scrum Master: `1 h/día`.
- Product Owner: `2 h/día`.
- DevOps/QA: `1 h/día`.
- Lead Tech: `1 h/día`.
- Developer: `1 h/día`.
- **Total:** `6 h/día`.
- **Por sprint:** `6 × 5 = 30 h`.
- **Tres sprints:** `3 × 30 = 90 h`.

Con las historias tal como aparecen en `specs/`:

```text
90 h netas - 25,5 h-p = 64,5 h de margen nominal
```

Con la cifra de `viabilidad.md`:

```text
90 h netas - 22,5 h = 67,5 h de margen nominal
```

Ambos cálculos son aritméticamente correctos por separado, pero no pueden coexistir como carga oficial de las mismas 17 historias sin explicar las 3 horas de diferencia.

### 5.3. Límites de capacidad

- La comparación agregada no prueba la capacidad por individuo.
- No se aporta la asignación del Excel para verificar cargas por sprint o por rol.
- No se determina si las estimaciones de historias incluyen todas las actividades del DoD.
- Las horas de gestión y desarrollo de la tabla de costes no son equivalentes, sin aclaración adicional, a las horas netas disponibles.
- No se inventa una reserva ni un factor de foco adicional: `viabilidad.md` ya declara la capacidad como neta.

## 6. Dependencias y observaciones de capacidades

### 6.1. Secuencia declarada

Las relaciones principales observadas son:

- `US-01 → US-02`, `US-03`, `US-16` y `US-17`.
- `US-12 → US-13 → US-17`.
- `US-04` y `US-09` → `US-05`.
- `US-04` y `US-06` → `US-11`.
- `US-09 → US-07`.
- `US-07` y `US-09` → `US-08`.
- `US-07 → US-10`.

No se observan ciclos en el grafo de `Predecessors`. La dependencia `US-17 → US-13` no aparece; la dirección declarada es `US-13 → US-17`, coherente con que la compra modifique el stock después de disponer de la capacidad de modificarlo.

### 6.2. Horizonte

El horizonte de tres sprints de una semana es compatible en duración con la capacidad declarada de 90 horas, pero la viabilidad temporal completa queda limitada al Excel externo. Se acepta como supuesto comunicado que dicho Excel respeta los `Predecessors`; queda pendiente validar la versión, la carga por sprint y la terminación efectiva de cada predecesora.

No se crea una asignación alternativa ni se decide qué historias pertenecen a cada sprint.

### 6.3. Capacidades requeridas

Las especificaciones requieren, como mínimo, autenticación y autorización, catálogo e inventario, eventos y aforo, foro y moderación, notificaciones, pruebas y verificación de requisitos no funcionales. La tabla de `viabilidad.md` identifica PO, SM, Lead Tech, DevOps/QA y Developer, pero no asigna capacidades de cada historia a esos roles. Esa relación debe verificarse en el Excel o en la fuente de planificación del equipo.

## 7. Resultado de costes

- **Resultado aritmético:** Soportado para el coste del equipo durante tres sprints.
- **Coste semanal declarado:** `1.322,50 €`.
- **Coste total declarado:** `3.967,50 €`.
- **Fórmula:** `5 días × (horas de gestión + horas de desarrollo) × tarifa por hora`.
- **Roles y tarifas:** PO `27 €/h`, SM `23 €/h`, Lead Tech `35 €/h`, DevOps/QA `29 €/h`, Developer `23 €/h`.
- **Comprobación:** La suma de los cinco costes semanales es `1.322,50 €`; multiplicada por tres semanas produce `3.967,50 €`.
- **Presupuesto declarado:** No se proporciona un límite presupuestario independiente.
- **Supuesto:** El coste es el coste fijo de mantener el equipo durante tres sprints, usando las horas de gestión y desarrollo indicadas.
- **Desconocido:** No está resuelto si las 52,5 horas semanales costeadas deben compararse con las 30 horas semanales netas de ejecución ni cómo se asigna el coste a las 17 historias.
- **Conclusión:** El cálculo tiene soporte aritmético según los roles y tarifas definidos, pero su interpretación como coste de la carga estimada queda condicionada a resolver `IPR-v01-004` y `IPR-v01-001`.

## 8. Preguntas y próximas acciones sugeridas

| Acción o pregunta | Propietario sugerido | Disparador de validación | Bloqueante |
|---|---|---|---|
| Reconciliar 25,5 h-p frente a 22,5 h | Product Owner y responsable de estimación | Tabla única historia por historia, con cifra aprobada | Sí |
| Aportar la versión del Excel de planificación | Scrum Master | Excel disponible con sprint, carga y predecesoras | Sí |
| Confirmar si las predecesoras deben finalizar antes de iniciar sucesoras | Equipo técnico | Regla de precedencia documentada | Sí para validar secuencia |
| Explicar 30 h netas frente a 52,5 h costeadas por semana | Responsable financiero y Scrum Master | Definiciones de unidades y fórmula relacionadas | Sí para viabilidad económica conjunta |
| Confirmar cobertura del DoD en las 25,5 h o 22,5 h | Equipo técnico y QA | Estimaciones revisadas por actividad | No, pero necesario para confianza |
| Confirmar si el coste de 3.967,50 € es fijo por calendario | Responsable financiero | Decisión presupuestaria registrada | No para la aritmética |
| Mantener como resueltos `RR-001` a `RR-009` | Equipo de requisitos | Referencia al archivo de trazabilidad | No, según la disposición comunicada |

## 9. Disposición RECHECK

No aplica. La ejecución solicitada está en modo `READINESS`, no en modo `RECHECK`.

Los hallazgos `RR-001` a `RR-009` se consideran resueltos por disposición explícita del equipo y no se vuelven a evaluar. No se identificó en el repositorio el archivo de trazabilidad que contiene esas justificaciones, por lo que esta aceptación se basa en la decisión comunicada por el usuario.

| Hallazgo previo | Decisión humana | Evidencia modificada | Estado verificado | Impacto restante |
|---|---|---|---|---|
| `RR-001` a `RR-009` | Procesados y justificados por el equipo | No aportada como archivo local en esta ejecución | Aceptados como resueltos para esta revisión | Ninguno dentro del alcance de estos hallazgos; quedan sujetos a la trazabilidad del equipo |

## 10. Consejo final y declaración de límites

El resultado es **NOT_READY** para declarar preparados, sin aclaraciones adicionales, los insumos de una hipótesis de planificación de las 17 historias en tres sprints.

La evidencia permite afirmar que:

1. La capacidad efectiva neta declarada es de 90 horas para tres sprints.
2. Las especificaciones suman 25,5 h-p, inferior a 90 h en términos agregados.
3. `viabilidad.md` usa 22,5 horas, generando una diferencia no resuelta de 3 horas.
4. Los `Predecessors` no muestran ciclos evidentes.
5. El coste semanal de 1.322,50 € y el total de 3.967,50 € están correctamente calculados según la fórmula y las tarifas documentadas.
6. La relación entre horas netas de ejecución y horas costeadas debe aclararse.
7. La asignación del Excel externo se acepta como supuesto comunicado, pero no se ha verificado directamente.

Para alcanzar `READY` o `READY_WITH_NON_BLOCKING_QUESTIONS`, el equipo debe reconciliar la carga de 22,5/25,5 horas, hacer verificable la asignación temporal y aclarar las unidades de capacidad y coste. La revisión no selecciona historias, no asigna recursos, no crea un calendario ni aprueba un compromiso.

Las fuentes existentes no han sido modificadas. Este informe es el único archivo creado y se ha guardado en `docs/project/reviews/initial-planning/initial-planning-review-v01.md`. No se aprueba ningún plan, baseline, presupuesto, asignación de recursos ni criterio de calidad.
