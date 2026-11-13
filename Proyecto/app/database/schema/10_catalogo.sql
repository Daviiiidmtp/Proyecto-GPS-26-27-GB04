-- Catálogo de productos (EP-01).
-- tipo: cartas, mesa o rol. activo = 1 si el producto está publicado.

CREATE TABLE IF NOT EXISTS productos (
    id      INTEGER PRIMARY KEY,
    nombre  TEXT    NOT NULL CHECK (length(trim(nombre)) > 0),
    tipo    TEXT    NOT NULL CHECK (tipo IN ('cartas', 'mesa', 'rol')),
    precio  REAL    NOT NULL CHECK (precio >= 0),
    stock   INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    imagen  TEXT,
    activo  INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1))
);

-- US-12: no puede haber dos productos con el mismo nombre (evita duplicados al guardar dos veces).
CREATE UNIQUE INDEX IF NOT EXISTS ux_productos_nombre ON productos (nombre COLLATE NOCASE);
