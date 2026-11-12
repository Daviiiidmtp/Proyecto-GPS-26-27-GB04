"""Consultas SQL sobre las tablas `usuarios` e `invitaciones`."""
from app.db import get_db


def obtener_invitacion(codigo):
    return get_db().execute(
        "SELECT id, codigo, estado FROM invitaciones WHERE codigo = ?", (codigo,)
    ).fetchone()


def existe_email(email):
    return get_db().execute(
        "SELECT 1 FROM usuarios WHERE email = ?", (email,)
    ).fetchone() is not None


def crear_pendiente(email, nombre_usuario, hash_contrasena, invitacion_id, token):
    """Crea la cuenta pendiente y marca la invitación como usada, en una sola operación."""
    db = get_db()
    with db:
        db.execute(
            "INSERT INTO usuarios (email, nombre_usuario, hash_contrasena, rol, estado, token_verificacion, invitacion_id) "
            "VALUES (?, ?, ?, 'cliente', 'pendiente', ?, ?)",
            (email, nombre_usuario, hash_contrasena, token, invitacion_id),
        )
        db.execute("UPDATE invitaciones SET estado = 'usada' WHERE id = ?", (invitacion_id,))


def obtener_por_token(token):
    return get_db().execute(
        "SELECT id, estado FROM usuarios WHERE token_verificacion = ?", (token,)
    ).fetchone()


def activar(id_usuario):
    db = get_db()
    with db:
        db.execute(
            "UPDATE usuarios SET estado = 'activa', token_verificacion = NULL WHERE id = ?", (id_usuario,)
        )


def obtener_por_email(email):
    return get_db().execute(
        "SELECT id, email, nombre_usuario, hash_contrasena, rol, estado FROM usuarios WHERE email = ?", (email,)
    ).fetchone()


def obtener_por_id(id_usuario):
    return get_db().execute(
        "SELECT id, email, nombre_usuario, rol, estado FROM usuarios WHERE id = ?", (id_usuario,)
    ).fetchone()
