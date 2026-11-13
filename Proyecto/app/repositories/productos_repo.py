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


def existe_nombre(nombre):
    """True si ya hay un producto con ese nombre, sin distinguir mayúsculas."""
    return get_db().execute(
        "SELECT 1 FROM productos WHERE nombre = ? COLLATE NOCASE", (nombre,)
    ).fetchone() is not None


def crear(nombre, tipo, precio, stock, imagen):
    """Guarda un producto publicado y devuelve su id, que asigna la base de datos.

    Se guarda en una sola operación: si algo falla, no queda nada a medias.
    """
    db = get_db()
    with db:
        cursor = db.execute(
            "INSERT INTO productos (nombre, tipo, precio, stock, imagen, activo) VALUES (?, ?, ?, ?, ?, 1)",
            (nombre, tipo, precio, stock, imagen),
        )
    return cursor.lastrowid
