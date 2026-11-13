"""Gestor Catálogo (EP-01 Catálogo y EP-06 Inventario).

Cada método lo implementa la historia indicada. Hasta entonces lanza
NotImplementedError. Los métodos @Admin solo los puede usar un administrador.
"""
import re
import sqlite3

from app.gestores import gestor_usuario
from app.gestores.categorias import CATEGORIAS
from app.repositories import productos_repo


class CatalogoNoDisponible(Exception):
    """No se ha podido leer el catálogo. La interfaz muestra un error y permite reintentar."""


class ProductoInvalido(Exception):
    """Los datos del producto no son válidos. `errores` indica el campo y el motivo."""

    def __init__(self, errores):
        super().__init__("; ".join(errores.values()))
        self.errores = errores


class PermisoDenegado(Exception):
    """Solo un administrador puede hacer esta operación."""


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
    """Productos cuyo nombre contiene el texto. -> list. US-02

    No distingue mayúsculas de minúsculas y quita los espacios del principio
    y del final. Si el texto está vacío, devuelve todo el catálogo.
    Lanza CatalogoNoDisponible si no se puede leer la base de datos.
    """
    texto = (nombre or "").strip().casefold()
    productos = getProductos()
    if not texto:
        return productos
    return [producto for producto in productos if texto in producto["nombre"].casefold()]


def getProductosPorTipo(tipo):
    """Productos disponibles de una categoría, ordenados por nombre. -> list. US-03

    Solo devuelve los que tienen stock, como pide US-03-AC-02.
    Lanza CatalogoNoDisponible si no se puede leer la base de datos.
    """
    return [producto for producto in getProductosDisponibles() if producto["tipo"] == tipo]


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

LONGITUD_MAXIMA_NOMBRE = 100
PATRON_PRECIO = re.compile(r"^\d+([.,]\d{1,2})?$")
PATRON_STOCK = re.compile(r"^\d+$")
INICIOS_IMAGEN = ("http://", "https://", "/static/")


def _validar_producto(producto):
    """Comprueba cada campo y devuelve (errores, datos limpios). US-12-AC-02 y 03"""
    errores = {}
    nombre = (producto.get("nombre") or "").strip()
    precio = (producto.get("precio") or "").strip()
    tipo = (producto.get("tipo") or "").strip()
    stock = (producto.get("stock") or "").strip()
    imagen = (producto.get("imagen") or "").strip()

    if not nombre:
        errores["nombre"] = "El nombre es obligatorio."
    elif len(nombre) > LONGITUD_MAXIMA_NOMBRE:
        errores["nombre"] = f"El nombre no puede tener más de {LONGITUD_MAXIMA_NOMBRE} caracteres."
    elif productos_repo.existe_nombre(nombre):
        errores["nombre"] = "Ya existe un producto con ese nombre."

    if not precio:
        errores["precio"] = "El precio es obligatorio."
    elif not PATRON_PRECIO.match(precio):
        errores["precio"] = "El precio debe ser un número no negativo con hasta 2 decimales, por ejemplo 19,95."

    if not tipo:
        errores["tipo"] = "Elige una categoría."
    elif tipo not in CATEGORIAS:
        errores["tipo"] = "La categoría no existe."

    if not stock:
        errores["stock"] = "El stock es obligatorio."
    elif not PATRON_STOCK.match(stock):
        errores["stock"] = "El stock debe ser un número entero igual o mayor que 0."

    if imagen and not imagen.startswith(INICIOS_IMAGEN):
        errores["imagen"] = "La dirección de la foto debe empezar por http://, https:// o /static/."

    datos = {
        "nombre": nombre,
        "tipo": tipo,
        "precio": float(precio.replace(",", ".")) if "precio" not in errores else None,
        "stock": int(stock) if "stock" not in errores else None,
        "imagen": imagen or None,  # sin foto se usa la imagen por defecto (US-12-AC-05)
    }
    return errores, datos


def crearProducto(producto, idUsuario):
    """@Admin. Da de alta un producto publicado y devuelve su id. US-12

    `producto` es un diccionario con nombre, precio, tipo, stock e imagen (opcional),
    tal y como llegan del formulario. El id lo asigna la base de datos.
    Lanza PermisoDenegado si el usuario no es administrador (US-12-AC-06),
    ProductoInvalido con el campo y el motivo de cada error (US-12-AC-03)
    y CatalogoNoDisponible si falla el guardado (US-12-AC-07).
    En el diagrama devuelve bool; aquí devuelve el id para poder enlazar el producto.
    """
    try:
        if idUsuario is None or gestor_usuario.getRolUsuario(idUsuario) != "admin":
            raise PermisoDenegado("Solo un administrador puede añadir productos.")
        errores, datos = _validar_producto(producto)
        if errores:
            raise ProductoInvalido(errores)
        return productos_repo.crear(datos["nombre"], datos["tipo"], datos["precio"], datos["stock"], datos["imagen"])
    except sqlite3.IntegrityError as error:
        # Dos altas a la vez con el mismo nombre: solo se guarda la primera
        raise ProductoInvalido({"nombre": "Ya existe un producto con ese nombre."}) from error
    except sqlite3.Error as error:
        raise CatalogoNoDisponible("No se ha podido guardar el producto") from error


def cambiarStock(idProducto, stock):
    """@Admin. Cambia las unidades disponibles. -> bool. US-13"""
    raise NotImplementedError("Pendiente: US-13 Modificar stock")
