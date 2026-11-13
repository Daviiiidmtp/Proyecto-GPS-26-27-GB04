"""Búsqueda de productos por nombre (US-02).

El campo de búsqueda aparece en el catálogo y envía el texto a /catalogo/buscar.
"""
from flask import Blueprint, render_template, request

from app.gestores import gestor_catalogo

bp = Blueprint("busqueda", __name__)

SIN_RESULTADOS = "No se han encontrado productos que coincidan con tu búsqueda."


@bp.route("/catalogo/buscar")
def buscar():
    busqueda = request.args.get("q", "").strip()
    try:
        productos = gestor_catalogo.getProductosPorNombre(busqueda)
    except gestor_catalogo.CatalogoNoDisponible:
        # US-02-AC-05: error con reintentar, sin borrar el texto de la búsqueda
        return render_template("catalogo/lista.html", productos=[], error=True, busqueda=busqueda), 503
    # US-02-AC-03: si la búsqueda está vacía se ve todo el catálogo
    return render_template("catalogo/lista.html", productos=productos, error=False,
                           busqueda=busqueda, mensaje_vacio=SIN_RESULTADOS if busqueda else None)
