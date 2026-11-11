"""Gestor Evento (EP-02 Eventos)."""
import sqlite3
from datetime import datetime

from app.repositories import eventos_repo

FORMATO = "%Y-%m-%d %H:%M"


class EventosNoDisponibles(Exception):
    """No se han podido leer los eventos. La interfaz muestra un error y permite reintentar."""


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


def apuntarmeEnEvento(idEvento, idUsuario):
    """Inscribe a un usuario verificado en un evento. -> bool. US-05"""
    raise NotImplementedError("Pendiente: US-05 Inscribirse en evento")


# ---------- @Admin ----------

def crearEvento(evento):
    """@Admin. Publica un evento nuevo. -> bool. US-06"""
    raise NotImplementedError("Pendiente: US-06 Añadir evento")
