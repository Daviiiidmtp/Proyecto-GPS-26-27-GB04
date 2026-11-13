"""Pruebas de la pantalla de inscripción en eventos (US-05, GB04-91)."""
from datetime import datetime

import pytest

from app.db import get_db
from app.gestores import gestor_evento

HOY = datetime(2026, 11, 11, 10, 0)
TORNEO, COMPLETO, PASADO = 1, 3, 7
ADMIN = 1


@pytest.fixture(autouse=True)
def fecha_fija(monkeypatch):
    """Fija la fecha de hoy para que las pruebas no dependan del día en que se ejecutan."""
    disponibles = gestor_evento.getEventosDisponibles
    apuntarme = gestor_evento.apuntarmeEnEvento
    monkeypatch.setattr(gestor_evento, "getEventosDisponibles",
                        lambda tipoEvento=None: disponibles(tipoEvento, ahora=HOY))
    monkeypatch.setattr(gestor_evento, "apuntarmeEnEvento",
                        lambda idEvento, idUsuario: apuntarme(idEvento, idUsuario, ahora=HOY))


def entrar(client, id_usuario=ADMIN):
    with client.session_transaction() as sesion:
        sesion["usuario_id"] = id_usuario
        sesion["nombre_usuario"] = "Prueba"
        sesion["rol"] = "cliente"


def inscribirse(client, id_evento=TORNEO):
    return client.post(f"/eventos/{id_evento}/inscribirse", follow_redirects=True)


def plazas(app, id_evento=TORNEO):
    with app.app_context():
        return get_db().execute("SELECT plazas_disponibles FROM eventos WHERE id = ?", (id_evento,)).fetchone()[0]


def test_los_eventos_con_plazas_tienen_boton_de_inscribirse(client):
    html = client.get("/eventos").get_data(as_text=True)
    assert 'aria-label="Inscribirse en Torneo de Dragones de Bruma"' in html
    assert 'action="/eventos/3/inscribirse"' not in html  # completo, sin botón


def test_sin_sesion_se_indica_que_hay_que_iniciar_sesion(app, client):
    """US-05-AC-01: no se consume plaza y se lleva al inicio de sesión."""
    assert "iniciar sesión</a> con una cuenta verificada" in client.get("/eventos").get_data(as_text=True)
    respuesta = client.post(f"/eventos/{TORNEO}/inscribirse")
    assert respuesta.status_code == 302 and respuesta.headers["Location"].endswith("/login")
    assert "Inicia sesión para inscribirte" in client.get("/login").get_data(as_text=True)
    assert plazas(app) == 12


def test_cuenta_pendiente_de_verificar(app, client):
    """US-05-AC-01."""
    with app.app_context():
        get_db().execute("INSERT INTO usuarios (id, email, nombre_usuario, hash_contrasena, rol, estado) "
                         "VALUES (50, 'sam@comarca.test', 'Sam', 'x', 'cliente', 'pendiente')")
        get_db().commit()
    entrar(client, 50)
    assert "pendiente de verificación" in inscribirse(client).get_data(as_text=True)
    assert plazas(app) == 12


def test_inscripcion_confirmada_muestra_mensaje_y_estado_inscrito(app, client):
    """US-05-AC-02 y AC-03."""
    entrar(client)
    html = inscribirse(client).get_data(as_text=True)
    assert "Inscripción confirmada" in html
    assert '<p class="evento-inscrito">Inscrito</p>' in html
    assert "11 de 32 plazas libres" in html
    assert plazas(app) == 11


def test_no_se_puede_inscribir_dos_veces(app, client):
    """US-05-AC-04."""
    entrar(client)
    inscribirse(client)
    html = inscribirse(client).get_data(as_text=True)
    assert "Ya estás inscrito en este evento" in html
    assert plazas(app) == 11


def test_evento_completo_o_pasado(client):
    """US-05-AC-06: aunque se envíe la petición a mano, se rechaza con su motivo."""
    entrar(client)
    assert "El evento está completo" in inscribirse(client, COMPLETO).get_data(as_text=True)
    assert "ya se ha celebrado" in inscribirse(client, PASADO).get_data(as_text=True)


def test_si_falla_la_inscripcion_se_avisa_y_se_puede_reintentar(app, client, monkeypatch):
    """US-05-AC-07."""
    def falla(idEvento, idUsuario):
        raise gestor_evento.EventosNoDisponibles("fallo")

    entrar(client)
    monkeypatch.setattr(gestor_evento, "apuntarmeEnEvento", falla)
    html = inscribirse(client).get_data(as_text=True)
    assert "No se ha podido completar la inscripción. Vuelve a intentarlo." in html
    assert 'aria-label="Inscribirse en Torneo de Dragones de Bruma"' in html
    assert plazas(app) == 12


def test_se_mantiene_el_filtro_al_volver(client):
    entrar(client)
    respuesta = client.post(f"/eventos/{TORNEO}/inscribirse", data={"tipo": "torneo"})
    assert respuesta.headers["Location"].endswith("/eventos?tipo=torneo")


def test_el_boton_muestra_un_mensaje_de_carga(client):
    assert "Inscribiendo…" in client.get("/eventos").get_data(as_text=True)
