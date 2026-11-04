# EP-07 Soporte y contacto

- **Goals:** G-01, G-04
- **Baseline:** v2 (re-entrega P1)
- **Boundary:** Formulario de contacto y FAQs de demostración con datos ficticios. No se envían correos electrónicos reales ni se recopilan datos personales reales.

## Epic outcome
Que los clientes puedan consultar respuestas a dudas habituales o dejar una incidencia para seguimiento de la tienda.

## Requisitos transversales de la épica
- La interfaz se adapta a móvil, tableta y escritorio sin perder información; los controles se pueden usar con teclado, tienen nombre y foco perceptibles, y los errores no se comunican solo mediante color.
- Los datos de contacto y ejemplos son ficticios/sintéticos. Los errores se diferencian de una lista vacía y no se muestra confirmación hasta completar la operación indicada.

## Stories

### 1. US-14 Formulario de contacto
> Como usuario, quiero rellenar un formulario para enviar incidencias a la tienda.

- **Priority:** Should — ofrece una vía de soporte, complementaria a la consulta autónoma de las FAQs y al objetivo de la tienda.
- **Estimate:** 5 h-p
- **Uncertainty:** Medium
- **Predecessors:** Ninguna
- **Initial plan:** IT-06 (R3)

#### Acceptance criteria
- **US-14-AC-01:** La página de Contacto es accesible desde el pie de página.
- **US-14-AC-02:** El formulario solicita nombre, email sintético, asunto y mensaje; todos son obligatorios.
- **US-14-AC-03:** Si falta un campo o el email no tiene formato válido, se indica qué corregir y no se registra la incidencia.
- **US-14-AC-04:** Al completar y registrar correctamente la solicitud ficticia, se muestra "Tu mensaje ha sido enviado correctamente".
- **US-14-AC-05:** Si falla el registro, se muestra un error distinto del éxito, se conservan los datos introducidos y se permite reintentar sin crear duplicados.
- **US-14-AC-06:** No se envían correos ni se aceptan datos personales reales; la confirmación indica que la solicitud quedó registrada para seguimiento, no que ya haya sido respondida.

#### Verification and constraints
- **Rules:** El campo de email solo admite un identificador sintético para la demostración. Una incidencia no se considera enviada hasta quedar registrada correctamente.
- **NFR:** Se aplican los requisitos transversales de esta épica; etiquetas, validaciones, confirmación y errores son accesibles mediante teclado y tecnologías de asistencia.
- **Assumptions:** Las solicitudes registradas quedan disponibles para seguimiento por la tienda fuera del flujo del usuario; la respuesta y el correo de confirmación están fuera de esta baseline.
- **Open questions:** Ninguna bloqueante para planificar esta historia.

### 2. US-15 Ver FAQs
> Como usuario, quiero leer una sección de preguntas frecuentes para resolver dudas rápidas.

- **Priority:** Should — permite resolver consultas comunes sin contacto directo, pero es complementaria al catálogo y a la inscripción en eventos.
- **Estimate:** 3 h-p
- **Uncertainty:** Low
- **Predecessors:** Ninguna
- **Initial plan:** IT-01 (R1)

#### Acceptance criteria
- **US-15-AC-01:** La página de Preguntas Frecuentes muestra una lista de preguntas y sus respuestas.
- **US-15-AC-02:** Cada pregunta permite identificar y consultar su respuesta; si se presenta como contenido expandible, su estado abierto/cerrado se comunica y se puede cambiar con teclado.
- **US-15-AC-03:** Si todavía no hay preguntas cargadas, se muestra un mensaje indicando que no hay preguntas frecuentes disponibles.
- **US-15-AC-04:** Si no se pueden cargar las FAQs, se muestra un error distinguible de la lista vacía y se permite reintentar.

#### Verification and constraints
- **Rules:** El contenido es ficticio y está disponible públicamente; gestionar o editar preguntas frecuentes no forma parte de esta historia.
- **NFR:** Se aplican los requisitos transversales de esta épica; preguntas y respuestas conservan un orden y estructura comprensibles y son accesibles con teclado.
- **Assumptions:** Las preguntas y respuestas son contenido estático de demostración suministrado con el proyecto.
- **Open questions:** Ninguna bloqueante para planificar esta historia.
