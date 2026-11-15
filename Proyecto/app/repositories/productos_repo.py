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


def actualizar_stock(id_producto, stock):
    """Cambia el stock de un producto publicado. Devuelve True si se ha cambiado.

    BEGIN IMMEDIATE bloquea la escritura mientras dura el cambio: si a la vez llega
    una compra simulada (US-17), una de las dos espera a que termine la otra.
    La tabla no admite stock negativo (CHECK stock >= 0), así que nunca puede quedar por debajo de 0.
    Si algo falla, se deshace y queda el último stock confirmado.
    """
    db = get_db()
    if not db.in_transaction:
        db.execute("BEGIN IMMEDIATE")
    try:
        cursor = db.execute(
            "UPDATE productos SET stock = ? WHERE id = ? AND activo = 1", (stock, id_producto)
        )
        db.commit()
        return cursor.rowcount == 1
    except Exception:
        db.rollback()
        raise
