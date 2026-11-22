"""Pruebas de la lógica y los datos de responder en el foro (US-08, GB04-112)."""
import sqlite3
from datetime import datetime, timedelta

import pytest

from app.db import get_db
from app.gestores import gestor_foro
from app.repositories import foro_repo

HOY = datetime(2026, 11, 18, 18, 0, 0)
ADMIN = 1
NORMAS, MAZOS = 1, 2   # temas de ejemplo. MAZOS ya tiene una respuesta


def crear_cuenta(app, id_usuario, estado="activa"):
    with app.app_context():
        get_db().execute(
            "INSERT INTO usuarios (id, email, nombre_usuario, hash_contrasena, rol, estado) "
            "VALUES (?, ?, ?, 'x', 'cliente', ?)",
            (id_usuario, f"usuario{id_usuario}@comarca.test", f"Usuario {id_usuario}", estado))
        get_db().commit()
    return id_usuario


def responder(app, id_usuario, id_tema=MAZOS, texto="Yo uso el de niebla.", ahora=HOY):
    with app.app_context():
        return gestor_foro.anadirComentario(id_usuario, id_tema, texto, ahora=ahora)


def tema(app, id_tema=MAZOS):
    with app.app_context():
        return gestor_foro.getTema(id_tema)


def total_respuestas(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM respuestas").fetchone()[0]


# ---------- Respuestas públicas (AC-01) ----------

def test_el_tema_trae_sus_respuestas_con_autor_y_fecha(app):
    """US-08-AC-01: se leen sin sesión."""
    respuestas = tema(app)["respuestas"]
    assert len(respuestas) == 1
    assert respuestas[0]["autor"] == "Administración"
    assert respuestas[0]["fecha"] == "09/11/2026" and respuestas[0]["hora"] == "11:15"


def test_un_tema_sin_respuestas_trae_una_lista_vacia(app):
    assert tema(app, NORMAS)["respuestas"] == []


def test_un_tema_que_no_existe_devuelve_none(app):
    assert tema(app, 999) is None


# ---------- Publicar (AC-02 y AC-03) ----------

def test_la_respuesta_sale_al_final_del_tema_con_autor_y_fecha(app):
    """US-08-AC-03."""
    usuario = crear_cuenta(app, 50)
    id_respuesta = responder(app, usuario)
    ultima = tema(app)["respuestas"][-1]
    assert ultima["id"] == id_respuesta and ultima["cuerpo"] == "Yo uso el de niebla."
    assert ultima["autor"] == "Usuario 50" and ultima["fecha"] == "18/11/2026" and ultima["hora"] == "18:00"


def test_las_respuestas_salen_en_orden_cronologico(app):
    """US-08-AC-03."""
    usuario = crear_cuenta(app, 51)
    responder(app, usuario, texto="Segunda", ahora=HOY)
    responder(app, usuario, texto="Tercera", ahora=HOY + timedelta(minutes=1))
    assert [r["cuerpo"] for r in tema(app)["respuestas"]][1:] == ["Segunda", "Tercera"]


def test_se_quitan_los_espacios_sobrantes(app):
    responder(app, crear_cuenta(app, 52), texto="   Hola   ")
    assert tema(app)["respuestas"][-1]["cuerpo"] == "Hola"


@pytest.mark.parametrize("texto", ["", "   ", None])
def test_una_respuesta_vacia_no_se_publica(app, texto):
    """US-08-AC-02."""
    usuario = crear_cuenta(app, 53)
    antes = total_respuestas(app)
    with pytest.raises(gestor_foro.RespuestaInvalida) as error:
        responder(app, usuario, texto=texto)
    assert error.value.errores == {"cuerpo": "Escribe el texto de la respuesta."}
    assert total_respuestas(app) == antes


def test_una_respuesta_demasiado_larga_no_se_publica(app):
    with pytest.raises(gestor_foro.RespuestaInvalida):
        responder(app, crear_cuenta(app, 54), texto="x" * 5001)


# ---------- Tema que no existe (AC-04) ----------

def test_responder_en_un_tema_que_no_existe_no_guarda_nada(app):
    """US-08-AC-04."""
    antes = total_respuestas(app)
    with pytest.raises(gestor_foro.TemaNoEncontrado) as error:
        responder(app, crear_cuenta(app, 55), id_tema=999)
    assert "ya no está disponible" in str(error.value)
    assert total_respuestas(app) == antes


# ---------- Quién no puede responder (AC-05) ----------

def test_un_visitante_o_una_sesion_caducada_no_pueden_responder(app):
    """US-08-AC-05."""
    antes = total_respuestas(app)
    for usuario in (None, 999):
        with pytest.raises(gestor_foro.PublicacionDenegada) as error:
            responder(app, usuario)
        assert error.value.motivo == "sin_sesion"
    assert total_respuestas(app) == antes


@pytest.mark.parametrize("estado", ["pendiente", "bloqueada"])
def test_una_cuenta_sin_verificar_o_bloqueada_no_puede_responder(app, estado):
    """US-08-AC-05."""
    usuario = crear_cuenta(app, 56, estado)
    with pytest.raises(gestor_foro.PublicacionDenegada) as error:
        responder(app, usuario)
    assert error.value.motivo == estado


def test_el_permiso_se_comprueba_antes_que_el_texto(app):
    with pytest.raises(gestor_foro.PublicacionDenegada):
        responder(app, None, texto="")


# ---------- Error al guardar y duplicados (AC-05) ----------

def test_si_falla_el_guardado_avisa_y_no_se_guarda_nada(app, monkeypatch):
    """US-08-AC-05."""
    usuario = crear_cuenta(app, 57)

    def falla(*args):
        raise sqlite3.OperationalError("disco lleno")

    antes = total_respuestas(app)
    monkeypatch.setattr(foro_repo, "crear_respuesta", falla)
    with pytest.raises(gestor_foro.ForoNoDisponible):
        responder(app, usuario)
    assert total_respuestas(app) == antes


def test_reintentar_tras_un_fallo_no_duplica_la_respuesta(app, monkeypatch):
    """US-08-AC-05."""
    usuario = crear_cuenta(app, 58)
    original = foro_repo.crear_respuesta

    def falla(*args):
        raise sqlite3.OperationalError("disco lleno")

    monkeypatch.setattr(foro_repo, "crear_respuesta", falla)
    with pytest.raises(gestor_foro.ForoNoDisponible):
        responder(app, usuario)
    monkeypatch.setattr(foro_repo, "crear_respuesta", original)
    primera = responder(app, usuario)
    segunda = responder(app, usuario, ahora=HOY + timedelta(seconds=30))
    assert primera == segunda and len(tema(app)["respuestas"]) == 2


def test_la_misma_respuesta_mucho_mas_tarde_si_se_publica(app):
    usuario = crear_cuenta(app, 59)
    primera = responder(app, usuario)
    segunda = responder(app, usuario, ahora=HOY + timedelta(minutes=10))
    assert primera != segunda


def test_si_falla_la_lectura_avisa(app, monkeypatch):
    def falla(*args):
        raise sqlite3.OperationalError("bloqueada")

    monkeypatch.setattr(foro_repo, "listar_respuestas", falla)
    with pytest.raises(gestor_foro.ForoNoDisponible):
        tema(app)


def test_al_borrar_un_tema_se_borran_sus_respuestas(app):
    with app.app_context():
        get_db().execute("DELETE FROM temas WHERE id = ?", (MAZOS,))
        get_db().commit()
    assert total_respuestas(app) == 0
