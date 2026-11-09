"""Rutas generales: página de inicio y comprobación de estado."""
from flask import Blueprint, jsonify

from app.db import get_db
from app.routes.catalogo import pagina_catalogo

bp = Blueprint("inicio", __name__)


@bp.route("/")
def portada():
    """US-01-AC-01: al entrar en la página principal se muestran primero los productos."""
    return pagina_catalogo(portada=True)


@bp.route("/salud")
def salud():
    """Comprueba que la web y la base de datos responden (útil para el CI)."""
    get_db().execute("SELECT 1")
    return jsonify(estado="ok")
