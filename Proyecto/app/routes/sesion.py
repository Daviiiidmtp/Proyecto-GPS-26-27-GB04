"""Cierra la sesión de las cuentas bloqueadas (US-10-AC-03).

Se ejecuta antes de cada petición. Si un administrador bloquea una cuenta que tiene
la sesión abierta, en su siguiente petición se cierra la sesión y se le avisa.
Las operaciones protegidas, además, vuelven a comprobar la cuenta al guardar.
"""
from flask import Blueprint, flash, session

from app.gestores import gestor_usuario

bp = Blueprint("sesion", __name__)


@bp.before_app_request
def cerrar_sesion_bloqueada():
    if gestor_usuario.cuentaBloqueada(session.get("usuario_id")):
        session.clear()
        flash("Tu cuenta está bloqueada. Se ha cerrado la sesión.", "error")
