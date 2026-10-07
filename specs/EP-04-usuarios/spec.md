# EP-04 Gestión de Usuarios

- **Goals:** G-01, G-02
- **Baseline:** Versión Inicial
- **Boundary:** No se van a recopilar datos bancarios reales. Las contraseñas deben ir encriptadas por seguridad.

## Epic outcome
Que el sistema diferencie quién es cliente y quién es administrador, para poder gestionar las cuentas, foros y eventos sin problemas de permisos.

## Stories

### 1. US-09 Registro de usuario
> Como usuario, quiero crear una cuenta con email y contraseña para registrarme en la web.

- **Priority:** Must
- **Estimate:** 2 h-p
- **Uncertainty:** Low
- **Predecessors:** Ninguna
- **Initial plan:** Sprint 1

#### Acceptance criteria
- **US-09-AC-01:** El formulario de registro pide un email, un nombre de usuario y escribir la contraseña dos veces para confirmar.
- **US-09-AC-02:** Si el email no tiene formato correcto o los campos están vacíos, la web avisa del error con un mensaje en rojo.
- **US-09-AC-03:** Una vez enviado el formulario, el sistema muestra un mensaje indicando que se ha enviado un correo (simulado) con un enlace de confirmación.
- **US-09-AC-04:** La cuenta solo se activa y permite el acceso al perfil después de que el usuario haya verificado su correo electrónico.

#### Verification and constraints
- **Rules:** Las contraseñas tienen que tener mínimo 8 caracteres. No se puede usar el mismo email para registrar dos cuentas distintas. El registro exige verificación (doble opt-in) para evitar cuentas automatizadas y cumplir con la exclusión E-03.
- **Edge cases:** Si el usuario copia y pega el email dejando un espacio en blanco sin querer al final, el sistema lo elimina automáticamente antes de guardar.
- **Constraints:** Las contraseñas se guardarán usando algoritmos de encriptación seguros (ej. bcrypt), nunca en texto plano.

### 2. US-10 Moderar foro
> Como administrador, quiero poder eliminar mensajes o bloquear cuentas que incumplan las normas.

- **Priority:** Must
- **Estimate:** 1.5 h-p
- **Predecessors:** US-07

#### Acceptance criteria
- **US-10-AC-01:** Si entras con cuenta de administrador, sale un botón de "Eliminar" al lado de los mensajes del foro.
- **US-10-AC-02:** El administrador tiene una opción en el perfil de cada usuario para cambiar su estado a "Bloqueado", impidiéndole iniciar sesión en la web.

#### Verification and constraints
- **Rules:** El acceso a los botones de eliminar mensajes y bloquear usuarios está restringido exclusivamente al rol de Administrador. Si un usuario no autorizado intenta acceder a funciones de moderación, el sistema lo redirige a la pantalla de inicio de sesión.