"""Pruebas del filtro del catálogo por categoría (US-03, GB04-98)."""
from app.db import get_db
from app.gestores import gestor_catalogo


def filtrar(app, tipo):
    with app.app_context():
        return gestor_catalogo.getProductosPorTipo(tipo)


# ---------- Lógica ----------

def test_devuelve_solo_los_productos_disponibles_de_la_categoria(app):
    """US-03-AC-02."""
    cartas = filtrar(app, "cartas")
    assert [p["nombre"] for p in cartas] == ["Sobre de cartas: Dragones de Bruma"]
    assert all(p["tipo"] == "cartas" and p["disponible"] for p in cartas)


def test_cada_categoria_sale_ordenada_por_nombre(app):
    nombres = [p["nombre"] for p in filtrar(app, "mesa")]
    assert nombres == ["Aldeas y Caminos", "Colonos de la Comarca", "El Último Puente"]


def test_categoria_sin_productos_disponibles_devuelve_lista_vacia(app):
    """US-03-AC-03."""
    with app.app_context():
        get_db().execute("UPDATE productos SET stock = 0 WHERE tipo = 'rol'")
        assert gestor_catalogo.getProductosPorTipo("rol") == []


# ---------- Pantalla ----------

def test_el_catalogo_permite_elegir_una_categoria(client):
    """US-03-AC-01."""
    html = client.get("/catalogo").get_data(as_text=True)
    assert 'aria-label="Filtrar por categoría"' in html
    for tipo in ["cartas", "mesa", "rol"]:
        assert f'href="/catalogo/categoria/{tipo}"' in html


def test_al_elegir_una_categoria_solo_salen_sus_productos(client):
    """US-03-AC-02: la categoría elegida queda marcada."""
    html = client.get("/catalogo/categoria/rol").get_data(as_text=True)
    assert "Manual del Aventurero Errante" in html and "Dados de rol de madera" in html
    assert "Pantalla del Narrador" not in html  # agotado
    assert "Colonos de la Comarca" not in html  # otra categoría
    assert 'href="/catalogo/categoria/rol" aria-current="page"' in html


def test_categoria_vacia_muestra_su_mensaje(app, client):
    """US-03-AC-03."""
    with app.app_context():
        get_db().execute("UPDATE productos SET stock = 0 WHERE tipo = 'cartas'")
        get_db().commit()
    html = client.get("/catalogo/categoria/cartas").get_data(as_text=True)
    assert "Actualmente no hay productos en esta categoría" in html


def test_se_puede_quitar_el_filtro(client):
    """US-03-AC-04."""
    html = client.get("/catalogo/categoria/mesa").get_data(as_text=True)
    assert "Quitar filtro" in html and 'href="/catalogo"' in html
    todos = client.get("/catalogo").get_data(as_text=True)
    assert "9 productos" in todos
    assert 'href="/catalogo" aria-current="page">Todas' in todos


def test_si_falla_la_carga_muestra_un_error_distinto_y_reintentar(client, monkeypatch):
    """US-03-AC-05."""
    def falla(tipo):
        raise gestor_catalogo.CatalogoNoDisponible("fallo")

    monkeypatch.setattr(gestor_catalogo, "getProductosPorTipo", falla)
    respuesta = client.get("/catalogo/categoria/mesa")
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 503
    assert "no se ha podido cargar el catálogo" in html
    assert "Volver a intentarlo" in html
    assert "Actualmente no hay productos en esta categoría" not in html


def test_una_categoria_que_no_existe_da_404(client):
    assert client.get("/catalogo/categoria/videojuegos").status_code == 404
