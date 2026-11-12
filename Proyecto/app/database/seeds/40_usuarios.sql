-- Datos ficticios de usuarios. Se usa INSERT OR IGNORE con id fijo.
-- Invitaciones de demostración que entrega el Administrador:
--   INV-HOBBIT-001 a INV-HOBBIT-005 están disponibles, INV-HOBBIT-900 ya se usó e INV-HOBBIT-999 está revocada.
-- Cuentas iniciales, creadas fuera del registro público (todos los datos son ficticios):
--   admin@hobbit.test      contraseña Admin-Hobbit-2026
--   moderador@hobbit.test  contraseña Moderador-Hobbit-2026

INSERT OR IGNORE INTO invitaciones (id, codigo, estado) VALUES
    (1, 'INV-HOBBIT-001', 'disponible'),
    (2, 'INV-HOBBIT-002', 'disponible'),
    (3, 'INV-HOBBIT-003', 'disponible'),
    (4, 'INV-HOBBIT-004', 'disponible'),
    (5, 'INV-HOBBIT-005', 'disponible'),
    (900, 'INV-HOBBIT-900', 'usada'),
    (999, 'INV-HOBBIT-999', 'revocada');

INSERT OR IGNORE INTO usuarios (id, email, nombre_usuario, hash_contrasena, rol, estado) VALUES
    (1, 'admin@hobbit.test', 'Administración', 'scrypt:32768:8:1$N5hMbvzggoSQjHmf$262f46cd1a704d36ed93064e869504b1f1c18415a1b853c428a1fa9f2c676d91e93aa1ee238aa269009a63bccc3c2a0b53b4985c00dee3a97c45ed387223e4e7', 'admin', 'activa'),
    (2, 'moderador@hobbit.test', 'Moderación', 'scrypt:32768:8:1$Ssa1WGCI7GMz7NPR$a2399dadae8df660e4a6347297ba45464e4aa5162a520784fa1269e900f15d89d9c98718e62d8d759668a682812758acb8ce5046f768275c242c20482adc7a93', 'moderador', 'activa');
