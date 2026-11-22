"""Añadir eventos desde administración (US-06).

Solo pueden entrar los administradores. La lógica y las validaciones están en
gestor_evento.crearEvento (GB04-115); aquí se muestra el formulario y los mensajes.
"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.gestores import gestor_evento

bp = Blueprint("admin_eventos", __name__)

CAMPOS = ["titulo", "tipo", "fecha", "hora", "capacidad"]
ACCION = "crear eventos"


def _formulario(datos=None, errores=None, error_general=None, codigo=200):
    return render_template("admin/evento_nuevo.html", datos=datos or {}, errores=errores or {},
                           error_general=error_general, tipos=gestor_evento.TIPOS), codigo


def _sin_sesion():
    # US-06-AC-04: visitante anónimo o sesión caducada, se indica que necesita sesión de administrador
    flash("Necesitas una sesión de administrador para crear eventos.", "info")
    return redirect(url_for("usuarios.login"))


def _denegado():
    # US-06-AC-04: cliente o moderador, se deniega sin guardar nada
    return render_template("admin/acceso_denegado.html", accion=ACCION), 403


@bp.route("/admin/eventos/nuevo", methods=["GET", "POST"])
def nuevo_evento():
    if not session.get("usuario_id"):
        return _sin_sesion()
    if session.get("rol") != "admin":
        return _denegado()
    if request.method == "GET":
        return _formulario()

    datos = {campo: request.form.get(campo, "") for campo in CAMPOS}
    try:
        # El gestor vuelve a comprobar el permiso al guardar (regla de US-06)
        gestor_evento.crearEvento(datos, session["usuario_id"])
    except gestor_evento.PermisoDenegado as error:
        return _sin_sesion() if error.motivo == "sin_sesion" else _denegado()
    except gestor_evento.EventoInvalido as error:
        # US-06-AC-03: se señala cada dato que hay que corregir y se conservan los datos
        return _formulario(datos, error.errores, codigo=400)
    except gestor_evento.EventosNoDisponibles:
        # US-06-AC-05: error, se conservan los datos y se puede reintentar
        return _formulario(datos, error_general="No se ha podido guardar el evento. Vuelve a intentarlo.", codigo=503)
    # US-06-AC-02: el evento ya está publicado en el calendario con todas las plazas libres
    flash(f"Evento «{datos['titulo'].strip()}» publicado en el calendario con {datos['capacidad'].strip()} plazas libres.",
          "exito")
    return redirect(url_for("eventos.ver_eventos"))
