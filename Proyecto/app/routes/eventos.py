"""Pantalla del calendario de eventos (US-04) e inscripción en eventos (US-05)."""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.gestores import gestor_evento

bp = Blueprint("eventos", __name__)

TIPOS = {"torneo": "Torneos", "actividad": "Actividades"}


@bp.route("/eventos")
def ver_eventos():
    tipo = request.args.get("tipo")
    tipo = tipo if tipo in TIPOS else None
    try:
        eventos = gestor_evento.getEventosDisponibles(tipo)
        # US-05-AC-02: los eventos en los que ya está inscrito salen como «Inscrito»
        inscritos = gestor_evento.getEventosInscritos(session.get("usuario_id"))
    except gestor_evento.EventosNoDisponibles:
        # US-04-AC-05: error distinto de la lista vacía, con opción de reintentar
        return render_template("eventos/lista.html", eventos=[], inscritos=set(), error=True,
                               tipo=tipo, tipos=TIPOS), 503
    return render_template("eventos/lista.html", eventos=eventos, inscritos=inscritos, error=False,
                           tipo=tipo, tipos=TIPOS)


@bp.route("/eventos/<int:id_evento>/inscribirse", methods=["POST"])
def inscribirse(id_evento):
    """US-05: inscribe al usuario de la sesión y vuelve al calendario con un mensaje."""
    volver = redirect(url_for("eventos.ver_eventos", tipo=request.form.get("tipo") or None))
    try:
        gestor_evento.apuntarmeEnEvento(id_evento, session.get("usuario_id"))
    except gestor_evento.InscripcionDenegada as error:
        flash(str(error), "error")
        if error.motivo == "sin_sesion":
            # US-05-AC-01: se le indica cómo continuar, iniciando sesión
            return redirect(url_for("usuarios.login"))
        return volver
    except gestor_evento.EventosNoDisponibles:
        # US-05-AC-07: no se confirma la plaza y se puede volver a intentar
        flash("No se ha podido completar la inscripción. Vuelve a intentarlo.", "error")
        return volver
    # US-05-AC-03: confirmación visible
    flash("Inscripción confirmada. Tienes tu plaza reservada.", "exito")
    return volver
