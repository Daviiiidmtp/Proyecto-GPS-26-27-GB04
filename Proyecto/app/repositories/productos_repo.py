"""Consultas SQL sobre la tabla `productos`."""
from app.db import get_db


def listar_activos():
    """Productos publicados, ordenados alfabéticamente por nombre."""
    return get_db().execute(
        "SELECT id, nombre, tipo, precio, stock, imagen FROM productos "
        "WHERE activo = 1 ORDER BY nombre COLLATE NOCASE"
    ).fetchall()


def obtener(id_producto):
    """Un producto publicado por su id, o None si no existe."""
    return get_db().execute(
        "SELECT id, nombre, tipo, precio, stock, imagen FROM productos "
        "WHERE id = ? AND activo = 1",
        (id_producto,),
    ).fetchone()
