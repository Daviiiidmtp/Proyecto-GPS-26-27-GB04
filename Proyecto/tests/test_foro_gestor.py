"""Pruebas de la lógica y los datos de crear tema en el foro (US-07, GB04-99)."""
import sqlite3
from datetime import datetime, timedelta

import pytest

from app.db import get_db
from app.gestores import gestor_foro
from app.repositories import foro_repo

HOY = datetime(2026, 11, 15, 12, 0, 0)
ADMIN, MODERADOR = 1, 2


def crear_cuenta(app, id_usuario, estado="activa"):
    with app.app_context():
        get_db().execute(
            "INSERT INTO usuarios (id, email, nombre_usuario, hash_contrasena, rol, estado) "
            "VALUES (?, ?, ?, 'x', 'cliente', ?)",
            (id_usuario, f"usuario{id_usuario}@comarca.test", f"Usuario {id_usuario}", estado))
        get_db().commit()
    return id_usuario


def publicar(app, id_usuario, titulo="Busco grupo de rol", cuerpo="¿Alguien juega los jueves?", ahora=HOY):
    with app.app_context():
        return gestor_foro.crearTema(titulo, cuerpo, id_usuario, ahora=ahora)


def total_temas(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM temas").fetchone()[0]


def temas(app):
    with app.app_context():
        return gestor_foro.getTemas()


# ---------- Lista pública (AC-01 y AC-03) ----------

def test_la_lista_de_temas_es_publica_y_trae_los_de_ejemplo(app):
    """US-07-AC-01: se lee sin sesión."""
    lista = temas(app)
    assert [t["titulo"] for t in lista] == [
        "¿Qué mazo usáis para el Torneo de Dragones de Bruma?", "Normas del foro"]
    assert lista[0]["autor"] == "Moderación" and lista[0]["fecha"] == "08/11/2026" and lista[0]["hora"] == "18:30"


def test_un_foro_sin_temas_devuelve_una_lista_vacia(app):
    with app.app_context():
        get_db().execute("DELETE FROM temas")
        get_db().commit()
    assert temas(app) == []


def test_el_tema_nuevo_sale_el_primero_con_autor_y_fecha(app):
    """US-07-AC-03."""
    usuario = crear_cuenta(app, 50)
    id_tema = publicar(app, usuario)
    primero = temas(app)[0]
    assert primero["id"] == id_tema
    assert primero["autor"] == "Usuario 50" and primero["fecha"] == "15/11/2026" and primero["hora"] == "12:00"
    with app.app_context():
        assert gestor_foro.getTema(id_tema)["cuerpo"] == "¿Alguien juega los jueves?"


def test_get_tema_de_uno_que_no_existe_devuelve_none(app):
    with app.app_context():
        assert gestor_foro.getTema(999) is None


# ---------- Quién puede publicar (AC-01 y AC-05) ----------

@pytest.mark.parametrize("estado, motivo", [("pendiente", "pendiente"), ("bloqueada", "bloqueada")])
def test_una_cuenta_sin_verificar_o_bloqueada_no_puede_publicar(app, estado, motivo):
    """US-07-AC-05: se deniega y no se guarda nada."""
    usuario = crear_cuenta(app, 60, estado)
    antes = total_temas(app)
    with pytest.raises(gestor_foro.PublicacionDenegada) as error:
        publicar(app, usuario)
    assert error.value.motivo == motivo
    assert total_temas(app) == antes


@pytest.mark.parametrize("id_usuario", [None, 999])
def test_sin_sesion_o_con_sesion_caducada_no_se_puede_publicar(app, id_usuario):
    """US-07-AC-05: visitante o cuenta que ya no existe."""
    antes = total_temas(app)
    with pytest.raises(gestor_foro.PublicacionDenegada) as error:
        publicar(app, id_usuario)
    assert error.value.motivo == "sin_sesion"
    assert total_temas(app) == antes


def test_puede_publicar_solo_con_cuenta_activa(app):
    """US-07-AC-01: la interfaz muestra «Nuevo tema» solo a estas cuentas."""
    activa, pendiente, bloqueada = crear_cuenta(app, 70), crear_cuenta(app, 71, "pendiente"), crear_cuenta(app, 72, "bloqueada")
    with app.app_context():
        assert gestor_foro.puedePublicar(activa) and gestor_foro.puedePublicar(MODERADOR)
        assert not gestor_foro.puedePublicar(pendiente)
        assert not gestor_foro.puedePublicar(bloqueada)
        assert not gestor_foro.puedePublicar(None)


# ---------- Validaciones (AC-02 y AC-04) ----------

@pytest.mark.parametrize("titulo, cuerpo, campos", [
    ("", "Texto", {"titulo"}),
    ("Título", "   ", {"cuerpo"}),
    ("  ", "", {"titulo", "cuerpo"}),
    ("x" * 121, "Texto", {"titulo"}),
])
def test_falta_titulo_o_cuerpo_se_indica_el_campo_y_no_se_publica(app, titulo, cuerpo, campos):
    """US-07-AC-02 y AC-04."""
    usuario = crear_cuenta(app, 80)
    antes = total_temas(app)
    with pytest.raises(gestor_foro.TemaInvalido) as error:
        publicar(app, usuario, titulo, cuerpo)
    assert set(error.value.errores) == campos
    assert total_temas(app) == antes


def test_se_quitan_los_espacios_de_los_extremos(app):
    usuario = crear_cuenta(app, 81)
    id_tema = publicar(app, usuario, "  Mi tema  ", "  Hola  ")
    with app.app_context():
        tema = gestor_foro.getTema(id_tema)
    assert tema["titulo"] == "Mi tema" and tema["cuerpo"] == "Hola"


# ---------- Errores y duplicados (AC-06) ----------

def test_publicar_dos_veces_seguidas_no_crea_un_duplicado(app):
    """US-07-AC-06: al reintentar no se añade otro tema igual."""
    usuario = crear_cuenta(app, 90)
    primero = publicar(app, usuario)
    segundo = publicar(app, usuario, ahora=HOY + timedelta(seconds=30))
    assert primero == segundo
    assert total_temas(app) == 3


def test_el_mismo_tema_mucho_despues_si_se_guarda(app):
    usuario = crear_cuenta(app, 91)
    primero = publicar(app, usuario)
    segundo = publicar(app, usuario, ahora=HOY + timedelta(minutes=10))
    assert primero != segundo


def test_si_falla_el_guardado_avisa_y_no_guarda_nada(app, monkeypatch):
    """US-07-AC-06."""
    usuario = crear_cuenta(app, 92)
    antes = total_temas(app)

    def falla(*args):
        raise sqlite3.OperationalError("disco lleno")

    monkeypatch.setattr(foro_repo, "crear_tema", falla)
    with pytest.raises(gestor_foro.ForoNoDisponible):
        publicar(app, usuario)
    assert total_temas(app) == antes


def test_si_no_se_puede_leer_el_foro_avisa(app, monkeypatch):
    def falla():
        raise sqlite3.OperationalError("base de datos bloqueada")

    monkeypatch.setattr(foro_repo, "listar_temas", falla)
    with pytest.raises(gestor_foro.ForoNoDisponible):
        temas(app)


def test_la_base_de_datos_no_admite_temas_vacios(app):
    """La tabla también impide guardar título o cuerpo vacíos."""
    with app.app_context(), pytest.raises(sqlite3.IntegrityError):
        foro_repo.crear_tema("   ", "Texto", ADMIN, "2026-11-15 12:00:00")
