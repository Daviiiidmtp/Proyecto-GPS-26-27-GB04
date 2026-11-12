"""Pantallas de registro, verificación e inicio de sesión (US-09).

La sesión guarda el id, el nombre y el rol del usuario que ha iniciado sesión.
"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.gestores import gestor_usuario

bp = Blueprint("usuarios", __name__)

CAMPOS = ["codigo_invitacion", "email", "nombre_usuario"]


@bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "GET":
        return render_template("usuarios/registro.html", datos={}, motivos=[])

    datos = {campo: request.form.get(campo, "") for campo in CAMPOS}
    datos.update(contrasena=request.form.get("contrasena", ""), contrasena2=request.form.get("contrasena2", ""))
    try:
        token = gestor_usuario.crearUsuario(datos)
    except gestor_usuario.RegistroInvalido as error:
        # US-09-AC-03: se indica el motivo y no se crea la cuenta. Las contraseñas no se devuelven.
        visibles = {campo: datos[campo] for campo in CAMPOS}
        return render_template("usuarios/registro.html", datos=visibles, motivos=error.motivos), 400
    except gestor_usuario.UsuariosNoDisponibles:
        visibles = {campo: datos[campo] for campo in CAMPOS}
        return render_template("usuarios/registro.html", datos=visibles,
                               motivos=["No se ha podido completar el registro. Inténtalo de nuevo."]), 503
    # US-09-AC-04: correo de confirmación simulado, sin enviar ningún correo real
    return render_template("usuarios/correo_simulado.html", email=datos["email"].strip().lower(),
                           enlace=url_for("usuarios.verificar", token=token))


@bp.route("/verificar/<token>")
def verificar(token):
    """US-09-AC-05 y 06: activa la cuenta con el enlace simulado."""
    try:
        gestor_usuario.verificarCuenta(token)
    except gestor_usuario.VerificacionInvalida as error:
        return render_template("usuarios/verificacion.html", correcto=False, mensaje=str(error)), 400
    except gestor_usuario.UsuariosNoDisponibles:
        return render_template("usuarios/verificacion.html", correcto=False,
                               mensaje="No se ha podido verificar la cuenta. Inténtalo de nuevo."), 503
    return render_template("usuarios/verificacion.html", correcto=True,
                           mensaje="Tu cuenta está activa. Ya puedes iniciar sesión.")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("usuarios/login.html", email="", error=None)
    email = request.form.get("email", "")
    try:
        usuario = gestor_usuario.iniciarSesion(email, request.form.get("contrasena", ""))
    except gestor_usuario.AccesoDenegado as error:
        return render_template("usuarios/login.html", email=email, error=str(error)), 400
    except gestor_usuario.UsuariosNoDisponibles:
        return render_template("usuarios/login.html", email=email,
                               error="No se ha podido iniciar sesión. Inténtalo de nuevo."), 503
    session.clear()
    session["usuario_id"] = usuario["id"]
    session["nombre_usuario"] = usuario["nombre_usuario"]
    session["rol"] = usuario["rol"]
    flash(f"Hola, {usuario['nombre_usuario']}. Has iniciado sesión.", "exito")
    return redirect(url_for("inicio.portada"))


@bp.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado la sesión.", "info")
    return redirect(url_for("inicio.portada"))
