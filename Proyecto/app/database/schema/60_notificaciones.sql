-- Notificaciones internas de eventos (US-11). No se envían correos reales.
-- Al publicarse un evento, cada cuenta Cliente activa recibe una notificación no leída.
-- UNIQUE (usuario_id, evento_id): nunca hay dos avisos del mismo evento para la misma cuenta (US-11-AC-01).
-- Leer una notificación no la borra: solo cambia `leida` a 1.
-- fecha_hora es el momento de la publicación, en hora local de la tienda, formato 'AAAA-MM-DD HH:MM'.

CREATE TABLE IF NOT EXISTS notificaciones (
    id          INTEGER PRIMARY KEY,
    usuario_id  INTEGER NOT NULL REFERENCES usuarios (id),
    evento_id   INTEGER NOT NULL REFERENCES eventos (id),
    fecha_hora  TEXT    NOT NULL,
    leida       INTEGER NOT NULL DEFAULT 0 CHECK (leida IN (0, 1)),
    UNIQUE (usuario_id, evento_id)
);

CREATE INDEX IF NOT EXISTS ix_notificaciones_usuario ON notificaciones (usuario_id, leida);
