"""Gestor Evento (EP-02 Eventos)."""
import sqlite3
from datetime import datetime

from app.repositories import eventos_repo, usuarios_repo

FORMATO = "%Y-%m-%d %H:%M"


class EventosNoDisponibles(Exception):
    """No se han podido leer los eventos. La interfaz muestra un error y permite reintentar."""


class InscripcionDenegada(Exception):
    """No se puede hacer la inscripción. `motivo` es un código para la interfaz y el mensaje explica qué hacer.

    Motivos: sin_sesion, pendiente, bloqueada, no_existe, pasado, completo, ya_inscrito.
    """

    def __init__(self, motivo, mensaje):
        super().__init__(mensaje)
        self.motivo = motivo


def _a_evento(fila):
    momento = datetime.strptime(fila["fecha_hora"], FORMATO)
    completo = fila["plazas_disponibles"] == 0
    return {
        "id": fila["id"],
        "titulo": fila["titulo"],
        "tipo": fila["tipo"],
        "fecha": momento.strftime("%d/%m/%Y"),
        "hora": momento.strftime("%H:%M"),
        "plazas_disponibles": fila["plazas_disponibles"],
        "plazas_totales": fila["plazas_totales"],
        "completo": completo,
        "estado": "Completo" if completo else "Con plazas",
    }


def getEventosDisponibles(tipoEvento=None, ahora=None):
    """Próximos eventos publicados, del más próximo al más lejano. -> list. US-04

    Si se indica tipoEvento ('torneo' o 'actividad'), solo los de ese tipo.
    `ahora` permite fijar la hora en las pruebas; por defecto, la hora local de la tienda.
    Los eventos completos se siguen mostrando, con estado «Completo».
    Lanza EventosNoDisponibles si no se puede leer la base de datos.
    """
    ahora = ahora or datetime.now()
    try:
        filas = eventos_repo.listar_publicados_desde(ahora.strftime(FORMATO), tipoEvento)
    except sqlite3.Error as error:
        raise EventosNoDisponibles("No se han podido cargar los eventos") from error
    return [_a_evento(fila) for fila in filas]


def _comprobar_cuenta(idUsuario):
    """US-05-AC-01: sesión iniciada, cuenta verificada y no bloqueada."""
    usuario = usuarios_repo.obtener_por_id(idUsuario) if idUsuario is not None else None
    if usuario is None:
        raise InscripcionDenegada("sin_sesion", "Inicia sesión para inscribirte en el evento.")
    if usuario["estado"] == "pendiente":
        raise InscripcionDenegada(
            "pendiente", "Tu cuenta está pendiente de verificación. Usa el enlace del correo de confirmación.")
    if usuario["estado"] == "bloqueada":
        raise InscripcionDenegada("bloqueada", "Tu cuenta está bloqueada y no puede inscribirse en eventos.")


def apuntarmeEnEvento(idEvento, idUsuario, ahora=None):
    """Inscribe a un usuario verificado en un evento y descuenta una plaza. -> bool. US-05

    `ahora` permite fijar la hora en las pruebas; por defecto, la hora local de la tienda.
    Devuelve True si la inscripción queda confirmada (US-05-AC-03).
    Lanza InscripcionDenegada con el motivo si no se puede (US-05-AC-01, 04, 05 y 06)
    y EventosNoDisponibles si falla la base de datos (US-05-AC-07).
    """
    ahora = ahora or datetime.now()
    try:
        _comprobar_cuenta(idUsuario)
        evento = eventos_repo.obtener(idEvento)
        if evento is None:
            raise InscripcionDenegada("no_existe", "El evento no existe o ya no está publicado.")
        if datetime.strptime(evento["fecha_hora"], FORMATO) < ahora:
            raise InscripcionDenegada("pasado", "El evento ya se ha celebrado y no admite inscripciones.")
        if eventos_repo.esta_inscrito(idEvento, idUsuario):
            raise InscripcionDenegada("ya_inscrito", "Ya estás inscrito en este evento.")
        if not eventos_repo.inscribir(idEvento, idUsuario, ahora.strftime(FORMATO)):
            raise InscripcionDenegada("completo", "El evento está completo. No quedan plazas.")
        return True
    except sqlite3.IntegrityError as error:
        # Dos peticiones a la vez de la misma cuenta: solo cuenta la primera
        raise InscripcionDenegada("ya_inscrito", "Ya estás inscrito en este evento.") from error
    except sqlite3.Error as error:
        raise EventosNoDisponibles("No se ha podido completar la inscripción") from error


def getEventosInscritos(idUsuario):
    """Ids de los eventos en los que está inscrito el usuario. -> set. US-05

    La interfaz lo usa para mostrar «Inscrito» en vez del botón «Inscribirse» (US-05-AC-02).
    Sin sesión devuelve un conjunto vacío.
    """
    if idUsuario is None:
        return set()
    try:
        return eventos_repo.eventos_de_usuario(idUsuario)
    except sqlite3.Error as error:
        raise EventosNoDisponibles("No se han podido cargar tus inscripciones") from error


# ---------- @Admin ----------

def crearEvento(evento):
    """@Admin. Publica un evento nuevo. -> bool. US-06"""
    raise NotImplementedError("Pendiente: US-06 Añadir evento")
