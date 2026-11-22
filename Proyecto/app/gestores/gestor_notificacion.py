"""Gestor Notificación (EP-05 Notificaciones).

US-11: alertas internas de la web cuando se publica un evento. No se envían correos reales.
Las notificaciones se crean al publicar el evento (gestor_evento.crearEvento).
"""
import sqlite3
from datetime import datetime

from app.repositories import notificaciones_repo, usuarios_repo

FORMATO = "%Y-%m-%d %H:%M"


class NotificacionesNoDisponibles(Exception):
    """No se han podido leer o guardar las notificaciones. La interfaz muestra un error y permite reintentar."""


class SinSesion(Exception):
    """No hay sesión activa: las notificaciones son personales (US-11-AC-07)."""


class NotificacionNoEncontrada(Exception):
    """La notificación no existe o es de otra cuenta. No se cambia nada."""


def _comprobar_sesion(idUsuario):
    """US-11-AC-07: sin sesión, o con la sesión de una cuenta que ya no existe, no se ven notificaciones."""
    try:
        usuario = usuarios_repo.obtener_por_id(idUsuario) if idUsuario is not None else None
    except sqlite3.Error as error:
        raise NotificacionesNoDisponibles("No se ha podido comprobar la cuenta") from error
    if usuario is None:
        raise SinSesion("Inicia sesión para ver tus notificaciones.")


def _a_notificacion(fila):
    publicada = datetime.strptime(fila["fecha_hora"], FORMATO)
    evento = datetime.strptime(fila["fecha_evento"], FORMATO)
    return {
        "id": fila["id"],
        "id_evento": fila["evento_id"],
        "titulo": fila["titulo"],
        "fecha": publicada.strftime("%d/%m/%Y"),
        "hora": publicada.strftime("%H:%M"),
        "fecha_evento": evento.strftime("%d/%m/%Y"),
        "hora_evento": evento.strftime("%H:%M"),
        "leida": bool(fila["leida"]),
    }


def getNotificaciones(idUsuario):
    """Notificaciones sin leer de la cuenta, de la más reciente a la más antigua. -> list. US-11-AC-02

    Cada una trae el título del evento, la fecha de publicación y la fecha del evento.
    Una lista vacía significa que no hay alertas sin leer (US-11-AC-04).
    Lanza SinSesion sin sesión activa (US-11-AC-07)
    y NotificacionesNoDisponibles si falla la carga (US-11-AC-06).
    """
    _comprobar_sesion(idUsuario)
    try:
        return [_a_notificacion(fila) for fila in notificaciones_repo.listar_no_leidas(idUsuario)]
    except sqlite3.Error as error:
        raise NotificacionesNoDisponibles("No se han podido cargar las notificaciones") from error


def contarNoLeidas(idUsuario):
    """Número de notificaciones sin leer, para la campana. -> int. US-11-AC-02

    Sin sesión devuelve 0: la campana no se muestra a los visitantes (US-11-AC-07).
    Lanza NotificacionesNoDisponibles si falla la carga.
    """
    if idUsuario is None:
        return 0
    try:
        return notificaciones_repo.contar_no_leidas(idUsuario)
    except sqlite3.Error as error:
        raise NotificacionesNoDisponibles("No se han podido cargar las notificaciones") from error


def abrirNotificacion(idNotificacion, idUsuario):
    """Marca la notificación como leída y devuelve el id de su evento. -> int. US-11-AC-03

    La interfaz lleva después a la ficha de ese evento. Si ya estaba leída, sigue leída (US-11-AC-04).
    Lanza SinSesion sin sesión activa (US-11-AC-07), NotificacionNoEncontrada si no existe
    o es de otra cuenta, y NotificacionesNoDisponibles si falla el guardado (US-11-AC-06).
    En esos casos no se cambia nada y se puede reintentar.
    """
    _comprobar_sesion(idUsuario)
    try:
        fila = notificaciones_repo.obtener(idNotificacion, idUsuario)
        if fila is None:
            raise NotificacionNoEncontrada("La notificación no existe.")
        notificaciones_repo.marcar_leida(idNotificacion, idUsuario)
    except sqlite3.Error as error:
        raise NotificacionesNoDisponibles("No se ha podido marcar la notificación como leída") from error
    return fila["evento_id"]
