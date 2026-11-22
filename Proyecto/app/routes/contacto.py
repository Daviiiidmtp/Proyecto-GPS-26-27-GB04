"""Página de contacto (US-14).

La lógica y las validaciones están en gestor_soporte.reportarIncidencia;
aquí se muestra el formulario y los mensajes.
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.gestores import gestor_soporte

bp = Blueprint("contacto", __name__)

CAMPOS = ["nombre", "email", "asunto", "mensaje"]
EXITO = ("Tu mensaje ha sido enviado correctamente. Ha quedado registrado para que la tienda "
         "haga el seguimiento. Todavía no ha sido respondido.")


def _formulario(datos=None, codigo=None, errores=None, error_general=None, estado=200):
    return render_template("contacto/formulario.html", datos=datos or {}, errores=errores or {},
                           error_general=error_general,
                           codigo=codigo or gestor_soporte.nuevoCodigoIncidencia()), estado


@bp.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "GET":
        return _formulario()

    datos = {campo: request.form.get(campo, "") for campo in CAMPOS}
    codigo = request.form.get("codigo", "")
    try:
        gestor_soporte.reportarIncidencia({**datos, "codigo": codigo})
    except gestor_soporte.IncidenciaInvalida as error:
        # US-14-AC-03: se indica qué corregir y se conservan los datos
        return _formulario(datos, codigo, errores=error.errores, estado=400)
    except gestor_soporte.SoporteNoDisponible:
        # US-14-AC-05: error distinto del éxito, se conservan los datos y el mismo código para no duplicar
        return _formulario(datos, codigo, error_general="No se ha podido enviar tu mensaje. "
                           "Tus datos siguen en el formulario: vuelve a intentarlo.", estado=503)
    # US-14-AC-04 y AC-06: confirmación de que la solicitud queda registrada, no respondida
    flash(EXITO, "exito")
    return redirect(url_for("contacto.contacto"))
