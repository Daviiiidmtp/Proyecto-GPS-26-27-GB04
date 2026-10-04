# EP-04 Gestión de Usuarios

- **Goals:** G-01, G-02
- **Baseline:** Versión Inicial
- **Boundary:** No se van a recopilar los datos bancarios. Las contraseñas deben ir encriptadas por seguridad.

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
- **US-09-AC-02:** Si el email no tiene formato correcto, la web avisa del error.
- **US-09-AC-03:** Una vez creada la cuenta, el sistema te lleva directo a la pantalla de inicio de sesión.

#### Verification and constraints
- **Rules:** Las contraseñas tienen que tener mínimo 8 caracteres. No se puede usar el mismo email para registrar dos cuentas distintas.
- **Edge cases:** Si el usuario copia y pega el email dejando un espacio en blanco sin querer al final, el usuario lo debe borrar.
- **Constraints:** Las contraseñas se guardarán con algoritmos de encriptación.

### 2. US-10 Moderar foro
> Como administrador, quiero poder eliminar mensajes o bloquear cuentas que incumplan las normas.

- **Priority:** Must
- **Estimate:** 1.5 h-p
- **Predecessors:** US-07, US-09

#### Acceptance criteria
- **US-10-AC-01:** Si entras con cuenta de administrador, sale un botón de "Eliminar" al lado de  los mensajes del foro.
- **US-10-AC-02:** El administrador tiene una opción en el perfil de cada usuario para cambiar su estado a "Bloqueado", impidiéndole entrar a la web.