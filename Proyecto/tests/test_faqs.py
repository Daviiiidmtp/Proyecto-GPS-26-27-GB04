"""Pruebas de la página de preguntas frecuentes (US-15, GB04-84)."""
from flask import render_template

from app.routes import faqs


def test_la_pagina_muestra_preguntas_y_respuestas(client):
    """US-15-AC-01."""
    respuesta = client.get("/faqs")
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 200
    assert "Preguntas frecuentes" in html
    assert html.count("<details") >= 5
    assert "¿Cómo compro un producto?" in html


def test_cada_pregunta_se_abre_y_cierra_con_teclado(client):
    """US-15-AC-02: <details>/<summary> es accesible con teclado y comunica si está abierto."""
    html = client.get("/faqs").get_data(as_text=True)
    assert html.count("<summary>") == html.count("<details")


def test_sin_preguntas_se_muestra_un_mensaje(app):
    """US-15-AC-03."""
    with app.test_request_context("/faqs"):
        html = render_template("faqs/lista.html", faqs=[])
    assert "No hay preguntas frecuentes disponibles" in html
    assert "<details" not in html


def test_si_falla_la_carga_se_muestra_un_error_con_reintentar(client, monkeypatch):
    """US-15-AC-04: el error es distinto de la lista vacía y permite reintentar."""
    def falla():
        raise RuntimeError("fallo al cargar")

    monkeypatch.setattr(faqs, "_pagina_faqs", falla)
    respuesta = client.get("/faqs")
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 500
    assert "no se han podido cargar" in html
    assert "Reintentar" in html
    assert "No hay preguntas frecuentes disponibles" not in html
