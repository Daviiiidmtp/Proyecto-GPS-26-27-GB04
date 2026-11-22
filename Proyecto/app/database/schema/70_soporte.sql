-- Incidencias del formulario de contacto (US-14). Datos ficticios: no se envía ningún correo.
-- La tienda las consulta fuera de la web para hacer el seguimiento.
-- codigo: se genera al mostrar el formulario. Si se envía dos veces con el mismo código,
-- solo se guarda una incidencia (US-14-AC-05).
-- fecha_hora en hora local de la tienda, formato 'AAAA-MM-DD HH:MM:SS'.

CREATE TABLE IF NOT EXISTS incidencias (
    id          INTEGER PRIMARY KEY,
    codigo      TEXT    NOT NULL UNIQUE,
    nombre      TEXT    NOT NULL CHECK (length(trim(nombre)) > 0),
    email       TEXT    NOT NULL CHECK (length(trim(email)) > 0),
    asunto      TEXT    NOT NULL CHECK (length(trim(asunto)) > 0),
    mensaje     TEXT    NOT NULL CHECK (length(trim(mensaje)) > 0),
    estado      TEXT    NOT NULL DEFAULT 'registrada' CHECK (estado IN ('registrada', 'respondida')),
    fecha_hora  TEXT    NOT NULL
);
