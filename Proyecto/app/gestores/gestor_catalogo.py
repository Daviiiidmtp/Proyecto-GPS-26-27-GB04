"""Gestor Catálogo (EP-01 Catálogo y EP-06 Inventario).

Cada método lo implementa la historia indicada. Hasta entonces lanza
NotImplementedError. Los métodos @Admin solo los puede usar un administrador.
"""
import re
import sqlite3

from app.gestores import gestor_usuario
from app.gestores.categorias import CATEGORIAS
from app.repositories import cesta_repo, productos_repo


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


# ---------- Cesta (US-16) ----------
# La cesta es un diccionario {"id del producto": cantidad} que la interfaz guarda en la
# sesión del navegador, porque el checkout simulado no exige cuenta (spec EP-01).
# La cesta no reserva stock: la disponibilidad se comprueba al añadir, al mostrar la
# cesta y de nuevo al simular la compra (US-17).

MAXIMO_POR_PRODUCTO = 99


class CantidadInvalida(Exception):
    """La cantidad no es un número entero positivo (regla de US-16)."""


class ProductoNoDisponible(Exception):
    """El producto no se puede añadir. Indica qué artículo es y por qué (US-16-AC-04).

    Motivos: no_existe, agotado, insuficiente.
    """

    def __init__(self, motivo, mensaje, nombre=None, disponibles=0):
        super().__init__(mensaje)
        self.motivo = motivo
        self.nombre = nombre
        self.disponibles = disponibles


def _cantidad(cantidad):
    """Convierte la cantidad en un entero positivo o lanza CantidadInvalida."""
    texto = str(cantidad).strip() if cantidad is not None else ""
    if not texto.isdigit() or int(texto) < 1:
        raise CantidadInvalida("La cantidad debe ser un número entero mayor que 0.")
    if int(texto) > MAXIMO_POR_PRODUCTO:
        raise CantidadInvalida(f"No puedes añadir más de {MAXIMO_POR_PRODUCTO} unidades de un producto.")
    return int(texto)


def anadirProductoCesta(idProducto, cantidad, cesta):
    """Añade unidades de un producto disponible a la cesta. -> bool. US-16

    En el diagrama es anadirProductoCesta(idProducto, cantidad); aquí también recibe
    la cesta de la sesión, que se modifica directamente.
    Lanza CantidadInvalida si la cantidad no es un entero positivo,
    ProductoNoDisponible si el producto no existe, está agotado o no hay unidades
    suficientes (US-16-AC-04), y CatalogoNoDisponible si falla la base de datos.
    """
    unidades = _cantidad(cantidad)
    producto = getProducto(idProducto)
    if producto is None:
        raise ProductoNoDisponible("no_existe", "El producto no existe o ya no está a la venta.")
    if not producto["disponible"]:
        raise ProductoNoDisponible("agotado", f"«{producto['nombre']}» está agotado.", producto["nombre"])
    clave = str(producto["id"])
    total = cesta.get(clave, 0) + unidades
    if total > MAXIMO_POR_PRODUCTO:
        raise CantidadInvalida(f"No puedes tener más de {MAXIMO_POR_PRODUCTO} unidades de un producto en la cesta.")
    if total > producto["stock"]:
        raise ProductoNoDisponible(
            "insuficiente",
            f"No hay unidades suficientes de «{producto['nombre']}». Quedan {producto['stock']}.",
            producto["nombre"], producto["stock"])
    cesta[clave] = total
    return True


def quitarProductoCesta(idProducto, cesta, cantidad=None):
    """Quita unidades de un producto de la cesta, o el producto entero si no se indica cantidad. -> bool. US-16

    Si la cantidad llega a 0, el producto sale de la cesta (US-16-AC-01).
    Devuelve False si el producto no estaba en la cesta.
    Lanza CantidadInvalida si la cantidad no es un entero positivo.
    """
    clave = str(idProducto)
    if clave not in cesta:
        return False
    if cantidad is None:
        del cesta[clave]
        return True
    restantes = cesta[clave] - _cantidad(cantidad)
    if restantes > 0:
        cesta[clave] = restantes
    else:
        del cesta[clave]
    return True


def realizarCompra(idUsuario):
    """Compra simulada de la cesta (sin pagos reales). -> bool. US-17"""
    raise NotImplementedError("Pendiente: US-17 Simular compra")


def _linea(clave, cantidad):
    """Una línea de la cesta con su subtotal y, si no se puede comprar, el motivo (US-16-AC-04)."""
    fila = cesta_repo.obtener_cualquiera(int(clave))
    if fila is None:
        return {"id": int(clave), "nombre": "Producto retirado", "cantidad": cantidad, "precio": 0.0,
                "subtotal": 0.0, "stock": 0, "se_puede_comprar": False,
                "problema": "Este producto ya no existe. Quítalo de la cesta."}
    precio = round(float(fila["precio"]), 2)
    problema = None
    if not fila["activo"]:
        problema = f"«{fila['nombre']}» ya no está a la venta. Quítalo de la cesta."
    elif fila["stock"] == 0:
        problema = f"«{fila['nombre']}» está agotado. Quítalo de la cesta."
    elif cantidad > fila["stock"]:
        problema = f"Solo quedan {fila['stock']} unidades de «{fila['nombre']}». Reduce la cantidad."
    return {"id": fila["id"], "nombre": fila["nombre"], "cantidad": cantidad, "precio": precio,
            "subtotal": round(precio * cantidad, 2), "stock": fila["stock"],
            "se_puede_comprar": problema is None, "problema": problema}


def getCesta(cesta):
    """Contenido de la cesta con cantidades, precios, subtotales y total. -> dict. US-16

    En el diagrama es getCesta(idUsuario); aquí recibe la cesta de la sesión.
    Devuelve: lineas (producto, cantidad, precio unitario, subtotal y problema si lo hay),
    total, unidades, vacia y se_puede_comprar. Con la cesta vacía o con algún artículo
    que no se puede comprar, se_puede_comprar es False y no se deja iniciar el checkout
    (US-16-AC-03 y AC-04). Las claves que no son ids válidos se ignoran.
    Lanza CatalogoNoDisponible si falla la base de datos.
    """
    try:
        lineas = [_linea(clave, cantidad) for clave, cantidad in (cesta or {}).items()
                  if str(clave).isdigit() and isinstance(cantidad, int) and cantidad > 0]
    except sqlite3.Error as error:
        raise CatalogoNoDisponible("No se ha podido cargar la cesta") from error
    vacia = not lineas
    return {
        "lineas": lineas,
        "total": round(sum(linea["subtotal"] for linea in lineas), 2),
        "unidades": sum(linea["cantidad"] for linea in lineas),
        "vacia": vacia,
        "se_puede_comprar": not vacia and all(linea["se_puede_comprar"] for linea in lineas),
    }


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


class StockInvalido(Exception):
    """El nuevo stock no es un número entero igual o mayor que 0 (US-13-AC-03)."""


class ProductoNoEncontrado(Exception):
    """El producto no existe o no está publicado (US-13-AC-05)."""


def _nuevo_stock(stock):
    """Convierte el nuevo stock en un entero no negativo o lanza StockInvalido."""
    texto = str(stock).strip() if stock is not None else ""
    if texto.startswith("-") and texto[1:].isdigit():
        raise StockInvalido("El stock no puede ser negativo.")
    if not texto.isdigit():
        raise StockInvalido("El stock debe ser un número entero igual o mayor que 0, sin decimales.")
    return int(texto)


def cambiarStock(idProducto, stock, idUsuario):
    """@Admin. Cambia las unidades disponibles de un producto y devuelve el producto actualizado. -> dict. US-13

    En el diagrama es cambiarStock(idProducto, stock) y devuelve bool; aquí también
    recibe el usuario de la sesión, para comprobar que es administrador, y devuelve
    el producto para que la interfaz muestre el stock y la disponibilidad nuevos.
    Con stock 0 el producto pasa a «Agotado» y sigue publicado (US-13-AC-02).
    Lanza PermisoDenegado si el usuario no es administrador (US-13-AC-05),
    ProductoNoEncontrado si el producto no existe (US-13-AC-05),
    StockInvalido si el valor es negativo o no es entero (US-13-AC-03)
    y CatalogoNoDisponible si falla el guardado (US-13-AC-06).
    En todos los errores se conserva el último stock confirmado.
    """
    try:
        if idUsuario is None or gestor_usuario.getRolUsuario(idUsuario) != "admin":
            raise PermisoDenegado("Solo un administrador puede modificar el stock.")
        nuevo = _nuevo_stock(stock)
        if productos_repo.obtener(idProducto) is None:
            raise ProductoNoEncontrado("El producto no existe o ya no está publicado.")
        if not productos_repo.actualizar_stock(idProducto, nuevo):
            raise ProductoNoEncontrado("El producto no existe o ya no está publicado.")
    except sqlite3.Error as error:
        raise CatalogoNoDisponible("No se ha podido guardar el stock") from error
    return getProducto(idProducto)
