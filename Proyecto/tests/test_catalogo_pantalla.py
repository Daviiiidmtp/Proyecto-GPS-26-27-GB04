"""Pruebas de la pantalla del catálogo (US-01, GB04-80)."""
from app.db import get_db
from app.gestores import gestor_catalogo


def test_la_pagina_principal_muestra_primero_los_productos(client):
    """US-01-AC-01: al entrar en la página principal se ven los productos."""
    html = client.get("/").get_data(as_text=True)
    assert "Catálogo" in html
    assert "Aldeas y Caminos" in html


def test_los_productos_salen_ordenados_alfabeticamente(client):
    """US-01-AC-01."""
    html = client.get("/catalogo").get_data(as_text=True)
    assert html.index("Aldeas y Caminos") < html.index("Colonos de la Comarca") < html.index("Pantalla del Narrador")


def test_cada_ficha_muestra_foto_nombre_precio_y_estado(client):
    """US-01-AC-02, con la imagen por defecto si falta la foto."""
    html = client.get("/catalogo").get_data(as_text=True)
    assert "39,95 €" in html
    assert "producto-por-defecto.svg" in html
    assert "Disponible" in html
    assert "Agotado" in html


def test_catalogo_vacio_muestra_su_mensaje(app, client):
    """US-01-AC-03."""
    with app.app_context():
        get_db().execute("UPDATE productos SET activo = 0")
        get_db().commit()
    html = client.get("/catalogo").get_data(as_text=True)
    assert "El catálogo está vacío actualmente" in html


def test_si_falla_la_carga_muestra_error_y_reintentar(client, monkeypatch):
    """US-01-AC-04: error con reintentar, sin mostrar el catálogo vacío."""
    def falla():
        raise gestor_catalogo.CatalogoNoDisponible("fallo")

    monkeypatch.setattr(gestor_catalogo, "getProductos", falla)
    respuesta = client.get("/catalogo")
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 503
    assert "no se ha podido cargar el catálogo" in html
    assert "Volver a intentarlo" in html
    assert "El catálogo está vacío actualmente" not in html
