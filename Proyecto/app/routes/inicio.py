"""Rutas generales: página de inicio y comprobación de estado."""
from flask import Blueprint, jsonify, render_template

from app.db import get_db
from app.gestores import gestor_inicio

bp = Blueprint("inicio", __name__)


@bp.route("/")
def portada():
    return render_template("inicio.html", **gestor_inicio.datos_portada())


@bp.route("/salud")
def salud():
    """Comprueba que la web y la base de datos responden (útil para el CI)."""
    get_db().execute("SELECT 1")
    return jsonify(estado="ok")
