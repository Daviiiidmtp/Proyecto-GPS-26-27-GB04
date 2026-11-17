"""Pruebas de la lógica y los datos de la cesta (US-16, GB04-106)."""
import sqlite3

import pytest

from app.db import get_db
from app.gestores import gestor_catalogo
from app.repositories import cesta_repo

COLONOS = 1       # 39,95 €, 12 unidades
SOBRE = 2         # 4,50 €, 80 unidades
PUENTE = 5        # 24,50 €, 3 unidades
AGOTADO = 4       # stock 0
RETIRADO = 10     # no publicado


def anadir(app, cesta, id_producto, cantidad=1):
    with app.app_context():
        return gestor_catalogo.anadirProductoCesta(id_producto, cantidad, cesta)


def ver(app, cesta):
    with app.app_context():
        return gestor_catalogo.getCesta(cesta)


def cambiar_producto(app, id_producto, **campos):
    with app.app_context():
        for campo, valor in campos.items():
            get_db().execute(f"UPDATE productos SET {campo} = ? WHERE id = ?", (valor, id_producto))
        get_db().commit()


# ---------- Añadir y quitar (AC-01) ----------

def test_se_anade_un_producto_disponible(app):
    """US-16-AC-01."""
    cesta = {}
    assert anadir(app, cesta, COLONOS, 2) is True
    assert cesta == {"1": 2}


def test_anadir_otra_vez_el_mismo_producto_suma_unidades(app):
    cesta = {}
    anadir(app, cesta, SOBRE, 3)
    anadir(app, cesta, SOBRE, "2")
    assert cesta == {"2": 5}


def test_quitar_unidades_y_quitar_el_producto(app):
    """US-16-AC-01: se pueden quitar unidades o el producto entero."""
    cesta = {"1": 3, "2": 1}
    assert gestor_catalogo.quitarProductoCesta(COLONOS, cesta, 2) is True
    assert cesta == {"1": 1, "2": 1}
    gestor_catalogo.quitarProductoCesta(COLONOS, cesta, 1)
    assert cesta == {"2": 1}
    gestor_catalogo.quitarProductoCesta(SOBRE, cesta)
    assert cesta == {}


def test_quitar_algo_que_no_esta_en_la_cesta_devuelve_false(app):
    assert gestor_catalogo.quitarProductoCesta(COLONOS, {}) is False


@pytest.mark.parametrize("cantidad", [0, -1, "", "dos", "1.5", None, 100])
def test_la_cantidad_debe_ser_un_entero_positivo(app, cantidad):
    """Regla de US-16: las cantidades son enteros positivos."""
    cesta = {}
    with pytest.raises(gestor_catalogo.CantidadInvalida):
        anadir(app, cesta, COLONOS, cantidad)
    assert cesta == {}


def test_quitar_con_cantidad_invalida_no_cambia_la_cesta(app):
    cesta = {"1": 2}
    with pytest.raises(gestor_catalogo.CantidadInvalida):
        gestor_catalogo.quitarProductoCesta(COLONOS, cesta, 0)
    assert cesta == {"1": 2}


# ---------- Producto no disponible (AC-04) ----------

@pytest.mark.parametrize("id_producto, motivo", [(AGOTADO, "agotado"), (RETIRADO, "no_existe"), (999, "no_existe")])
def test_no_se_anade_un_producto_agotado_retirado_o_inexistente(app, id_producto, motivo):
    """US-16-AC-04: se informa del artículo y no se añade."""
    cesta = {}
    with pytest.raises(gestor_catalogo.ProductoNoDisponible) as error:
        anadir(app, cesta, id_producto)
    assert error.value.motivo == motivo
    assert cesta == {}


def test_no_se_anaden_mas_unidades_de_las_que_hay(app):
    """US-16-AC-04: se dice qué artículo es y cuántas quedan."""
    cesta = {"5": 2}
    with pytest.raises(gestor_catalogo.ProductoNoDisponible) as error:
        anadir(app, cesta, PUENTE, 2)
    assert error.value.motivo == "insuficiente"
    assert error.value.nombre == "El Último Puente" and error.value.disponibles == 3
    assert "Quedan 3" in str(error.value)
    assert cesta == {"5": 2}


def test_la_cesta_no_reserva_stock(app):
    """Regla de US-16: añadir a la cesta no cambia el stock."""
    anadir(app, {}, PUENTE, 3)
    with app.app_context():
        assert gestor_catalogo.getProducto(PUENTE)["stock"] == 3


# ---------- Contenido de la cesta (AC-02 y AC-03) ----------

def test_la_cesta_muestra_cantidad_precio_subtotal_y_total(app):
    """US-16-AC-02."""
    datos = ver(app, {"1": 2, "2": 3})
    colonos, sobre = datos["lineas"]
    assert colonos == {"id": 1, "nombre": "Colonos de la Comarca", "cantidad": 2, "precio": 39.95,
                       "subtotal": 79.9, "stock": 12, "se_puede_comprar": True, "problema": None}
    assert sobre["subtotal"] == 13.5
    assert datos["total"] == 93.4 and datos["unidades"] == 5
    assert datos["vacia"] is False and datos["se_puede_comprar"] is True


def test_la_cesta_vacia_no_deja_iniciar_el_checkout(app):
    """US-16-AC-03."""
    for cesta in ({}, None):
        datos = ver(app, cesta)
        assert datos["vacia"] is True and datos["se_puede_comprar"] is False
        assert datos["lineas"] == [] and datos["total"] == 0


def test_si_un_producto_se_agota_despues_la_cesta_lo_indica(app):
    """US-16-AC-04: se informa qué artículo no puede comprarse y se permite corregir."""
    cesta = {}
    anadir(app, cesta, PUENTE, 3)
    anadir(app, cesta, COLONOS, 1)
    cambiar_producto(app, PUENTE, stock=1)
    datos = ver(app, cesta)
    puente = next(linea for linea in datos["lineas"] if linea["id"] == PUENTE)
    assert puente["se_puede_comprar"] is False and "Solo quedan 1 unidades de «El Último Puente»" in puente["problema"]
    assert datos["se_puede_comprar"] is False
    # Al corregir la cantidad, ya se puede comprar
    gestor_catalogo.quitarProductoCesta(PUENTE, cesta, 2)
    assert ver(app, cesta)["se_puede_comprar"] is True


@pytest.mark.parametrize("campos, texto", [({"stock": 0}, "está agotado"), ({"activo": 0}, "ya no está a la venta")])
def test_producto_agotado_o_retirado_despues_de_anadirlo(app, campos, texto):
    """US-16-AC-04."""
    cesta = {}
    anadir(app, cesta, COLONOS, 1)
    cambiar_producto(app, COLONOS, **campos)
    linea = ver(app, cesta)["lineas"][0]
    assert linea["nombre"] == "Colonos de la Comarca" and texto in linea["problema"]


def test_producto_borrado_sale_como_retirado(app):
    linea = ver(app, {"999": 1})["lineas"][0]
    assert linea["nombre"] == "Producto retirado" and linea["se_puede_comprar"] is False


def test_se_ignoran_datos_extranos_en_la_cesta(app):
    """Si la sesión trae claves o cantidades raras, no se rompe la cesta."""
    datos = ver(app, {"abc": 1, "1": "2", "2": 0, "3": 1})
    assert [linea["id"] for linea in datos["lineas"]] == [3]


def test_si_falla_la_base_de_datos_avisa(app, monkeypatch):
    def falla(*args):
        raise sqlite3.OperationalError("base de datos bloqueada")

    monkeypatch.setattr(cesta_repo, "obtener_cualquiera", falla)
    with pytest.raises(gestor_catalogo.CatalogoNoDisponible):
        ver(app, {"1": 1})
