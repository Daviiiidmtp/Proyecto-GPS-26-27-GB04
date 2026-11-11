"""Pantalla del calendario de eventos (US-04)."""
from flask import Blueprint, render_template, request

from app.gestores import gestor_evento

bp = Blueprint("eventos", __name__)

TIPOS = {"torneo": "Torneos", "actividad": "Actividades"}


@bp.route("/eventos")
def ver_eventos():
    tipo = request.args.get("tipo")
    tipo = tipo if tipo in TIPOS else None
    try:
        eventos = gestor_evento.getEventosDisponibles(tipo)
    except gestor_evento.EventosNoDisponibles:
        # US-04-AC-05: error distinto de la lista vacía, con opción de reintentar
        return render_template("eventos/lista.html", eventos=[], error=True, tipo=tipo, tipos=TIPOS), 503
    return render_template("eventos/lista.html", eventos=eventos, error=False, tipo=tipo, tipos=TIPOS)
