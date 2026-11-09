"""Página de preguntas frecuentes (US-15).

Las preguntas son contenido fijo escrito en la plantilla faqs/lista.html,
sin gestor ni base de datos.
"""
from flask import Blueprint, render_template

bp = Blueprint("faqs", __name__)


def _pagina_faqs():
    return render_template("faqs/lista.html")


@bp.route("/faqs")
def ver_faqs():
    try:
        return _pagina_faqs()
    except Exception:
        # US-15-AC-04: error distinto de la lista vacía, con opción de reintentar
        return render_template("faqs/error.html"), 500
