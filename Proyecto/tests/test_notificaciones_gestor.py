"""Pruebas de la lógica y los datos de notificación de eventos (US-11, GB04-123)."""
import sqlite3
from datetime import datetime

import pytest

from app.db import get_db
from app.gestores import gestor_evento, gestor_notificacion
from app.repositories import eventos_repo, notificaciones_repo

HOY = datetime(2026, 11, 21, 10, 0)
ADMIN, MODERADOR = 1, 2
EVENTO = {"titulo": "Torneo de Navidad", "tipo": "torneo", "fecha": "2026-12-20", "hora": "17:30", "capacidad": "24"}


def crear_cuenta(app, id_usuario, estado="activa", rol="cliente"):
    with app.app_context():
        get_db().execute(
            "INSERT INTO usuarios (id, email, nombre_usuario, hash_contrasena, rol, estado) VALUES (?, ?, ?, 'x', ?, ?)",
            (id_usuario, f"usuario{id_usuario}@comarca.test", f"Usuario {id_usuario}", rol, estado))
        get_db().commit()
    return id_usuario


def publicar(app, ahora=HOY, **cambios):
    with app.app_context():
        return gestor_evento.crearEvento({**EVENTO, **cambios}, ADMIN, ahora=ahora)


def avisos(app, id_usuario):
    with app.app_context():
        return gestor_notificacion.getNotificaciones(id_usuario)


def total_avisos(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM notificaciones").fetchone()[0]


def falla_la_base_de_datos(monkeypatch, modulo, nombre):
    def fallo(*args, **kwargs):
        raise sqlite3.OperationalError("database is locked")
    monkeypatch.setattr(modulo, nombre, fallo)


# ---------- Crear las notificaciones al publicar (AC-01) ----------

def test_al_publicar_un_evento_cada_cliente_activo_recibe_un_aviso_sin_leer(app):
    """US-11-AC-01."""
    ana, bea = crear_cuenta(app, 50), crear_cuenta(app, 51)
    id_evento = publicar(app)
    for cliente in (ana, bea):
        lista = avisos(app, cliente)
        assert len(lista) == 1
        assert lista[0]["id_evento"] == id_evento and lista[0]["leida"] is False
        assert lista[0]["titulo"] == "Torneo de Navidad"
        assert (lista[0]["fecha"], lista[0]["hora"]) == ("21/11/2026", "10:00")
        assert (lista[0]["fecha_evento"], lista[0]["hora_evento"]) == ("20/12/2026", "17:30")


@pytest.mark.parametrize("estado, rol", [("pendiente", "cliente"), ("bloqueada", "cliente")])
def test_las_cuentas_no_activas_no_reciben_aviso(app, estado, rol):
    """US-11-AC-01: solo cuentas Cliente activas."""
    otra = crear_cuenta(app, 50, estado=estado, rol=rol)
    publicar(app)
    with app.app_context():
        assert notificaciones_repo.contar_no_leidas(otra) == 0


def test_moderador_y_administrador_no_reciben_aviso(app):
    publicar(app)
    assert avisos(app, ADMIN) == [] and avisos(app, MODERADOR) == []


def test_no_se_crean_avisos_duplicados_del_mismo_evento(app):
    """US-11-AC-01."""
    cliente = crear_cuenta(app, 50)
    id_evento = publicar(app)
    with app.app_context():
        assert notificaciones_repo.avisar_evento(id_evento, "2026-11-21 10:05") == 0
        get_db().commit()
    assert len(avisos(app, cliente)) == 1 and total_avisos(app) == 1


def test_cada_evento_publicado_tiene_su_aviso(app):
    cliente = crear_cuenta(app, 50)
    primero = publicar(app, titulo="Torneo de Navidad")
    segundo = publicar(app, ahora=datetime(2026, 11, 21, 11, 0), titulo="Partida de rol")
    # De la más reciente a la más antigua
    assert [a["id_evento"] for a in avisos(app, cliente)] == [segundo, primero]


def test_un_evento_que_no_se_publica_no_genera_avisos(app):
    """Regla de US-11: solo publicaciones correctas."""
    crear_cuenta(app, 50)
    with app.app_context(), pytest.raises(gestor_evento.EventoInvalido):
        gestor_evento.crearEvento({**EVENTO, "titulo": ""}, ADMIN, ahora=HOY)
    with app.app_context(), pytest.raises(gestor_evento.PermisoDenegado):
        gestor_evento.crearEvento(EVENTO, MODERADOR, ahora=HOY)
    assert total_avisos(app) == 0


def test_si_fallan_los_avisos_no_se_guarda_el_evento(app, monkeypatch):
    """El evento y sus avisos se guardan juntos o no se guarda nada."""
    crear_cuenta(app, 50)
    with app.app_context():
        antes = get_db().execute("SELECT COUNT(*) FROM eventos").fetchone()[0]
    falla_la_base_de_datos(monkeypatch, notificaciones_repo, "avisar_evento")
    with pytest.raises(gestor_evento.EventosNoDisponibles):
        publicar(app)
    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM eventos").fetchone()[0] == antes
    assert total_avisos(app) == 0


# ---------- Campana y lista (AC-02 y AC-04) ----------

def test_la_campana_cuenta_los_avisos_sin_leer(app):
    """US-11-AC-02."""
    cliente = crear_cuenta(app, 50)
    publicar(app, titulo="Torneo de Navidad")
    publicar(app, titulo="Partida de rol")
    with app.app_context():
        assert gestor_notificacion.contarNoLeidas(cliente) == 2
        assert gestor_notificacion.contarNoLeidas(None) == 0


def test_sin_avisos_la_lista_esta_vacia(app):
    """US-11-AC-04."""
    cliente = crear_cuenta(app, 50)
    assert avisos(app, cliente) == []


# ---------- Abrir un aviso (AC-03 y AC-04) ----------

def test_abrir_un_aviso_lo_marca_como_leido_y_devuelve_su_evento(app):
    """US-11-AC-03 y AC-04."""
    cliente = crear_cuenta(app, 50)
    id_evento = publicar(app)
    id_aviso = avisos(app, cliente)[0]["id"]
    with app.app_context():
        assert gestor_notificacion.abrirNotificacion(id_aviso, cliente) == id_evento
        assert gestor_notificacion.contarNoLeidas(cliente) == 0
        # Abrirla otra vez sigue llevando al evento y no vuelve a estar sin leer
        assert gestor_notificacion.abrirNotificacion(id_aviso, cliente) == id_evento
    assert avisos(app, cliente) == []
    # Leer no borra el registro
    assert total_avisos(app) == 1


def test_no_se_puede_abrir_el_aviso_de_otra_cuenta(app):
    ana, bea = crear_cuenta(app, 50), crear_cuenta(app, 51)
    publicar(app)
    id_aviso_ana = avisos(app, ana)[0]["id"]
    with app.app_context(), pytest.raises(gestor_notificacion.NotificacionNoEncontrada):
        gestor_notificacion.abrirNotificacion(id_aviso_ana, bea)
    assert len(avisos(app, ana)) == 1


def test_un_aviso_que_no_existe_no_se_abre(app):
    cliente = crear_cuenta(app, 50)
    with app.app_context(), pytest.raises(gestor_notificacion.NotificacionNoEncontrada):
        gestor_notificacion.abrirNotificacion(999, cliente)


# ---------- Ficha del evento (AC-03 y AC-05) ----------

def test_la_ficha_de_un_evento_con_plazas_admite_inscripcion(app):
    """US-11-AC-03."""
    id_evento = publicar(app)
    with app.app_context():
        ficha = gestor_evento.getEvento(id_evento, ahora=HOY)
    assert ficha["titulo"] == "Torneo de Navidad" and ficha["fecha"] == "20/12/2026" and ficha["hora"] == "17:30"
    assert ficha["estado"] == "Con plazas" and ficha["admite_inscripcion"] is True and ficha["pasado"] is False


def test_la_ficha_de_un_evento_completo_sigue_disponible_sin_inscripcion(app):
    """US-11-AC-05."""
    id_evento = publicar(app, capacidad="1")
    cliente = crear_cuenta(app, 50)
    with app.app_context():
        gestor_evento.apuntarmeEnEvento(id_evento, cliente, ahora=HOY)
        ficha = gestor_evento.getEvento(id_evento, ahora=HOY)
    assert ficha["estado"] == "Completo" and ficha["admite_inscripcion"] is False


def test_la_ficha_de_un_evento_pasado_sigue_disponible_sin_inscripcion(app):
    """US-11-AC-05."""
    id_evento = publicar(app)
    with app.app_context():
        ficha = gestor_evento.getEvento(id_evento, ahora=datetime(2026, 12, 21, 10, 0))
    assert ficha["pasado"] is True and ficha["estado"] == "Ya celebrado" and ficha["admite_inscripcion"] is False


def test_la_ficha_de_un_evento_que_no_existe_es_none(app):
    with app.app_context():
        assert gestor_evento.getEvento(999, ahora=HOY) is None


def test_si_falla_la_ficha_se_informa(app, monkeypatch):
    falla_la_base_de_datos(monkeypatch, eventos_repo, "obtener")
    with app.app_context(), pytest.raises(gestor_evento.EventosNoDisponibles):
        gestor_evento.getEvento(1, ahora=HOY)


# ---------- Errores (AC-06) ----------

def test_si_falla_la_carga_se_informa(app, monkeypatch):
    """US-11-AC-06."""
    cliente = crear_cuenta(app, 50)
    falla_la_base_de_datos(monkeypatch, notificaciones_repo, "listar_no_leidas")
    with app.app_context(), pytest.raises(gestor_notificacion.NotificacionesNoDisponibles):
        gestor_notificacion.getNotificaciones(cliente)
    falla_la_base_de_datos(monkeypatch, notificaciones_repo, "contar_no_leidas")
    with app.app_context(), pytest.raises(gestor_notificacion.NotificacionesNoDisponibles):
        gestor_notificacion.contarNoLeidas(cliente)


def test_si_falla_el_marcado_sigue_sin_leer_y_se_puede_reintentar(app, monkeypatch):
    """US-11-AC-06."""
    cliente = crear_cuenta(app, 50)
    id_evento = publicar(app)
    id_aviso = avisos(app, cliente)[0]["id"]
    original = notificaciones_repo.marcar_leida
    falla_la_base_de_datos(monkeypatch, notificaciones_repo, "marcar_leida")
    with app.app_context(), pytest.raises(gestor_notificacion.NotificacionesNoDisponibles):
        gestor_notificacion.abrirNotificacion(id_aviso, cliente)
    assert len(avisos(app, cliente)) == 1
    monkeypatch.setattr(notificaciones_repo, "marcar_leida", original)
    with app.app_context():
        assert gestor_notificacion.abrirNotificacion(id_aviso, cliente) == id_evento
    assert avisos(app, cliente) == []


# ---------- Sin sesión (AC-07) ----------

@pytest.mark.parametrize("id_usuario", [None, 999])
def test_sin_sesion_no_se_ven_notificaciones(app, id_usuario):
    """US-11-AC-07."""
    crear_cuenta(app, 50)
    publicar(app)
    with app.app_context():
        with pytest.raises(gestor_notificacion.SinSesion) as error:
            gestor_notificacion.getNotificaciones(id_usuario)
        assert "Inicia sesión" in str(error.value)
        with pytest.raises(gestor_notificacion.SinSesion):
            gestor_notificacion.abrirNotificacion(1, id_usuario)
