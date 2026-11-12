"""Pruebas de la búsqueda de productos por nombre (US-02, GB04-95)."""
from app.db import get_db
from app.gestores import gestor_catalogo


def buscar(app, texto):
    with app.app_context():
        return [p["nombre"] for p in gestor_catalogo.getProductosPorNombre(texto)]


# ---------- Lógica ----------

def test_devuelve_los_nombres_que_contienen_el_texto(app):
    """US-02-AC-02."""
    assert buscar(app, "dragones") == ["Sobre de cartas: Dragones de Bruma"]
    assert buscar(app, "de") == buscar(app, "DE")


def test_no_distingue_mayusculas_ni_espacios_de_los_extremos(app):
    """US-02-AC-02."""
    assert buscar(app, "  COLONOS ") == ["Colonos de la Comarca"]


def test_busqueda_vacia_o_con_espacios_devuelve_todo_el_catalogo(app):
    """US-02-AC-03."""
    with app.app_context():
        todos = [p["nombre"] for p in gestor_catalogo.getProductos()]
    assert buscar(app, "") == todos
    assert buscar(app, "   ") == todos
    assert len(todos) == 9


def test_no_busca_en_productos_no_publicados(app):
    """Solo se busca en el catálogo publicado."""
    assert buscar(app, "retirada") == []


def test_los_agotados_tambien_aparecen_con_su_estado(app):
    with app.app_context():
        resultado = gestor_catalogo.getProductosPorNombre("mazo")
    assert resultado[0]["estado"] == "Agotado"


# ---------- Pantalla ----------

def test_el_catalogo_tiene_un_campo_de_busqueda(client):
    """US-02-AC-01."""
    html = client.get("/catalogo").get_data(as_text=True)
    assert 'role="search"' in html
    assert '<label for="q">Buscar por nombre</label>' in html
    assert 'name="q"' in html


def test_la_pantalla_muestra_solo_las_coincidencias(client):
    """US-02-AC-02."""
    html = client.get("/catalogo/buscar?q=  caminos ").get_data(as_text=True)
    assert "Aldeas y Caminos" in html
    assert "Colonos de la Comarca" not in html
    assert "Resultados para «caminos»" in html


def test_busqueda_vacia_muestra_todos_los_productos(client):
    """US-02-AC-03."""
    html = client.get("/catalogo/buscar?q=%20%20").get_data(as_text=True)
    assert "9 productos" in html
    assert "No se han encontrado" not in html


def test_sin_coincidencias_muestra_su_mensaje(client):
    """US-02-AC-04."""
    html = client.get("/catalogo/buscar?q=xyz").get_data(as_text=True)
    assert "No se han encontrado productos que coincidan con tu búsqueda" in html


def test_si_falla_la_busqueda_muestra_error_y_conserva_el_texto(client, monkeypatch):
    """US-02-AC-05: error con reintentar y sin borrar el texto."""
    def falla(nombre):
        raise gestor_catalogo.CatalogoNoDisponible("fallo")

    monkeypatch.setattr(gestor_catalogo, "getProductosPorNombre", falla)
    respuesta = client.get("/catalogo/buscar?q=dragones")
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 503
    assert "no se ha podido cargar el catálogo" in html
    assert 'value="dragones"' in html
    assert "Volver a intentarlo" in html and "q=dragones" in html
    assert "No se han encontrado" not in html


def test_el_texto_se_muestra_escapado(client):
    """Un texto con etiquetas HTML no se interpreta como código."""
    html = client.get("/catalogo/buscar?q=<b>hola</b>").get_data(as_text=True)
    assert "<b>hola</b>" not in html
    assert "&lt;b&gt;hola&lt;/b&gt;" in html
