"""Pruebas de la pantalla de resumen y método de pago de la compra simulada (US-17, GB04-109)."""
import re

from app.db import get_db
from app.gestores import gestor_catalogo

COLONOS = 1      # 39,95 €, 12 unidades
SOBRE = 2        # 4,50 €, 80 unidades
PUENTE = 5       # 24,50 €, 3 unidades
CHECKOUT = "/cesta/checkout"


def poner_cesta(client, cesta):
    with client.session_transaction() as sesion:
        sesion["cesta"] = cesta


def total_pedidos(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]


# ---------- Resumen (AC-02) ----------

def test_el_resumen_muestra_articulos_cantidades_precios_y_total(client):
    """US-17-AC-02."""
    poner_cesta(client, {"1": 2, "2": 3})
    html = client.get(CHECKOUT).get_data(as_text=True)
    for texto in ["Colonos de la Comarca", "Sobre de cartas: Dragones de Bruma", "39,95 €", "79,90 €",
                  "13,50 €", "Total ficticio", "93,40 €", "5 unidades"]:
        assert texto in html


def test_abrir_el_resumen_no_crea_pedidos_ni_cambia_el_stock(app, client):
    poner_cesta(client, {"1": 2})
    client.get(CHECKOUT)
    with app.app_context():
        assert get_db().execute("SELECT stock FROM productos WHERE id = 1").fetchone()[0] == 12
    assert total_pedidos(app) == 0


# ---------- Método de pago de demostración (AC-01) ----------

def test_solo_se_ofrecen_metodos_de_demostracion_sin_datos_financieros(client):
    """US-17-AC-01."""
    poner_cesta(client, {"1": 1})
    html = client.get(CHECKOUT).get_data(as_text=True)
    for clave, texto in gestor_catalogo.METODOS_PAGO.items():
        assert f'value="{clave}"' in html and texto in html
    assert "<legend>Método de pago de demostración</legend>" in html
    for campo in ["tarjeta_numero", "cvv", "iban", 'type="password"']:
        assert campo not in html
    assert "no se cobra nada" in html


def test_el_formulario_envia_a_confirmar_con_un_codigo_de_checkout(client):
    poner_cesta(client, {"1": 1})
    html = client.get(CHECKOUT).get_data(as_text=True)
    assert 'action="/cesta/confirmar"' in html and 'method="post"' in html
    assert re.search(r'name="codigo" value="[0-9a-f]{32}"', html)


def test_cada_vez_que_se_abre_el_resumen_hay_un_codigo_nuevo(client):
    poner_cesta(client, {"1": 1})
    codigos = [re.search(r'name="codigo" value="(\w+)"', client.get(CHECKOUT).get_data(as_text=True)).group(1)
               for _ in range(2)]
    assert codigos[0] != codigos[1]


def test_hay_mensaje_de_carga_y_enlace_para_volver_a_la_cesta(client):
    poner_cesta(client, {"1": 1})
    html = client.get(CHECKOUT).get_data(as_text=True)
    assert "Procesando la compra simulada" in html and 'href="/cesta"' in html


# ---------- No se puede empezar el checkout (US-16-AC-03 y AC-04, US-17-AC-04) ----------

def test_con_la_cesta_vacia_vuelve_a_la_cesta(client):
    respuesta = client.get(CHECKOUT)
    assert respuesta.status_code == 302 and respuesta.headers["Location"].endswith("/cesta")


def test_con_un_articulo_sin_stock_suficiente_vuelve_a_la_cesta_para_corregir(client):
    """US-17-AC-04."""
    poner_cesta(client, {"5": 4})
    respuesta = client.get(CHECKOUT)
    assert respuesta.status_code == 302 and respuesta.headers["Location"].endswith("/cesta")
    assert "Corrige la cesta antes de tramitar el pedido." in client.get("/cesta").get_data(as_text=True)


def test_si_falla_la_base_de_datos_avisa_y_vuelve_a_la_cesta(client, monkeypatch):
    poner_cesta(client, {"1": 1})

    def falla(*args):
        raise gestor_catalogo.CatalogoNoDisponible("fallo")

    monkeypatch.setattr(gestor_catalogo, "getCesta", falla)
    respuesta = client.get(CHECKOUT)
    assert respuesta.status_code == 302 and respuesta.headers["Location"].endswith("/cesta")
