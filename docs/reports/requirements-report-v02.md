# Requirements review v02

## 1. Run metadata

- **Baseline/snapshot:** `Versión Inicial`, según las siete especificaciones revisadas.
- **Supplied commit:** No proporcionado.
- **Fecha/hora:** 2026-10-15 20:26 +02:00, proporcionada por la invocación.
- **Agente:** `.github/agents/requirements-reviewer.agent.md`.
- **Modelo/herramienta:** No proporcionado.
- **Modo:** `INITIAL`; no se proporcionaron decisiones humanas ni un paquete de `RECHECK`.
- **Alcance:** `EP-01`–`EP-07`, historias `US-01`–`US-17`, misión, objetivos, constitución, DoR y DoD.
- **Idioma:** Español.
- **Precedencia aplicada:** la constitución gobierna los principios y el flujo de calidad; `mission.md` y `goals.md` gobiernan misión, objetivos, alcance, exclusiones y restricciones; las épicas detallan historias. Cuando una épica contradice `goals.md`, se reporta la contradicción y no se elige una fuente silenciosamente.

## 2. Source manifest and limitations

### Fuentes leídas

| Fuente | Rol | Baseline/versión | Secciones revisadas |
|---|---|---|---|
| `.specify/memory/constitution.md` | Gobierno y principios | No indicado | Principios, artefactos y puntos de control |
| `specs/product/mission.md` | Misión y stakeholders | No indicado | Problemas, usuarios, propuesta de valor y experiencia |
| `specs/product/goals.md` | Objetivos, alcance, exclusiones y restricciones | No indicado | `G-01`–`G-04`, `M-01`–`M-04`, `S-01`–`S-04`, `E-01`–`E-03`, `R-01`–`R-02`, trazabilidad y cambios |
| `docs/quality/definition-of-ready.md` | Definition of Ready | No indicado | Los 19 criterios D1–D19 |
| `docs/quality/definition-of-done.md` | Definition of Done | No indicado | Implementación, aceptación, pruebas, integración, NFR, documentación y revisión |
| `specs/EP-01-catalogo/spec.md` | Catálogo | Versión Inicial | `US-01`–`US-03`, `US-16`–`US-17`, criterios y restricciones |
| `specs/EP-02-eventos/spec.md` | Eventos | Versión Inicial | `US-04`–`US-06`, criterios y restricciones |
| `specs/EP-03-foro/spec.md` | Foro | Versión Inicial | `US-07`–`US-08`, reglas y boundary |
| `specs/EP-04-usuarios/spec.md` | Usuarios y moderación | Versión Inicial | `US-09`–`US-10`, criterios y restricciones |
| `specs/EP-05-notificaciones/spec.md` | Notificaciones | Versión Inicial | `US-11`, criterios y boundary |
| `specs/EP-06-inventario/spec.md` | Inventario | Versión Inicial | `US-12`–`US-13`, criterios y restricciones |
| `specs/EP-07-soporte/spec.md` | Soporte | Versión Inicial | `US-14`–`US-15`, criterios y boundary |
| `docs/reports/requirements-report-v01.md` | Informe anterior | v01, 2026-10-07 | Hallazgos y límites para preservar trazabilidad; no se trata como decisión humana |

### Fuentes no accesibles o límites

- No se proporcionaron commit, registro de decisiones, prioridades externas, estimaciones revisadas, planes, tareas, código ni evidencias de pruebas. Por ello no se evalúa conformidad de implementación con el DoD.
- No se inspeccionaron fuentes fuera de las indicadas ni el Wiki.
- `readme.md` está vacío en el snapshot revisado y no aporta contexto adicional.
- La ausencia de un requisito se formula solo como “no encontrado en las fuentes revisadas”, no como ausencia en todo el proyecto.

## 3. Scoped assessment

**Recomendación: NEEDS_REFINEMENT.**

El alcance revisado es `EP-01`–`EP-07` y `US-01`–`US-17`. Persisten bloqueadores de interpretación compartida: `EP-03` está trazada a `G-01` aunque su resultado corresponde a `G-03`; `G-04` no tiene cobertura detallada; la compra declarada en `S-01` no está descrita de forma coherente y `US-17` puede contradecir `E-02`; el control del registro y los roles no están completamente definidos; y faltan estados, errores, NFR y contratos de concurrencia verificables.

La constitución sí fue accesible en esta revisión, pero no aporta la especificación funcional que falta. No se aprueba baseline ni gate.

## 4. Coverage matrix

| Dimensión | IDs inspeccionados | Resultado | Hallazgos |
|---|---|---|---|
| Claridad y consistencia | Misión, objetivos, `EP-01`–`EP-07`, `US-01`–`US-17` | **NO_MET** | `RR-001`, `RR-002`, `RR-003`, `RR-010` |
| Cobertura y alcance | `G-01`–`G-04`, `S-01`–`S-04`, `E-01`–`E-03`, todas las épicas | **NO_MET** | `RR-001`, `RR-004`, `RR-005`, `RR-010` |
| Elementos de especificación | Todas las historias y sus criterios | **NO_MET** | `RR-006`, `RR-007`, `RR-009` |
| Granularidad | `US-05`, `US-10`, `US-12`, `US-14`, `US-17` | **NO_MET** | `RR-008`, `RR-010` |
| Aceptación y DoR | `US-01`–`US-17` frente a D1–D19 | **NO_MET** | `RR-006`, `RR-007`, §6 |
| Dependencias y supuestos | Todos los `Predecessors`, boundaries y contratos cruzados | **NO_MET** | `RR-003`, `RR-009`, `RR-010` |

## 5. Findings

### 5.1 Compact index

| ID | Severidad | Confianza | Bloqueante | Categoría | Afectación |
|---|---|---|---|---|---|
| `RR-001` | CRITICAL | HIGH | Sí | Trazabilidad de objetivos | `EP-03`, `G-03`, `G-04` |
| `RR-002` | CRITICAL | HIGH | Sí | Contradicción de alcance | `US-09`, `E-03` |
| `RR-003` | MAJOR | HIGH | Sí | Roles y dependencias | `US-07`, `US-08`, `US-10` |
| `RR-004` | MAJOR | HIGH | Sí | Cobertura de misión | `S-01`, `EP-01` |
| `RR-005` | MAJOR | HIGH | Sí | Accesibilidad | `G-04`, `M-04` |
| `RR-006` | MAJOR | HIGH | Sí | Aceptación incompleta | `US-02`, `US-03`, `US-04`, `US-06`, `US-09`, `US-11`, `US-13`, `US-14`, `US-15` |
| `RR-007` | MAJOR | HIGH | Sí | Seguridad y errores | `US-06`, `US-09`, `US-10`, `US-12`, `US-14` |
| `RR-008` | MAJOR | HIGH | Sí para planificación | Granularidad | `US-05`, `US-10`, `US-12`, `US-14` |
| `RR-009` | MAJOR | HIGH | Sí | Estados y dependencias | `US-05`, `US-06`, `US-11`, `US-12`, `US-13` |
| `RR-010` | CRITICAL | HIGH | Sí | Compra y exclusión monetaria | `US-16`, `US-17`, `S-01`, `E-02` |

### 5.2 Detailed evidence records

#### RR-001 — El foro está trazado al objetivo equivocado y G-04 no está cubierto

- **Categoría:** Trazabilidad y consistencia.
- **Fuente + extracto:** `specs/EP-03-foro/spec.md`, cabecera: `Goals: G-01`; `specs/product/goals.md`, `G-03`: comunicación entre usuarios y `G-04`: accesibilidad.
- **Observación:** El resultado del foro y `M-03` corresponden a `G-03`, pero la épica declara `G-01`. Ninguna épica declara `G-04`.
- **Impacto:** Se rompe la cadena misión → objetivo → épica y no puede planificarse ni verificarse el objetivo de accesibilidad.
- **Acción sugerida:** Decidir la asociación de `EP-03` y añadir criterios/historias trazados a `G-04`, o documentar formalmente su exclusión.
- **Confianza:** HIGH; ambos lados son explícitos. **Bloqueante:** Sí.

#### RR-002 — El registro puede contradecir la exclusión de registros no controlados

- **Categoría:** Alcance, privacidad y control de cuentas.
- **Fuente + extracto:** `US-09`: “crear una cuenta”; `goals.md`, `E-03`: “Registros no controlados de nuevos usuarios”.
- **Observación:** Aunque `US-09` incluye verificación simulada, no define quién autoriza el alta ni qué hace que el registro sea controlado.
- **Impacto:** No puede determinarse el flujo permitido ni comprobar la exclusión `E-03`.
- **Acción sugerida:** Definir el control de alta, sus actores y estados, o reformular la historia mediante el proceso de cambios.
- **Confianza:** HIGH. **Bloqueante:** Sí.

#### RR-003 — Los roles del foro y sus permisos no están cerrados

- **Categoría:** Roles y dependencias.
- **Fuente + extracto:** `mission.md` enumera Jugador/Coleccionista, Administrador y Moderador; `US-07`/`US-08` requieren autenticación; `US-10` permite eliminar y bloquear al administrador.
- **Observación:** No se establece si moderador y administrador son el mismo rol ni se completa la matriz de permisos para leer, publicar, responder, eliminar, bloquear y acceder con sesión caducada.
- **Impacto:** El flujo mínimo y las pruebas de autorización no son determinables.
- **Acción sugerida:** Definir roles, permisos, denegaciones y dependencias reales.
- **Confianza:** HIGH para la falta de definición. **Bloqueante:** Sí.

#### RR-004 — La misión y `S-01` incluyen compra simulada sin cobertura completa

- **Categoría:** Cobertura.
- **Fuente + extracto:** `goals.md`, `S-01`: búsqueda, selección y simulación de compra; `EP-01` solo cubre catálogo, búsqueda, filtro, cesta y compra, sin delimitar la simulación.
- **Observación:** `US-16` y `US-17` aparecen ahora, pero no dicen explícitamente que el pago sea simulado, ni definen el alcance de selección, checkout, fallo y resultado.
- **Impacto:** No se puede saber qué parte de `S-01` entra en la baseline ni verificar `E-02`.
- **Acción sugerida:** Declarar el flujo simulado y sus límites; contrastarlo con `RR-010`.
- **Confianza:** HIGH. **Bloqueante:** Sí para cobertura global.

#### RR-005 — G-04 no tiene requisitos transversales verificables

- **Categoría:** NFR y cobertura.
- **Fuente + extracto:** `goals.md`, `G-04`/`M-04`; `US-04` menciona responsive, contraste y navegación con Tab.
- **Observación:** Un criterio localizado en eventos no cubre catálogo, foro, autenticación, formularios y notificaciones; tampoco define el conjunto de comprobaciones aplicable.
- **Impacto:** La accesibilidad no puede verificarse de forma consistente ni satisfacer el DoD.
- **Acción sugerida:** Definir NFR transversales observables para las superficies incluidas, sin inventar umbrales no decididos.
- **Confianza:** HIGH. **Bloqueante:** Sí para G-04.

#### RR-006 — Faltan estados vacíos, errores y límites

- **Categoría:** Aceptación.
- **Fuente + extracto:** `US-02`–`US-04` describen principalmente el caso feliz; `US-09` no cubre contraseña distinta/email duplicado; `US-11`–`US-15` no definen fallo, duplicación o contenido vacío.
- **Observación:** No se especifican de forma suficiente búsquedas vacías, eventos llenos/cancelados, capacidades o fechas inválidas, errores de envío, duplicados, reintentos, preguntas sin respuesta ni notificaciones ya leídas.
- **Impacto:** Los equipos pueden implementar respuestas incompatibles y no hay pruebas verificables para escenarios previsibles.
- **Acción sugerida:** Añadir criterios positivos, negativos, vacíos, límite y fallo con estado visible y recuperación.
- **Confianza:** HIGH. **Bloqueante:** Sí.

#### RR-007 — Seguridad y autorización no son verificables de manera uniforme

- **Categoría:** Seguridad y permisos.
- **Fuente + extracto:** `US-06`, `US-10` y `US-12` describen acceso administrativo; `US-09` exige “algoritmos de encriptación”; `US-13` protege la modificación de stock.
- **Observación:** La respuesta a cliente, anónimo, moderador o sesión caducada no está completa en todas las operaciones. “Encriptación” no distingue hash de contraseña, y no se define el efecto del bloqueo sobre sesiones activas.
- **Impacto:** No puede comprobarse el aislamiento de operaciones ni la protección de cuentas.
- **Acción sugerida:** Especificar permisos por rol, denegación, sesión, bloqueo/desbloqueo y almacenamiento seguro de contraseñas con terminología verificable.
- **Confianza:** HIGH. **Bloqueante:** Sí.

#### RR-008 — Varias historias agrupan outcomes con pruebas y permisos distintos

- **Categoría:** Granularidad/INVEST.
- **Fuente + extracto:** `US-05` combina reserva, unicidad y concurrencia; `US-10` eliminar mensajes y bloquear cuentas; `US-12` alta, validación, imagen y publicación; `US-14` navegación, formulario y entrega.
- **Observación:** Son outcomes independientemente inspeccionables presentados como una única historia y con estimaciones pequeñas.
- **Impacto:** Riesgo de aceptación parcial y estimaciones no fiables.
- **Acción sugerida:** Considerar una división vertical por outcome, sin decidir aquí la partición ni cambiar estimaciones.
- **Confianza:** HIGH. **Bloqueante:** Sí para planificar.

#### RR-009 — Estados y operaciones que comparten datos no tienen contrato común

- **Categoría:** Integridad y dependencias.
- **Fuente + extracto:** `US-05` modifica plazas; `US-06` crea eventos; `US-11` depende de `US-04` y `US-06`; `US-12` crea productos; `US-13` cambia stock a “Agotado”.
- **Observación:** No se define el ciclo de estados de eventos/productos, cancelación, unicidad de inscripción, atomicidad de la última plaza ni prohibición de stock negativo.
- **Impacto:** Calendario, notificaciones, catálogo e inventario pueden divergir.
- **Acción sugerida:** Documentar entidades, estados, transiciones, invariantes, dependencias y escenarios concurrentes.
- **Confianza:** HIGH. **Bloqueante:** Sí.

#### RR-010 — `US-17` puede exigir operaciones monetarias excluidas

- **Categoría:** Contradicción de alcance y seguridad.
- **Fuente + extracto:** `US-17-AC-01`: “elección de método de pago”; `US-17-AC-03`: confirmación o error del pedido; `goals.md`, `E-02`: “Cualquier clase de operación monetaria que no sea simulada”.
- **Observación:** La historia no contiene la palabra simulada ni limita el método de pago a una demostración sin operación monetaria. `US-16` además promete “compra en conjunto” y `US-17` modifica stock.
- **Impacto:** Una interpretación literal puede introducir una capacidad fuera de alcance y datos/operaciones no permitidos.
- **Acción sugerida:** Decidir si `US-17` es exclusivamente un checkout simulado; expresarlo en boundary, historia y criterios, incluyendo el no cobro real. Si no, retirar o modificar la historia mediante el proceso de cambios.
- **Confianza:** HIGH; la contradicción se observa directamente. **Bloqueante:** Sí.

## 6. DoR matrix

**Leyenda:** D1 identificador; D2 épica; D3 objetivo; D4 usuario/stakeholder; D5 capacidad; D6 valor; D7 límites; D8 aceptación; D9 observabilidad; D10 independencia de implementación; D11 casos límite; D12 prioridad; D13 estimación; D14 incertidumbre; D15 dependencias; D16 NFR; D17 restricciones; D18 dudas bloqueantes resueltas; D19 supuestos documentados. `N/A` significa no aplicable al texto de la historia; no equivale a conformidad global.

| Historia | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 | D13 | D14 | D15 | D16 | D17 | D18 | D19 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `US-01` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-02` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | NOT_MET | N/A | NOT_MET | NOT_MET |
| `US-03` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | NOT_MET | N/A | NOT_MET | NOT_MET |
| `US-04` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-05` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-06` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | NOT_MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-07` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | MET | NOT_MET | NOT_MET |
| `US-08` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | MET | NOT_MET | NOT_MET |
| `US-09` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_MET | NOT_MET |
| `US-10` | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | MET | MET | NOT_MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-11` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-12` | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-13` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-14` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | NOT_MET | NOT_MET | N/A | NOT_MET | NOT_MET |
| `US-15` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | N/A | N/A | NOT_MET | NOT_MET | NOT_MET |
| `US-16` | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_MET | NOT_MET | NOT_MET |
| `US-17` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | MET | NOT_MET | NOT_MET | NOT_MET | NOT_MET |

**Base de la evaluación:** D1–D7, D12 y D13 se marcan `MET` solo cuando hay evidencia textual en la historia/épica; D8–D11 se marcan `NOT_MET` cuando los criterios no cubren el comportamiento o dejan el resultado no verificable; D14 falla cuando no se declara incertidumbre; D16 falla cuando faltan NFR aplicables; D18 y D19 fallan ante decisiones o supuestos no documentados. `US-16` y `US-17` no declaran incertidumbre. En `US-15`, la ausencia de dependencias puede ser `N/A`, pero no resuelve la falta de casos vacíos, prioridad justificada, NFR y supuestos.

**Diferidos:** compra simulada, control del registro, roles, accesibilidad transversal, estados de dominio, concurrencia, entrega del contacto y lectura de notificaciones requieren decisión humana y actualización de las fuentes.

## 7. Candidate omissions, missing stakeholder questions and OUT_OF_SCOPE suggestions

### IN_SCOPE_CANDIDATE

- **Compra simulada:** deriva de `S-01`, `US-16` y `US-17`; pregunta: ¿qué flujo se simula y qué nunca se cobra o almacena?
- **Accesibilidad transversal:** deriva de `G-04`/`M-04`; pregunta: ¿qué criterios observables se aplican a cada pantalla?
- **Matriz de roles y sesiones:** deriva de los stakeholders de `mission.md` y `US-09`/`US-10`; pregunta: ¿moderador es independiente y qué ocurre con sesiones bloqueadas o caducadas?
- **Estados y cancelación de eventos/productos:** deriva de `US-04`–`US-06` y `US-12`–`US-13`; pregunta: ¿qué transiciones y efectos sobre inscripciones/notificaciones son válidos?

### SCOPE_UNCLEAR

- Recuperación de cuenta y gestión de sesiones.
- Mantenimiento de categorías y FAQs.
- Almacenamiento, entrega y respuesta del formulario de contacto.
- Lectura anónima del catálogo, eventos y FAQs, que se infiere parcialmente pero no está declarada de forma transversal.

### OUT_OF_SCOPE

- Operaciones monetarias reales (`E-02`), salvo que el equipo cambie formalmente el alcance.
- Datos personales reales (`E-01`, `R-01`).
- Correos electrónicos reales (`EP-05` boundary).
- Fotos o archivos en mensajes (`EP-03` boundary).

## 8. Dependencies, assumptions and traceability gaps

### Dependencias

- `US-05` depende de `US-04` y de autenticación/estado verificado de `US-09`; esta última dependencia no aparece en `Predecessors`.
- `US-07` y `US-08` dependen de autenticación; `US-08` depende además de la existencia de temas.
- `US-10` depende de usuarios, mensajes y permisos; `US-07` como único predecesor no expresa todo el contrato.
- `US-11` depende de publicación de eventos (`US-06`) y de su consulta (`US-04`); ambas aparecen en esta versión, pero faltan estados de entrega/leído.
- `US-12` alimenta `US-01` y debe compartir el estado `Activo`; `US-13` modifica el stock visible y el estado `Agotado`.
- `US-16` es precondición funcional de `US-17`, pero `US-17` solo declara `US-01` y `US-13`.

### Supuestos e hipótesis no confirmados

- **UNCONFIRMED:** administrador y moderador podrían ser el mismo rol.
- **UNCONFIRMED:** usuarios anónimos pueden consultar catálogo, eventos y FAQs.
- **UNCONFIRMED:** la confirmación de contacto implica persistencia o entrega real.
- **UNCONFIRMED:** la confirmación de registro simula un correo sin proveedor real y sin datos personales reales.
- No se define zona horaria exacta, ciclo de estados, bloqueo de sesiones, cancelación de eventos ni política de stock negativo.

### Trazabilidad

La cadena historia → épica → objetivo existe parcialmente. `EP-03` apunta a `G-01` aunque su contenido corresponde a `G-03`; `G-04` carece de épica; `S-01` ahora tiene `US-16`/`US-17`, pero su simulación y exclusión monetaria no son explícitas. La cadena hasta tareas, código, pruebas y evidencias no es evaluable porque esos artefactos no fueron suministrados.

## 9. Questions for humans

### Alta prioridad

1. ¿Debe `EP-03` trazarse a `G-03` y qué requisitos cubrirán `G-04`?
2. ¿Qué control hace compatible `US-09` con `E-03`?
3. ¿`US-16`/`US-17` son exclusivamente compra simulada? ¿Qué datos y efectos quedan expresamente excluidos?
4. ¿Moderador es un rol distinto de administrador? ¿Qué permisos tiene cada rol?
5. ¿Qué estados, cancelaciones y reglas de concurrencia aplican a reservas, eventos y stock?

### Prioridad media

6. ¿Qué criterios verificables de accesibilidad, rendimiento y seguridad son aplicables transversalmente?
7. ¿Qué ocurre ante campos vacíos, duplicados, errores de red y sesiones caducadas?
8. ¿Quién mantiene categorías y FAQs y cuál es el comportamiento cuando no hay contenido?
9. ¿Dónde se almacenan o entregan los mensajes de contacto?
10. ¿Cuándo se marcan como leídas las notificaciones y qué ocurre si el evento deja de estar disponible?

## 10. RECHECK crosswalk

No aplica: esta es una revisión `INITIAL`. El reporte v01 se consultó como contexto de continuidad, pero no se proporcionaron decisiones humanas ni fuentes revisadas para reclasificar sus hallazgos. `RR-001`–`RR-009` conservan su continuidad temática; `RR-010` es nuevo para las historias `US-16`/`US-17`.

## 11. Explicit closure

**This is an advisory review. No source requirement, priority, estimate, plan or human decision was changed. No baseline or gate was approved.**
