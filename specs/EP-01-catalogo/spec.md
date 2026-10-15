# EP-01 Gestión del Catálogo

- **Goals:** G-01, G-04
- **Baseline:** Versión Inicial
- **Boundary:** Uso exclusivo de productos y datos ficticios. La cesta y el checkout son una simulación: no se realizan cobros ni se solicitan, transmiten o almacenan datos financieros reales.

## Epic outcome
Que cualquier persona que entre a la web pueda ver, buscar y encontrar fácilmente los juegos y cartas disponibles, y completar una simulación de compra.

## Requisitos transversales de la épica
- La interfaz se adapta a móvil, tableta y escritorio sin perder información; los controles se pueden usar con teclado y tienen nombre y foco perceptibles; la información no depende solo del color y el texto mantiene contraste legible.
- Solo se usan datos de demostración ficticios. Los errores de carga o de operación se muestran con un mensaje comprensible; no se comunica éxito si la operación no se completó.

## Stories

### 1. US-01 Ver catálogo general
> Como usuario, quiero ver los productos disponibles para saber qué vende la tienda.

- **Priority:** Must — es la capacidad central de G-01 y alimenta búsqueda, selección y compra.
- **Estimate:** 3 h-p
- **Uncertainty:** Low
- **Predecessors:** Ninguna
- **Initial plan:** Sprint 1

#### Acceptance criteria
- **US-01-AC-01:** Al entrar en la página principal, se muestran primero los productos disponibles ordenados alfabéticamente por nombre.
- **US-01-AC-02:** Cada producto muestra foto, nombre, precio y disponibilidad; los productos agotados conservan su ficha y se identifican como "Agotado".
- **US-01-AC-03:** Si no hay productos activos, se muestra "El catálogo está vacío actualmente".
- **US-01-AC-04:** Si no se puede cargar el catálogo, se informa del error y se ofrece volver a intentarlo; no se muestra el estado vacío como si la carga hubiera tenido éxito.

#### Verification and constraints
- **Rules:** Solo se muestran productos publicados/activos. La disponibilidad se deriva del stock: disponible si es mayor que cero y agotado si es cero.
- **Edge cases:** Las imágenes grandes o pequeñas conservan una presentación legible sin deformar la ficha; una imagen ausente usa la imagen por defecto.
- **NFR:** Se aplican los requisitos transversales de esta épica. La carga inicial de la página principal debe tardar menos de 2 segundos.
- **Assumptions:** Los productos y precios son ficticios y los usuarios anónimos pueden consultar el catálogo.
- **Open questions:** Ninguna bloqueante para planificar esta historia.

### 2. US-02 Buscar productos
> Como usuario, quiero buscar productos por nombre para encontrarlos rápidamente.

- **Priority:** Must — encontrar productos es parte del recorrido esencial de G-01 y depende del catálogo.
- **Estimate:** 1 h-p
- **Uncertainty:** Low
- **Predecessors:** US-01

#### Acceptance criteria
- **US-02-AC-01:** El catálogo ofrece un campo identificable para buscar por nombre.
- **US-02-AC-02:** La búsqueda devuelve los nombres que contienen el texto introducido, sin distinguir mayúsculas de minúsculas y sin considerar espacios accidentales al principio o al final.
- **US-02-AC-03:** Una búsqueda vacía o compuesta solo por espacios muestra de nuevo todos los productos disponibles.
- **US-02-AC-04:** Si no hay coincidencias, se muestra "No se han encontrado productos que coincidan con tu búsqueda".
- **US-02-AC-05:** Si falla la búsqueda, se muestra un error y se permite reintentar sin borrar el texto introducido.

#### Verification and constraints
- **NFR:** Se aplican los requisitos transversales de esta épica; el campo y sus resultados son operables con teclado y su estado se comunica sin depender solo del color.
- **Assumptions:** La búsqueda se limita al nombre de los productos del catálogo publicado.
- **Open questions:** Ninguna bloqueante para planificar esta historia.

### 3. US-03 Filtrar por categoría
> Como usuario, quiero filtrar productos por tipo para acotar la búsqueda.

- **Priority:** Should — mejora la exploración, pero el catálogo y la búsqueda permiten consultar productos sin este refinamiento.
- **Estimate:** 1 h-p
- **Uncertainty:** Medium
- **Predecessors:** US-01

#### Acceptance criteria
- **US-03-AC-01:** El catálogo permite seleccionar una categoría existente.
- **US-03-AC-02:** Al seleccionar una categoría, se muestran solo los productos disponibles de esa categoría.
- **US-03-AC-03:** Si la categoría no tiene productos disponibles, se muestra "Actualmente no hay productos en esta categoría".
- **US-03-AC-04:** Se puede quitar el filtro y volver a ver todos los productos disponibles.
- **US-03-AC-05:** Si no se pueden cargar las categorías, se muestra un error distinguible de una categoría sin productos y se permite reintentar.

#### Verification and constraints
- **NFR:** Se aplican los requisitos transversales de esta épica; la categoría seleccionada y la opción de quitar el filtro son perceptibles y operables con teclado.
- **Assumptions:** Las categorías ya están disponibles en los datos ficticios; su mantenimiento no forma parte de esta historia.
- **Open questions:** Ninguna bloqueante para planificar esta historia.

### 4. US-16 Añadir productos a la cesta
> Como usuario, quiero añadir a una cesta los productos que tengo intención de comprar para no comprarlos de forma individual.

- **Priority:** Should — habilita la selección de varios artículos dentro del recorrido de compra de S-01, que sigue siendo simulado.
- **Estimate:** 1 h-p
- **Uncertainty:** Medium
- **Predecessors:** US-01

#### Acceptance criteria
- **US-16-AC-01:** Se pueden añadir productos disponibles a la cesta y quitar productos o unidades de ella.
- **US-16-AC-02:** La cesta muestra producto, cantidad, precio unitario y subtotal, además del total.
- **US-16-AC-03:** Si la cesta está vacía, se informa y no se permite iniciar el checkout.
- **US-16-AC-04:** Si el producto deja de estar disponible o no hay unidades suficientes, se informa qué artículo no puede comprarse y se permite corregir la cesta.

#### Verification and constraints
- **Rules:** Las cantidades son enteros positivos; la cesta no reserva stock. Se comprueba de nuevo la disponibilidad al simular el checkout.
- **NFR:** Se aplican los requisitos transversales de esta épica; cantidades, subtotales y total se presentan de forma comprensible.
- **Assumptions:** El checkout es una demostración con datos ficticios y no exige cuenta.
- **Open questions:** Ninguna bloqueante para planificar esta historia.

### 5. US-17 Simular compra
> Como usuario, quiero completar una compra simulada de los productos de mi cesta para ver el resultado de mi pedido.

- **Priority:** Must — cubre el recorrido de compra simulado declarado en S-01; no autoriza transacciones monetarias reales.
- **Estimate:** 1.5 h-p
- **Uncertainty:** Medium
- **Predecessors:** US-01, US-13, US-16

#### Acceptance criteria
- **US-17-AC-01:** El checkout permite seleccionar un método de pago de demostración, sin conectarse a un proveedor ni solicitar datos financieros reales.
- **US-17-AC-02:** Antes de confirmar, se muestra el resumen con artículos, cantidades, precios y total ficticio.
- **US-17-AC-03:** La confirmación genera un resultado de pedido simulado y un mensaje explícito de éxito; no se realiza ningún cobro.
- **US-17-AC-04:** Si un artículo está inactivo o su stock es insuficiente, se muestra un error, no se crea un pedido exitoso y no se modifica ningún stock.
- **US-17-AC-05:** Si la simulación se completa, descuenta las unidades del stock una sola vez; el stock nunca puede quedar negativo.
- **US-17-AC-06:** Si falla la operación, se informa del error y el usuario puede corregir o reintentar el checkout.
- **US-17-AC-07:** Repetir la confirmación de un checkout ya completado devuelve el mismo resultado y no crea otro pedido ni vuelve a descontar stock.

#### Verification and constraints
- **Rules:** Solo se simulan productos y métodos de pago ficticios. No se cobran importes, ni se transmiten o almacenan credenciales o datos bancarios reales.
- **NFR:** Se aplican los requisitos transversales de esta épica; el resumen, el resultado y los errores son perceptibles y navegables con teclado.
- **Assumptions:** La reserva de stock solo ocurre al confirmar una simulación exitosa; no se ofrece cancelación ni reembolso en esta baseline.
- **Open questions:** Ninguna bloqueante para planificar esta historia.
