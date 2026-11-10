"""Pantalla del catálogo general (US-01).

La página principal y /catalogo muestran los productos publicados.
"""
from flask import Blueprint, render_template

from app.gestores import gestor_catalogo

bp = Blueprint("catalogo", __name__)


def pagina_catalogo(portada=False):
    """Muestra el catálogo con sus tres estados: lista, vacío o error."""
    try:
        productos = gestor_catalogo.getProductos()
    except gestor_catalogo.CatalogoNoDisponible:
        # US-01-AC-04: error distinto del catálogo vacío, con opción de reintentar
        return render_template("catalogo/lista.html", productos=[], error=True, portada=portada), 503
    return render_template("catalogo/lista.html", productos=productos, error=False, portada=portada)


@bp.route("/catalogo")
def ver_catalogo():
    return pagina_catalogo()
