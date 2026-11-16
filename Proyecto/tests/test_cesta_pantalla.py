"""Pruebas de la pantalla de la cesta y del botón del catálogo (US-16, GB04-105)."""
import pytest

from app.db import get_db
from app.gestores import gestor_catalogo

COLONOS = 1       # 39,95 €, 12 unidades
SOBRE = 2         # 4,50 €, 80 unidades
PUENTE = 5        # 24,50 €, 3 unidades
AGOTADO = 4


def anadir(client, id_producto, cantidad="1", volver="/catalogo"):
    return client.post(f"/cesta/anadir/{id_producto}", data={"cantidad": cantidad, "volver": volver})


def cesta_de(client):
    with client.session_transaction() as sesion:
        return dict(sesion.get("cesta", {}))


def poner_stock(app, id_producto, stock):
    with app.app_context():
        get_db().execute("UPDATE productos SET stock = ? WHERE id = ?", (stock, id_producto))
        get_db().commit()


# ---------- Botón del catálogo y menú ----------

def test_el_catalogo_tiene_el_boton_solo_en_productos_disponibles(client):
    html = client.get("/catalogo").get_data(as_text=True)
    assert 'aria-label="Añadir Colonos de la Comarca a la cesta"' in html
    assert 'aria-label="Añadir Mazo inicial: Bosque Antiguo a la cesta"' not in html  # agotado


def test_el_menu_muestra_la_cesta_con_las_unidades(client):
    assert 'href="/cesta"' in client.get("/catalogo").get_data(as_text=True)
    anadir(client, SOBRE, "3")
    assert "Cesta (3)" in client.get("/catalogo").get_data(as_text=True)


# ---------- Añadir y quitar (AC-01) ----------

def test_anadir_desde_el_catalogo_vuelve_al_catalogo_con_mensaje(client):
    """US-16-AC-01."""
    respuesta = anadir(client, COLONOS)
    assert respuesta.status_code == 302 and respuesta.headers["Location"].endswith("/catalogo")
    assert "«Colonos de la Comarca» añadido a la cesta." in client.get("/catalogo").get_data(as_text=True)
    assert cesta_de(client) == {"1": 1}


def test_los_botones_mas_y_menos_cambian_la_cantidad(client):
    """US-16-AC-01."""
    anadir(client, COLONOS, "2")
    anadir(client, COLONOS, "1", volver="/cesta")
    assert cesta_de(client) == {"1": 3}
    client.post(f"/cesta/quitar/{COLONOS}", data={"cantidad": "1"})
    assert cesta_de(client) == {"1": 2}


def test_quitar_un_producto_entero(client):
    """US-16-AC-01."""
    anadir(client, COLONOS)
    anadir(client, SOBRE)
    client.post(f"/cesta/quitar/{COLONOS}")
    assert cesta_de(client) == {"2": 1}


def test_volver_solo_lleva_a_paginas_de_esta_web(client):
    respuesta = anadir(client, COLONOS, volver="https://otra-web.test")
    assert respuesta.headers["Location"].endswith("/catalogo")


# ---------- Contenido de la cesta (AC-02 y AC-03) ----------

def test_la_cesta_muestra_producto_cantidad_precio_subtotal_y_total(client):
    """US-16-AC-02."""
    anadir(client, COLONOS, "2")
    anadir(client, SOBRE, "3")
    html = client.get("/cesta").get_data(as_text=True)
    for texto in ["Colonos de la Comarca", "39,95 €", "79,90 €", "4,50 €", "13,50 €", "93,40 €", "5 unidades en la cesta"]:
        assert texto in html
    assert "Tramitar pedido" in html


def test_la_cesta_vacia_lo_dice_y_no_deja_tramitar(client):
    """US-16-AC-03."""
    html = client.get("/cesta").get_data(as_text=True)
    assert "Tu cesta está vacía." in html and "Tramitar pedido" not in html
    client.get("/cesta/checkout")
    assert "Añade algún producto antes de tramitar el pedido." in client.get("/cesta").get_data(as_text=True)


# ---------- Producto no disponible (AC-04) ----------

def test_no_se_puede_anadir_un_producto_agotado(client):
    """US-16-AC-04."""
    anadir(client, AGOTADO)
    assert "«Mazo inicial: Bosque Antiguo» está agotado." in client.get("/catalogo").get_data(as_text=True)
    assert cesta_de(client) == {}


def test_no_se_anaden_mas_unidades_de_las_que_hay(client):
    """US-16-AC-04."""
    anadir(client, PUENTE, "3")
    anadir(client, PUENTE, "1")
    assert "No hay unidades suficientes de «El Último Puente». Quedan 3." in client.get("/catalogo").get_data(as_text=True)
    assert cesta_de(client) == {"5": 3}


def test_si_se_agota_despues_la_cesta_lo_marca_y_deja_corregir(app, client):
    """US-16-AC-04."""
    anadir(client, PUENTE, "3")
    poner_stock(app, PUENTE, 1)
    html = client.get("/cesta").get_data(as_text=True)
    assert "Solo quedan 1 unidades de «El Último Puente». Reduce la cantidad." in html
    assert "Tramitar pedido" not in html
    client.get("/cesta/checkout")
    assert "Corrige la cesta antes de tramitar el pedido." in client.get("/cesta").get_data(as_text=True)
    # Corrige la cantidad y ya puede tramitar
    client.post(f"/cesta/quitar/{PUENTE}", data={"cantidad": "2"})
    assert "Tramitar pedido" in client.get("/cesta").get_data(as_text=True)


@pytest.mark.parametrize("cantidad", ["0", "-2", "abc"])
def test_una_cantidad_que_no_es_entera_positiva_avisa(client, cantidad):
    anadir(client, COLONOS, cantidad)
    assert "La cantidad debe ser un número entero mayor que 0." in client.get("/catalogo").get_data(as_text=True)
    assert cesta_de(client) == {}


def test_si_falla_la_carga_sale_un_error_con_reintentar(client, monkeypatch):
    def falla(*args):
        raise gestor_catalogo.CatalogoNoDisponible("fallo")

    monkeypatch.setattr(gestor_catalogo, "getCesta", falla)
    respuesta = client.get("/cesta")
    assert respuesta.status_code == 503
    assert "Volver a intentarlo" in respuesta.get_data(as_text=True)


def test_tramitar_con_todo_correcto_avisa_de_que_llega_con_la_compra_simulada(client):
    anadir(client, COLONOS)
    client.get("/cesta/checkout")
    assert "La compra simulada estará disponible en la próxima versión." in client.get("/cesta").get_data(as_text=True)
