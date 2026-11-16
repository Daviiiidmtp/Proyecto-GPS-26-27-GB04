"""Pantallas del foro: lista pública de temas, ver un tema y crear un tema nuevo (US-07).

La lógica y las validaciones están en gestor_foro (GB04-99); aquí se muestran las páginas y los mensajes.
"""
from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from app.gestores import gestor_foro

bp = Blueprint("foro", __name__)


@bp.route("/foro")
def ver_foro():
    """US-07-AC-01: la lista es pública. «Nuevo tema» solo sale a cuentas verificadas y no bloqueadas."""
    try:
        temas = gestor_foro.getTemas()
        puede_publicar = gestor_foro.puedePublicar(session.get("usuario_id"))
    except gestor_foro.ForoNoDisponible:
        # Error distinto del foro vacío, con opción de reintentar
        return render_template("foro/lista.html", temas=[], error=True, puede_publicar=False), 503
    return render_template("foro/lista.html", temas=temas, error=False, puede_publicar=puede_publicar)


@bp.route("/foro/temas/<int:id_tema>")
def ver_tema(id_tema):
    try:
        tema = gestor_foro.getTema(id_tema)
    except gestor_foro.ForoNoDisponible:
        return render_template("foro/tema.html", tema=None, error=True), 503
    if tema is None:
        abort(404)
    return render_template("foro/tema.html", tema=tema, error=False)


def _denegado(error):
    """US-07-AC-05: se deniega la operación y no se guarda nada."""
    if error.motivo == "sin_sesion":
        # Visitante o sesión caducada: se le indica cómo continuar
        flash(str(error), "info")
        return redirect(url_for("usuarios.login"))
    return render_template("foro/denegado.html", mensaje=str(error)), 403


@bp.route("/foro/nuevo", methods=["GET", "POST"])
def nuevo_tema():
    id_usuario = session.get("usuario_id")
    if request.method == "GET":
        try:
            if not gestor_foro.puedePublicar(id_usuario):
                # puedePublicar no dice el motivo: crearTema sin datos lo averigua sin guardar nada
                gestor_foro.crearTema("", "", id_usuario)
        except gestor_foro.PublicacionDenegada as error:
            return _denegado(error)
        except (gestor_foro.TemaInvalido, gestor_foro.ForoNoDisponible):
            pass
        return render_template("foro/nuevo.html", datos={}, errores={})

    datos = {"titulo": request.form.get("titulo", ""), "cuerpo": request.form.get("cuerpo", "")}
    try:
        gestor_foro.crearTema(datos["titulo"], datos["cuerpo"], id_usuario)
    except gestor_foro.PublicacionDenegada as error:
        return _denegado(error)
    except gestor_foro.TemaInvalido as error:
        # US-07-AC-04: se indica qué campo falta y se conserva lo escrito
        return render_template("foro/nuevo.html", datos=datos, errores=error.errores), 400
    except gestor_foro.ForoNoDisponible:
        # US-07-AC-06: error, se conserva el texto para reintentar y no se guarda nada
        return render_template("foro/nuevo.html", datos=datos, errores={},
                               error_general="No se ha podido publicar el tema. Vuelve a intentarlo."), 503
    # US-07-AC-03: el tema aparece el primero de la lista
    flash(f"Tema «{datos['titulo'].strip()}» publicado.", "exito")
    return redirect(url_for("foro.ver_foro"))
