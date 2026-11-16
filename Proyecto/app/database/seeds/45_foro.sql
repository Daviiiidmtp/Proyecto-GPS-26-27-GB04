-- Temas ficticios de ejemplo. Se usa INSERT OR IGNORE con id fijo.
-- Va después de 40_usuarios.sql porque cada tema necesita que su autor ya exista.
-- Los escriben las cuentas iniciales (1 Administración, 2 Moderación).

INSERT OR IGNORE INTO temas (id, titulo, cuerpo, usuario_id, fecha_hora) VALUES
    (1, 'Normas del foro',
        'Bienvenidos al foro de El Hogar del Hobbit. Respetad a los demás, hablad de juegos y no publiquéis datos personales.',
        1, '2026-11-01 10:00:00'),
    (2, '¿Qué mazo usáis para el Torneo de Dragones de Bruma?',
        'Estoy preparando el torneo de diciembre y dudo entre un mazo de bosque y uno de niebla. ¿Qué os funciona mejor?',
        2, '2026-11-08 18:30:00');
