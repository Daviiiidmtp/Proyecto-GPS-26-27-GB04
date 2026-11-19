"""Pruebas de confirmar la compra simulada y ver el resultado del pedido (US-17, GB04-110)."""
from app.db import get_db
from app.gestores import gestor_catalogo

COLONOS = 1      # 39,95 €, 12 unidades
PUENTE = 5       # 24,50 €, 3 unidades
CONFIRMAR = "/cesta/confirmar"
VALIDO = {"metodo_pago": "tarjeta_demo", "codigo": "checkout-prueba-1"}


def poner_cesta(client, cesta):
    with client.session_transaction() as sesion:
        sesion["cesta"] = cesta


def cesta_de(client):
    with client.session_transaction() as sesion:
        return dict(sesion.get("cesta", {}))


def stock(app, id_producto):
    with app.app_context():
        return get_db().execute("SELECT stock FROM productos WHERE id = ?", (id_producto,)).fetchone()[0]


def total_pedidos(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]


# ---------- Confirmar bien (AC-03 y AC-05) ----------

def test_confirmar_lleva_al_resultado_con_mensaje_de_exito(client):
    """US-17-AC-03."""
    poner_cesta(client, {"1": 2, "2": 3})
    respuesta = client.post(CONFIRMAR, data=VALIDO)
    assert respuesta.status_code == 302 and respuesta.headers["Location"].endswith("/pedidos/checkout-prueba-1")
    html = client.get("/pedidos/checkout-prueba-1").get_data(as_text=True)
    assert "Compra simulada completada" in html and "se ha completado con éxito" in html
    assert "no se ha cobrado nada" in html


def test_el_resultado_muestra_numero_fecha_metodo_articulos_y_total(client):
    """US-17-AC-03."""
    poner_cesta(client, {"1": 2, "2": 3})
    client.post(CONFIRMAR, data=VALIDO)
    html = client.get("/pedidos/checkout-prueba-1").get_data(as_text=True)
    for texto in ["PED-00001", "Tarjeta de demostración", "Colonos de la Comarca", "79,90 €",
                  "Sobre de cartas: Dragones de Bruma", "13,50 €", "93,40 €", "5 unidades compradas"]:
        assert texto in html


def test_confirmar_vacia_la_cesta_y_descuenta_el_stock(app, client):
    """US-17-AC-05."""
    poner_cesta(client, {"1": 2})
    client.post(CONFIRMAR, data=VALIDO)
    assert cesta_de(client) == {} and stock(app, COLONOS) == 10


def test_con_sesion_el_pedido_queda_a_nombre_del_usuario(app, client):
    with client.session_transaction() as sesion:
        sesion["usuario_id"] = 1
        sesion["cesta"] = {"1": 1}
    client.post(CONFIRMAR, data=VALIDO)
    with app.app_context():
        assert get_db().execute("SELECT usuario_id FROM pedidos").fetchone()[0] == 1


# ---------- Confirmar dos veces (AC-07) ----------

def test_confirmar_dos_veces_da_el_mismo_pedido_sin_descontar_mas(app, client):
    """US-17-AC-07: por ejemplo, pulsar dos veces o volver atrás y reenviar."""
    poner_cesta(client, {"1": 2})
    primera = client.post(CONFIRMAR, data=VALIDO)
    segunda = client.post(CONFIRMAR, data=VALIDO)
    assert primera.headers["Location"] == segunda.headers["Location"]
    assert total_pedidos(app) == 1 and stock(app, COLONOS) == 10


# ---------- No se puede comprar (AC-04) ----------

def test_sin_stock_suficiente_vuelve_a_la_cesta_sin_pedido_ni_cambios(app, client):
    """US-17-AC-04."""
    poner_cesta(client, {"1": 1, "5": 4})
    respuesta = client.post(CONFIRMAR, data=VALIDO)
    assert respuesta.status_code == 302 and respuesta.headers["Location"].endswith("/cesta")
    assert "Hay artículos que no se pueden comprar." in client.get("/cesta").get_data(as_text=True)
    assert total_pedidos(app) == 0 and stock(app, COLONOS) == 12 and stock(app, PUENTE) == 3
    assert cesta_de(client) == {"1": 1, "5": 4}


def test_con_la_cesta_vacia_vuelve_a_la_cesta(app, client):
    respuesta = client.post(CONFIRMAR, data=VALIDO)
    assert respuesta.headers["Location"].endswith("/cesta") and total_pedidos(app) == 0


def test_sin_metodo_de_pago_vuelve_al_resumen_con_el_aviso(app, client):
    """US-17-AC-01."""
    poner_cesta(client, {"1": 1})
    respuesta = client.post(CONFIRMAR, data={"codigo": "checkout-prueba-1"})
    assert respuesta.status_code == 302 and respuesta.headers["Location"].endswith("/cesta/checkout")
    with client.session_transaction() as sesion:
        mensajes = [m for _, m in sesion.get("_flashes", [])]
    assert "Elige un método de pago de demostración." in mensajes
    assert total_pedidos(app) == 0 and cesta_de(client) == {"1": 1}


# ---------- Error al guardar (AC-06) ----------

def test_si_falla_la_compra_avisa_conserva_la_cesta_y_deja_reintentar(app, client, monkeypatch):
    """US-17-AC-06."""
    poner_cesta(client, {"1": 2})
    original = gestor_catalogo.realizarCompra

    def falla(*args, **kwargs):
        raise gestor_catalogo.CatalogoNoDisponible("fallo")

    monkeypatch.setattr(gestor_catalogo, "realizarCompra", falla)
    respuesta = client.post(CONFIRMAR, data=VALIDO)
    assert respuesta.headers["Location"].endswith("/cesta/checkout")
    with client.session_transaction() as sesion:
        mensajes = [m for _, m in sesion.get("_flashes", [])]
    assert any("No se ha podido completar la compra." in m for m in mensajes)
    assert cesta_de(client) == {"1": 2} and stock(app, COLONOS) == 12
    # Reintenta y ya funciona
    monkeypatch.setattr(gestor_catalogo, "realizarCompra", original)
    assert client.post(CONFIRMAR, data=VALIDO).headers["Location"].endswith("/pedidos/checkout-prueba-1")


# ---------- Ver un pedido ----------

def test_un_pedido_que_no_existe_da_404(client):
    respuesta = client.get("/pedidos/no-existe")
    assert respuesta.status_code == 404 and "No existe ningún pedido con ese código." in respuesta.get_data(as_text=True)


def test_si_falla_la_carga_del_pedido_sale_un_error_con_reintentar(client, monkeypatch):
    def falla(*args):
        raise gestor_catalogo.CatalogoNoDisponible("fallo")

    monkeypatch.setattr(gestor_catalogo, "getPedido", falla)
    respuesta = client.get("/pedidos/checkout-prueba-1")
    assert respuesta.status_code == 503 and "Volver a intentarlo" in respuesta.get_data(as_text=True)
