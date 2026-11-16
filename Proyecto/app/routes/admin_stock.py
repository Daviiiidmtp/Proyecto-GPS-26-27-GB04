"""Modificar el stock de los productos desde administración (US-13).

Solo pueden entrar los administradores. La lógica y las validaciones están en
gestor_catalogo.cambiarStock; aquí se muestra la tabla de productos y los mensajes.
"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.gestores import gestor_catalogo

bp = Blueprint("admin_stock", __name__)

ACCION = "modificar el stock"


def _tabla(errores=None, intentos=None, error_general=None, codigo=200):
    """Muestra la tabla de stock. Si no se puede leer el catálogo, muestra el error."""
    try:
        productos = gestor_catalogo.getProductos()
    except gestor_catalogo.CatalogoNoDisponible:
        return render_template("admin/stock.html", productos=[], errores={}, intentos={},
                               error_general="No se ha podido cargar el catálogo. Vuelve a intentarlo."), 503
    return render_template("admin/stock.html", productos=productos, errores=errores or {},
                           intentos=intentos or {}, error_general=error_general), codigo


def _comprobar_acceso():
    """Devuelve la respuesta de acceso denegado, o None si es un administrador con sesión."""
    if not session.get("usuario_id"):
        # Visitante anónimo o sesión caducada (US-13-AC-05)
        flash("Inicia sesión como administrador para modificar el stock.", "info")
        return redirect(url_for("usuarios.login"))
    if session.get("rol") != "admin":
        return render_template("admin/acceso_denegado.html", accion=ACCION), 403
    return None


@bp.route("/admin/productos/stock")
def ver_stock():
    return _comprobar_acceso() or _tabla()


@bp.route("/admin/productos/<int:id_producto>/stock", methods=["POST"])
def cambiar_stock(id_producto):
    denegado = _comprobar_acceso()
    if denegado:
        return denegado
    valor = request.form.get("stock", "")
    try:
        producto = gestor_catalogo.cambiarStock(id_producto, valor, session["usuario_id"])
    except gestor_catalogo.PermisoDenegado:
        return render_template("admin/acceso_denegado.html", accion=ACCION), 403
    except gestor_catalogo.ProductoNoEncontrado:
        # US-13-AC-05: no se aplica ningún cambio
        return _tabla(error_general="El producto no existe o ya no está publicado. No se ha cambiado nada.",
                      codigo=404)
    except gestor_catalogo.StockInvalido as error:
        # US-13-AC-03: se explica el error y se conserva el valor anterior
        return _tabla(errores={id_producto: f"{error} Se conserva el stock anterior."},
                      intentos={id_producto: valor}, codigo=400)
    except gestor_catalogo.CatalogoNoDisponible:
        # US-13-AC-06: error y se conserva el último stock confirmado
        return _tabla(errores={id_producto: "No se ha podido guardar el stock. Se conserva el último stock guardado."},
                      intentos={id_producto: valor}, codigo=503)
    # US-13-AC-02 y AC-04: nuevo stock y disponibilidad visibles
    flash(f"Stock de «{producto['nombre']}» actualizado a {producto['stock']} unidades. "
          f"Disponibilidad: {producto['estado']}.", "exito")
    return redirect(url_for("admin_stock.ver_stock"))
