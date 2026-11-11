-- Usuarios e invitaciones (EP-04).
-- El alta solo es posible con una invitación de un solo uso entregada por un Administrador.

CREATE TABLE IF NOT EXISTS invitaciones (
    id      INTEGER PRIMARY KEY,
    codigo  TEXT NOT NULL UNIQUE,
    estado  TEXT NOT NULL DEFAULT 'disponible' CHECK (estado IN ('disponible', 'usada', 'revocada'))
);

CREATE TABLE IF NOT EXISTS usuarios (
    id                  INTEGER PRIMARY KEY,
    email               TEXT NOT NULL UNIQUE COLLATE NOCASE,
    nombre_usuario      TEXT NOT NULL,
    hash_contrasena     TEXT NOT NULL,
    rol                 TEXT NOT NULL DEFAULT 'cliente' CHECK (rol IN ('cliente', 'moderador', 'admin')),
    estado              TEXT NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'activa', 'bloqueada')),
    token_verificacion  TEXT UNIQUE,
    invitacion_id       INTEGER REFERENCES invitaciones (id)
);
