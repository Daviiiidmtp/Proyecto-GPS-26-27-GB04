"""Pruebas de la lógica y los datos de moderar el foro y bloquear cuentas (US-10, GB04-120)."""
import sqlite3
from datetime import datetime

import pytest

from app.db import get_db
from app.gestores import gestor_foro, gestor_usuario
from app.repositories import foro_repo, usuarios_repo

HOY = datetime(2026, 11, 21, 12, 0, 0)
ADMIN, MODERADOR = 1, 2
NORMAS, MAZOS = 1, 2          # temas de ejemplo
RESPUESTA_MAZOS = 1           # respuesta de ejemplo del tema MAZOS


def crear_cuenta(app, id_usuario, estado="activa", rol="cliente"):
    with app.app_context():
        get_db().execute(
            "INSERT INTO usuarios (id, email, nombre_usuario, hash_contrasena, rol, estado) VALUES (?, ?, ?, 'x', ?, ?)",
            (id_usuario, f"usuario{id_usuario}@comarca.test", f"Usuario {id_usuario}", rol, estado))
        get_db().commit()
    return id_usuario


def retirar(app, id_mensaje, id_usuario, tipo="respuesta"):
    with app.app_context():
        return gestor_foro.eliminarMensaje(id_mensaje, id_usuario, tipo, ahora=HOY)


def estado(app, id_usuario):
    with app.app_context():
        return usuarios_repo.obtener_por_id(id_usuario)["estado"]


def total_retirados(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM mensajes_retirados").fetchone()[0]


def tema(app, id_tema):
    with app.app_context():
        return gestor_foro.getTema(id_tema)


def falla_la_base_de_datos(monkeypatch, modulo, nombre):
    def fallo(*args, **kwargs):
        raise sqlite3.OperationalError("database is locked")
    monkeypatch.setattr(modulo, nombre, fallo)


# ---------- Retirar mensajes (AC-01) ----------

@pytest.mark.parametrize("moderador", [MODERADOR, ADMIN])
def test_moderador_y_admin_retiran_una_respuesta_y_deja_de_verse(app, moderador):
    """US-10-AC-01."""
    assert retirar(app, RESPUESTA_MAZOS, moderador) is True
    assert tema(app, MAZOS)["respuestas"] == []
    with app.app_context():
        fila = get_db().execute("SELECT tipo, mensaje_id, usuario_id, fecha_hora FROM mensajes_retirados").fetchone()
    assert tuple(fila) == ("respuesta", RESPUESTA_MAZOS, moderador, "2026-11-21 12:00:00")


def test_retirar_un_tema_lo_quita_de_la_lista_y_de_su_pagina(app):
    """US-10-AC-01: el tema retirado no lo ve nadie."""
    assert retirar(app, MAZOS, MODERADOR, "tema") is True
    with app.app_context():
        titulos = [t["titulo"] for t in gestor_foro.getTemas()]
    assert titulos == ["Normas del foro"]
    assert tema(app, MAZOS) is None


def test_no_se_puede_responder_a_un_tema_retirado(app):
    """US-10-AC-01 y US-08-AC-04."""
    cliente = crear_cuenta(app, 50)
    retirar(app, MAZOS, MODERADOR, "tema")
    with app.app_context(), pytest.raises(gestor_foro.TemaNoEncontrado):
        gestor_foro.anadirComentario(cliente, MAZOS, "Hola", ahora=HOY)


def test_el_mensaje_retirado_no_se_borra_de_la_base_de_datos(app):
    """Regla de US-10: la retirada solo se deshace con una nueva publicación."""
    retirar(app, RESPUESTA_MAZOS, MODERADOR)
    with app.app_context():
        assert foro_repo.existe_mensaje("respuesta", RESPUESTA_MAZOS)
        assert foro_repo.esta_retirado("respuesta", RESPUESTA_MAZOS)


def test_una_respuesta_retirada_no_cuenta_como_duplicado(app):
    """Si el autor vuelve a publicar el mismo texto, se guarda como mensaje nuevo."""
    cliente = crear_cuenta(app, 50)
    with app.app_context():
        primera = gestor_foro.anadirComentario(cliente, MAZOS, "Mazo de niebla", ahora=HOY)
    retirar(app, primera, MODERADOR)
    with app.app_context():
        segunda = gestor_foro.anadirComentario(cliente, MAZOS, "Mazo de niebla", ahora=HOY)
    assert segunda != primera
    assert [r["id"] for r in tema(app, MAZOS)["respuestas"]] == [RESPUESTA_MAZOS, segunda]


# ---------- Permisos (AC-05 y AC-06) ----------

def test_un_cliente_no_puede_retirar_mensajes(app):
    """US-10-AC-05."""
    cliente = crear_cuenta(app, 50)
    with pytest.raises(gestor_foro.ModeracionDenegada) as error:
        retirar(app, RESPUESTA_MAZOS, cliente)
    assert error.value.motivo == "sin_permiso"
    assert total_retirados(app) == 0


@pytest.mark.parametrize("id_usuario", [None, 999])
def test_sin_sesion_o_con_sesion_caducada_no_se_retira(app, id_usuario):
    """US-10-AC-05 y AC-06: se le indica que inicie sesión."""
    with pytest.raises(gestor_foro.ModeracionDenegada) as error:
        retirar(app, RESPUESTA_MAZOS, id_usuario)
    assert error.value.motivo == "sin_sesion" and "Inicia sesión" in str(error.value)
    assert total_retirados(app) == 0


def test_un_moderador_bloqueado_no_puede_retirar(app):
    """Regla de EP-04: el estado de la cuenta se comprueba al guardar."""
    moderador = crear_cuenta(app, 60, estado="bloqueada", rol="moderador")
    with pytest.raises(gestor_foro.ModeracionDenegada):
        retirar(app, RESPUESTA_MAZOS, moderador)
    assert total_retirados(app) == 0


def test_puede_moderar_solo_para_moderador_y_admin(app):
    cliente = crear_cuenta(app, 50)
    with app.app_context():
        assert gestor_foro.puedeModerar(MODERADOR) and gestor_foro.puedeModerar(ADMIN)
        assert not gestor_foro.puedeModerar(cliente)
        assert not gestor_foro.puedeModerar(None)


def test_un_fallo_al_retirar_se_informa_y_no_cambia_nada(app, monkeypatch):
    """US-10-AC-06."""
    falla_la_base_de_datos(monkeypatch, foro_repo, "retirar")
    with pytest.raises(gestor_foro.ForoNoDisponible):
        retirar(app, RESPUESTA_MAZOS, MODERADOR)
    assert total_retirados(app) == 0
    assert len(tema(app, MAZOS)["respuestas"]) == 1


# ---------- Mensajes que no existen o ya retirados (AC-07) ----------

def test_retirar_dos_veces_informa_y_no_duplica(app):
    """US-10-AC-07."""
    assert retirar(app, RESPUESTA_MAZOS, MODERADOR) is True
    assert retirar(app, RESPUESTA_MAZOS, ADMIN) is False
    assert total_retirados(app) == 1
    with app.app_context():
        autor = get_db().execute("SELECT usuario_id FROM mensajes_retirados").fetchone()[0]
    assert autor == MODERADOR


@pytest.mark.parametrize("id_mensaje, tipo", [(999, "respuesta"), (999, "tema"), (1, "foto")])
def test_un_mensaje_que_no_existe_no_se_retira(app, id_mensaje, tipo):
    with pytest.raises(gestor_foro.MensajeNoEncontrado):
        retirar(app, id_mensaje, MODERADOR, tipo)
    assert total_retirados(app) == 0


# ---------- Bloquear cuentas (AC-02 y AC-03) ----------

def test_el_admin_bloquea_un_cliente_activo(app):
    """US-10-AC-02."""
    cliente = crear_cuenta(app, 50)
    with app.app_context():
        assert gestor_usuario.banearUsuario(cliente, ADMIN) is True
    assert estado(app, cliente) == "bloqueada"


def test_la_cuenta_bloqueada_no_puede_entrar_ni_participar(app):
    """US-10-AC-02 y AC-03: las operaciones protegidas se deniegan y no guardan nada."""
    cliente = crear_cuenta(app, 50)
    with app.app_context():
        gestor_usuario.banearUsuario(cliente, ADMIN)
        assert gestor_usuario.cuentaBloqueada(cliente)
        assert not gestor_foro.puedePublicar(cliente)
        with pytest.raises(gestor_foro.PublicacionDenegada):
            gestor_foro.anadirComentario(cliente, MAZOS, "Hola", ahora=HOY)
        total = get_db().execute("SELECT COUNT(*) FROM respuestas").fetchone()[0]
    assert total == 1


def test_al_bloquear_se_cierra_la_sesion_abierta(app, client):
    """US-10-AC-03: en la siguiente petición la sesión se cierra y se avisa."""
    cliente = crear_cuenta(app, 50)
    with client.session_transaction() as sesion:
        sesion["usuario_id"] = cliente
        sesion["nombre_usuario"] = "Usuario 50"
        sesion["rol"] = "cliente"
    with app.app_context():
        gestor_usuario.banearUsuario(cliente, ADMIN)
    pagina = client.get("/foro").get_data(as_text=True)
    assert "Tu cuenta está bloqueada. Se ha cerrado la sesión." in pagina
    with client.session_transaction() as sesion:
        assert "usuario_id" not in sesion
    respuesta = client.post(f"/foro/temas/{MAZOS}/responder", data={"cuerpo": "Hola"})
    assert respuesta.status_code == 302 and "/login" in respuesta.headers["Location"]


def test_una_sesion_normal_no_se_cierra(app, client):
    cliente = crear_cuenta(app, 50)
    with client.session_transaction() as sesion:
        sesion["usuario_id"] = cliente
    client.get("/foro")
    with client.session_transaction() as sesion:
        assert sesion["usuario_id"] == cliente


# ---------- Desbloquear (AC-04) ----------

def test_el_admin_desbloquea_sin_borrar_mensajes_ni_abrir_sesion(app):
    """US-10-AC-04."""
    cliente = crear_cuenta(app, 50)
    with app.app_context():
        id_respuesta = gestor_foro.anadirComentario(cliente, MAZOS, "Mazo de bosque", ahora=HOY)
        gestor_usuario.banearUsuario(cliente, ADMIN)
        assert gestor_usuario.desbanearUsuario(cliente, ADMIN) is True
    assert estado(app, cliente) == "activa"
    assert id_respuesta in [r["id"] for r in tema(app, MAZOS)["respuestas"]]


def test_desbloquear_una_cuenta_activa_informa_y_no_cambia(app):
    """US-10-AC-07."""
    cliente = crear_cuenta(app, 50)
    with app.app_context():
        assert gestor_usuario.desbanearUsuario(cliente, ADMIN) is False
    assert estado(app, cliente) == "activa"


# ---------- Permisos del bloqueo (AC-05 y AC-06) ----------

@pytest.mark.parametrize("quien, motivo", [(MODERADOR, "no_admin"), (None, "sin_sesion"), (999, "sin_sesion")])
def test_solo_el_admin_puede_bloquear_y_desbloquear(app, quien, motivo):
    """US-10-AC-05 y AC-06."""
    cliente = crear_cuenta(app, 50)
    bloqueado = crear_cuenta(app, 51, estado="bloqueada")
    with app.app_context():
        with pytest.raises(gestor_usuario.PermisoDenegado) as error:
            gestor_usuario.banearUsuario(cliente, quien)
        assert error.value.motivo == motivo
        with pytest.raises(gestor_usuario.PermisoDenegado):
            gestor_usuario.desbanearUsuario(bloqueado, quien)
        with pytest.raises(gestor_usuario.PermisoDenegado):
            gestor_usuario.getClientes(quien)
    assert estado(app, cliente) == "activa" and estado(app, bloqueado) == "bloqueada"


def test_un_cliente_no_puede_bloquear(app):
    """US-10-AC-05."""
    cliente = crear_cuenta(app, 50)
    otro = crear_cuenta(app, 51)
    with app.app_context(), pytest.raises(gestor_usuario.PermisoDenegado):
        gestor_usuario.banearUsuario(otro, cliente)
    assert estado(app, otro) == "activa"


@pytest.mark.parametrize("cuenta", [MODERADOR, ADMIN, 999])
def test_solo_se_bloquean_cuentas_de_cliente(app, cuenta):
    """US-10-AC-02: moderador y administrador no se bloquean desde aquí."""
    with app.app_context(), pytest.raises(gestor_usuario.CuentaNoValida):
        gestor_usuario.banearUsuario(cuenta, ADMIN)
    assert estado(app, MODERADOR) == "activa" and estado(app, ADMIN) == "activa"


def test_una_cuenta_pendiente_no_se_bloquea(app):
    pendiente = crear_cuenta(app, 50, estado="pendiente")
    with app.app_context(), pytest.raises(gestor_usuario.CuentaNoValida):
        gestor_usuario.banearUsuario(pendiente, ADMIN)
    assert estado(app, pendiente) == "pendiente"


def test_bloquear_dos_veces_informa_y_no_cambia(app):
    """US-10-AC-07."""
    cliente = crear_cuenta(app, 50)
    with app.app_context():
        assert gestor_usuario.banearUsuario(cliente, ADMIN) is True
        assert gestor_usuario.banearUsuario(cliente, ADMIN) is False
    assert estado(app, cliente) == "bloqueada"


def test_un_fallo_al_bloquear_se_informa_y_no_cambia(app, monkeypatch):
    """US-10-AC-06."""
    cliente = crear_cuenta(app, 50)
    falla_la_base_de_datos(monkeypatch, usuarios_repo, "cambiar_estado_cliente")
    with app.app_context(), pytest.raises(gestor_usuario.UsuariosNoDisponibles):
        gestor_usuario.banearUsuario(cliente, ADMIN)
    assert estado(app, cliente) == "activa"


def test_el_admin_ve_las_cuentas_de_cliente_con_su_estado(app):
    crear_cuenta(app, 50)
    crear_cuenta(app, 51, estado="bloqueada")
    with app.app_context():
        cuentas = gestor_usuario.getClientes(ADMIN)
    assert [(c["id"], c["estado"]) for c in cuentas] == [(50, "activa"), (51, "bloqueada")]
    assert all(c["email"] and c["nombre_usuario"] for c in cuentas)
