"""Pruebas de la lógica y los datos del catálogo (US-01, GB04-81)."""
import sqlite3

import pytest

from app.db import get_db
from app.gestores import gestor_catalogo
from app.repositories import productos_repo


def test_los_productos_salen_ordenados_alfabeticamente(app):
    """US-01-AC-01: ordenados por nombre."""
    with app.app_context():
        nombres = [p["nombre"] for p in gestor_catalogo.getProductos()]
    assert nombres == sorted(nombres, key=str.lower)
    assert len(nombres) == 9


def test_cada_producto_tiene_los_datos_que_muestra_la_ficha(app):
    """US-01-AC-02: foto, nombre, precio y disponibilidad."""
    with app.app_context():
        producto = gestor_catalogo.getProductos()[0]
    for campo in ["id", "nombre", "precio", "imagen", "disponible", "estado"]:
        assert campo in producto


def test_los_agotados_se_muestran_como_agotado(app):
    """US-01-AC-02: los agotados conservan su ficha con «Agotado»."""
    with app.app_context():
        agotados = [p for p in gestor_catalogo.getProductos() if p["stock"] == 0]
    assert agotados
    assert all(not p["disponible"] and p["estado"] == "Agotado" for p in agotados)


def test_los_productos_no_publicados_no_aparecen(app):
    """Regla: solo se muestran productos publicados."""
    with app.app_context():
        nombres = [p["nombre"] for p in gestor_catalogo.getProductos()]
    assert "Edición coleccionista retirada" not in nombres


def test_catalogo_vacio_devuelve_lista_vacia(app):
    """US-01-AC-03: sin productos activos, la lista está vacía."""
    with app.app_context():
        get_db().execute("UPDATE productos SET activo = 0")
        assert gestor_catalogo.getProductos() == []


def test_si_falla_la_base_de_datos_se_avisa_con_un_error(app, monkeypatch):
    """US-01-AC-04: el fallo no se confunde con un catálogo vacío."""
    def falla():
        raise sqlite3.OperationalError("base de datos no disponible")

    monkeypatch.setattr(productos_repo, "listar_activos", falla)
    with app.app_context(), pytest.raises(gestor_catalogo.CatalogoNoDisponible):
        gestor_catalogo.getProductos()


def test_get_producto_devuelve_uno_o_none(app):
    with app.app_context():
        assert gestor_catalogo.getProducto(1)["nombre"] == "Colonos de la Comarca"
        assert gestor_catalogo.getProducto(999) is None
        assert gestor_catalogo.getProducto(10) is None  # no publicado


def test_disponibles_solo_incluye_productos_con_stock(app):
    with app.app_context():
        disponibles = gestor_catalogo.getProductosDisponibles()
    assert disponibles
    assert all(p["stock"] > 0 for p in disponibles)
