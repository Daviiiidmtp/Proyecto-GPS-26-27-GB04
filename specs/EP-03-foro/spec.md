# EP-03 Gestión de Foro

- **Goals:** G-03
- **Baseline:** Versión Inicial
- **Boundary:** Con una funcionalidad básica de texto, sin subir fotos ni archivos en los mensajes.

## Epic outcome
Que los usuarios tengan un espacio dentro de la web para charlar, debatir sobre los juegos y hacer comunidad.

## Stories

### 1. US-07 Crear tema en foro
> Como usuario, quiero crear un hilo de discusión para interactuar con la comunidad.

- **Priority:** Should
- **Estimate:** 1.5 h-p
- **Predecessors:** US-09 

#### Acceptance criteria
- **US-07-AC-01:** Si el usuario ha iniciado sesión, ve un botón de "Nuevo Tema" en la sección del foro.
- **US-07-AC-02:** Para publicarlo, el sistema pide obligatoriamente escribir un título y el cuerpo del mensaje.
- **US-07-AC-03:** Al darle a enviar, el tema nuevo aparece el primero en la lista principal del foro.

### 2. US-08 Responder en foro
> Como usuario, quiero responder en hilos existentes para participar en debates.

- **Priority:** Should
- **Estimate:** 1.5 h-p
- **Predecessors:** US-07, US-09

#### Acceptance criteria
- **US-08-AC-01:** Al entrar en cualquier hilo del foro, aparece una caja de texto abajo del todo para poder escribir y responder.
- **US-08-AC-02:** Cuando se envía la respuesta, esta se coloca al final de la conversación con la fecha y hora de publicación.