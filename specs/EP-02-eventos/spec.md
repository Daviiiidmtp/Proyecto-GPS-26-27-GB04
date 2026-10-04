# EP-02 Gestión de Eventos

- **Goals:** G-02
- **Baseline:** Versión Inicial
- **Boundary:** Gestión de plazas locales.

## Epic outcome
Que los jugadores tengan un lugar donde ver los próximos torneos de la tienda y puedan reservar su plaza fácilmente.

## Stories

### 1. US-04 Ver calendario de eventos
> Como usuario, quiero ver un calendario con los próximos torneos y actividades.

- **Priority:** Must
- **Estimate:** 2 h-p
- **Uncertainty:** Low
- **Predecessors:** Ninguna
- **Initial plan:** Sprint 1

#### Acceptance criteria
- **US-04-AC-01:** Los eventos se muestran ordenados por fecha, empezando por los más próximos.
- **US-04-AC-02:** Cada evento muestra el título, la fecha, la hora y cuántas plazas quedan libres.
- **US-04-AC-03:** Los eventos que ya han pasado no se deben mostrar.

#### Verification and constraints
- **Rules:** Las horas de los eventos deben coincidir con la zona horaria local de la tienda.
- **Edge cases:** Si hay dos eventos  a la misma hora y día, la web tiene que poder mostrarlos sin que se vea mal. 
- **Constraints:** El calendario debe verse bien tanto en la pantalla del ordenador como en el móvil.

### 2. US-05 Inscribirse en evento
> Como usuario, quiero apuntarme a un evento para asegurar mi plaza.

- **Priority:** Must
- **Estimate:** 1.5 h-p
- **Uncertainty:** Medium
- **Predecessors:** US-04
- **Initial plan:** Sprint 1

#### Acceptance criteria
- **US-05-AC-01:** Si el usuario ha iniciado sesión y quedan plazas, aparece un botón de "Inscribirse".
- **US-05-AC-02:** Al pulsar el botón, el número de plazas disponibles baja automáticamente en 1.
- **US-05-AC-03:** La pantalla muestra un mensaje confirmando que la plaza ha sido reservada con éxito.

#### Verification and constraints
- **Rules:** Una misma cuenta no puede apuntarse dos veces al mismo torneo.
- **Edge cases:** Si queda solo 1 plaza y dos personas le dan a "Inscribirse" a la vez, el sistema tiene que dársela al primer que le dió y avisar al segundo de que ya está lleno.

### 3. US-06 Añadir evento
> Como administrador, quiero crear la ficha de un nuevo evento.

- **Priority:** Must
- **Estimate:** 1.5 h-p
- **Predecessors:** Ninguna

#### Acceptance criteria
- **US-06-AC-01:** Los administradores tienen un formulario donde pueden escribir el nombre del evento, la fecha y el límite de jugadores.
- **US-06-AC-02:** En cuanto guardan el formulario, el evento aparece publicado en el calendario de los usuarios.