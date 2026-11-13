"""Filtro del catálogo por categoría (US-03).

El selector aparece en el catálogo y cada categoría tiene su dirección:
/catalogo/categoria/cartas, /catalogo/categoria/mesa y /catalogo/categoria/rol.
"""
from flask import Blueprint, abort, render_template

from app.gestores import gestor_catalogo
from app.gestores.categorias import CATEGORIAS

bp = Blueprint("categorias", __name__)

SIN_PRODUCTOS = "Actualmente no hay productos en esta categoría."


@bp.app_context_processor
def categorias_del_catalogo():
    """Deja la lista de categorías disponible para el selector del catálogo."""
    return {"categorias": CATEGORIAS}


@bp.route("/catalogo/categoria/<tipo>")
def filtrar(tipo):
    if tipo not in CATEGORIAS:
        abort(404)
    try:
        productos = gestor_catalogo.getProductosPorTipo(tipo)
    except gestor_catalogo.CatalogoNoDisponible:
        # US-03-AC-05: error distinto de la categoría vacía, con opción de reintentar
        return render_template("catalogo/lista.html", productos=[], error=True, categoria=tipo), 503
    # US-03-AC-03: mensaje propio si la categoría no tiene productos disponibles
    return render_template("catalogo/lista.html", productos=productos, error=False,
                           categoria=tipo, mensaje_vacio=SIN_PRODUCTOS)
