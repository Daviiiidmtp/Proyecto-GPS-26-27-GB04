"""Pruebas de la pantalla del calendario de eventos (US-04, GB04-88)."""
from datetime import datetime

import pytest

from app.db import get_db
from app.gestores import gestor_evento

HOY = datetime(2026, 11, 11, 10, 0)


@pytest.fixture(autouse=True)
def fecha_fija(monkeypatch):
    """Fija la fecha de hoy para que las pruebas no dependan del día en que se ejecutan."""
    original = gestor_evento.getEventosDisponibles
    monkeypatch.setattr(gestor_evento, "getEventosDisponibles",
                        lambda tipoEvento=None: original(tipoEvento, ahora=HOY))


def test_muestra_los_proximos_eventos_en_orden(client):
    """US-04-AC-01."""
    html = client.get("/eventos").get_data(as_text=True)
    assert html.index("Torneo de Dragones de Bruma") < html.index("Noche de juegos de mesa") < html.index("Gran torneo de invierno")


def test_cada_evento_muestra_fecha_hora_plazas_y_estado(client):
    """US-04-AC-02."""
    html = client.get("/eventos").get_data(as_text=True)
    assert "05/12/2026" in html and "17:00" in html
    assert "12 de 32 plazas libres" in html
    assert "Con plazas" in html and "Completo" in html


def test_no_muestra_eventos_pasados(client):
    """US-04-AC-03."""
    html = client.get("/eventos").get_data(as_text=True)
    assert "ya celebrado" not in html


def test_sin_eventos_muestra_su_mensaje(app, client):
    """US-04-AC-04."""
    with app.app_context():
        get_db().execute("UPDATE eventos SET publicado = 0")
        get_db().commit()
    assert "No hay eventos próximos" in client.get("/eventos").get_data(as_text=True)


def test_si_falla_la_carga_muestra_error_y_reintentar(client, monkeypatch):
    """US-04-AC-05: error con reintentar, sin mostrar la lista vacía."""
    def falla(tipoEvento=None):
        raise gestor_evento.EventosNoDisponibles("fallo")

    monkeypatch.setattr(gestor_evento, "getEventosDisponibles", falla)
    respuesta = client.get("/eventos")
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 503
    assert "no se han podido cargar los eventos" in html
    assert "Volver a intentarlo" in html
    assert "No hay eventos próximos" not in html


def test_filtrar_por_torneos(client):
    html = client.get("/eventos?tipo=torneo").get_data(as_text=True)
    assert "Torneo relámpago de Colonos" in html
    assert "Noche de juegos de mesa" not in html
