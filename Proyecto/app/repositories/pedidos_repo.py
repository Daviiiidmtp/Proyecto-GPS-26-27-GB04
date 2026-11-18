"""Consultas SQL de la compra simulada (US-17): tablas `pedidos` y `lineas_pedido`."""
from app.db import get_db


class SinStock(Exception):
    """Un producto ya no tiene unidades suficientes o ya no está a la venta al confirmar la compra."""

    def __init__(self, producto_id, nombre):
        super().__init__(nombre)
        self.producto_id = producto_id
        self.nombre = nombre


def obtener_por_codigo(codigo):
    """Un pedido por el código de su checkout, o None si no existe."""
    return get_db().execute(
        "SELECT id, codigo, usuario_id, metodo_pago, total, fecha_hora FROM pedidos WHERE codigo = ?",
        (codigo,),
    ).fetchone()


def lineas(pedido_id):
    """Líneas de un pedido, en el orden en que se guardaron."""
    return get_db().execute(
        "SELECT producto_id, nombre, cantidad, precio FROM lineas_pedido WHERE pedido_id = ? ORDER BY id",
        (pedido_id,),
    ).fetchall()


def crear(codigo, usuario_id, metodo_pago, total, lineas_cesta, fecha_hora):
    """Descuenta el stock y guarda el pedido con sus líneas en una sola operación. Devuelve el id del pedido.

    `lineas_cesta` es la lista de líneas de getCesta (id, nombre, cantidad, precio).
    BEGIN IMMEDIATE bloquea la escritura: si llegan dos confirmaciones a la vez, la segunda
    espera, encuentra el pedido ya guardado con el mismo código y lo devuelve sin descontar nada.
    El stock solo baja si quedan unidades suficientes, así nunca queda negativo (US-17-AC-05).
    Si a un producto le faltan unidades o ya no está a la venta, se deshace todo y salta SinStock,
    sin pedido y sin cambios en ningún stock (US-17-AC-04).
    """
    db = get_db()
    if not db.in_transaction:
        db.execute("BEGIN IMMEDIATE")
    try:
        existente = db.execute("SELECT id FROM pedidos WHERE codigo = ?", (codigo,)).fetchone()
        if existente is not None:
            db.rollback()
            return existente["id"]
        for linea in lineas_cesta:
            cursor = db.execute(
                "UPDATE productos SET stock = stock - ? WHERE id = ? AND activo = 1 AND stock >= ?",
                (linea["cantidad"], linea["id"], linea["cantidad"]),
            )
            if cursor.rowcount == 0:
                raise SinStock(linea["id"], linea["nombre"])
        cursor = db.execute(
            "INSERT INTO pedidos (codigo, usuario_id, metodo_pago, total, fecha_hora) VALUES (?, ?, ?, ?, ?)",
            (codigo, usuario_id, metodo_pago, total, fecha_hora),
        )
        pedido_id = cursor.lastrowid
        db.executemany(
            "INSERT INTO lineas_pedido (pedido_id, producto_id, nombre, cantidad, precio) VALUES (?, ?, ?, ?, ?)",
            [(pedido_id, linea["id"], linea["nombre"], linea["cantidad"], linea["precio"]) for linea in lineas_cesta],
        )
        db.commit()
        return pedido_id
    except Exception:
        db.rollback()
        raise
