# EP-01 Gestión del Catálogo

- **Goals:** G-01
- **Baseline:** Versión Inicial
- **Boundary:** Uso de productos y datos totalmente ficticios. 
## Epic outcome
Que cualquier persona que entre a la web pueda ver, buscar y encontrar fácilmente los juegos y cartas que tenemos a la venta sin perderse.

## Stories

### 1. US-01 Ver catálogo general
> Como usuario, quiero ver los productos disponibles para saber qué vende la tienda.

- **Priority:** Must
- **Estimate:** 3 h-p
- **Uncertainty:** Low
- **Predecessors:** Ninguna
- **Initial plan:** Sprint 1

#### Acceptance criteria
- **US-01-AC-01:** Al entrar en la página principal, se ven los productos ordenados alfabeticamente.
- **US-01-AC-02:** Cada producto tiene su propia tarjeta donde se ve la foto, el nombre y cuánto cuesta.
- **US-01-AC-03:** Si no hay productos subidos a la web, la pantalla avisa con un mensaje con un mensaje por pantalla diciendo que "El catálogo está vacío actualmente".

#### Verification and constraints
- **Rules:** Solo tienen que aparecer los productos que tengamos marcados como "Activos".
- **Edge cases:** Si se sube una foto muy grande o muy pequeña de un producto, la web tiene que ajustarla sola para que quede bien.
- **Constraints:** La página principal tiene que cargar rápido para que la gente no se canse de esperar y se vaya.

### 2. US-02 Buscar productos
> Como usuario, quiero buscar productos por nombre para encontrarlos rápidamente..

- **Priority:** Must
- **Estimate:** 1 h-p
- **Predecessors:** US-01

#### Acceptance criteria
- **US-02-AC-01:** Tiene que haber una barra de búsqueda en la parte de arriba de la web para poder escribir en ella para buscar los productos.
- **US-02-AC-02:** Si escribo algo, la web me debe mostrar los productos que lleven esas letras en el nombre, aunque no escriba la palabra completa.

### 3. US-03 Filtrar por categoría
> Como usuario, quiero filtrar productos por tipo para acotar la búsqueda.

- **Priority:** Should
- **Estimate:** 1 h-p
- **Predecessors:** US-01

#### Acceptance criteria
- **US-03-AC-01:** Tiene que haber una opción que permita elegir qué categoría de productos quieres ver.
- **US-03-AC-02:** Cuando seleccionas una categoría, la web me debe mostrar los productos de esa categoria.
