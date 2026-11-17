"""Pruebas de la lógica y los datos del alta de productos (US-12, GB04-94)."""
import sqlite3

import pytest

from app.db import get_db
from app.gestores import gestor_catalogo
from app.repositories import productos_repo

ADMIN, MODERADOR = 1, 2
VALIDO = {"nombre": "Ajedrez de la Tierra Media", "precio": "34,90", "tipo": "mesa", "stock": "6", "imagen": ""}


def crear(app, id_usuario=ADMIN, **cambios):
    with app.app_context():
        return gestor_catalogo.crearProducto({**VALIDO, **cambios}, id_usuario)


def errores(app, **cambios):
    with pytest.raises(gestor_catalogo.ProductoInvalido) as error:
        crear(app, **cambios)
    return error.value.errores


def total_productos(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM productos").fetchone()[0]


def test_el_administrador_crea_un_producto_y_el_sistema_asigna_el_id(app):
    """US-12-AC-02: id único asignado por el sistema."""
    id_nuevo = crear(app)
    otro = crear(app, nombre="Otro juego")
    assert id_nuevo == 11 and otro == 12
    with app.app_context():
        producto = gestor_catalogo.getProducto(id_nuevo)
    assert producto["precio"] == 34.90 and producto["stock"] == 6 and producto["tipo"] == "mesa"


def test_el_producto_queda_activo_en_el_catalogo(app):
    """US-12-AC-04."""
    crear(app)
    with app.app_context():
        nombres = [p["nombre"] for p in gestor_catalogo.getProductos()]
    assert "Ajedrez de la Tierra Media" in nombres


def test_con_stock_cero_sale_como_agotado(app):
    """US-12-AC-04."""
    id_nuevo = crear(app, stock="0")
    with app.app_context():
        assert gestor_catalogo.getProducto(id_nuevo)["estado"] == "Agotado"


def test_la_foto_es_opcional(app):
    """US-12-AC-05: sin foto se guarda vacía y la interfaz usa la imagen por defecto."""
    id_nuevo = crear(app, imagen="")
    with app.app_context():
        assert gestor_catalogo.getProducto(id_nuevo)["imagen"] is None


def test_acepta_una_foto_con_direccion_valida(app):
    id_nuevo = crear(app, imagen="https://ejemplo.test/ajedrez.png")
    with app.app_context():
        assert gestor_catalogo.getProducto(id_nuevo)["imagen"] == "https://ejemplo.test/ajedrez.png"


def test_los_campos_obligatorios_se_senalan_uno_a_uno(app):
    """US-12-AC-02 y 03: se indica cada campo que hay que corregir y no se guarda nada."""
    antes = total_productos(app)
    fallos = errores(app, nombre="  ", precio="", tipo="", stock="")
    assert set(fallos) == {"nombre", "precio", "tipo", "stock"}
    assert total_productos(app) == antes


@pytest.mark.parametrize("campo, valor", [
    ("precio", "-3"), ("precio", "abc"), ("precio", "4,999"),
    ("stock", "-1"), ("stock", "2.5"), ("stock", "muchos"),
    ("tipo", "videojuegos"), ("imagen", "foto.png"), ("nombre", "x" * 101),
])
def test_los_valores_no_validos_se_rechazan(app, campo, valor):
    """US-12-AC-02 y 03: precio no negativo, stock entero no negativo y categoría existente."""
    assert campo in errores(app, **{campo: valor})


def test_admite_precio_con_punto_o_coma_y_cero(app):
    assert crear(app, precio="0") and crear(app, nombre="Juego dos", precio="12.5")


def test_no_se_puede_repetir_el_nombre(app):
    """US-12-AC-07: no aparece un producto duplicado."""
    crear(app)
    assert "nombre" in errores(app, nombre="ajedrez de la tierra media")


@pytest.mark.parametrize("id_usuario", [MODERADOR, None, 999])
def test_solo_un_administrador_puede_crear_productos(app, id_usuario):
    """US-12-AC-06: moderador, visitante, sesión caducada o usuario que no existe."""
    antes = total_productos(app)
    with pytest.raises(gestor_catalogo.PermisoDenegado):
        crear(app, id_usuario=id_usuario)
    assert total_productos(app) == antes


def test_un_cliente_no_puede_crear_productos(app):
    """US-12-AC-06."""
    with app.app_context():
        get_db().execute("INSERT INTO usuarios (id, email, nombre_usuario, hash_contrasena, rol, estado) "
                         "VALUES (50, 'frodo@comarca.test', 'Frodo', 'x', 'cliente', 'activa')")
        get_db().commit()
    with pytest.raises(gestor_catalogo.PermisoDenegado):
        crear(app, id_usuario=50)


def test_si_falla_el_guardado_se_avisa_y_no_queda_nada(app, monkeypatch):
    """US-12-AC-07."""
    def falla(*args):
        raise sqlite3.OperationalError("base de datos no disponible")

    antes = total_productos(app)
    monkeypatch.setattr(productos_repo, "crear", falla)
    with pytest.raises(gestor_catalogo.CatalogoNoDisponible):
        crear(app)
    assert total_productos(app) == antes


def test_la_base_de_datos_impide_duplicados_aunque_lleguen_a_la_vez(app, monkeypatch):
    """Si dos altas iguales pasan la comprobación a la vez, solo se guarda una."""
    crear(app)
    monkeypatch.setattr(productos_repo, "existe_nombre", lambda nombre: False)
    assert "nombre" in errores(app)
