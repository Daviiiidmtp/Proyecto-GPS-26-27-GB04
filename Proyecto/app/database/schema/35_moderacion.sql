-- Moderación del foro (US-10).
-- Un mensaje retirado no se borra: se apunta aquí y deja de mostrarse a todos.
-- tipo es 'tema' o 'respuesta'. Cada mensaje solo se puede retirar una vez (US-10-AC-07).
-- fecha_hora en hora local de la tienda, formato 'AAAA-MM-DD HH:MM:SS'.

CREATE TABLE IF NOT EXISTS mensajes_retirados (
    id           INTEGER PRIMARY KEY,
    tipo         TEXT    NOT NULL CHECK (tipo IN ('tema', 'respuesta')),
    mensaje_id   INTEGER NOT NULL,
    usuario_id   INTEGER NOT NULL REFERENCES usuarios (id),
    fecha_hora   TEXT    NOT NULL,
    UNIQUE (tipo, mensaje_id)
);
