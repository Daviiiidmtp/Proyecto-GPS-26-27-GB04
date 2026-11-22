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


# ---------- Bloqueo de cuentas (US-10) ----------

def listar_clientes():
    """Cuentas Cliente con su estado, ordenadas por nombre de usuario."""
    return get_db().execute(
        "SELECT id, email, nombre_usuario, rol, estado FROM usuarios WHERE rol = 'cliente' "
        "ORDER BY nombre_usuario COLLATE NOCASE, id"
    ).fetchall()


def cambiar_estado_cliente(id_usuario, desde, hasta):
    """Pasa una cuenta Cliente del estado `desde` al estado `hasta` en una sola operación.

    Devuelve True si ha cambiado y False si la cuenta no estaba en `desde` o no es Cliente.
    Así, si dos administradores pulsan a la vez, solo cuenta el primero (US-10-AC-07).
    """
    db = get_db()
    with db:
        cursor = db.execute(
            "UPDATE usuarios SET estado = ? WHERE id = ? AND rol = 'cliente' AND estado = ?",
            (hasta, id_usuario, desde),
        )
    return cursor.rowcount == 1
