"""Pruebas de la pantalla de contacto (US-14, GB04-125)."""
from app.db import get_db
from app.gestores import gestor_soporte

CONTACTO = "/contacto"
VALIDA = {"nombre": "Sam Gamyi", "email": "sam@comarca.test", "asunto": "Duda sobre un torneo",
          "mensaje": "¿Hay que llevar mazo propio?", "codigo": "envio-sam"}


def total(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM incidencias").fetchone()[0]


def test_el_pie_de_pagina_enlaza_con_contacto(client):
    """US-14-AC-01."""
    for pagina in ("/", "/catalogo", "/faqs"):
        assert 'href="/contacto"' in client.get(pagina).get_data(as_text=True)


def test_el_formulario_pide_los_cuatro_campos_obligatorios(client):
    """US-14-AC-02 y AC-06."""
    respuesta = client.get(CONTACTO)
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 200
    for campo in ("nombre", "email", "asunto", "mensaje"):
        assert f'name="{campo}"' in html and f'for="{campo}"' in html
    assert html.count("required") >= 4
    assert 'name="codigo"' in html and "no se envía ningún correo" in html


def test_enviar_bien_muestra_la_confirmacion(app, client):
    """US-14-AC-04 y AC-06."""
    respuesta = client.post(CONTACTO, data=VALIDA, follow_redirects=True)
    html = respuesta.get_data(as_text=True)
    assert "Tu mensaje ha sido enviado correctamente" in html
    assert "registrado para que la tienda haga el seguimiento" in html and "Todavía no ha sido respondido" in html
    assert total(app) == 1
    # El formulario vuelve vacío para otro mensaje
    assert "Sam Gamyi" not in html


def test_un_campo_vacio_se_indica_y_conserva_lo_escrito(app, client):
    """US-14-AC-03."""
    respuesta = client.post(CONTACTO, data={**VALIDA, "asunto": ""})
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 400
    assert "No se ha enviado el mensaje" in html and "Escribe el asunto." in html
    assert 'value="Sam Gamyi"' in html and "¿Hay que llevar mazo propio?" in html
    assert 'aria-invalid="true"' in html and "enviado correctamente" not in html
    assert total(app) == 0


def test_un_email_no_valido_se_indica(app, client):
    """US-14-AC-03."""
    respuesta = client.post(CONTACTO, data={**VALIDA, "email": "sam@gmail.com"})
    assert respuesta.status_code == 400 and ".test" in respuesta.get_data(as_text=True)
    assert total(app) == 0


def test_si_falla_el_registro_avisa_conserva_los_datos_y_no_duplica(app, client, monkeypatch):
    """US-14-AC-05."""
    original = gestor_soporte.reportarIncidencia

    def falla(*args, **kwargs):
        raise gestor_soporte.SoporteNoDisponible("fallo")

    monkeypatch.setattr(gestor_soporte, "reportarIncidencia", falla)
    respuesta = client.post(CONTACTO, data=VALIDA)
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 503
    assert "No se ha podido enviar tu mensaje" in html and "enviado correctamente" not in html
    assert 'value="Sam Gamyi"' in html and 'value="envio-sam"' in html
    monkeypatch.setattr(gestor_soporte, "reportarIncidencia", original)
    client.post(CONTACTO, data=VALIDA)
    client.post(CONTACTO, data=VALIDA)
    assert total(app) == 1
