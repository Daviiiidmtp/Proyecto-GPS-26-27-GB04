-- Datos ficticios comunes. Usar siempre INSERT OR IGNORE con id/clave fija,
-- porque este archivo se ejecuta en cada arranque.

INSERT OR IGNORE INTO ajustes (clave, valor) VALUES
    ('nombre_tienda', 'El Hogar del Hobbit'),
    ('lema', 'Cartas, juegos de mesa, rol y comunidad');
