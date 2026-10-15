# EP-02 Gestión de Eventos

- **Goals:** G-02, G-04
- **Baseline:** Versión Inicial
- **Boundary:** Gestión de plazas locales para eventos ficticios. La cancelación de eventos queda fuera de esta baseline.

## Epic outcome
Que los jugadores puedan consultar los próximos torneos de la tienda y reservar una plaza disponible.

## Requisitos transversales de la épica
- La interfaz se adapta a móvil, tableta y escritorio sin perder información; los controles se pueden usar con teclado y tienen nombre y foco perceptibles; la información no depende solo del color y el texto mantiene contraste legible.
- Las fechas y horas se muestran en la zona horaria local de la tienda. Los errores se diferencian de listas vacías y no se comunica éxito si la operación no se completó.
- Solo se usan datos ficticios o sintéticos; una operación administrativa requiere una sesión autenticada y autorizada.

## Stories

### 1. US-04 Ver calendario de eventos
> Como usuario, quiero ver un calendario con los próximos torneos y actividades.

- **Priority:** Must — es la capacidad de consulta central de G-02 y antecede a la inscripción.
- **Estimate:** 2 h-p
- **Uncertainty:** Low
- **Predecessors:** Ninguna
- **Initial plan:** Sprint 1

#### Acceptance criteria
- **US-04-AC-01:** Los eventos publicados con fecha futura se muestran por fecha y hora, empezando por el más próximo.
- **US-04-AC-02:** Cada evento muestra título, fecha, hora, plazas disponibles y su estado (con plazas o completo).
- **US-04-AC-03:** Los eventos pasados no se muestran en la lista de próximos eventos.
- **US-04-AC-04:** Si no hay eventos futuros, se muestra "No hay eventos próximos".
- **US-04-AC-05:** Si falla la carga, se muestra un error distinguible de la lista vacía y se permite reintentar.

#### Verification and constraints
- **Rules:** Las horas se presentan en la zona horaria local de la tienda. Un evento con cero plazas se presenta como completo y no admite inscripciones.
- **Edge cases:** Dos eventos con igual fecha u hora aparecen sin solaparse ni ocultar su información; los eventos completos siguen visibles.
- **NFR:** Se aplican los requisitos transversales de esta épica; la lista mantiene la información al cambiar de tamaño de pantalla y sus controles son accesibles con teclado.
- **Assumptions:** Cualquier visitante puede consultar eventos; la hora local de la tienda se configura para la demostración.
- **Open questions:** Ninguna bloqueante para planificar esta historia.

### 2. US-05 Inscribirse en evento
> Como usuario con cuenta verificada, quiero apuntarme a un evento para asegurar mi plaza.

- **Priority:** Must — completa el objetivo G-02 cuando un evento tiene aforo disponible y depende de la consulta y autenticación.
- **Estimate:** 1.5 h-p
- **Uncertainty:** Medium
- **Predecessors:** US-04, US-09
- **Initial plan:** Sprint 1

#### Acceptance criteria
- **US-05-AC-01:** Solo una persona con sesión autenticada, cuenta verificada y no bloqueada puede inscribirse; si no cumple una condición, recibe un mensaje que indica el motivo y cómo continuar.
- **US-05-AC-02:** Si el evento tiene plazas y la cuenta aún no está inscrita, se ofrece la acción "Inscribirse".
- **US-05-AC-03:** Una inscripción confirmada reduce en una unidad las plazas disponibles y muestra un mensaje de confirmación.
- **US-05-AC-04:** Una cuenta no puede inscribirse dos veces al mismo evento; la segunda solicitud informa que ya está inscrita y no consume otra plaza.
- **US-05-AC-05:** Cuando solo queda una plaza y llegan solicitudes simultáneas, solo una se confirma; las demás reciben aviso de aforo completo. Las plazas disponibles nunca son negativas.
- **US-05-AC-06:** Si el evento está completo o ya ha pasado, no se permite la inscripción y se informa del motivo.
- **US-05-AC-07:** Si falla la inscripción, se informa del error, no se confirma una plaza y se puede reintentar si el evento continúa disponible.

#### Verification and constraints
- **Rules:** Cada cuenta tiene como máximo una inscripción por evento. La reserva de la última plaza debe ser indivisible desde el punto de vista de quienes solicitan la inscripción.
- **NFR:** Se aplican los requisitos transversales de esta épica; los estados de inscripción y los errores se comunican sin depender solo del color.
- **Assumptions:** Las inscripciones no se pueden cancelar en esta baseline; una cuenta bloqueada no puede iniciar ni completar una nueva inscripción.
- **Open questions:** Ninguna bloqueante para planificar esta historia.

### 3. US-06 Añadir evento
> Como administrador, quiero crear la ficha de un nuevo evento.

- **Priority:** Must — publicar eventos es necesario para ofrecer el calendario y las inscripciones de G-02.
- **Estimate:** 1.5 h-p
- **Uncertainty:** Medium
- **Predecessors:** Ninguna

#### Acceptance criteria
- **US-06-AC-01:** Un administrador puede introducir título, fecha y hora futuras y una capacidad entera positiva.
- **US-06-AC-02:** Al guardar correctamente, el evento queda publicado con todas las plazas disponibles y aparece en el calendario.
- **US-06-AC-03:** Si falta un campo, la fecha/hora no es futura o la capacidad no es un entero positivo, el evento no se publica y se indica qué dato debe corregirse.
- **US-06-AC-04:** Un cliente, moderador, visitante anónimo o usuario con sesión caducada no puede crear eventos; se deniega la operación sin guardar cambios y se indica que necesita una sesión de administrador.
- **US-06-AC-05:** Si falla el guardado, se informa del error, se conservan los datos introducidos y se puede reintentar.

#### Verification and constraints
- **Rules:** La creación está reservada al rol Administrador; el sistema valida autorización también al guardar, no solo al mostrar el formulario. La capacidad inicial es el aforo total del evento.
- **NFR:** Se aplican los requisitos transversales de esta épica, incluidos controles etiquetados, errores identificables y navegación por teclado.
- **Assumptions:** Los eventos son ficticios, no se editan ni cancelan en esta baseline, y sus fechas se introducen y muestran en la zona horaria local de la tienda.
- **Open questions:** Ninguna bloqueante para planificar esta historia.
