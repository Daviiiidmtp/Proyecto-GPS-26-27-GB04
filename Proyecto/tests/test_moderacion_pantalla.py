"""Pruebas de la interfaz de moderar el foro y bloquear cuentas (US-10, GB04-119)."""
import pytest

from app.db import get_db
from app.gestores import gestor_foro, gestor_usuario

ADMIN, MODERADOR = 1, 2
MAZOS = 2                 # tema de ejemplo con una respuesta
RESPUESTA_MAZOS = 1
TEMA = f"/foro/temas/{MAZOS}"
RETIRAR_TEMA = f"/foro/temas/{MAZOS}/retirar"
RETIRAR_RESPUESTA = f"/foro/temas/{MAZOS}/respuestas/{RESPUESTA_MAZOS}/retirar"
CUENTAS = "/admin/usuarios"


def crear_cuenta(app, id_usuario, estado="activa"):
    with app.app_context():
        get_db().execute(
            "INSERT INTO usuarios (id, email, nombre_usuario, hash_contrasena, rol, estado) VALUES (?, ?, ?, 'x', 'cliente', ?)",
            (id_usuario, f"usuario{id_usuario}@comarca.test", f"Usuario {id_usuario}", estado))
        get_db().commit()
    return id_usuario


def entrar(client, id_usuario, rol):
    with client.session_transaction() as sesion:
        sesion["usuario_id"] = id_usuario
        sesion["nombre_usuario"] = f"Usuario {id_usuario}"
        sesion["rol"] = rol


def estado(app, id_usuario):
    with app.app_context():
        return get_db().execute("SELECT estado FROM usuarios WHERE id = ?", (id_usuario,)).fetchone()[0]


def total_retirados(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM mensajes_retirados").fetchone()[0]


def falla(*args, **kwargs):
    raise gestor_foro.ForoNoDisponible("fallo")


# ---------- Botones «Retirar» (AC-01 y AC-05) ----------

@pytest.mark.parametrize("quien, rol", [(MODERADOR, "moderador"), (ADMIN, "admin")])
def test_moderador_y_admin_ven_los_botones_con_confirmacion(client, quien, rol):
    """US-10-AC-01."""
    entrar(client, quien, rol)
    html = client.get(TEMA).get_data(as_text=True)
    assert "Retirar tema" in html and f'action="{RETIRAR_RESPUESTA}"' in html
    assert "data-confirmar=" in html and "window.confirm" in html


def test_un_cliente_y_un_visitante_no_ven_los_botones(app, client):
    """US-10-AC-05."""
    assert "Retirar" not in client.get(TEMA).get_data(as_text=True)
    entrar(client, crear_cuenta(app, 50), "cliente")
    assert "Retirar" not in client.get(TEMA).get_data(as_text=True)


# ---------- Retirar (AC-01, AC-05, AC-06 y AC-07) ----------

def test_retirar_una_respuesta_la_quita_y_lo_comunica(app, client):
    """US-10-AC-01."""
    entrar(client, MODERADOR, "moderador")
    respuesta = client.post(RETIRAR_RESPUESTA)
    assert respuesta.status_code == 302 and respuesta.headers["Location"].endswith(TEMA)
    html = client.get(TEMA).get_data(as_text=True)
    assert "La respuesta se ha retirado. Ya no se ve en el foro." in html and "Respuestas (0)" in html


def test_retirar_un_tema_vuelve_al_foro_y_ya_no_sale(app, client):
    """US-10-AC-01."""
    entrar(client, ADMIN, "admin")
    respuesta = client.post(RETIRAR_TEMA)
    assert respuesta.headers["Location"].endswith("/foro")
    html = client.get("/foro").get_data(as_text=True)
    assert "El tema se ha retirado." in html and f'href="{TEMA}"' not in html
    assert client.get(TEMA).status_code == 404


def test_retirar_dos_veces_informa_del_estado(app, client):
    """US-10-AC-07."""
    entrar(client, MODERADOR, "moderador")
    client.post(RETIRAR_RESPUESTA)
    html = client.post(RETIRAR_RESPUESTA, follow_redirects=True).get_data(as_text=True)
    assert "La respuesta ya estaba retirada. No se ha cambiado nada." in html
    assert total_retirados(app) == 1


def test_un_cliente_no_puede_retirar(app, client):
    """US-10-AC-05."""
    entrar(client, crear_cuenta(app, 50), "cliente")
    respuesta = client.post(RETIRAR_RESPUESTA)
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 403 and "No se ha retirado ningún mensaje." in html
    assert total_retirados(app) == 0


def test_sin_sesion_se_pide_iniciar_sesion(app, client):
    """US-10-AC-05 y AC-06."""
    respuesta = client.post(RETIRAR_TEMA)
    assert respuesta.status_code == 302 and "/login" in respuesta.headers["Location"]
    assert "Inicia sesión" in client.get("/login").get_data(as_text=True)
    assert total_retirados(app) == 0


def test_si_falla_al_retirar_se_avisa_y_sigue_visible(app, client, monkeypatch):
    """US-10-AC-06."""
    entrar(client, MODERADOR, "moderador")
    monkeypatch.setattr(gestor_foro, "eliminarMensaje", falla)
    html = client.post(RETIRAR_RESPUESTA, follow_redirects=True).get_data(as_text=True)
    assert "no se ha podido retirar el mensaje" in html and "se ha retirado." not in html
    assert "Respuestas (1)" in html


def test_un_mensaje_que_no_existe_da_404(client):
    entrar(client, MODERADOR, "moderador")
    assert client.post(f"/foro/temas/{MAZOS}/respuestas/999/retirar").status_code == 404


# ---------- Página de cuentas (AC-02, AC-04 y AC-05) ----------

def test_el_admin_ve_las_cuentas_con_su_estado_y_el_boton(app, client):
    crear_cuenta(app, 50)
    crear_cuenta(app, 51, "bloqueada")
    entrar(client, ADMIN, "admin")
    html = client.get(CUENTAS).get_data(as_text=True)
    assert 'href="/admin/usuarios"' in html
    assert "Usuario 50" in html and "Activa" in html and "Bloquear la cuenta de Usuario 50" in html
    assert "Usuario 51" in html and "Bloqueada" in html and "Desbloquear la cuenta de Usuario 51" in html
    assert "data-confirmar=" in html


def test_sin_cuentas_se_indica(client):
    entrar(client, ADMIN, "admin")
    assert "Todavía no hay cuentas de cliente." in client.get(CUENTAS).get_data(as_text=True)


@pytest.mark.parametrize("quien, rol", [(MODERADOR, "moderador"), (None, None)])
def test_moderador_y_cliente_no_entran_en_cuentas(app, client, quien, rol):
    """US-10-AC-05."""
    cliente = crear_cuenta(app, 50)
    entrar(client, quien or cliente, rol or "cliente")
    for respuesta in (client.get(CUENTAS), client.post(f"/admin/usuarios/{cliente}/bloquear")):
        assert respuesta.status_code == 403 and "bloquear o desbloquear cuentas" in respuesta.get_data(as_text=True)
    assert estado(app, cliente) == "activa"
    assert 'href="/admin/usuarios"' not in client.get("/").get_data(as_text=True)


def test_sin_sesion_cuentas_pide_iniciar_sesion(app, client):
    """US-10-AC-06."""
    cliente = crear_cuenta(app, 50)
    for respuesta in (client.get(CUENTAS), client.post(f"/admin/usuarios/{cliente}/bloquear")):
        assert respuesta.status_code == 302 and "/login" in respuesta.headers["Location"]
    assert estado(app, cliente) == "activa"


def test_bloquear_y_desbloquear_desde_la_pagina(app, client):
    """US-10-AC-02 y AC-04."""
    cliente = crear_cuenta(app, 50)
    entrar(client, ADMIN, "admin")
    html = client.post(f"/admin/usuarios/{cliente}/bloquear", follow_redirects=True).get_data(as_text=True)
    assert "Cuenta bloqueada." in html and estado(app, cliente) == "bloqueada"
    html = client.post(f"/admin/usuarios/{cliente}/bloquear", follow_redirects=True).get_data(as_text=True)
    assert "La cuenta ya estaba bloqueada. No se ha cambiado nada." in html
    html = client.post(f"/admin/usuarios/{cliente}/desbloquear", follow_redirects=True).get_data(as_text=True)
    assert "Cuenta desbloqueada." in html and estado(app, cliente) == "activa"
    html = client.post(f"/admin/usuarios/{cliente}/desbloquear", follow_redirects=True).get_data(as_text=True)
    assert "La cuenta ya estaba activa. No se ha cambiado nada." in html


def test_no_se_puede_bloquear_al_moderador(app, client):
    """US-10-AC-02."""
    entrar(client, ADMIN, "admin")
    html = client.post(f"/admin/usuarios/{MODERADOR}/bloquear", follow_redirects=True).get_data(as_text=True)
    assert "Solo se pueden bloquear cuentas de cliente." in html and estado(app, MODERADOR) == "activa"


def test_si_falla_al_bloquear_se_avisa(app, client, monkeypatch):
    """US-10-AC-06."""
    cliente = crear_cuenta(app, 50)
    entrar(client, ADMIN, "admin")

    def falla_cuenta(*args, **kwargs):
        raise gestor_usuario.UsuariosNoDisponibles("fallo")

    monkeypatch.setattr(gestor_usuario, "banearUsuario", falla_cuenta)
    html = client.post(f"/admin/usuarios/{cliente}/bloquear", follow_redirects=True).get_data(as_text=True)
    assert "no se ha podido bloquear la cuenta" in html and "Cuenta bloqueada." not in html
    assert estado(app, cliente) == "activa"


def test_si_falla_la_lista_de_cuentas_se_avisa(client, monkeypatch):
    entrar(client, ADMIN, "admin")

    def falla_cuenta(*args, **kwargs):
        raise gestor_usuario.UsuariosNoDisponibles("fallo")

    monkeypatch.setattr(gestor_usuario, "getClientes", falla_cuenta)
    respuesta = client.get(CUENTAS)
    assert respuesta.status_code == 503 and "no se han podido cargar las cuentas" in respuesta.get_data(as_text=True)


def test_al_bloquear_se_cierra_la_sesion_del_cliente(app):
    """US-10-AC-03: el cliente pierde la sesión en su siguiente petición."""
    cliente = crear_cuenta(app, 50)
    admin, otro = app.test_client(), app.test_client()
    entrar(otro, cliente, "cliente")
    entrar(admin, ADMIN, "admin")
    admin.post(f"/admin/usuarios/{cliente}/bloquear")
    html = otro.get("/foro").get_data(as_text=True)
    assert "Tu cuenta está bloqueada. Se ha cerrado la sesión." in html and "Cerrar sesión" not in html
