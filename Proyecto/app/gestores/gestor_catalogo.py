"""Gestor Catálogo (EP-01 Catálogo y EP-06 Inventario).

Cada método lo implementa la historia indicada. Hasta entonces lanza
NotImplementedError. Los métodos @Admin solo los puede usar un administrador.
"""
import sqlite3

from app.repositories import productos_repo


class CatalogoNoDisponible(Exception):
    """No se ha podido leer el catálogo. La interfaz muestra un error y permite reintentar."""


def _a_producto(fila):
    """Convierte una fila de la base de datos en un producto para la interfaz.

    La disponibilidad se calcula a partir del stock: disponible si es mayor que cero.
    """
    disponible = fila["stock"] > 0
    return {
        "id": fila["id"],
        "nombre": fila["nombre"],
        "tipo": fila["tipo"],
        "precio": round(float(fila["precio"]), 2),
        "stock": fila["stock"],
        "imagen": fila["imagen"],  # None: la interfaz usa la imagen por defecto
        "disponible": disponible,
        "estado": "Disponible" if disponible else "Agotado",
    }


def _es_valido(fila):
    """Descarta filas con datos incoherentes para no mostrarlas en la tienda."""
    return (
        bool(fila["nombre"] and fila["nombre"].strip())
        and fila["precio"] is not None and fila["precio"] >= 0
        and fila["stock"] is not None and fila["stock"] >= 0
    )


def getProductos():
    """Lista de productos activos ordenada por nombre. -> list. US-01

    Incluye los agotados, que conservan su ficha con estado «Agotado».
    Lanza CatalogoNoDisponible si no se puede leer la base de datos.
    """
    try:
        filas = productos_repo.listar_activos()
    except sqlite3.Error as error:
        raise CatalogoNoDisponible("No se ha podido cargar el catálogo") from error
    return [_a_producto(fila) for fila in filas if _es_valido(fila)]


def getProducto(idProducto):
    """Un producto por su id (None si no existe). -> dict. US-01
    En el diagrama es getProductos(int idProducto); Python no permite dos
    funciones con el mismo nombre, así que se llama getProducto."""
    try:
        fila = productos_repo.obtener(idProducto)
    except sqlite3.Error as error:
        raise CatalogoNoDisponible("No se ha podido cargar el producto") from error
    return _a_producto(fila) if fila and _es_valido(fila) else None


def getProductosPorNombre(nombre):
    """Productos cuyo nombre contiene el texto. -> list. US-02"""
    raise NotImplementedError("Pendiente: US-02 Buscar productos")


def getProductosPorTipo(tipo):
    """Productos de una categoría. -> list. US-03"""
    raise NotImplementedError("Pendiente: US-03 Filtrar por categoría")


def getProductosDisponibles():
    """Productos con stock mayor que cero. -> list. US-01"""
    return [producto for producto in getProductos() if producto["disponible"]]


def anadirProductoCesta(idProducto, cantidad):
    """Añade un producto a la cesta. -> bool. US-16"""
    raise NotImplementedError("Pendiente: US-16 Añadir productos a la cesta")


def realizarCompra(idUsuario):
    """Compra simulada de la cesta (sin pagos reales). -> bool. US-17"""
    raise NotImplementedError("Pendiente: US-17 Simular compra")


def getCesta(idUsuario):
    """Cesta del usuario. -> dict. US-16"""
    raise NotImplementedError("Pendiente: US-16 Añadir productos a la cesta")


# ---------- @Admin ----------

def crearProducto(producto):
    """@Admin. Da de alta un producto. -> bool. US-12"""
    raise NotImplementedError("Pendiente: US-12 Añadir producto")


def cambiarStock(idProducto, stock):
    """@Admin. Cambia las unidades disponibles. -> bool. US-13"""
    raise NotImplementedError("Pendiente: US-13 Modificar stock")
