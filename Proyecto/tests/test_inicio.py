"""Pruebas del proyecto base (TK-001)."""
from app.repositories import ajustes_repo


def test_la_portada_carga_y_muestra_el_nombre_de_la_tienda(client):
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert "El Hogar del Hobbit" in respuesta.get_data(as_text=True)


def test_la_portada_incluye_el_menu_principal(client):
    html = client.get("/").get_data(as_text=True)
    for seccion in ["Catálogo", "Eventos", "Foro", "FAQs", "Registro"]:
        assert seccion in html


def test_salud_confirma_que_web_y_base_de_datos_responden(client):
    respuesta = client.get("/salud")
    assert respuesta.status_code == 200
    assert respuesta.get_json() == {"estado": "ok"}


def test_una_pagina_inexistente_muestra_un_mensaje_claro(client):
    respuesta = client.get("/no-existe")
    assert respuesta.status_code == 404
    assert "Página no encontrada" in respuesta.get_data(as_text=True)


def test_la_base_de_datos_se_crea_con_los_datos_de_ejemplo(app):
    with app.app_context():
        assert ajustes_repo.obtener("nombre_tienda") == "El Hogar del Hobbit"
        assert ajustes_repo.obtener("clave_inexistente") is None
