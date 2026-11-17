"""Pruebas de la lógica y los datos de modificar stock (US-13, GB04-103)."""
import sqlite3

import pytest

from app.db import get_db
from app.gestores import gestor_catalogo
from app.repositories import productos_repo

ADMIN, MODERADOR = 1, 2
COLONOS = 1      # 12 unidades
AGOTADO = 4      # 0 unidades
RETIRADO = 10    # no publicado


def cambiar(app, id_producto, stock, id_usuario=ADMIN):
    with app.app_context():
        return gestor_catalogo.cambiarStock(id_producto, stock, id_usuario)


def stock(app, id_producto):
    with app.app_context():
        return get_db().execute("SELECT stock FROM productos WHERE id = ?", (id_producto,)).fetchone()[0]


def crear_cliente(app, id_usuario=50):
    with app.app_context():
        get_db().execute(
            "INSERT INTO usuarios (id, email, nombre_usuario, hash_contrasena, rol, estado) "
            "VALUES (?, 'cliente@comarca.test', 'Cliente', 'x', 'cliente', 'activa')", (id_usuario,))
        get_db().commit()
    return id_usuario


@pytest.mark.parametrize("nuevo", [20, "3", " 7 "])
def test_el_administrador_aumenta_o_reduce_el_stock(app, nuevo):
    """US-13-AC-01."""
    producto = cambiar(app, COLONOS, nuevo)
    assert producto["stock"] == int(str(nuevo).strip()) == stock(app, COLONOS)


def test_con_stock_cero_pasa_a_agotado_y_sigue_publicado(app):
    """US-13-AC-02."""
    producto = cambiar(app, COLONOS, 0)
    assert producto["estado"] == "Agotado" and producto["disponible"] is False
    with app.app_context():
        assert COLONOS in [p["id"] for p in gestor_catalogo.getProductos()]


def test_con_stock_mayor_que_cero_pasa_a_disponible(app):
    """US-13-AC-02."""
    assert cambiar(app, AGOTADO, 5)["estado"] == "Disponible"


@pytest.mark.parametrize("nuevo", [-1, "-5"])
def test_un_stock_negativo_se_rechaza_y_se_conserva_el_anterior(app, nuevo):
    """US-13-AC-03."""
    with pytest.raises(gestor_catalogo.StockInvalido) as error:
        cambiar(app, COLONOS, nuevo)
    assert "negativo" in str(error.value)
    assert stock(app, COLONOS) == 12


@pytest.mark.parametrize("nuevo", ["", "2,5", "1.5", "diez", None])
def test_un_valor_que_no_es_entero_se_rechaza(app, nuevo):
    """Las cantidades son enteros y no se admiten fracciones."""
    with pytest.raises(gestor_catalogo.StockInvalido):
        cambiar(app, COLONOS, nuevo)
    assert stock(app, COLONOS) == 12


def test_el_nuevo_stock_se_ve_en_el_catalogo(app):
    """US-13-AC-04: el catálogo y la cesta usan el stock nuevo."""
    cambiar(app, COLONOS, 0)
    with app.app_context():
        assert gestor_catalogo.getProducto(COLONOS)["estado"] == "Agotado"
        assert COLONOS not in [p["id"] for p in gestor_catalogo.getProductosDisponibles()]


@pytest.mark.parametrize("id_usuario", [MODERADOR, None, 999])
def test_moderador_visitante_o_sesion_caducada_no_pueden_cambiar_el_stock(app, id_usuario):
    """US-13-AC-05."""
    with pytest.raises(gestor_catalogo.PermisoDenegado):
        cambiar(app, COLONOS, 1, id_usuario)
    assert stock(app, COLONOS) == 12


def test_un_cliente_no_puede_cambiar_el_stock(app):
    """US-13-AC-05."""
    cliente = crear_cliente(app)
    with pytest.raises(gestor_catalogo.PermisoDenegado):
        cambiar(app, COLONOS, 1, cliente)
    assert stock(app, COLONOS) == 12


@pytest.mark.parametrize("id_producto", [999, RETIRADO])
def test_un_producto_inexistente_no_se_puede_cambiar(app, id_producto):
    """US-13-AC-05."""
    with pytest.raises(gestor_catalogo.ProductoNoEncontrado):
        cambiar(app, id_producto, 3)
    assert stock(app, RETIRADO) == 2


def test_si_falla_el_guardado_se_conserva_el_ultimo_stock(app, monkeypatch):
    """US-13-AC-06."""
    def falla(*args):
        raise sqlite3.OperationalError("disco lleno")

    monkeypatch.setattr(productos_repo, "actualizar_stock", falla)
    with pytest.raises(gestor_catalogo.CatalogoNoDisponible):
        cambiar(app, COLONOS, 3)
    assert stock(app, COLONOS) == 12


def test_la_base_de_datos_nunca_deja_stock_negativo(app):
    """US-13-AC-07: aunque llegue un valor negativo por otro camino, la tabla lo rechaza y no cambia nada."""
    with app.app_context():
        with pytest.raises(sqlite3.IntegrityError):
            productos_repo.actualizar_stock(COLONOS, -3)
        assert not get_db().in_transaction
    assert stock(app, COLONOS) == 12


def test_dos_cambios_seguidos_dejan_el_ultimo(app):
    """US-13-AC-07: cada cambio se confirma entero; no se mezclan."""
    cambiar(app, COLONOS, 4)
    cambiar(app, COLONOS, 9)
    assert stock(app, COLONOS) == 9
