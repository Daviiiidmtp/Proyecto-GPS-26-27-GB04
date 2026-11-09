-- Tablas comunes a toda la aplicación.
-- Cada módulo crea las suyas en su propio archivo:
--   10_catalogo.sql, 20_eventos.sql, 30_foro.sql, 40_usuarios.sql,
--   50_notificaciones.sql, 60_inventario.sql, 70_soporte.sql

CREATE TABLE IF NOT EXISTS ajustes (
    clave TEXT PRIMARY KEY,
    valor TEXT NOT NULL
);
