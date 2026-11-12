"""Gestor Usuario (EP-04 Usuarios).

US-09: alta con invitación de un solo uso, verificación simulada e inicio de sesión.
La contraseña se guarda con un hash seguro (werkzeug), nunca en texto plano.
"""
import re
import secrets
import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

from app.repositories import usuarios_repo

PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
LONGITUD_MINIMA = 8


class RegistroInvalido(Exception):
    """Los datos del alta no son válidos. `motivos` explica cada problema."""

    def __init__(self, motivos):
        super().__init__("; ".join(motivos))
        self.motivos = motivos


class VerificacionInvalida(Exception):
    """El enlace de verificación no es válido o ya se usó."""


class AccesoDenegado(Exception):
    """No se puede iniciar sesión. El mensaje explica el motivo."""


class UsuariosNoDisponibles(Exception):
    """Fallo al guardar o leer en la base de datos."""


def _validar(datos):
    motivos = []
    codigo = (datos.get("codigo_invitacion") or "").strip()
    email = (datos.get("email") or "").strip().lower()
    nombre = (datos.get("nombre_usuario") or "").strip()
    contrasena = datos.get("contrasena") or ""
    repetida = datos.get("contrasena2") or ""

    invitacion = usuarios_repo.obtener_invitacion(codigo) if codigo else None
    if not codigo:
        motivos.append("Hace falta un código de invitación.")
    elif invitacion is None:
        motivos.append("El código de invitación no existe.")
    elif invitacion["estado"] == "usada":
        motivos.append("La invitación ya se ha utilizado.")
    elif invitacion["estado"] == "revocada":
        motivos.append("La invitación ha sido revocada.")

    if not PATRON_EMAIL.match(email):
        motivos.append("El email no tiene un formato válido.")
    elif usuarios_repo.existe_email(email):
        motivos.append("Ya existe una cuenta con ese email.")

    if not nombre:
        motivos.append("El nombre de usuario es obligatorio.")

    if len(contrasena) < LONGITUD_MINIMA:
        motivos.append(f"La contraseña debe tener al menos {LONGITUD_MINIMA} caracteres.")
    elif contrasena != repetida:
        motivos.append("Las contraseñas no coinciden.")

    return motivos, invitacion, email, nombre, contrasena


def crearUsuario(usuario):
    """Crea una cuenta Cliente pendiente de verificación. US-09-AC-01 a 04

    `usuario` es un diccionario con codigo_invitacion, email, nombre_usuario,
    contrasena y contrasena2. Devuelve el token de verificación simulado
    (lo que iría en el correo). Lanza RegistroInvalido con los motivos si algo falla.
    """
    try:
        motivos, invitacion, email, nombre, contrasena = _validar(usuario)
        if motivos:
            raise RegistroInvalido(motivos)
        token = secrets.token_urlsafe(24)
        usuarios_repo.crear_pendiente(email, nombre, generate_password_hash(contrasena), invitacion["id"], token)
        return token
    except sqlite3.IntegrityError as error:
        # Dos altas a la vez con el mismo email: solo se guarda la primera
        raise RegistroInvalido(["Ya existe una cuenta con ese email."]) from error
    except sqlite3.Error as error:
        raise UsuariosNoDisponibles("No se ha podido completar el registro") from error


def verificarCuenta(token):
    """Activa la cuenta asociada al enlace de verificación simulado. US-09-AC-05 y 06"""
    try:
        fila = usuarios_repo.obtener_por_token(token) if token else None
        if fila is None or fila["estado"] != "pendiente":
            raise VerificacionInvalida("El enlace de verificación no es válido o ya se ha utilizado.")
        usuarios_repo.activar(fila["id"])
        return True
    except sqlite3.Error as error:
        raise UsuariosNoDisponibles("No se ha podido verificar la cuenta") from error


def iniciarSesion(email, contrasena):
    """Comprueba las credenciales. Solo entran las cuentas activas. US-09-AC-05

    Devuelve un diccionario con id, nombre_usuario y rol.
    """
    try:
        fila = usuarios_repo.obtener_por_email((email or "").strip().lower())
    except sqlite3.Error as error:
        raise UsuariosNoDisponibles("No se ha podido iniciar sesión") from error
    if fila is None or not check_password_hash(fila["hash_contrasena"], contrasena or ""):
        raise AccesoDenegado("El email o la contraseña no son correctos.")
    if fila["estado"] == "pendiente":
        raise AccesoDenegado("La cuenta está pendiente de verificación. Usa el enlace del correo de confirmación.")
    if fila["estado"] == "bloqueada":
        raise AccesoDenegado("La cuenta está bloqueada.")
    return {"id": fila["id"], "nombre_usuario": fila["nombre_usuario"], "rol": fila["rol"]}


def getRolUsuario(idUsuario):
    """Rol del usuario, o None si no existe. -> str. Lo usan los métodos @Admin y @Moderador. US-09"""
    fila = usuarios_repo.obtener_por_id(idUsuario)
    return fila["rol"] if fila else None


def cambiarRol(idUsuario, rol):
    """Cambia el rol de un usuario (cliente, moderador, admin). -> bool. US-10"""
    raise NotImplementedError("Pendiente: US-10 Moderar foro y bloquear cuentas")


# ---------- @Admin @Moderador ----------

def banearUsuario(idUsuario):
    """@Admin @Moderador. Bloquea una cuenta. -> bool. US-10"""
    raise NotImplementedError("Pendiente: US-10 Moderar foro y bloquear cuentas")
