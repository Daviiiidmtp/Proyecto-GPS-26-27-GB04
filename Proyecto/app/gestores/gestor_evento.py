"""Gestor Evento (EP-02 Eventos)."""
import sqlite3
from datetime import datetime

from app.gestores import gestor_usuario
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

TIPOS = {"torneo": "Torneo", "actividad": "Actividad"}
LONGITUD_MAXIMA_TITULO = 120
CAPACIDAD_MAXIMA = 1000


class EventoInvalido(Exception):
    """Los datos del evento no son válidos. `errores` indica el campo y el motivo (US-06-AC-03)."""

    def __init__(self, errores):
        super().__init__("; ".join(errores.values()))
        self.errores = errores


class PermisoDenegado(Exception):
    """Solo un administrador puede crear eventos (US-06-AC-04). `motivo` es sin_sesion o no_admin."""

    def __init__(self, motivo, mensaje):
        super().__init__(mensaje)
        self.motivo = motivo


def _validar_evento(evento, ahora):
    """US-06-AC-01 y AC-03: comprueba cada campo y devuelve (errores, datos limpios)."""
    errores = {}
    titulo = (evento.get("titulo") or "").strip()
    tipo = (evento.get("tipo") or "").strip()
    fecha = (evento.get("fecha") or "").strip()
    hora = (evento.get("hora") or "").strip()
    capacidad = str(evento.get("capacidad") or "").strip()

    if not titulo:
        errores["titulo"] = "Escribe el título del evento."
    elif len(titulo) > LONGITUD_MAXIMA_TITULO:
        errores["titulo"] = f"El título no puede tener más de {LONGITUD_MAXIMA_TITULO} caracteres."

    if not tipo:
        errores["tipo"] = "Elige si es un torneo o una actividad."
    elif tipo not in TIPOS:
        errores["tipo"] = "El tipo de evento no existe."

    momento = None
    if not fecha:
        errores["fecha"] = "Escribe la fecha del evento."
    if not hora:
        errores["hora"] = "Escribe la hora del evento."
    if fecha and hora:
        try:
            momento = datetime.strptime(f"{fecha} {hora}", FORMATO)
        except ValueError:
            errores["fecha"] = "La fecha o la hora no son válidas. Usa el formato día/mes/año y horas:minutos."
        else:
            if momento <= ahora:
                errores["fecha"] = "La fecha y la hora del evento deben ser futuras."

    if not capacidad:
        errores["capacidad"] = "Escribe la capacidad del evento."
    elif not capacidad.isdigit() or int(capacidad) < 1:
        errores["capacidad"] = "La capacidad debe ser un número entero mayor que 0."
    elif int(capacidad) > CAPACIDAD_MAXIMA:
        errores["capacidad"] = f"La capacidad no puede ser mayor que {CAPACIDAD_MAXIMA} plazas."

    datos = {
        "titulo": titulo,
        "tipo": tipo,
        "fecha_hora": momento.strftime(FORMATO) if momento else None,
        "capacidad": int(capacidad) if "capacidad" not in errores else None,
    }
    return errores, datos


def crearEvento(evento, idUsuario, ahora=None):
    """@Admin. Publica un evento nuevo con todas sus plazas libres y devuelve su id. -> int. US-06

    En el diagrama es crearEvento(evento) y devuelve bool; aquí también recibe el usuario de
    la sesión, porque la autorización se comprueba al guardar y no solo al mostrar el formulario,
    y devuelve el id para poder enlazar el evento.
    `evento` es un diccionario con titulo, tipo (torneo o actividad), fecha (AAAA-MM-DD),
    hora (HH:MM) y capacidad, tal y como llegan del formulario.
    `ahora` permite fijar la hora en las pruebas; por defecto, la hora local de la tienda.
    Lanza PermisoDenegado si no hay sesión o la cuenta no es de administrador (US-06-AC-04),
    EventoInvalido con el campo y el motivo de cada error (US-06-AC-03)
    y EventosNoDisponibles si falla el guardado (US-06-AC-05). En los tres casos no se guarda nada.
    """
    ahora = ahora or datetime.now()
    try:
        rol = gestor_usuario.getRolUsuario(idUsuario) if idUsuario is not None else None
        if rol is None:
            raise PermisoDenegado("sin_sesion", "Necesitas una sesión de administrador para crear eventos.")
        if rol != "admin":
            raise PermisoDenegado("no_admin", "Solo un administrador puede crear eventos.")
        errores, datos = _validar_evento(evento, ahora)
        if errores:
            raise EventoInvalido(errores)
        return eventos_repo.crear(datos["titulo"], datos["tipo"], datos["fecha_hora"], datos["capacidad"])
    except sqlite3.Error as error:
        raise EventosNoDisponibles("No se ha podido guardar el evento") from error
