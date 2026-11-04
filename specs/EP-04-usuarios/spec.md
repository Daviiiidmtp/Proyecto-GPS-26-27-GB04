# EP-04 Gestión de Usuarios

- **Goals:** G-01, G-02, G-03, G-04
- **Baseline:** v2 (re-entrega P1)
- **Boundary:** Se usan cuentas y datos ficticios/sintéticos; no se recopilan datos personales ni bancarios reales. La verificación y las notificaciones de correo son simuladas.

## Epic outcome
Que el sistema gestione cuentas de clientes y distinga los permisos de Moderador y Administrador para proteger la comunidad y las funciones de gestión.

## Roles y requisitos transversales de la épica
- **Cliente:** cuenta activa con acceso a las funciones de cliente.
- **Moderador:** puede retirar mensajes del foro; no puede bloquear cuentas ni gestionar usuarios, eventos o productos.
- **Administrador:** puede crear eventos y productos, retirar mensajes y bloquear cuentas.
- Las cuentas nuevas son Clientes. Las cuentas iniciales de Moderador y Administrador son preconfiguradas para la demostración; el registro público no puede asignar esos roles.
- La interfaz se adapta a móvil, tableta y escritorio sin perder información; los controles se pueden usar con teclado, tienen nombre y foco perceptibles, y los errores no se comunican solo mediante color.
- Las funciones protegidas verifican el rol y el estado de la cuenta al ejecutar la operación, no solo al mostrar la pantalla.

## Stories

### 1. US-09 Registro de usuario
> Como usuario invitado previamente, quiero activar una cuenta de cliente con email sintético y contraseña para participar en la web.

- **Priority:** Must — autenticación y verificación son necesarias para participar en eventos y foros y hacen compatible el alta con E-03.
- **Estimate:** 13 h-p
- **Uncertainty:** Medium
- **Predecessors:** Ninguna
- **Initial plan:** IT-02 (R1)

#### Acceptance criteria
- **US-09-AC-01:** Solo se puede iniciar el alta con una invitación de un solo uso autorizada y entregada por un Administrador; la invitación se aprovisiona fuera del registro público y una visita sin invitación no crea una cuenta.
- **US-09-AC-02:** El formulario solicita email sintético, nombre de usuario y contraseña dos veces; las contraseñas deben coincidir, tener al menos 8 caracteres y no estar vacías.
- **US-09-AC-03:** El email debe tener formato válido y ser único. Si el email, la invitación o cualquier campo no cumple las condiciones, se indica el motivo y no se crea una cuenta activa.
- **US-09-AC-04:** Una solicitud válida crea una cuenta Cliente pendiente de verificación y muestra que se ha enviado un correo de confirmación simulado, sin enviar correo real.
- **US-09-AC-05:** La cuenta solo pasa a activa después de utilizar el enlace/token de verificación simulado asociado a la invitación; antes de ello no permite iniciar sesión ni participar.
- **US-09-AC-06:** Una invitación no puede activar más de una cuenta; si ya se utilizó o fue revocada, se informa del estado y no se activa la cuenta.

#### Verification and constraints
- **Rules:** El flujo controlado es invitación autorizada por Administrador más verificación simulada. El alta asigna únicamente el rol Cliente. No se aceptan datos personales reales.
- **NFR:** Se aplican los requisitos transversales de esta épica. La contraseña se almacena mediante hash seguro para contraseñas (por ejemplo, bcrypt), nunca en texto plano ni mediante cifrado reversible.
- **Assumptions:** Las invitaciones y los datos de contacto de demostración son sintéticos; el Administrador las entrega a usuarios autorizados y las cuentas iniciales de Administrador y Moderador se aprovisionan fuera del registro público.
- **Open questions:** Ninguna bloqueante para planificar esta historia.

### 2. US-10 Moderar foro y bloquear cuentas
> Como administrador, quiero retirar mensajes que incumplan las normas o bloquear cuentas para proteger a la comunidad.

- **Priority:** Must — es el control necesario para que la participación de la comunidad pueda moderarse con los roles definidos.
- **Estimate:** 8 h-p
- **Uncertainty:** Medium
- **Predecessors:** US-07, US-08, US-09
- **Initial plan:** IT-06 (R3)

#### Acceptance criteria
- **US-10-AC-01:** El Moderador y el Administrador pueden retirar un mensaje; la acción requiere confirmación, el mensaje deja de ser visible para todos y se comunica el resultado.
- **US-10-AC-02:** Solo el Administrador puede cambiar una cuenta Cliente activa a bloqueada; la cuenta bloqueada no puede iniciar sesión ni participar.
- **US-10-AC-03:** Bloquear una cuenta invalida sus sesiones activas; las siguientes operaciones protegidas se deniegan y no guardan cambios.
- **US-10-AC-04:** Solo el Administrador puede devolver una cuenta bloqueada al estado activo; el cambio no borra sus mensajes ni crea una sesión automáticamente.
- **US-10-AC-05:** Un Cliente o visitante no puede acceder a ninguna acción de moderación; un Moderador no puede bloquear/desbloquear cuentas. Se deniega el acceso y no se modifica el mensaje ni la cuenta.
- **US-10-AC-06:** Una sesión caducada no puede completar ninguna acción de moderación; se informa de que debe iniciar sesión. Una falla al guardar se comunica y no muestra un resultado exitoso.
- **US-10-AC-07:** Retirar un mensaje o bloquear una cuenta que ya está retirada/bloqueada informa del estado actual y no duplica ni altera la operación.

#### Verification and constraints
- **Rules:** Moderador y Administrador son roles distintos. Solo Administrador puede gestionar eventos, productos y estados de cuenta; Moderador solo puede retirar contenido del foro.
- **NFR:** Se aplican los requisitos transversales de esta épica; las acciones protegidas y sus resultados son identificables y accesibles con teclado.
- **Assumptions:** La retirada de mensajes es reversible solo mediante una nueva publicación; la recuperación de una cuenta bloqueada requiere acción explícita de Administrador.
- **Open questions:** Ninguna bloqueante para planificar esta historia.
