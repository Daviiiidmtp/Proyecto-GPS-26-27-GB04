"""Gestor Catálogo (EP-01 Catálogo y EP-06 Inventario).

Cada método lo implementa la historia indicada. Hasta entonces lanza
NotImplementedError. Los métodos @Admin solo los puede usar un administrador.
"""


def getProductos():
    """Lista de productos activos ordenada por nombre. -> list. US-01"""
    raise NotImplementedError("Pendiente: US-01 Ver catálogo general")


def getProducto(idProducto):
    """Un producto por su id (None si no existe). -> dict. US-01
    En el diagrama es getProductos(int idProducto); Python no permite dos
    funciones con el mismo nombre, así que se llama getProducto."""
    raise NotImplementedError("Pendiente: US-01 Ver catálogo general")


def getProductosPorNombre(nombre):
    """Productos cuyo nombre contiene el texto. -> list. US-02"""
    raise NotImplementedError("Pendiente: US-02 Buscar productos")


def getProductosPorTipo(tipo):
    """Productos de una categoría. -> list. US-03"""
    raise NotImplementedError("Pendiente: US-03 Filtrar por categoría")


def getProductosDisponibles():
    """Productos con stock mayor que cero. -> list. US-01"""
    raise NotImplementedError("Pendiente: US-01 Ver catálogo general")


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
