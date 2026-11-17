"""Pruebas de la pantalla de alta de productos (US-12, GB04-93)."""
import pytest

from app.db import get_db
from app.gestores import gestor_catalogo

URL = "/admin/productos/nuevo"
VALIDO = {"nombre": "Ajedrez de la Tierra Media", "precio": "34,90", "tipo": "mesa", "stock": "6", "imagen": ""}


def entrar(client, id_usuario=1, rol="admin"):
    with client.session_transaction() as sesion:
        sesion["usuario_id"] = id_usuario
        sesion["nombre_usuario"] = "Prueba"
        sesion["rol"] = rol


def total(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM productos").fetchone()[0]


def test_el_administrador_ve_el_formulario_y_el_enlace_del_menu(client):
    """US-12-AC-01."""
    entrar(client)
    html = client.get(URL).get_data(as_text=True)
    assert "<h1>Añadir producto</h1>" in html
    for campo in ["nombre", "precio", "tipo", "stock", "imagen"]:
        assert f'<label for="{campo}">' in html
    assert "Juegos de rol" in html
    assert 'href="/admin/productos/nuevo"' in html


def test_guardar_bien_publica_el_producto_en_el_catalogo(app, client):
    """US-12-AC-02 y AC-04."""
    entrar(client)
    respuesta = client.post(URL, data=VALIDO)
    assert respuesta.status_code == 302 and respuesta.headers["Location"].endswith("/catalogo")
    html = client.get("/catalogo").get_data(as_text=True)
    assert "Producto «Ajedrez de la Tierra Media» añadido al catálogo" in html
    assert "Ajedrez de la Tierra Media" in html and "34,90 €" in html


def test_con_stock_cero_sale_agotado_y_sin_foto_usa_la_imagen_por_defecto(client):
    """US-12-AC-04 y AC-05."""
    entrar(client)
    client.post(URL, data={**VALIDO, "stock": "0"})
    html = client.get("/catalogo").get_data(as_text=True)
    posicion = html.index('alt="Ajedrez de la Tierra Media"')
    ficha = html[posicion - 200:posicion + 400]
    assert "Agotado" in ficha and "producto-por-defecto.svg" in ficha


def test_los_campos_con_error_se_senalan_y_se_conservan_los_datos(app, client):
    """US-12-AC-03."""
    entrar(client)
    antes = total(app)
    respuesta = client.post(URL, data={**VALIDO, "precio": "-5", "stock": "dos"})
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 400
    assert 'id="precio" name="precio" value="-5"' in html and 'aria-describedby="error-precio"' in html
    assert 'aria-describedby="error-stock"' in html
    assert 'aria-describedby="error-nombre"' not in html
    assert 'value="Ajedrez de la Tierra Media"' in html
    assert '<option value="mesa" selected>' in html
    assert total(app) == antes


@pytest.mark.parametrize("rol", ["cliente", "moderador"])
def test_cliente_o_moderador_no_pueden_crear_productos(app, client, rol):
    """US-12-AC-06."""
    entrar(client, 2, rol)
    antes = total(app)
    assert client.get(URL).status_code == 403
    respuesta = client.post(URL, data=VALIDO)
    assert respuesta.status_code == 403
    assert "Solo un administrador" in respuesta.get_data(as_text=True)
    assert total(app) == antes
    assert 'href="/admin/productos/nuevo"' not in client.get("/catalogo").get_data(as_text=True)


def test_visitante_o_sesion_caducada_van_a_iniciar_sesion(app, client):
    """US-12-AC-06."""
    antes = total(app)
    respuesta = client.post(URL, data=VALIDO)
    assert respuesta.status_code == 302 and respuesta.headers["Location"].endswith("/login")
    assert "Inicia sesión como administrador" in client.get("/login").get_data(as_text=True)
    assert total(app) == antes


def test_si_el_gestor_deniega_el_permiso_tampoco_se_guarda(app, client):
    """Una sesión que dice admin pero cuyo usuario ya no lo es."""
    entrar(client, 2, "admin")
    antes = total(app)
    assert client.post(URL, data=VALIDO).status_code == 403
    assert total(app) == antes


def test_si_falla_el_guardado_se_avisa_y_se_conservan_los_datos(app, client, monkeypatch):
    """US-12-AC-07."""
    def falla(producto, idUsuario):
        raise gestor_catalogo.CatalogoNoDisponible("fallo")

    entrar(client)
    monkeypatch.setattr(gestor_catalogo, "crearProducto", falla)
    respuesta = client.post(URL, data=VALIDO)
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 503
    assert "No se ha podido guardar el producto" in html
    assert 'value="Ajedrez de la Tierra Media"' in html and 'value="34,90"' in html


def test_no_se_duplica_al_guardar_dos_veces(app, client):
    """US-12-AC-07."""
    entrar(client)
    client.post(URL, data=VALIDO)
    antes = total(app)
    html = client.post(URL, data=VALIDO).get_data(as_text=True)
    assert "Ya existe un producto con ese nombre" in html
    assert total(app) == antes
