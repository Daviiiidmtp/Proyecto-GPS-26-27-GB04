"""Pruebas de la lógica y los datos de añadir evento (US-06, GB04-115)."""
import sqlite3
from datetime import datetime

import pytest

from app.db import get_db
from app.gestores import gestor_evento
from app.repositories import eventos_repo

HOY = datetime(2026, 11, 19, 10, 0)
ADMIN, MODERADOR = 1, 2
VALIDO = {"titulo": "Torneo de Navidad", "tipo": "torneo", "fecha": "2026-12-20", "hora": "17:30", "capacidad": "24"}


def crear(app, datos=None, id_usuario=ADMIN):
    with app.app_context():
        return gestor_evento.crearEvento(VALIDO if datos is None else datos, id_usuario, ahora=HOY)


def con(**cambios):
    return {**VALIDO, **cambios}


def total_eventos(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM eventos").fetchone()[0]


def crear_cliente(app, id_usuario=50):
    with app.app_context():
        get_db().execute(
            "INSERT INTO usuarios (id, email, nombre_usuario, hash_contrasena, rol, estado) "
            "VALUES (?, 'cliente@comarca.test', 'Cliente', 'x', 'cliente', 'activa')", (id_usuario,))
        get_db().commit()
    return id_usuario


# ---------- Alta correcta (AC-01 y AC-02) ----------

def test_el_administrador_crea_un_evento_publicado_con_todas_las_plazas(app):
    """US-06-AC-01 y AC-02."""
    id_evento = crear(app)
    with app.app_context():
        fila = eventos_repo.obtener(id_evento)
    assert fila["titulo"] == "Torneo de Navidad" and fila["tipo"] == "torneo"
    assert fila["fecha_hora"] == "2026-12-20 17:30"
    assert fila["plazas_totales"] == fila["plazas_disponibles"] == 24


def test_el_evento_nuevo_aparece_en_el_calendario(app):
    """US-06-AC-02."""
    crear(app, con(tipo="actividad"))
    with app.app_context():
        calendario = gestor_evento.getEventosDisponibles(ahora=HOY)
    nuevo = [e for e in calendario if e["titulo"] == "Torneo de Navidad"]
    assert len(nuevo) == 1 and nuevo[0]["fecha"] == "20/12/2026" and nuevo[0]["hora"] == "17:30"
    assert nuevo[0]["estado"] == "Con plazas" and nuevo[0]["tipo"] == "actividad"


def test_se_quitan_los_espacios_sobrantes(app):
    id_evento = crear(app, con(titulo="  Noche de rol  ", capacidad=" 8 "))
    with app.app_context():
        fila = eventos_repo.obtener(id_evento)
    assert fila["titulo"] == "Noche de rol" and fila["plazas_totales"] == 8


def test_el_id_lo_asigna_la_base_de_datos(app):
    assert crear(app) != crear(app, con(titulo="Otro evento"))


# ---------- Datos que hay que corregir (AC-03) ----------

@pytest.mark.parametrize("campo", ["titulo", "tipo", "fecha", "hora", "capacidad"])
def test_si_falta_un_campo_no_se_publica_y_se_indica_cual(app, campo):
    """US-06-AC-03."""
    antes = total_eventos(app)
    with pytest.raises(gestor_evento.EventoInvalido) as error:
        crear(app, con(**{campo: "  "}))
    assert campo in error.value.errores
    assert total_eventos(app) == antes


@pytest.mark.parametrize("fecha, hora", [("2026-11-19", "10:00"), ("2026-11-19", "09:59"), ("2026-10-01", "18:00")])
def test_una_fecha_que_no_es_futura_no_se_publica(app, fecha, hora):
    """US-06-AC-03."""
    with pytest.raises(gestor_evento.EventoInvalido) as error:
        crear(app, con(fecha=fecha, hora=hora))
    assert error.value.errores == {"fecha": "La fecha y la hora del evento deben ser futuras."}


@pytest.mark.parametrize("fecha, hora", [("2026-02-30", "17:00"), ("20/12/2026", "17:00"), ("2026-12-20", "25:00")])
def test_una_fecha_o_una_hora_que_no_existen_se_indican(app, fecha, hora):
    with pytest.raises(gestor_evento.EventoInvalido) as error:
        crear(app, con(fecha=fecha, hora=hora))
    assert "fecha" in error.value.errores


@pytest.mark.parametrize("capacidad", ["0", "-5", "2.5", "doce", "1001"])
def test_la_capacidad_debe_ser_un_entero_positivo(app, capacidad):
    """US-06-AC-03."""
    with pytest.raises(gestor_evento.EventoInvalido) as error:
        crear(app, con(capacidad=capacidad))
    assert list(error.value.errores) == ["capacidad"]


def test_un_tipo_que_no_existe_no_se_acepta(app):
    with pytest.raises(gestor_evento.EventoInvalido) as error:
        crear(app, con(tipo="fiesta"))
    assert error.value.errores == {"tipo": "El tipo de evento no existe."}


def test_un_titulo_demasiado_largo_no_se_acepta(app):
    with pytest.raises(gestor_evento.EventoInvalido) as error:
        crear(app, con(titulo="x" * 121))
    assert "titulo" in error.value.errores


def test_se_indican_todos_los_errores_a_la_vez(app):
    with pytest.raises(gestor_evento.EventoInvalido) as error:
        crear(app, {"titulo": "", "tipo": "", "fecha": "", "hora": "", "capacidad": ""})
    assert set(error.value.errores) == {"titulo", "tipo", "fecha", "hora", "capacidad"}


# ---------- Quién no puede crear eventos (AC-04) ----------

def test_sin_sesion_o_con_la_sesion_caducada_se_deniega(app):
    """US-06-AC-04: visitante anónimo o cuenta que ya no existe."""
    antes = total_eventos(app)
    for usuario in (None, 999):
        with pytest.raises(gestor_evento.PermisoDenegado) as error:
            crear(app, id_usuario=usuario)
        assert error.value.motivo == "sin_sesion" and "sesión de administrador" in str(error.value)
    assert total_eventos(app) == antes


def test_un_cliente_o_un_moderador_no_pueden_crear_eventos(app):
    """US-06-AC-04."""
    antes = total_eventos(app)
    for usuario in (crear_cliente(app), MODERADOR):
        with pytest.raises(gestor_evento.PermisoDenegado) as error:
            crear(app, id_usuario=usuario)
        assert error.value.motivo == "no_admin"
    assert total_eventos(app) == antes


def test_el_permiso_se_comprueba_antes_que_los_datos(app):
    """Un cliente con datos incorrectos recibe el aviso de permiso, no el de los datos."""
    with pytest.raises(gestor_evento.PermisoDenegado):
        crear(app, {"titulo": ""}, id_usuario=crear_cliente(app))


# ---------- Error al guardar (AC-05) ----------

def test_si_falla_el_guardado_avisa_y_no_se_guarda_nada(app, monkeypatch):
    """US-06-AC-05."""
    def falla(*args):
        raise sqlite3.OperationalError("disco lleno")

    antes = total_eventos(app)
    monkeypatch.setattr(eventos_repo, "crear", falla)
    with pytest.raises(gestor_evento.EventosNoDisponibles):
        crear(app)
    assert total_eventos(app) == antes


def test_tras_un_fallo_se_puede_reintentar(app, monkeypatch):
    """US-06-AC-05."""
    original = eventos_repo.crear

    def falla(*args):
        raise sqlite3.OperationalError("disco lleno")

    monkeypatch.setattr(eventos_repo, "crear", falla)
    with pytest.raises(gestor_evento.EventosNoDisponibles):
        crear(app)
    monkeypatch.setattr(eventos_repo, "crear", original)
    assert crear(app) > 0
