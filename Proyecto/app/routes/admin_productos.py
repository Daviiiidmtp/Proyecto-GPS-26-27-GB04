"""Alta de productos desde administración (US-12).

Solo pueden entrar los administradores. La lógica y las validaciones están en
gestor_catalogo.crearProducto (GB04-94); aquí se muestra el formulario y los mensajes.
"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.gestores import gestor_catalogo
from app.gestores.categorias import CATEGORIAS

bp = Blueprint("admin_productos", __name__)

CAMPOS = ["nombre", "precio", "tipo", "stock", "imagen"]


def _formulario(datos=None, errores=None, error_general=None, codigo=200):
    return render_template("admin/producto_nuevo.html", datos=datos or {}, errores=errores or {},
                           error_general=error_general, categorias=CATEGORIAS), codigo


def _denegado():
    # US-12-AC-06: se deniega sin guardar nada
    return render_template("admin/acceso_denegado.html"), 403


@bp.route("/admin/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    if not session.get("usuario_id"):
        # Visitante anónimo o sesión caducada
        flash("Inicia sesión como administrador para añadir productos.", "info")
        return redirect(url_for("usuarios.login"))
    if session.get("rol") != "admin":
        return _denegado()
    if request.method == "GET":
        return _formulario()

    datos = {campo: request.form.get(campo, "") for campo in CAMPOS}
    try:
        id_producto = gestor_catalogo.crearProducto(datos, session["usuario_id"])
    except gestor_catalogo.PermisoDenegado:
        return _denegado()
    except gestor_catalogo.ProductoInvalido as error:
        # US-12-AC-03: se señala cada campo que hay que corregir y se conservan los datos
        return _formulario(datos, error.errores, codigo=400)
    except gestor_catalogo.CatalogoNoDisponible:
        # US-12-AC-07: error, se conservan los datos y no se guarda nada a medias
        return _formulario(datos, error_general="No se ha podido guardar el producto. Vuelve a intentarlo.", codigo=503)
    # US-12-AC-04: el producto ya está activo en el catálogo
    flash(f"Producto «{datos['nombre'].strip()}» añadido al catálogo con el número {id_producto}.", "exito")
    return redirect(url_for("catalogo.ver_catalogo"))
