-- Pedidos de la compra simulada (US-17).
-- No se cobra nada ni se guardan datos de pago reales: solo el nombre del método de demostración.
-- fecha_hora en hora local de la tienda, formato 'AAAA-MM-DD HH:MM:SS'.

-- codigo identifica el checkout. Si se confirma dos veces con el mismo código,
-- se devuelve el mismo pedido y no se crea otro (US-17-AC-07).
-- usuario_id queda vacío si se compra sin iniciar sesión, porque el checkout no exige cuenta.
CREATE TABLE IF NOT EXISTS pedidos (
    id           INTEGER PRIMARY KEY,
    codigo       TEXT    NOT NULL UNIQUE,
    usuario_id   INTEGER REFERENCES usuarios (id),
    metodo_pago  TEXT    NOT NULL,
    total        REAL    NOT NULL CHECK (total >= 0),
    fecha_hora   TEXT    NOT NULL
);

-- Cada línea guarda el nombre y el precio del momento de la compra,
-- así el resultado del pedido no cambia aunque después cambie el catálogo.
CREATE TABLE IF NOT EXISTS lineas_pedido (
    id           INTEGER PRIMARY KEY,
    pedido_id    INTEGER NOT NULL REFERENCES pedidos (id),
    producto_id  INTEGER NOT NULL REFERENCES productos (id),
    nombre       TEXT    NOT NULL,
    cantidad     INTEGER NOT NULL CHECK (cantidad > 0),
    precio       REAL    NOT NULL CHECK (precio >= 0)
);
