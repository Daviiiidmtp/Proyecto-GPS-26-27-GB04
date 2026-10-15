# EP-05 Sistema de Notificaciones

- **Goals:** G-02, G-04
- **Baseline:** Versión Inicial
- **Boundary:** Alertas internas de la web sobre eventos; no se envían correos electrónicos reales.

## Epic outcome
Que los usuarios se enteren cuando la tienda publique un torneo o evento y puedan consultarlo.

## Requisitos transversales de la épica
- La interfaz se adapta a móvil, tableta y escritorio sin perder información; los controles se pueden usar con teclado, tienen nombre y foco perceptibles, y la información no depende solo del color.
- Los datos y las alertas son ficticios/sintéticos. Un error de carga o actualización se comunica como tal, no como una lista vacía o una notificación enviada correctamente.

## Stories

### 1. US-11 Notificación de eventos
> Como usuario con cuenta activa, quiero recibir alertas internas cuando se publique un nuevo evento.

- **Priority:** Could — informa sobre novedades y facilita G-02, pero consultar el calendario e inscribirse no dependen de las alertas.
- **Estimate:** 1.5 h-p
- **Uncertainty:** Medium
- **Predecessors:** US-04, US-06, US-09

#### Acceptance criteria
- **US-11-AC-01:** Al publicarse un evento, cada cuenta Cliente activa recibe una notificación interna no leída asociada a ese evento; no se crean duplicados para la misma publicación.
- **US-11-AC-02:** La campana muestra que hay notificaciones sin leer y, al abrirse, lista las alertas no leídas con título y fecha.
- **US-11-AC-03:** Al abrir una notificación, esta queda marcada como leída y lleva a la ficha del evento asociado.
- **US-11-AC-04:** Si no hay alertas sin leer, la lista lo indica; las alertas leídas no reaparecen como no leídas.
- **US-11-AC-05:** Si el evento está completo o ya ha pasado, su ficha sigue disponible y muestra ese estado; no se ofrece la inscripción si no hay plazas o el evento ya pasó.
- **US-11-AC-06:** Si falla la carga o el marcado como leído, se informa del error; no se cambia el estado localmente como si la operación hubiese tenido éxito y se permite reintentar.
- **US-11-AC-07:** Una cuenta sin sesión activa no ve notificaciones personales; se le indica que debe iniciar sesión.

#### Verification and constraints
- **Rules:** Las notificaciones se generan solo para publicaciones correctas de eventos (`US-06`) y su destino es el evento consultable de `US-04`. No se notifican cambios de estado no cubiertos por esta baseline.
- **NFR:** Se aplican los requisitos transversales de esta épica; el estado leído/no leído se comunica con texto o semántica además de cualquier indicador visual.
- **Assumptions:** Un evento publicado no se cancela ni se elimina en esta baseline; leer una notificación no elimina el registro ni la ficha del evento.
- **Open questions:** Ninguna bloqueante para planificar esta historia.
