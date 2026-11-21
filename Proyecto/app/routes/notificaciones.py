"""Notificaciones de eventos (US-11): campana del menú, lista y abrir una notificación.

La lógica está en gestor_notificacion; aquí se muestran las pantallas y los mensajes.
La ficha del evento a la que lleva cada notificación está en routes/eventos.py.
"""
from flask import Blueprint, abort, flash, redirect, render_template, session, url_for

from app.gestores import gestor_notificacion

bp = Blueprint("notificaciones", __name__)


@bp.app_context_processor
def campana():
    """Número de notificaciones sin leer para la campana del menú (US-11-AC-02).

    Sin sesión no hay campana (US-11-AC-07). Si falla la carga, la campana sale sin número
    y el error se ve al abrir la lista (US-11-AC-06).
    """
    id_usuario = session.get("usuario_id")
    if id_usuario is None:
        return {"notificaciones_sin_leer": None}
    try:
        return {"notificaciones_sin_leer": gestor_notificacion.contarNoLeidas(id_usuario)}
    except gestor_notificacion.NotificacionesNoDisponibles:
        return {"notificaciones_sin_leer": None}


def _iniciar_sesion(error):
    # US-11-AC-07: se le indica que inicie sesión
    flash(str(error), "error")
    return redirect(url_for("usuarios.login"))


@bp.route("/notificaciones")
def ver_notificaciones():
    try:
        avisos = gestor_notificacion.getNotificaciones(session.get("usuario_id"))
    except gestor_notificacion.SinSesion as error:
        return _iniciar_sesion(error)
    except gestor_notificacion.NotificacionesNoDisponibles:
        # US-11-AC-06: error distinto de la lista vacía, con opción de reintentar
        return render_template("notificaciones/lista.html", avisos=[], error=True), 503
    return render_template("notificaciones/lista.html", avisos=avisos, error=False)


@bp.route("/notificaciones/<int:id_notificacion>/abrir", methods=["POST"])
def abrir(id_notificacion):
    """US-11-AC-03: marca la notificación como leída y lleva a la ficha del evento."""
    try:
        id_evento = gestor_notificacion.abrirNotificacion(id_notificacion, session.get("usuario_id"))
    except gestor_notificacion.SinSesion as error:
        return _iniciar_sesion(error)
    except gestor_notificacion.NotificacionNoEncontrada:
        abort(404)
    except gestor_notificacion.NotificacionesNoDisponibles:
        # US-11-AC-06: sigue sin leer y se puede volver a intentar
        flash("No se ha podido abrir la notificación. Sigue sin leer: vuelve a intentarlo.", "error")
        return redirect(url_for("notificaciones.ver_notificaciones"))
    return redirect(url_for("eventos.ver_evento", id_evento=id_evento))
