-- Eventos ficticios de ejemplo. Se usa INSERT OR IGNORE con id fijo.
-- Hay un evento pasado, uno completo, dos a la misma hora y uno sin publicar para probar todos los casos.

INSERT OR IGNORE INTO eventos (id, titulo, tipo, fecha_hora, plazas_totales, plazas_disponibles, publicado) VALUES
    (1, 'Torneo de Dragones de Bruma',          'torneo',    '2026-12-05 17:00', 32, 12, 1),
    (2, 'Noche de juegos de mesa',               'actividad', '2026-12-11 19:30', 20, 20, 1),
    (3, 'Campaña de rol: El Último Puente',      'actividad', '2026-12-12 18:00',  6,  0, 1),
    (4, 'Torneo relámpago de Colonos',           'torneo',    '2026-12-12 18:00', 16,  9, 1),
    (5, 'Taller de pintura de miniaturas',       'actividad', '2027-01-16 11:00', 10,  4, 1),
    (6, 'Gran torneo de invierno',               'torneo',    '2027-02-06 10:00', 64, 64, 1),
    (7, 'Torneo de otoño (ya celebrado)',        'torneo',    '2026-10-03 17:00', 32,  0, 1),
    (8, 'Evento en preparación',                 'actividad', '2027-03-01 18:00', 12, 12, 0);
