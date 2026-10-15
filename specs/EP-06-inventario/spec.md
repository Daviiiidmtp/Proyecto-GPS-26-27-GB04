# EP-06 Gestión de Inventario

- **Goals:** G-01, G-04
- **Baseline:** Versión Inicial
- **Boundary:** Gestión interna de productos y cantidades para la demostración; solo se usan datos y precios ficticios.

## Epic outcome
Que los Administradores puedan publicar juegos y cartas y mantener actualizadas sus cantidades disponibles en el catálogo.

## Requisitos transversales de la épica
- La interfaz se adapta a móvil, tableta y escritorio sin perder información; los controles se pueden usar con teclado, tienen nombre y foco perceptibles, y los errores no se comunican solo mediante color.
- Los cambios de inventario son visibles en el catálogo tras guardarse correctamente. No se muestra éxito ni se publica un cambio parcial si falla el guardado.
- Solo el rol Administrador puede gestionar el inventario; las operaciones protegidas verifican el rol al guardarse.

## Stories

### 1. US-12 Añadir producto
> Como administrador, quiero crear la ficha de un nuevo producto para mostrarlo en tienda.

- **Priority:** Must — es la fuente de productos para G-01 y hace posible consultar y comprar el catálogo de demostración.
- **Estimate:** 2 h-p
- **Uncertainty:** Low
- **Predecessors:** Ninguna
- **Initial plan:** Sprint 2

#### Acceptance criteria
- **US-12-AC-01:** Un Administrador autorizado dispone de un formulario para crear la ficha del producto.
- **US-12-AC-02:** El formulario requiere nombre, precio no negativo, categoría y stock entero no negativo; el sistema asigna un identificador único.
- **US-12-AC-03:** Si falta o no es válido un campo, se señala el campo que debe corregirse y no se publica la ficha.
- **US-12-AC-04:** Al guardar correctamente, el producto queda activo y aparece en el catálogo público; con stock cero se muestra como "Agotado".
- **US-12-AC-05:** La foto es opcional; cuando falta se usa una imagen por defecto y la ficha sigue siendo comprensible.
- **US-12-AC-06:** Un cliente, moderador, visitante anónimo o usuario con sesión caducada no puede crear productos; se deniega la operación sin guardar cambios.
- **US-12-AC-07:** Si falla el guardado, se muestra un error, se conservan los datos introducidos y no aparece un producto parcial o duplicado.

#### Verification and constraints
- **Rules:** Solo Administrador puede crear productos. El identificador lo asigna el sistema y no se puede introducir manualmente. El precio y stock son valores ficticios.
- **NFR:** Se aplican los requisitos transversales de esta épica; controles, validaciones y errores se perciben y operan con teclado.
- **Assumptions:** Las categorías existen como datos ficticios; administrar categorías y desactivar productos no forma parte de esta historia.
- **Open questions:** Ninguna bloqueante para planificar esta historia.

### 2. US-13 Modificar stock
> Como administrador, quiero actualizar las unidades disponibles de un artículo.

- **Priority:** Must — mantiene fiable la disponibilidad de G-01 y evita ofrecer una cantidad que ya no existe.
- **Estimate:** 1 h-p
- **Uncertainty:** Medium
- **Predecessors:** US-12

#### Acceptance criteria
- **US-13-AC-01:** Un Administrador autorizado puede aumentar o reducir el stock de un producto existente mediante una cantidad entera no negativa.
- **US-13-AC-02:** Si el nuevo stock es cero, la disponibilidad pasa a "Agotado"; si es mayor que cero, pasa a "Disponible". El producto permanece publicado en ambos casos.
- **US-13-AC-03:** Una actualización que produciría stock negativo se rechaza, conserva el valor anterior y explica el error.
- **US-13-AC-04:** Tras un cambio correcto, el nuevo stock y disponibilidad aparecen en el catálogo y se usan en el checkout simulado.
- **US-13-AC-05:** Un producto inexistente, un cliente, un moderador, un visitante o una sesión caducada no puede modificar el stock; no se aplica ningún cambio.
- **US-13-AC-06:** Si falla el guardado, se comunica el error y se conserva el último stock confirmado.
- **US-13-AC-07:** Si una actualización de stock coincide con un checkout, solo se confirman operaciones compatibles con las unidades disponibles; el stock resultante nunca es negativo y cualquier operación rechazada informa el motivo.

#### Verification and constraints
- **Rules:** Solo Administrador puede cambiar stock. Los cambios confirmados y los descuentos de checkout (`US-17`) no pueden llevar el stock por debajo de cero.
- **NFR:** Se aplican los requisitos transversales de esta épica; el stock anterior, el nuevo y los errores son distinguibles y operables con teclado.
- **Assumptions:** "Agotado" es una disponibilidad derivada del stock, no una baja del producto; las cantidades son enteros y no se admiten fracciones.
- **Open questions:** Ninguna bloqueante para planificar esta historia.
