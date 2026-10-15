# EP-03 Gestión de Foro

- **Goals:** G-03, G-04
- **Baseline:** Versión Inicial
- **Boundary:** Foro de texto básico; no se suben fotos ni archivos. Leer temas y respuestas es público; participar requiere una cuenta verificada y activa.

## Epic outcome
Que los usuarios puedan comunicarse y debatir sobre los juegos en un espacio comunitario.

## Roles y requisitos transversales de la épica
- **Cliente:** puede leer públicamente y, con sesión autenticada y cuenta verificada no bloqueada, crear temas y responder.
- **Moderador:** puede retirar mensajes que incumplan las normas; no puede bloquear cuentas ni gestionar eventos, productos o usuarios.
- **Administrador:** puede retirar mensajes y bloquear cuentas.
- La interfaz se adapta a móvil, tableta y escritorio sin perder información; los controles se pueden usar con teclado y tienen nombre y foco perceptibles; la información no depende solo del color y el texto mantiene contraste legible.
- Los mensajes son texto sin adjuntos. Se usan cuentas y contenido ficticios o sintéticos; los errores de publicación se comunican sin fingir que el contenido se guardó.

## Stories

### 1. US-07 Crear tema en foro
> Como usuario con cuenta verificada, quiero crear un hilo de discusión para interactuar con la comunidad.

- **Priority:** Should — la conversación inicia la participación comunitaria de G-03, después de habilitar las cuentas.
- **Estimate:** 1.5 h-p
- **Uncertainty:** Medium
- **Predecessors:** US-09

#### Acceptance criteria
- **US-07-AC-01:** Los visitantes pueden consultar la lista pública de temas; solo una cuenta autenticada, verificada y no bloqueada ve y puede usar "Nuevo tema".
- **US-07-AC-02:** Para publicar se requieren título y cuerpo no vacíos; los mensajes no admiten fotos ni archivos.
- **US-07-AC-03:** Tras guardar correctamente, el tema aparece al principio de la lista con autor y fecha/hora.
- **US-07-AC-04:** Si falta título o cuerpo, se indica qué campo debe completarse y no se publica el tema.
- **US-07-AC-05:** Un visitante, una cuenta sin verificar, bloqueada o con sesión caducada no puede publicar; se deniega la operación y no se guarda el tema.
- **US-07-AC-06:** Si falla el guardado, se muestra un error, se conserva el texto para reintentar y no se añade un duplicado.

#### Verification and constraints
- **Rules:** Administrador y Moderador tienen las facultades de moderación descritas en esta épica, pero no necesitan permisos especiales para leer el foro.
- **NFR:** Se aplican los requisitos transversales de esta épica; el título, autor, fecha y acciones son distinguibles y operables con teclado.
- **Assumptions:** La lista vacía se presenta como foro sin temas; no se permiten publicaciones anónimas ni edición de temas en esta baseline.
- **Open questions:** Ninguna bloqueante para planificar esta historia.

### 2. US-08 Responder en foro
> Como usuario con cuenta verificada, quiero responder en hilos existentes para participar en debates.

- **Priority:** Should — permite conversaciones de G-03, una vez que existen temas y autenticación.
- **Estimate:** 1.5 h-p
- **Uncertainty:** Medium
- **Predecessors:** US-07, US-09

#### Acceptance criteria
- **US-08-AC-01:** Las respuestas de un hilo son visibles públicamente; solo una cuenta autenticada, verificada y no bloqueada puede responder.
- **US-08-AC-02:** Una respuesta no puede estar vacía; si falta el texto, se indica el error y no se publica.
- **US-08-AC-03:** Al guardarse correctamente, la respuesta aparece al final del hilo con autor y fecha/hora.
- **US-08-AC-04:** Si el hilo no existe, se informa de que no está disponible y no se guarda la respuesta.
- **US-08-AC-05:** Visitantes, cuentas sin verificar, bloqueadas o con sesión caducada no pueden responder; una falla al guardar se informa y permite reintentar sin duplicar la respuesta.

#### Verification and constraints
- **Rules:** La respuesta es texto plano sin fotos ni archivos. El Moderador puede retirar respuestas que incumplan las normas; el Administrador puede retirarlas también.
- **NFR:** Se aplican los requisitos transversales de esta épica; el orden cronológico, autor, fecha/hora y errores son perceptibles y accesibles con teclado.
- **Assumptions:** No se pueden editar respuestas ni reabrir hilos retirados en esta baseline.
- **Open questions:** Ninguna bloqueante para planificar esta historia.
