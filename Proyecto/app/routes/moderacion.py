"""Moderación del foro y bloqueo de cuentas (US-10).

- Moderador y Administrador: botón «Retirar» en temas y respuestas, con confirmación.
- Administrador: página /admin/usuarios para bloquear y desbloquear cuentas de cliente.
La lógica y los permisos están en gestor_foro y gestor_usuario (GB04-120); aquí se muestran
las pantallas y los mensajes. El cierre de sesión de las cuentas bloqueadas está en routes/sesion.py.
"""
from flask import Blueprint, abort, flash, redirect, render_template, session, url_for

from app.gestores import gestor_foro, gestor_usuario

bp = Blueprint("moderacion", __name__)

NADA_FORO = "No se ha retirado ningún mensaje."
NADA_CUENTA = "No se ha cambiado ninguna cuenta."


@bp.app_context_processor
def permiso_de_moderar():
    """Deja `puede_moderar` en las plantillas para mostrar los botones «Retirar» (US-10-AC-05)."""
    if session.get("rol") not in gestor_foro.ROLES_MODERACION:
        return {"puede_moderar": False}
    return {"puede_moderar": gestor_foro.puedeModerar(session.get("usuario_id"))}


def _iniciar_sesion(error):
    # US-10-AC-06: sesión caducada o visitante, se indica que inicie sesión
    flash(str(error), "info")
    return redirect(url_for("usuarios.login"))


# ---------- Retirar mensajes (US-10-AC-01, AC-05, AC-06 y AC-07) ----------

def _retirar(id_mensaje, tipo, despues, si_falla):
    """Retira el mensaje y vuelve a `despues`. Si falla el guardado vuelve a `si_falla`."""
    try:
        retirado = gestor_foro.eliminarMensaje(id_mensaje, session.get("usuario_id"), tipo)
    except gestor_foro.ModeracionDenegada as error:
        if error.motivo == "sin_sesion":
            return _iniciar_sesion(error)
        return render_template("foro/denegado.html", mensaje=str(error), nada=NADA_FORO), 403
    except gestor_foro.MensajeNoEncontrado:
        abort(404)
    except gestor_foro.ForoNoDisponible:
        # US-10-AC-06: el fallo se comunica y no se muestra un resultado de éxito
        flash("Error: no se ha podido retirar el mensaje. Sigue visible: vuelve a intentarlo.", "error")
        return redirect(si_falla)
    nombre, retirado_texto = ("El tema", "retirado") if tipo == "tema" else ("La respuesta", "retirada")
    if retirado:
        # US-10-AC-01: se comunica el resultado
        flash(f"{nombre} se ha retirado. Ya no se ve en el foro.", "exito")
    else:
        # US-10-AC-07: ya estaba retirado, se informa y no se cambia nada
        flash(f"{nombre} ya estaba {retirado_texto}. No se ha cambiado nada.", "info")
    return redirect(despues)


@bp.route("/foro/temas/<int:id_tema>/retirar", methods=["POST"])
def retirar_tema(id_tema):
    """Un tema retirado ya no tiene página: se vuelve a la lista del foro."""
    return _retirar(id_tema, "tema", url_for("foro.ver_foro"), url_for("foro.ver_tema", id_tema=id_tema))


@bp.route("/foro/temas/<int:id_tema>/respuestas/<int:id_respuesta>/retirar", methods=["POST"])
def retirar_respuesta(id_tema, id_respuesta):
    tema = url_for("foro.ver_tema", id_tema=id_tema)
    return _retirar(id_respuesta, "respuesta", tema, tema)


# ---------- Bloquear y desbloquear cuentas (US-10-AC-02 a AC-07) ----------

def _cuentas(cuentas, error=False, codigo=200):
    return render_template("moderacion/cuentas.html", cuentas=cuentas, error=error), codigo


def _sin_permiso_admin(error):
    if error.motivo == "sin_sesion":
        return _iniciar_sesion(error)
    # US-10-AC-05: Cliente o Moderador, se deniega sin cambiar nada
    return render_template("admin/acceso_denegado.html", accion="bloquear o desbloquear cuentas"), 403


@bp.route("/admin/usuarios")
def ver_cuentas():
    try:
        cuentas = gestor_usuario.getClientes(session.get("usuario_id"))
    except gestor_usuario.PermisoDenegado as error:
        return _sin_permiso_admin(error)
    except gestor_usuario.UsuariosNoDisponibles:
        return _cuentas([], error=True, codigo=503)
    return _cuentas(cuentas)


def _cambiar(id_usuario, accion):
    volver = redirect(url_for("moderacion.ver_cuentas"))
    funcion = gestor_usuario.banearUsuario if accion == "bloquear" else gestor_usuario.desbanearUsuario
    try:
        cambiado = funcion(id_usuario, session.get("usuario_id"))
    except gestor_usuario.PermisoDenegado as error:
        return _sin_permiso_admin(error)
    except gestor_usuario.CuentaNoValida as error:
        flash(f"{error} {NADA_CUENTA}", "error")
        return volver
    except gestor_usuario.UsuariosNoDisponibles:
        # US-10-AC-06: el fallo se comunica y no se muestra un resultado de éxito
        flash(f"Error: no se ha podido {accion} la cuenta. Vuelve a intentarlo.", "error")
        return volver
    if accion == "bloquear":
        if cambiado:
            flash("Cuenta bloqueada. No puede iniciar sesión ni participar, y su sesión abierta se ha cerrado.", "exito")
        else:
            flash("La cuenta ya estaba bloqueada. No se ha cambiado nada.", "info")
    elif cambiado:
        flash("Cuenta desbloqueada. Sus mensajes siguen igual y tendrá que volver a iniciar sesión.", "exito")
    else:
        flash("La cuenta ya estaba activa. No se ha cambiado nada.", "info")
    return volver


@bp.route("/admin/usuarios/<int:id_usuario>/bloquear", methods=["POST"])
def bloquear(id_usuario):
    return _cambiar(id_usuario, "bloquear")


@bp.route("/admin/usuarios/<int:id_usuario>/desbloquear", methods=["POST"])
def desbloquear(id_usuario):
    return _cambiar(id_usuario, "desbloquear")
