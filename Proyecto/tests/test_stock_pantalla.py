"""Pruebas de la pantalla de modificar stock (US-13, GB04-103)."""
import pytest

from app.db import get_db
from app.gestores import gestor_catalogo

URL = "/admin/productos/stock"
COLONOS = 1


def entrar(client, id_usuario=1, rol="admin"):
    with client.session_transaction() as sesion:
        sesion["usuario_id"] = id_usuario
        sesion["nombre_usuario"] = "Prueba"
        sesion["rol"] = rol


def stock(app, id_producto=COLONOS):
    with app.app_context():
        return get_db().execute("SELECT stock FROM productos WHERE id = ?", (id_producto,)).fetchone()[0]


def guardar(client, valor, id_producto=COLONOS):
    return client.post(f"/admin/productos/{id_producto}/stock", data={"stock": valor})


def test_el_administrador_ve_la_tabla_y_el_enlace_del_menu(client):
    """US-13-AC-01."""
    entrar(client)
    html = client.get(URL).get_data(as_text=True)
    assert "<h1>Modificar stock</h1>" in html
    assert '<label class="solo-lectores" for="stock-1">Nuevo stock de Colonos de la Comarca</label>' in html
    assert 'href="/admin/productos/stock"' in html
    assert "Edición coleccionista retirada" not in html  # los no publicados no salen


def test_guardar_bien_muestra_el_stock_y_la_disponibilidad(app, client):
    """US-13-AC-01, AC-02 y AC-04."""
    entrar(client)
    respuesta = guardar(client, "0")
    assert respuesta.status_code == 302 and respuesta.headers["Location"].endswith(URL)
    html = client.get(URL).get_data(as_text=True)
    assert "Stock de «Colonos de la Comarca» actualizado a 0 unidades. Disponibilidad: Agotado." in html
    assert stock(app) == 0
    catalogo = client.get("/catalogo").get_data(as_text=True)
    assert "Colonos de la Comarca" in catalogo  # sigue publicado, ahora agotado


def test_un_stock_negativo_se_explica_y_se_conserva_el_anterior(app, client):
    """US-13-AC-03."""
    entrar(client)
    respuesta = guardar(client, "-4")
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 400
    assert "El stock no puede ser negativo. Se conserva el stock anterior." in html
    assert 'aria-invalid="true"' in html and 'value="-4"' in html
    assert stock(app) == 12


@pytest.mark.parametrize("rol", ["cliente", "moderador"])
def test_cliente_o_moderador_no_pueden_entrar_ni_guardar(app, client, rol):
    """US-13-AC-05."""
    entrar(client, 2, rol)
    assert client.get(URL).status_code == 403
    respuesta = guardar(client, "1")
    assert respuesta.status_code == 403
    assert "Solo un administrador de la tienda puede modificar el stock." in respuesta.get_data(as_text=True)
    assert stock(app) == 12


def test_un_visitante_va_a_iniciar_sesion(app, client):
    """US-13-AC-05: visitante o sesión caducada."""
    for respuesta in (client.get(URL), guardar(client, "1")):
        assert respuesta.status_code == 302 and "/login" in respuesta.headers["Location"]
    assert stock(app) == 12


def test_un_producto_inexistente_avisa_y_no_cambia_nada(client):
    """US-13-AC-05."""
    entrar(client)
    respuesta = guardar(client, "3", id_producto=999)
    assert respuesta.status_code == 404
    assert "El producto no existe o ya no está publicado." in respuesta.get_data(as_text=True)


def test_si_falla_el_guardado_avisa_y_se_conserva_el_stock(app, client, monkeypatch):
    """US-13-AC-06."""
    def falla(*args):
        raise gestor_catalogo.CatalogoNoDisponible("fallo")

    monkeypatch.setattr(gestor_catalogo, "cambiarStock", falla)
    entrar(client)
    respuesta = guardar(client, "5")
    assert respuesta.status_code == 503
    assert "Se conserva el último stock guardado." in respuesta.get_data(as_text=True)
    assert stock(app) == 12


def test_el_menu_no_muestra_el_enlace_a_quien_no_es_admin(client):
    entrar(client, 2, "moderador")
    assert 'href="/admin/productos/stock"' not in client.get("/catalogo").get_data(as_text=True)
