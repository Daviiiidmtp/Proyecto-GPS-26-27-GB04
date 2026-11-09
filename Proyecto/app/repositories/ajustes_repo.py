"""Consultas sobre la tabla `ajustes`."""
from app.db import get_db


def obtener(clave):
    """Devuelve el valor de un ajuste o None si no existe."""
    fila = get_db().execute(
        "SELECT valor FROM ajustes WHERE clave = ?", (clave,)
    ).fetchone()
    return fila["valor"] if fila else None
