"""Consultas SQL que necesita la cesta (US-16).

La cesta se guarda en la sesión, no en la base de datos. Aquí solo se leen los productos
que hay en ella, también los retirados, para poder decir qué artículo ya no se puede comprar.
"""
from app.db import get_db


def obtener_cualquiera(id_producto):
    """Un producto por su id, esté publicado o no, o None si no existe."""
    return get_db().execute(
        "SELECT id, nombre, precio, stock, activo FROM productos WHERE id = ?", (id_producto,)
    ).fetchone()
