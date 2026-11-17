-- Eventos y torneos del local (EP-02).
-- fecha_hora en hora local de la tienda, formato 'AAAA-MM-DD HH:MM'.

CREATE TABLE IF NOT EXISTS eventos (
    id                  INTEGER PRIMARY KEY,
    titulo              TEXT    NOT NULL CHECK (length(trim(titulo)) > 0),
    tipo                TEXT    NOT NULL CHECK (tipo IN ('torneo', 'actividad')),
    fecha_hora          TEXT    NOT NULL,
    plazas_totales      INTEGER NOT NULL CHECK (plazas_totales > 0),
    plazas_disponibles  INTEGER NOT NULL CHECK (plazas_disponibles >= 0),
    publicado           INTEGER NOT NULL DEFAULT 1 CHECK (publicado IN (0, 1)),
    CHECK (plazas_disponibles <= plazas_totales)
);

-- Inscripciones en eventos (US-05). Cada cuenta se puede inscribir una sola vez en cada evento.
CREATE TABLE IF NOT EXISTS inscripciones (
    id          INTEGER PRIMARY KEY,
    evento_id   INTEGER NOT NULL REFERENCES eventos (id),
    usuario_id  INTEGER NOT NULL REFERENCES usuarios (id),
    fecha_hora  TEXT    NOT NULL,
    UNIQUE (evento_id, usuario_id)
);
