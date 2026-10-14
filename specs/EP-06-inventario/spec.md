# EP-06 Gestión de Inventario

- **Goals:** G-01
- **Baseline:** Versión Inicial
- **Boundary:** Gestión interna básica para la web.

## Epic outcome
Que los dueños de la tienda puedan añadir juegos y cartas nuevas a la web, y cambiar las cantidades disponibles.

## Stories

### 1. US-12 Añadir producto
> Como administrador, quiero crear la ficha de un nuevo producto para mostrarlo en tienda.

- **Priority:** Must
- **Estimate:** 2 h-p
- **Uncertainty:** Low
- **Predecessors:** Ninguna
- **Initial plan:** Sprint 2

#### Acceptance criteria
- **US-12-AC-01:** Hay un panel privado de administrador con un formulario claro para crear productos.
- **US-12-AC-02:** El formulario obliga a rellenar sí o sí: nombre, precio, categoría y cantidad de stock.
- **US-12-AC-03:** Cuando se guarda, el producto aparece automáticamente en el catálogo público de la web.

#### Verification and constraints
- **Rules:** El sistema no puede permitir que se pongan precios en negativo ni que se escriban letras en la casilla del stock. Además, el acceso a la creación de productos está restringido exclusivamente al rol de Administrador. Si un usuario normal, anónimo o con sesión caducada intenta acceder, el sistema denegará el acceso y lo redirigirá al Login.
- **Edge cases:** Si al administrador se le olvida subir la foto del producto, el sistema le pone una imagen "por defecto" (como el logo de la tienda) para que la página del catálogo no se vea con un hueco en blanco.
- **Constraints:** El código o ID de cada producto lo tiene que crear la base de datos de forma automática, no lo puede escribir el administrador a mano para evitar duplicados.

### 2. US-13 Modificar stock
> Como administrador, quiero actualizar las unidades disponibles de un artículo.

- **Priority:** Must
- **Estimate:** 1 h-p
- **Predecessors:** US-12

#### Acceptance criteria
- **US-13-AC-01:** En el panel privado, el administrador puede entrar a un producto ya creado y sumar o restar el número de artículos que quedan.
- **US-13-AC-02:** Si cambia el stock a 0, el producto cambia automáticamente de estado y pone "Agotado".

#### Verification and constraints
- **Rules:** La modificación de stock está restringida al rol de Administrador. Cualquier intento de acceso por parte de usuarios no autorizados o con sesión caducada redirigirá a la pantalla de inicio de sesión.