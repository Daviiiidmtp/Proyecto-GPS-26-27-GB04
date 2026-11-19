"""Gestión Foro (EP-03 Foro)."""
import sqlite3
from datetime import datetime, timedelta

from app.repositories import foro_repo, usuarios_repo

FORMATO = "%Y-%m-%d %H:%M:%S"
LONGITUD_MAXIMA_TITULO = 120
LONGITUD_MAXIMA_CUERPO = 5000
# Si el mismo autor publica el mismo tema dentro de este margen, se entiende que ha
# pulsado «Publicar» otra vez y no se guarda un duplicado (US-07-AC-06).
MARGEN_DUPLICADO = timedelta(minutes=5)


class ForoNoDisponible(Exception):
    """No se ha podido leer o guardar en el foro. La interfaz muestra un error y permite reintentar."""


class TemaInvalido(Exception):
    """Faltan datos del tema o no son válidos. `errores` indica el campo y el motivo."""

    def __init__(self, errores):
        super().__init__("; ".join(errores.values()))
        self.errores = errores


class RespuestaInvalida(Exception):
    """El texto de la respuesta no es válido. `errores` indica el campo y el motivo (US-08-AC-02)."""

    def __init__(self, errores):
        super().__init__("; ".join(errores.values()))
        self.errores = errores


class TemaNoEncontrado(Exception):
    """El tema no existe o ya no está disponible. No se guarda la respuesta (US-08-AC-04)."""


class PublicacionDenegada(Exception):
    """La cuenta no puede publicar. `motivo` es un código para la interfaz y el mensaje explica qué hacer.

    Motivos: sin_sesion, pendiente, bloqueada.
    """

    def __init__(self, motivo, mensaje):
        super().__init__(mensaje)
        self.motivo = motivo


def _a_tema(fila):
    momento = datetime.strptime(fila["fecha_hora"], FORMATO)
    return {
        "id": fila["id"],
        "titulo": fila["titulo"],
        "cuerpo": fila["cuerpo"],
        "autor": fila["autor"],
        "fecha": momento.strftime("%d/%m/%Y"),
        "hora": momento.strftime("%H:%M"),
    }


def getTemas():
    """Lista pública de temas, del más reciente al más antiguo. -> list. US-07

    No hace falta sesión para leerla (US-07-AC-01). Una lista vacía es un foro sin temas.
    Lanza ForoNoDisponible si no se puede leer la base de datos.
    """
    try:
        filas = foro_repo.listar_temas()
    except sqlite3.Error as error:
        raise ForoNoDisponible("No se han podido cargar los temas del foro") from error
    return [_a_tema(fila) for fila in filas]


def _a_respuesta(fila):
    momento = datetime.strptime(fila["fecha_hora"], FORMATO)
    return {
        "id": fila["id"],
        "cuerpo": fila["cuerpo"],
        "autor": fila["autor"],
        "fecha": momento.strftime("%d/%m/%Y"),
        "hora": momento.strftime("%H:%M"),
    }


def getTema(idTema):
    """Un tema por su id con sus respuestas, o None si no existe. -> dict. US-07 y US-08

    `respuestas` va de la más antigua a la más reciente, cada una con autor, fecha y hora.
    Se lee sin sesión: las respuestas son públicas (US-08-AC-01).
    """
    try:
        fila = foro_repo.obtener_tema(idTema)
        if fila is None:
            return None
        tema = _a_tema(fila)
        tema["respuestas"] = [_a_respuesta(r) for r in foro_repo.listar_respuestas(idTema)]
    except sqlite3.Error as error:
        raise ForoNoDisponible("No se ha podido cargar el tema") from error
    return tema


def puedePublicar(idUsuario):
    """True si la cuenta puede crear temas: sesión iniciada, verificada y no bloqueada. -> bool. US-07

    La interfaz lo usa para mostrar u ocultar el botón «Nuevo tema» (US-07-AC-01).
    """
    try:
        _comprobar_cuenta(idUsuario)
    except PublicacionDenegada:
        return False
    return True


def _comprobar_cuenta(idUsuario):
    """US-07-AC-01 y AC-05: sesión iniciada, cuenta verificada y no bloqueada."""
    try:
        usuario = usuarios_repo.obtener_por_id(idUsuario) if idUsuario is not None else None
    except sqlite3.Error as error:
        raise ForoNoDisponible("No se ha podido comprobar la cuenta") from error
    if usuario is None:
        raise PublicacionDenegada("sin_sesion", "Inicia sesión para publicar en el foro.")
    if usuario["estado"] == "pendiente":
        raise PublicacionDenegada(
            "pendiente", "Tu cuenta está pendiente de verificación. Usa el enlace del correo de confirmación.")
    if usuario["estado"] == "bloqueada":
        raise PublicacionDenegada("bloqueada", "Tu cuenta está bloqueada y no puede publicar en el foro.")


def _validar(titulo, cuerpo):
    """US-07-AC-02 y AC-04: título y cuerpo obligatorios. Devuelve (errores, título, cuerpo) sin espacios sobrantes."""
    titulo = (titulo or "").strip()
    cuerpo = (cuerpo or "").strip()
    errores = {}
    if not titulo:
        errores["titulo"] = "Escribe el título del tema."
    elif len(titulo) > LONGITUD_MAXIMA_TITULO:
        errores["titulo"] = f"El título no puede tener más de {LONGITUD_MAXIMA_TITULO} caracteres."
    if not cuerpo:
        errores["cuerpo"] = "Escribe el mensaje del tema."
    elif len(cuerpo) > LONGITUD_MAXIMA_CUERPO:
        errores["cuerpo"] = f"El mensaje no puede tener más de {LONGITUD_MAXIMA_CUERPO} caracteres."
    return errores, titulo, cuerpo


def crearTema(titulo, cuerpo, idUsuario, ahora=None):
    """Crea un tema y devuelve su id. -> int. US-07

    En el diagrama es crearTema(titulo); aquí también recibe el cuerpo del mensaje
    y el usuario de la sesión, que hacen falta para cumplir los criterios.
    `ahora` permite fijar la hora en las pruebas; por defecto, la hora local de la tienda.
    Lanza PublicacionDenegada si la cuenta no puede publicar (US-07-AC-05),
    TemaInvalido con el campo y el motivo si falta título o cuerpo (US-07-AC-04)
    y ForoNoDisponible si falla el guardado (US-07-AC-06).
    Si el mismo autor ya ha publicado el mismo tema hace un momento, devuelve ese id
    y no guarda un duplicado (US-07-AC-06).
    """
    ahora = ahora or datetime.now()
    _comprobar_cuenta(idUsuario)
    errores, titulo, cuerpo = _validar(titulo, cuerpo)
    if errores:
        raise TemaInvalido(errores)
    try:
        repetido = foro_repo.buscar_igual_reciente(
            idUsuario, titulo, cuerpo, (ahora - MARGEN_DUPLICADO).strftime(FORMATO))
        if repetido is not None:
            return repetido
        return foro_repo.crear_tema(titulo, cuerpo, idUsuario, ahora.strftime(FORMATO))
    except sqlite3.Error as error:
        raise ForoNoDisponible("No se ha podido publicar el tema") from error


def anadirComentario(idUsuario, idTema, comentario, ahora=None):
    """Publica una respuesta al final de un tema y devuelve su id. -> int. US-08

    En el diagrama devuelve bool; aquí devuelve el id para poder enlazar la respuesta.
    `ahora` permite fijar la hora en las pruebas; por defecto, la hora local de la tienda.
    Lanza PublicacionDenegada si la cuenta no puede responder: visitante, sesión caducada,
    cuenta sin verificar o bloqueada (US-08-AC-01 y AC-05),
    TemaNoEncontrado si el tema no existe (US-08-AC-04),
    RespuestaInvalida si el texto está vacío o es demasiado largo (US-08-AC-02)
    y ForoNoDisponible si falla el guardado (US-08-AC-05). En todos los casos no se guarda nada.
    Si el mismo autor ya ha publicado la misma respuesta en ese tema hace un momento,
    devuelve ese id y no guarda un duplicado (US-08-AC-05).
    """
    ahora = ahora or datetime.now()
    _comprobar_cuenta(idUsuario)
    try:
        if foro_repo.obtener_tema(idTema) is None:
            raise TemaNoEncontrado("Este tema ya no está disponible. No se ha guardado tu respuesta.")
    except sqlite3.Error as error:
        raise ForoNoDisponible("No se ha podido comprobar el tema") from error
    cuerpo = (comentario or "").strip()
    if not cuerpo:
        raise RespuestaInvalida({"cuerpo": "Escribe el texto de la respuesta."})
    if len(cuerpo) > LONGITUD_MAXIMA_CUERPO:
        raise RespuestaInvalida({"cuerpo": f"La respuesta no puede tener más de {LONGITUD_MAXIMA_CUERPO} caracteres."})
    try:
        repetida = foro_repo.buscar_respuesta_igual_reciente(
            idTema, idUsuario, cuerpo, (ahora - MARGEN_DUPLICADO).strftime(FORMATO))
        if repetida is not None:
            return repetida
        return foro_repo.crear_respuesta(idTema, cuerpo, idUsuario, ahora.strftime(FORMATO))
    except sqlite3.Error as error:
        raise ForoNoDisponible("No se ha podido publicar la respuesta") from error


def eliminarMensaje(idMensaje):
    """@Admin @Moderador. Retira un mensaje. -> bool. US-10"""
    raise NotImplementedError("Pendiente: US-10 Moderar foro y bloquear cuentas")
