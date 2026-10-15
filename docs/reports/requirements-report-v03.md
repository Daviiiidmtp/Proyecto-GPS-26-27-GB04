# Requirements review v03

## 1. Run metadata

- **Baseline/snapshot:** `Versión Inicial`, tal como declaran las siete especificaciones consultadas; no se suministró commit.
- **Supplied commit:** No proporcionado.
- **Fecha/hora:** 2026-10-16 00:23 +02:00, según la invocación.
- **Agente:** Requirements Reviewer, configuración de esta sesión; versión no indicada.
- **Modelo/herramienta:** No proporcionado.
- **Modo:** `RECHECK`.
- **Informe previo solicitado:** `docs/reports/requirements-report-v01.md`.
- **Alcance:** `EP-01`–`EP-07`, historias `US-01`–`US-17`, objetivos y alcance de producto, Constitución, DoR y DoD.
- **Idioma:** Español.
- **Precedencia aplicada:** La Constitución gobierna los principios y el flujo de calidad; `mission.md` y `goals.md` gobiernan misión, stakeholders, objetivos, alcance y exclusiones; las épicas detallan las capacidades. Si una épica contradice una fuente de producto, se informa del conflicto sin elegir silenciosamente una.

## 2. Source manifest and limitations

### Fuentes leídas

| Fuente | Rol | Baseline/versión | Secciones revisadas |
|---|---|---|---|
| `.specify/memory/constitution.md` | Gobierno y principios | No indicado | Principios, artefactos, calidad y gobierno |
| `specs/product/mission.md` | Misión y stakeholders | No indicado | Idea, problemas, usuarios, propuesta de valor y experiencia |
| `specs/product/goals.md` | Objetivos, alcance y restricciones | No indicado | `G-01`–`G-04`, `M-01`–`M-04`, `S-01`–`S-04`, `E-01`–`E-03`, `R-01`–`R-02`, trazabilidad y cambios |
| `specs/EP-01-catalogo/spec.md` | Catálogo, cesta y compra simulada | Versión Inicial | `US-01`–`US-03`, `US-16`–`US-17`, criterios, reglas, NFR y supuestos |
| `specs/EP-02-eventos/spec.md` | Eventos | Versión Inicial | `US-04`–`US-06`, criterios, reglas, NFR y supuestos |
| `specs/EP-03-foro/spec.md` | Foro | Versión Inicial | `US-07`–`US-08`, roles, criterios, reglas y boundary |
| `specs/EP-04-usuarios/spec.md` | Registro, roles y moderación | Versión Inicial | `US-09`–`US-10`, criterios, reglas, NFR y supuestos |
| `specs/EP-05-notificaciones/spec.md` | Notificaciones | Versión Inicial | `US-11`, criterios, reglas, NFR y boundary |
| `specs/EP-06-inventario/spec.md` | Inventario | Versión Inicial | `US-12`–`US-13`, criterios, reglas, NFR y supuestos |
| `specs/EP-07-soporte/spec.md` | Soporte | Versión Inicial | `US-14`–`US-15`, criterios, reglas, NFR y supuestos |
| `docs/quality/definition-of-ready.md` | Definition of Ready | No indicado | Criterios D1–D19 |
| `docs/quality/definition-of-done.md` | Definition of Done | No indicado | Implementación, aceptación, pruebas, integración, NFR, documentación y revisión |
| `docs/reports/requirements-report-v01.md` | Informe previo indicado | v01, fechado 2026-10-07 | Alcance, hallazgos `RR-001`–`RR-009`, matrices, preguntas y crosswalk previo |
| `docs/reports/requirements-report-v02.md` | Informe existente, contextual | v02 | Lectura parcial de metadatos, alcance y extractos de hallazgos; no se utilizó como decisión humana ni como informe previo solicitado |

### Fuentes ausentes y límites

- **No se proporcionó un registro de decisiones humanas** ni su ruta. Es un insumo requerido para relacionar cada hallazgo anterior con decisiones del equipo; por eso el estado de cada fila del crosswalk es `NOT_ASSESSABLE`, aunque se consigna la evidencia actual observada.
- No se suministró un registro que identifique qué rutas fueron revisadas o modificadas tras v01. Se revisaron las rutas actuales listadas arriba por corresponder al alcance indicado; no se presupone que sean las rutas aprobadas por el equipo.
- No se proporcionaron commit, tareas, planes, código ni evidencias de pruebas. No se evalúa la implementación ni se declara cumplimiento del DoD.
- No se consultó el Wiki ni se inspeccionaron fuentes fuera del alcance listado. La ausencia de contenido se expresa como “no encontrado en las fuentes revisadas”, no como inexistencia en todo el proyecto.

## 3. Scoped assessment

**Recomendación: NOT_ASSESSABLE.**

El alcance de contenido revisado es `EP-01`–`EP-07` y `US-01`–`US-17`. Las especificaciones actuales contienen evidencia de que varios problemas señalados en v01 se han atendido: `EP-03` declara `G-03` y `G-04`; `US-09` define un alta por invitación y verificación simulada; las épicas distinguen roles y permisos; `EP-01` incorpora cesta y checkout simulado; y varias historias describen estados vacíos, errores, reintentos y concurrencia.

Sin el registro de decisiones no se puede completar el RECHECK según el protocolo ni distinguir una corrección decidida de un cambio no revisado. Además, en las fuentes actuales quedan cuestiones que impiden una lectura compartida y verificable: la semántica de la actualización de stock (`US-13`), la atomicidad del checkout fallido (`US-17`) y la verificación del objetivo de accesibilidad `G-04`. Estas observaciones se reportan sin aprobar una baseline ni atribuir decisiones al equipo.

**Bloqueadores actuales observados:** `RR-011` afecta `US-13`; `RR-012` afecta `US-17`; `RR-013` afecta la verificación de `G-04` y las historias que declaran esos NFR transversales. `RR-014` es una pregunta de privacidad, no un defecto confirmado.

## 4. Coverage matrix

| Dimensión | IDs inspeccionados | Resultado | Hallazgos |
|---|---|---|---|
| Claridad y consistencia | `EP-01`–`EP-07`, `US-01`–`US-17`, misión y objetivos | **NO_MET** | `RR-011`, `RR-012`, `RR-013` |
| Cobertura y alcance | `G-01`–`G-04`, `S-01`–`S-04`, `E-01`–`E-03`, siete épicas | **NO_MET** | `RR-013`; `RR-014` requiere aclaración |
| Elementos de especificación | Criterios, reglas, errores, límites, NFR y supuestos de `US-01`–`US-17` | **NO_MET** | `RR-011`–`RR-014` |
| Granularidad | `US-05`, `US-10`, `US-12`, `US-14`, `US-16`–`US-17` | **QUESTION** | `RR-008` en crosswalk; persiste posible agrupación de outcomes en `US-10` |
| Aceptación y DoR | `US-01`–`US-17` frente a D1–D19 | **NO_MET** | `RR-011`–`RR-013`; §6 |
| Dependencias y supuestos | Predecesoras, boundaries y contratos entre historias | **NO_MET** | `RR-011`, `RR-012`; hipótesis de provisión de invitaciones en §8 |

## 5. Findings

### 5.1 Compact index

| ID | Severidad | Confianza | Bloqueante | Categoría | Afectación |
|---|---|---|---|---|---|
| `RR-011` | MAJOR | HIGH | Sí | Ambigüedad de operación | `US-13` |
| `RR-012` | MAJOR | HIGH | Sí | Integridad y fallo transaccional | `US-17`, relación con `US-13` |
| `RR-013` | MAJOR | HIGH | Sí para verificar `G-04` | NFR y verificabilidad | `G-04`, `EP-01`–`EP-07` |
| `RR-014` | QUESTION | MEDIUM | No confirmado | Privacidad y datos sintéticos | `US-09`, `US-14`, `E-01`, `R-01` |

### 5.2 Detailed evidence records

#### RR-011 — No se distingue si `US-13` asigna stock o aplica un ajuste

- **Categoría:** Claridad de reglas e integridad del inventario.
- **Fuente + extracto:** `specs/EP-06-inventario/spec.md`, `US-13-AC-01`: “aumentar o reducir el stock [...] mediante una cantidad entera no negativa”; `US-13-AC-03`: “Una actualización que produciría stock negativo se rechaza”.
- **Observación:** No queda claro si la cantidad introducida es el nuevo stock absoluto o el delta que se suma/resta al stock actual. En el primer caso, un valor negativo ya incumple la entrada no negativa; en el segundo, se necesita precisar cómo se indica la dirección y se calcula el resultado.
- **Impacto:** El equipo no puede implementar ni probar de forma consistente la modificación, el rechazo por stock negativo y la concurrencia con checkout.
- **Acción sugerida:** Aclarar si la operación asigna una cantidad final o aplica un ajuste; definir qué dato introduce el administrador y cómo se calcula el saldo resultante, sin imponer interfaz ni técnica.
- **Confianza:** HIGH; las dos formulaciones están en los criterios. **Bloqueante:** Sí para `US-13`.

#### RR-012 — El checkout no define el resultado del stock ante cualquier fallo

- **Categoría:** Integridad de pedido e inventario.
- **Fuente + extracto:** `specs/EP-01-catalogo/spec.md`, `US-17-AC-04`: si un artículo está inactivo o no tiene stock suficiente, no se crea pedido exitoso ni se modifica stock; `US-17-AC-05`: en simulación completada se descuenta stock una sola vez; `US-17-AC-06`: si falla la operación, se informa y se puede corregir o reintentar; `US-17-AC-07`: repetir un checkout ya completado no crea otro pedido ni descuenta stock de nuevo.
- **Observación:** Se definen la validación de disponibilidad y la idempotencia después de completar, pero no se declara qué sucede si el pedido o el descuento de stock falla parcialmente, ni si toda la operación se confirma o revierte como una unidad. El reintento tras ese fallo podría tener un resultado ambiguo.
- **Impacto:** Pedido y stock podrían quedar en estados incompatibles o el usuario podría recibir resultados distintos al reintentar.
- **Acción sugerida:** Especificar el resultado observable ante fallos en cada etapa y la regla de consistencia entre pedido y stock, incluyendo que los reintentos no dupliquen pedido ni descuento. No se prescribe una implementación transaccional concreta.
- **Confianza:** HIGH; los criterios cubren éxito, ciertas validaciones y repetición tras éxito, pero no el fallo parcial. **Bloqueante:** Sí para `US-17`.

#### RR-013 — `G-04` y los NFR de accesibilidad no tienen un oráculo de verificación suficiente

- **Categoría:** Requisitos no funcionales y cobertura.
- **Fuente + extracto:** `specs/product/goals.md`, `G-04`: “Todos los usuarios pueden navegar [...] utilizando funcionalidades comprensibles y adaptadas”; especificaciones EP-01–EP-07: requisitos transversales como “se pueden usar con teclado”, “foco perceptible”, “contraste legible” y adaptación a móvil, tableta y escritorio.
- **Observación:** La cobertura transversal está declarada, pero términos como “legible”, “perceptible” y “sin perder información” no indican cómo decidir si se satisface. No se encuentra en las fuentes revisadas un conjunto común de comprobaciones observables que permita demostrar `G-04` de forma consistente entre superficies.
- **Impacto:** No se puede verificar el objetivo ni cumplir con evidencia el DoD para los NFR de accesibilidad; una revisión podría considerar correcto un resultado que otra rechace.
- **Acción sugerida:** Acordar comprobaciones observables para las superficies incluidas y vincularlas a las historias pertinentes. El equipo debe decidir los criterios y umbrales aplicables; esta revisión no inventa estándares ni valores.
- **Confianza:** HIGH; la formulación cualitativa está explícita y no se encontró un criterio compartido más concreto en las fuentes revisadas. **Bloqueante:** Sí para verificar `G-04`.

#### RR-014 — “Email sintético” no define cómo se mantiene la restricción de datos ficticios

- **Categoría:** Privacidad y datos de demostración.
- **Fuente + extracto:** `specs/EP-04-usuarios/spec.md`, `US-09-AC-02`–`AC-04` solicita email sintético y correo de verificación simulado; `specs/EP-07-soporte/spec.md`, `US-14-AC-02`–`AC-06` pide email sintético con formato válido y declara que no se aceptan datos personales reales; `goals.md`, `E-01` y `R-01` excluyen datos reales.
- **Observación:** No se define en los criterios qué hace que un identificador sea sintético ni cómo se distingue de un email personal real. El formato válido por sí solo no acredita que el dato sea sintético. La fuente no permite concluir si la demostración se restringe a datos de prueba controlados o si el formulario acepta entradas arbitrarias.
- **Impacto:** La aplicación de la restricción de privacidad es difícil de verificar y podría interpretarse de forma distinta en registro y contacto.
- **Acción sugerida:** Aclarar la regla de datos sintéticos y cómo se aplica en los flujos de demostración, sin proponer un patrón de email o mecanismo no aprobado por el equipo.
- **Confianza:** MEDIUM; los límites están escritos, pero no consta cómo se hacen cumplir. **Bloqueante:** No confirmado; requiere decisión/aclaración humana.

## 6. DoR matrix

**Criterios:** D1 identificador; D2 asociación a épica; D3 trazabilidad a objetivo; D4 usuario/rol; D5 capacidad; D6 valor; D7 límites; D8 aceptación; D9 comportamiento observable; D10 independencia de implementación; D11 casos límite; D12 prioridad; D13 estimación; D14 incertidumbre; D15 dependencias; D16 NFR; D17 restricciones; D18 dudas bloqueantes resueltas; D19 supuestos documentados.

**Leyenda de celdas:** `MET`, `NOT_MET`, `NOT_ASSESSABLE`, `NOT_APPLICABLE`. En esta matriz, `NM` abrevia `NOT_MET`; las demás celdas usan los valores completos. La evidencia compartida para `MET` es: cada fila corresponde a una historia con ID único bajo la épica indicada; las cabeceras de épica declaran objetivos; cada historia expresa capacidad/valor y presenta criterios formales, prioridad, estimación, incertidumbre, predecesoras y NFR/restricciones en la épica; las historias incluyen supuestos y límites explícitos. D9 se apoya en los resultados observables descritos en criterios de mensajes, estados, listas, errores o confirmaciones. D18 se marca `NOT_MET` por la cuestión transversal de verificación de `G-04` (`RR-013`), que las épicas vinculan a sus historias sin un oráculo común.

| Historia | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 | D13 | D14 | D15 | D16 | D17 | D18 | D19 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `US-01` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |
| `US-02` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |
| `US-03` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |
| `US-04` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |
| `US-05` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |
| `US-06` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |
| `US-07` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |
| `US-08` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |
| `US-09` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |
| `US-10` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |
| `US-11` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |
| `US-12` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |
| `US-13` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |
| `US-14` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |
| `US-15` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |
| `US-16` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |
| `US-17` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NM | MET |

### Interpretación

- Los estados reflejan la información de las especificaciones actuales, no evidencia de implementación.
- D16 está `MET` en cuanto a que se han considerado NFR transversales en las épicas; su falta de criterios de verificación comunes se registra por separado en `RR-013` y hace que D18 no esté satisfecho.
- D4 se considera cubierto por el actor de la historia y el contexto de acceso descrito en las reglas o supuestos de su épica. Si el equipo interpreta “usuario” como insuficiente para identificar un rol, conviene precisarlo.
- D18 está `NOT_MET` en las 17 historias por la cuestión transversal de accesibilidad; además, `US-13` y `US-17` tienen las ambigüedades específicas de `RR-011` y `RR-012`. `US-14` requiere además aclaración según `RR-014`.
- No se marca D10 como fallo por el ejemplo `bcrypt` de `US-09`: la fuente lo presenta como ejemplo de una propiedad de seguridad, no como tecnología obligatoria.

## 7. Candidate omissions, missing stakeholder questions and scope suggestions

### IN_SCOPE_CANDIDATE

- **Criterios de verificación de accesibilidad:** racional: `G-04`, `M-04` y NFR de las siete épicas; pregunta: ¿qué resultados observables permitirán al equipo y al Product Owner confirmar la accesibilidad de cada superficie?
- **Regla verificable de datos sintéticos:** racional: `E-01`, `R-01`, `US-09` y `US-14`; pregunta: ¿cómo se asegura que los datos usados en registro y contacto sean solo sintéticos?

### SCOPE_UNCLEAR

- **Provisión de invitaciones para `US-09`:** la historia sitúa el aprovisionamiento fuera del registro público; pregunta: ¿quién prepara y entrega las invitaciones de demostración y qué evidencia permite probar el flujo sin añadir gestión de invitaciones al alcance?
- **Normas de moderación:** `US-10` permite retirar mensajes que incumplan las normas, pero las fuentes revisadas no describen esas normas; pregunta: ¿son reglas de contenido externas al alcance de esta baseline o deben especificarse?
- **Granularidad de `US-10`:** retirar contenido y bloquear/desbloquear cuentas tienen permisos distintos; pregunta: ¿el equipo desea mantenerlos como un outcome o inspeccionarlos/planificarlos por separado?

### OUT_OF_SCOPE

- Operaciones monetarias reales y datos financieros reales (`E-02`, boundary de `EP-01`).
- Datos personales reales (`E-01`, `R-01`).
- Envío de correos electrónicos reales (`EP-04` y `EP-05`).
- Adjuntos en el foro (`EP-03`).
- Cancelación de eventos, expresamente fuera de la baseline de `EP-02`.

## 8. Dependencies, assumptions and traceability gaps

### Dependencias observadas

- `US-05` depende de `US-04` y `US-09`; `US-07` depende de `US-09`; `US-08` depende de `US-07` y `US-09`; `US-10` depende de `US-07`, `US-08` y `US-09`.
- `US-11` declara `US-04`, `US-06` y `US-09`; la creación de la alerta se limita a una publicación correcta (`US-06`) y el destino es el evento consultable (`US-04`).
- `US-12` aporta productos para catálogo; `US-13` depende de `US-12`; `US-17` depende de `US-01`, `US-13` y `US-16`. La semántica de la operación de `US-13` y el tratamiento de fallos de `US-17` siguen abiertos (`RR-011`, `RR-012`).
- Las dependencias declaradas son coherentes en general con los outcomes actuales. No se identificó un ciclo confirmado en las predecesoras revisadas.

### Supuestos e hipótesis

- **UNCONFIRMED:** que la provisión de invitaciones, expresamente situada fuera del registro público, esté resuelta operativamente para poder demostrar `US-09`.
- **UNCONFIRMED:** que “email sintético” baste como control de privacidad sin una regla adicional; `US-09` y `US-14` no permiten confirmar cómo se evita o detecta una entrada real.
- La tienda local configura la zona horaria para `US-04`–`US-06`; el soporte indica que las solicitudes registradas quedan disponibles para seguimiento fuera del flujo del usuario. Estos límites están declarados, aunque no se revisaron sistemas externos.

### Trazabilidad

- La trazabilidad declarada enlaza objetivos y épicas; `EP-03` ahora declara `G-03` y `G-04`, y `EP-01` contiene `US-16`/`US-17` para el recorrido de selección y compra simulado.
- La cadena hasta tareas, código, pruebas y evidencias no puede comprobarse porque esos artefactos no se suministraron.
- No se puede enlazar la evidencia actual con decisiones humanas ni con un paquete de rutas revisadas por ausencia del registro requerido.

## 9. Questions for humans

### Prioridad alta

1. ¿Dónde está el registro de decisiones humanas de v01 y cuáles son las rutas revisadas para este RECHECK?
2. En `US-13`, ¿el número introducido es el nuevo stock final o un ajuste al stock existente?
3. En `US-17`, ¿qué resultado debe observarse si falla una parte del checkout después de que otra parte haya cambiado? ¿Cómo se garantiza que el pedido y el stock no queden en estados incompatibles al reintentar?
4. ¿Qué comprobaciones observables acordará el equipo para demostrar `G-04` y los NFR de accesibilidad declarados en las épicas?

### Prioridad media

5. ¿Qué regla hará verificable que los emails usados en registro/contacto son sintéticos, según `E-01` y `R-01`?
6. ¿Quién aprovisiona las invitaciones de demostración y cómo se prueba su ciclo de uso único/revocación?
7. ¿Dónde se definen las normas que permiten decidir cuándo un mensaje incumple las reglas y debe retirarse?
8. ¿Se mantiene `US-10` como historia que agrupa moderación y bloqueo, o el equipo desea inspeccionar esos outcomes por separado?

## 10. RECHECK crosswalk

El crosswalk conserva los IDs de v01. Al faltar el registro de decisiones, el estado de resolución solicitado no puede inferirse solo de que las fuentes actuales contengan cambios. Se registra la evidencia disponible, pero cada estado de resolución queda `NOT_ASSESSABLE`.

| Hallazgo v01 | Evidencia actual en las fuentes revisadas | Estado |
|---|---|---|
| `RR-001` | `EP-03` ahora declara `G-03` y `G-04`; varias épicas tienen requisitos transversales de accesibilidad. La verificabilidad de `G-04` sigue abierta (`RR-013`). | NOT_ASSESSABLE |
| `RR-002` | `US-09` ahora requiere invitación autorizada de un solo uso y verificación simulada; el registro público sin invitación no crea cuenta. | NOT_ASSESSABLE |
| `RR-003` | `EP-03` y `EP-04` distinguen Cliente, Moderador y Administrador y describen permisos y denegaciones para foro, eventos, productos y cuentas. | NOT_ASSESSABLE |
| `RR-004` | `EP-01` incorpora `US-16` (cesta) y `US-17` (checkout simulado); el boundary excluye cobros y datos financieros reales. | NOT_ASSESSABLE |
| `RR-005` | Las épicas declaran teclado, foco, contraste y adaptación de pantalla; no se encontró un oráculo común verificable para `G-04` (`RR-013`). | NOT_ASSESSABLE |
| `RR-006` | Las historias actuales incluyen más estados vacíos, entradas inválidas, denegaciones, errores, reintentos y duplicados; la consistencia ante fallo parcial de checkout sigue abierta (`RR-012`). | NOT_ASSESSABLE |
| `RR-007` | Se especifican permisos, sesiones caducadas, bloqueo de sesiones, denegaciones y hash de contraseñas; la aplicación de datos sintéticos requiere aclaración (`RR-014`). | NOT_ASSESSABLE |
| `RR-008` | Varias historias siguen agrupando reglas de distintas pruebas; en particular `US-10` combina retirar mensajes y bloquear/desbloquear cuentas. No se interpreta la agrupación como defecto confirmado sin decisión de equipo. | NOT_ASSESSABLE |
| `RR-009` | `US-05` especifica unicidad y reserva concurrente; `US-11` depende de publicación (`US-06`); `US-13` y `US-17` añaden invariantes de stock. Persisten las ambigüedades `RR-011` y `RR-012`. | NOT_ASSESSABLE |

Los IDs nuevos de este informe son `RR-011`–`RR-014`. No se declara ningún hallazgo anterior resuelto, parcialmente resuelto, abierto, rechazado justificadamente o diferido sin el registro humano exigido.

## 11. Explicit closure

**This is an advisory review. No source requirement, priority, estimate, plan or human decision was changed. No baseline or gate was approved.**
