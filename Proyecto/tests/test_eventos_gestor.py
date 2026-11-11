"""Pruebas de la lógica y los datos del calendario de eventos (US-04, GB04-90)."""
import sqlite3
from datetime import datetime

import pytest

from app.db import get_db
from app.gestores import gestor_evento
from app.repositories import eventos_repo

HOY = datetime(2026, 11, 11, 10, 0)


def eventos(app, **kw):
    with app.app_context():
        return gestor_evento.getEventosDisponibles(ahora=HOY, **kw)


def test_los_proximos_eventos_salen_del_mas_proximo_al_mas_lejano(app):
    """US-04-AC-01."""
    lista = eventos(app)
    assert lista[0]["titulo"] == "Torneo de Dragones de Bruma"
    assert [ (e["fecha"][6:], e["fecha"][3:5], e["fecha"][:2], e["hora"]) for e in lista ] == \
           sorted((e["fecha"][6:], e["fecha"][3:5], e["fecha"][:2], e["hora"]) for e in lista)


def test_cada_evento_tiene_titulo_fecha_hora_plazas_y_estado(app):
    """US-04-AC-02."""
    evento = eventos(app)[0]
    assert evento["fecha"] == "05/12/2026" and evento["hora"] == "17:00"
    assert evento["plazas_disponibles"] == 12 and evento["estado"] == "Con plazas"


def test_los_eventos_completos_siguen_visibles(app):
    """US-04: con cero plazas se muestra como completo."""
    completo = [e for e in eventos(app) if e["plazas_disponibles"] == 0]
    assert completo and all(e["completo"] and e["estado"] == "Completo" for e in completo)


def test_los_eventos_pasados_y_no_publicados_no_aparecen(app):
    """US-04-AC-03."""
    titulos = [e["titulo"] for e in eventos(app)]
    assert "Torneo de otoño (ya celebrado)" not in titulos
    assert "Evento en preparación" not in titulos
    assert len(titulos) == 6


def test_dos_eventos_a_la_misma_hora_aparecen_los_dos(app):
    """Caso límite: misma fecha y hora."""
    a_la_vez = [e for e in eventos(app) if e["fecha"] == "12/12/2026" and e["hora"] == "18:00"]
    assert len(a_la_vez) == 2


def test_se_puede_filtrar_por_tipo(app):
    assert all(e["tipo"] == "torneo" for e in eventos(app, tipoEvento="torneo"))
    assert len(eventos(app, tipoEvento="torneo")) == 3


def test_sin_eventos_futuros_devuelve_lista_vacia(app):
    """US-04-AC-04."""
    with app.app_context():
        get_db().execute("UPDATE eventos SET publicado = 0")
        assert gestor_evento.getEventosDisponibles(ahora=HOY) == []


def test_si_falla_la_base_de_datos_se_avisa_con_un_error(app, monkeypatch):
    """US-04-AC-05: el fallo no se confunde con la lista vacía."""
    def falla(*args):
        raise sqlite3.OperationalError("base de datos no disponible")

    monkeypatch.setattr(eventos_repo, "listar_publicados_desde", falla)
    with app.app_context(), pytest.raises(gestor_evento.EventosNoDisponibles):
        gestor_evento.getEventosDisponibles(ahora=HOY)
