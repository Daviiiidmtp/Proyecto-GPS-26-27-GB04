-- Productos ficticios de ejemplo. Se usa INSERT OR IGNORE con id fijo.
-- Hay productos agotados (stock 0) y uno no publicado (activo 0) para probar todos los casos.

INSERT OR IGNORE INTO productos (id, nombre, tipo, precio, stock, imagen, activo) VALUES
    (1,  'Colonos de la Comarca',            'mesa',   39.95, 12, NULL, 1),
    (2,  'Sobre de cartas: Dragones de Bruma','cartas',  4.50, 80, NULL, 1),
    (3,  'Manual del Aventurero Errante',     'rol',    29.90,  5, NULL, 1),
    (4,  'Mazo inicial: Bosque Antiguo',      'cartas', 14.95,  0, NULL, 1),
    (5,  'El Último Puente',                  'mesa',   24.50,  3, NULL, 1),
    (6,  'Dados de rol de madera (set de 7)', 'rol',     9.99, 40, NULL, 1),
    (7,  'Caja de mejora: Torres de Niebla',  'cartas', 89.00,  0, NULL, 1),
    (8,  'Aldeas y Caminos',                  'mesa',   19.95,  8, NULL, 1),
    (9,  'Pantalla del Narrador',             'rol',    17.50,  0, NULL, 1),
    (10, 'Edición coleccionista retirada',    'mesa',  120.00,  2, NULL, 0);
