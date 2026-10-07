# Requirements review v01

## 1. Run metadata

- **Baseline/snapshot:** `Versión Inicial`, según las siete especificaciones revisadas.
- **Supplied commit:** No proporcionado.
- **Fecha/hora:** 2026-10-07; hora exacta de inicio no registrada.
- **Agente:** `.github/agents/requirements-reviewer.agent.md`.
- **Modelo/herramienta:** No proporcionado.
- **Modo:** `INITIAL`.
- **Alcance:** Todas las historias `US-01`–`US-15` de `specs/`, sus épicas, `specs/product/mission.md`, `specs/product/goals.md`, DoR y DoD.
- **Idioma:** Español.
- **Precedencia:** La misión y objetivos de `specs/product/` son la autoridad de producto; las épicas detallan la funcionalidad; DoR y DoD son reglas transversales. La constitución no pudo resolverse con la ruta disponible en esta ejecución, por lo que sus comprobaciones quedan limitadas.

## 2. Source manifest and limitations

### Fuentes leídas

| Fuente | Rol | Baseline/versión | Secciones revisadas |
|---|---|---|---|
| `specs/product/mission.md` | Misión y stakeholders | No indicado | Misión, problemas, usuarios, propuesta de valor y experiencia |
| `specs/product/goals.md` | Objetivos, alcance y exclusiones | No indicado | `G-01`–`G-04`, `M-01`–`M-04`, `S-01`–`S-04`, `E-01`–`E-03`, `R-01`–`R-02` y trazabilidad |
| `specs/EP-01-catalogo/spec.md` | Catálogo | Versión Inicial | EP, `US-01`–`US-03`, criterios y verificaciones |
| `specs/EP-02-eventos/spec.md` | Eventos | Versión Inicial | EP, `US-04`–`US-06`, criterios y verificaciones |
| `specs/EP-03-foro/spec.md` | Foro | Versión Inicial | EP, `US-07`–`US-08`, criterios y boundary |
| `specs/EP-04-usuarios/spec.md` | Usuarios | Versión Inicial | EP, `US-09`–`US-10`, criterios y verificaciones |
| `specs/EP-05-notificaciones/spec.md` | Notificaciones | Versión Inicial | EP, `US-11`, criterios y boundary |
| `specs/EP-06-inventario/spec.md` | Inventario | Versión Inicial | EP, `US-12`–`US-13`, criterios y verificaciones |
| `specs/EP-07-soporte/spec.md` | Soporte | Versión Inicial | EP, `US-14`–`US-15`, criterios y boundary |
| `docs/quality/definition-of-ready.md` | Definition of Ready | No indicado | Todos sus criterios |
| `docs/quality/definition-of-done.md` | Definition of Done | No indicado | Implementación, aceptación, pruebas, integración, NFR y revisión |

### Fuentes no accesibles o no encontradas

- La ruta de constitución indicada por la configuración no pudo resolverse en esta ejecución. No se inventa una política sustitutiva; las comprobaciones específicas de constitución quedan **NOT_ASSESSABLE**.
- `docs/reports/` existía como directorio autorizado y no contenía `requirements-report-v01.md`; se creó únicamente el nuevo informe.
- No se proporcionaron commit, informe previo, log de decisiones ni revisión `RECHECK`.
- No se inspeccionó código ni se ejecutaron pruebas. Este informe evalúa requisitos, no conformidad de implementación con el DoD.

## 3. Scoped assessment

**Recomendación: NEEDS_REFINEMENT.**

El alcance revisado es `EP-01`–`EP-07` y `US-01`–`US-15`. Existen conflictos confirmados entre objetivos y épicas, una secuencia y separación de roles insuficientemente definidas en foro y registro, criterios de aceptación incompletos, NFR no verificables y dependencias de dominio no declaradas.

Además, `G-04` (accesibilidad) no tiene trazabilidad detallada, `US-09` puede contradecir `E-03` si el registro es abierto y `S-01` incluye compra simulada sin historias que la cubran. Estas cuestiones bloquean una planificación fiable. La constitución no pudo evaluarse por falta de ruta accesible.

## 4. Coverage matrix

| Dimensión | IDs inspeccionados | Resultado | Hallazgos |
|---|---|---|---|
| Claridad y consistencia | `EP-01`–`EP-07`, `US-01`–`US-15`, misión y objetivos | **NO_MET** | `RR-001`, `RR-002`, `RR-003` |
| Cobertura y alcance | `G-01`–`G-04`, `S-01`–`S-04`, `E-01`–`E-03` | **NO_MET** | `RR-001`, `RR-004`, `RR-005` |
| Elementos de especificación | Todas las historias | **NO_MET** | `RR-006`, `RR-007`, `RR-009` |
| Granularidad | Especialmente `US-05`, `US-10`, `US-12`, `US-14` | **NO_MET** | `RR-008` |
| Aceptación y DoR | `US-01`–`US-15` frente al DoR | **NO_MET** | `RR-006`, `RR-007`; §6 |
| Dependencias y supuestos | Todos los `Predecessors`, boundaries y contratos cruzados | **NO_MET** | `RR-003`, `RR-009` |

## 5. Findings

### 5.1 Compact index

| ID | Severidad | Confianza | Bloqueante | Categoría | Afectación |
|---|---|---|---|---|---|
| `RR-001` | CRITICAL | HIGH | Sí | Trazabilidad de objetivos | `EP-03`, `G-03`, `G-04` |
| `RR-002` | CRITICAL | HIGH | Sí | Contradicción de alcance | `US-09`, `E-03` |
| `RR-003` | MAJOR | HIGH | Sí | Roles y dependencias | `US-07`, `US-08`, `US-10` |
| `RR-004` | MAJOR | HIGH | Sí | Cobertura de misión | `S-01`, `EP-01` |
| `RR-005` | MAJOR | MEDIUM | Sí para cobertura global | Accesibilidad | `G-04`, `M-04` |
| `RR-006` | MAJOR | HIGH | Sí | Aceptación insuficiente | `US-02`, `US-03`, `US-04`, `US-06`, `US-09`, `US-11`, `US-13`, `US-14` |
| `RR-007` | MAJOR | HIGH | Sí | Seguridad y errores | `US-06`, `US-09`, `US-10`, `US-12`, `US-14` |
| `RR-008` | MAJOR | HIGH | Sí para planificación | Granularidad | `US-05`, `US-10`, `US-12`, `US-14` |
| `RR-009` | MAJOR | HIGH | Sí | Integridad y dependencias | `US-05`, `US-06`, `US-11`, `US-12`, `US-13` |

### 5.2 Detailed evidence records

#### RR-001 — El foro está trazado al objetivo equivocado y G-04 no está cubierto

- **Categoría:** Trazabilidad y consistencia.
- **Fuente + extracto:** `specs/EP-03-foro/spec.md`, cabecera: `Goals: G-01`; `specs/product/goals.md`, `G-03`: “Comunicación entre usuarios” y `G-04`: “Implementación de accesibilidad”.
- **Observación:** El outcome del foro y `M-03` corresponden a `G-03`, pero la épica declara `G-01` (stock). Ninguna épica declara `G-04`.
- **Impacto:** La cadena misión → objetivo → épica queda rota y no se puede planificar ni verificar accesibilidad como objetivo.
- **Acción sugerida:** Corregir la asociación de `EP-03` tras decisión del equipo y añadir historias o criterios de accesibilidad trazados a `G-04`, o documentar formalmente su alcance.
- **Confianza:** HIGH. Ambos lados están explícitos.
- **Bloqueante:** Sí.

#### RR-002 — El registro abierto puede contradecir la exclusión E-03

- **Categoría:** Contradicción de alcance.
- **Fuente + extracto:** `US-09`: “Como usuario, quiero crear una cuenta”; `goals.md`, `E-03`: “Registros no controlados de nuevos usuarios”.
- **Observación:** `US-09` no indica invitación, aprobación, verificación ni otro control. Puede permitir el registro no controlado excluido.
- **Impacto:** No se conoce el flujo autorizado de alta ni quién puede probarlo.
- **Acción sugerida:** Decidir si `US-09` representa un registro controlado; especificar el mecanismo y criterios, o retirar/reformular la historia.
- **Confianza:** HIGH.
- **Bloqueante:** Sí.

#### RR-003 — Roles y secuencia del foro no están definidos

- **Categoría:** Dependencias y permisos.
- **Fuente + extracto:** `US-07`, `Predecessors: US-09`; `US-10`, `Predecessors: US-07, US-09`; misión: `Jugador/Coleccionista`, `Administrador` y `Moderardor`.
- **Observación:** No se define si moderador y administrador son el mismo rol, ni los permisos de lectura, creación, respuesta y moderación. La secuencia de capacidades queda implícita.
- **Impacto:** No puede determinarse el flujo mínimo entregable antes de moderar ni probar los permisos.
- **Acción sugerida:** Definir roles, permisos y dependencias funcionales reales, separando lectura, publicación, respuesta, eliminación y bloqueo.
- **Confianza:** HIGH para la falta de roles explícitos; MEDIUM para cualquier ciclo, que no aparece cerrado textualmente.
- **Bloqueante:** Sí.

#### RR-004 — La misión incluye compra simulada sin historias de compra

- **Categoría:** Cobertura.
- **Fuente + extracto:** `mission.md`: “tienda donde se pueda comprar productos de forma telemática”; `goals.md`, `S-01`: “búsqueda, selección y simulación de compra”; `EP-01`: solo catálogo, búsqueda y filtro.
- **Observación:** No hay historias de selección, carrito, simulación de compra ni resultado de compra.
- **Impacto:** La planificación puede omitir un resultado incluido en el alcance.
- **Acción sugerida:** Confirmar si compra simulada pertenece a esta baseline; si sí, añadir historias y criterios; si no, actualizar alcance mediante el proceso de cambios.
- **Confianza:** HIGH.
- **Bloqueante:** Sí para cobertura global.

#### RR-005 — Accesibilidad declarada pero no especificada

- **Categoría:** NFR y cobertura.
- **Fuente + extracto:** `G-04`/`M-04`; `US-04`: “verse bien ... en ordenador como en móvil”.
- **Observación:** No hay criterios observables para teclado, comprensión, navegación, contraste, formularios o tecnologías de asistencia. Responsive no equivale a accesibilidad.
- **Impacto:** No se puede comprobar `G-04` ni satisfacer el DoD sobre accesibilidad.
- **Acción sugerida:** Definir criterios transversales verificables para las pantallas incluidas, sin inventar estándares o umbrales no decididos.
- **Confianza:** HIGH.
- **Bloqueante:** Sí para G-04.

#### RR-006 — Estados alternativos y entradas inválidas insuficientes

- **Categoría:** Aceptación.
- **Fuente + extracto:** `US-02-AC-02` solo describe coincidencia parcial; `US-03-AC-02` solo resultado por categoría; `US-04-AC-03` solo eventos pasados; `US-09-AC-01`–`AC-03` no cubren contraseña distinta/email duplicado; `US-14-AC-03` solo confirma éxito.
- **Observación:** Faltan búsqueda vacía/sin resultados, mayúsculas y espacios, categorías sin productos, eventos llenos o cancelados, fechas/capacidades inválidas, errores de envío, duplicados y reintentos.
- **Impacto:** No existe un comportamiento verificable común para escenarios previsibles.
- **Acción sugerida:** Añadir criterios positivos, negativos, vacíos, límite y fallo, con estado visible y recuperación.
- **Confianza:** HIGH.
- **Bloqueante:** Sí.

#### RR-007 — Seguridad y autorización no son verificables

- **Categoría:** Seguridad, privacidad y permisos.
- **Fuente + extracto:** `US-06-AC-01`, `US-10-AC-01`, `US-12-AC-01` solo indican capacidades administrativas; `US-09` exige “algoritmos de encriptación”; la misión identifica administrador y moderador.
- **Observación:** No se define respuesta para usuario anónimo, cliente, moderador o sesión caducada al acceder a funciones administrativas. “Encriptación” no precisa el almacenamiento de contraseñas ni el efecto del bloqueo sobre sesiones activas.
- **Impacto:** No puede comprobarse el aislamiento de operaciones ni la protección de cuentas.
- **Acción sugerida:** Especificar permisos por rol, denegación, sesión, bloqueo y desbloqueo; describir almacenamiento mediante hash seguro sin imponer tecnología no decidida.
- **Confianza:** HIGH.
- **Bloqueante:** Sí.

#### RR-008 — Historias con varios outcomes independientes

- **Categoría:** Granularidad/INVEST.
- **Fuente + extracto:** `US-05` combina reserva, unicidad y concurrencia; `US-10` combina eliminar mensajes y bloquear cuentas; `US-12` combina alta, validación, imagen y publicación; `US-14` combina navegación, formulario y entrega.
- **Observación:** Cada conjunto tiene reglas, permisos y pruebas distintas, aunque se presenta como una sola historia y con estimaciones de 1–2 h-p.
- **Impacto:** Riesgo de aceptación parcial, estimaciones poco fiables y tareas no verticales.
- **Acción sugerida:** Considerar dividir por outcome independientemente inspeccionable, sin decidir aquí la partición.
- **Confianza:** HIGH.
- **Bloqueante:** Sí para planificar esas historias.

#### RR-009 — Contratos de estado, concurrencia y notificaciones incompletos

- **Categoría:** Dependencias e integridad.
- **Fuente + extracto:** `US-05` modifica plazas; `US-06` crea eventos; `US-11` depende solo de `US-04`; `US-12` crea productos activos; `US-13` cambia stock a “Agotado”.
- **Observación:** No se define la dependencia `US-11` → `US-06`, estados de eventos/productos, cancelación, unicidad de inscripción, atomicidad de última plaza ni prohibición de stock negativo.
- **Impacto:** Pueden divergir calendario, notificaciones, catálogo e inventario.
- **Acción sugerida:** Documentar entidades, estados, transiciones, relaciones y operaciones atómicas; añadir dependencias y escenarios concurrentes.
- **Confianza:** HIGH.
- **Bloqueante:** Sí.

## 6. DoR matrix

**Criterios:** D1 identificador; D2 épica; D3 objetivo; D4 usuario/stakeholder; D5 capacidad; D6 valor; D7 límites; D8 aceptación; D9 observabilidad; D10 independencia de implementación; D11 casos límite; D12 prioridad; D13 estimación; D14 incertidumbre; D15 dependencias; D16 NFR; D17 restricciones; D18 dudas bloqueantes resueltas; D19 supuestos documentados.

| Historia | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 | D13 | D14 | D15 | D16 | D17 | D18 | D19 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `US-01` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-02` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_APPLICABLE | NOT_MET | NOT_MET |
| `US-03` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_APPLICABLE | NOT_MET | NOT_MET |
| `US-04` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-05` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-06` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | NOT_MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-07` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | MET | NOT_MET | NOT_MET |
| `US-08` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | MET | NOT_MET | NOT_MET |
| `US-09` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-10` | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-11` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-12` | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-13` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | MET | NOT_MET | MET | NOT_MET | NOT_MET |
| `US-14` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_MET | NOT_MET | NOT_MET | NOT_APPLICABLE | NOT_MET | NOT_MET |
| `US-15` | MET | MET | MET | MET | MET | MET | MET | MET | MET | MET | NOT_MET | MET | MET | NOT_APPLICABLE | NOT_APPLICABLE | NOT_MET | NOT_MET | NOT_MET | NOT_MET |

### Interpretación y diferidos

- `MET` se basa en evidencia explícita en las historias, no en una inferencia de implementación.
- D3 está formalmente presente en cada épica, pero `EP-03` tiene una asociación semánticamente incorrecta según `RR-001`.
- D14 falta donde no se declara incertidumbre (`US-02`, `US-03`, `US-06`–`US-08`, `US-10`–`US-15`).
- D16 falla por NFR no verificables o por NFR transversales exigidos por el DoD. `NOT_APPLICABLE` no exime de esos NFR.
- Los criterios D18/D19 son `NOT_MET` cuando no hay dudas resueltas o supuestos documentados.
- **Diferidos:** compra simulada, control del registro, roles de moderación, accesibilidad, estados de dominio, concurrencia, contacto y notificaciones requieren decisión humana y actualización de fuentes.

## 7. Candidate omissions, stakeholder questions and scope suggestions

### IN_SCOPE_CANDIDATE

- **Compra simulada:** racional: `mission.md` y `S-01`; pregunta: ¿se deben planificar selección, carrito y simulación?
- **Accesibilidad transversal:** racional: `G-04` y `M-04`; pregunta: ¿qué criterios verificables aplican a catálogo, eventos, foro y formularios?
- **Gestión de roles de moderador:** racional: usuario principal declarado; pregunta: ¿moderador es independiente del administrador?
- **Cancelación/edición de eventos:** racional: `US-04`–`US-06`; pregunta: ¿qué ocurre con plazas e inscripciones?

### SCOPE_UNCLEAR

- Recuperación de cuenta y gestión de sesiones.
- Mantenimiento de categorías y FAQs.
- Almacenamiento o entrega del formulario de contacto.

### OUT_OF_SCOPE

- Operaciones monetarias reales (`E-02`).
- Datos personales reales (`E-01`, `R-01`).
- Correos electrónicos reales (`EP-05` boundary).
- Fotos o archivos en mensajes (`EP-03` boundary).

## 8. Dependencies, assumptions and traceability gaps

### Dependencias

- `US-05` necesita `US-04` y autenticación de `US-09`, aunque esta última no figura como predecesora.
- `US-07` necesita `US-09`; `US-08` necesita publicación de temas; `US-10` necesita mensajes, usuarios y permisos.
- `US-11` debería relacionarse con `US-06`, que publica eventos, no solo con `US-04`.
- `US-12` alimenta `US-01` y comparte el estado `Activo`; `US-13` puede cambiar la visibilidad del producto.
- La compra simulada de `S-01` no tiene historias ni dependencias.

### Supuestos e hipótesis

- **UNCONFIRMED:** administrador y moderador podrían ser el mismo rol.
- **UNCONFIRMED:** usuarios anónimos pueden consultar catálogo, eventos y FAQs.
- **UNCONFIRMED:** la confirmación de contacto representa persistencia o entrega real.
- No se define zona horaria exacta, carga inicial, ciclo de estados, bloqueo de sesiones ni canal de soporte.

### Trazabilidad

La cadena historia → épica → objetivo existe parcialmente. `EP-03` apunta al objetivo incorrecto; `G-04` no tiene épica; `S-01` no tiene historias de compra. La cadena hasta tareas, código, pruebas y evidencias no puede evaluarse porque esos artefactos no fueron suministrados.

## 9. Questions for humans

### Alta prioridad

1. ¿Debe `EP-03` trazarse a `G-03` y qué historias/criterios cubrirán `G-04`?
2. ¿Cómo se compatibiliza `US-09` con `E-03`? ¿Qué control hace que el registro sea autorizado?
3. ¿La compra simulada de `S-01` está dentro de esta baseline?
4. ¿Moderador es un rol distinto de administrador? ¿Qué permisos tiene cada uno?
5. ¿Qué estados y reglas de concurrencia aplican a reservas, eventos y stock?

### Prioridad media

6. ¿Qué criterios verificables de accesibilidad y rendimiento se aplican?
7. ¿Qué ocurre ante campos vacíos, duplicados, errores de red y sesiones caducadas?
8. ¿Quién mantiene categorías y FAQs?
9. ¿Dónde se almacenan o entregan los mensajes de contacto?
10. ¿Cuándo se marcan como leídas las notificaciones?

## 10. RECHECK crosswalk

No aplica: revisión `INITIAL`; no se proporcionaron informe previo ni decisiones humanas.

## 11. Explicit closure

**This is an advisory review. No source requirement, priority, estimate, plan or human decision was changed. No baseline or gate was approved.**
