"""Consultas SQL sobre la tabla `incidencias` (US-14)."""
from app.db import get_db


def obtener_por_codigo(codigo):
    return get_db().execute(
        "SELECT id, codigo, nombre, email, asunto, mensaje, estado, fecha_hora FROM incidencias WHERE codigo = ?",
        (codigo,),
    ).fetchone()


def crear(codigo, nombre, email, asunto, mensaje, fecha_hora):
    """Guarda la incidencia y devuelve su id.

    INSERT OR IGNORE con codigo UNIQUE: si llega dos veces el mismo envío, solo se guarda
    la primera vez y se devuelve el id de la que ya existe (US-14-AC-05).
    """
    db = get_db()
    with db:
        db.execute(
            "INSERT OR IGNORE INTO incidencias (codigo, nombre, email, asunto, mensaje, fecha_hora) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (codigo, nombre, email, asunto, mensaje, fecha_hora),
        )
    return obtener_por_codigo(codigo)["id"]
