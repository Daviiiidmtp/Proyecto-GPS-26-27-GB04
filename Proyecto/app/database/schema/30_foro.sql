-- Foro de la comunidad (EP-03).
-- Solo texto, sin fotos ni archivos. fecha_hora en hora local de la tienda, formato 'AAAA-MM-DD HH:MM:SS'.

-- Temas del foro (US-07). Cada tema tiene un autor, un título y el texto con el que se abre el debate.
CREATE TABLE IF NOT EXISTS temas (
    id          INTEGER PRIMARY KEY,
    titulo      TEXT    NOT NULL CHECK (length(trim(titulo)) > 0),
    cuerpo      TEXT    NOT NULL CHECK (length(trim(cuerpo)) > 0),
    usuario_id  INTEGER NOT NULL REFERENCES usuarios (id),
    fecha_hora  TEXT    NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_temas_fecha ON temas (fecha_hora);
