"""Pruebas de las pantallas del foro (US-07, GB04-100)."""
import pytest

from app.db import get_db
from app.gestores import gestor_foro

NUEVO = "/foro/nuevo"
VALIDO = {"titulo": "Busco grupo de rol", "cuerpo": "¿Alguien juega los jueves por la tarde?"}


def crear_cuenta(app, id_usuario, estado="activa"):
    with app.app_context():
        get_db().execute(
            "INSERT INTO usuarios (id, email, nombre_usuario, hash_contrasena, rol, estado) "
            "VALUES (?, ?, ?, 'x', 'cliente', ?)",
            (id_usuario, f"usuario{id_usuario}@comarca.test", f"Usuario {id_usuario}", estado))
        get_db().commit()
    return id_usuario


def entrar(client, id_usuario):
    with client.session_transaction() as sesion:
        sesion["usuario_id"] = id_usuario
        sesion["nombre_usuario"] = f"Usuario {id_usuario}"
        sesion["rol"] = "cliente"


def total_temas(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM temas").fetchone()[0]


# ---------- Lista pública (AC-01 y AC-03) ----------

def test_un_visitante_ve_la_lista_pero_no_el_boton_nuevo_tema(client):
    """US-07-AC-01."""
    html = client.get("/foro").get_data(as_text=True)
    assert "<h1>Foro de la comunidad</h1>" in html
    assert "Normas del foro" in html and "Por <strong>Moderación</strong>" in html
    assert "Nuevo tema" not in html and "iniciar sesión" in html


def test_una_cuenta_activa_ve_el_boton_nuevo_tema(app, client):
    """US-07-AC-01."""
    entrar(client, crear_cuenta(app, 50))
    assert 'href="/foro/nuevo"' in client.get("/foro").get_data(as_text=True)


@pytest.mark.parametrize("estado", ["pendiente", "bloqueada"])
def test_una_cuenta_sin_verificar_o_bloqueada_no_ve_el_boton(app, client, estado):
    """US-07-AC-01."""
    entrar(client, crear_cuenta(app, 51, estado))
    assert 'href="/foro/nuevo"' not in client.get("/foro").get_data(as_text=True)


def test_el_foro_vacio_lo_dice(app, client):
    with app.app_context():
        get_db().execute("DELETE FROM temas")
        get_db().commit()
    assert "Todavía no hay temas en el foro." in client.get("/foro").get_data(as_text=True)


def test_si_falla_la_carga_sale_un_error_con_reintentar(client, monkeypatch):
    def falla():
        raise gestor_foro.ForoNoDisponible("fallo")

    monkeypatch.setattr(gestor_foro, "getTemas", falla)
    respuesta = client.get("/foro")
    assert respuesta.status_code == 503
    html = respuesta.get_data(as_text=True)
    assert "no se han podido cargar los temas" in html and "Volver a intentarlo" in html


def test_ver_un_tema_muestra_titulo_autor_fecha_y_mensaje(client):
    html = client.get("/foro/temas/1").get_data(as_text=True)
    assert "<h1>Normas del foro</h1>" in html and "01/11/2026 a las 10:00" in html
    assert "Respetad a los demás" in html


def test_un_tema_que_no_existe_da_404(client):
    assert client.get("/foro/temas/999").status_code == 404


# ---------- Publicar (AC-02, AC-03 y AC-04) ----------

def test_la_cuenta_activa_ve_el_formulario_sin_adjuntos(app, client):
    """US-07-AC-02: solo texto, sin fotos ni archivos."""
    entrar(client, crear_cuenta(app, 52))
    html = client.get(NUEVO).get_data(as_text=True)
    assert '<label for="titulo">' in html and '<label for="cuerpo">' in html
    assert 'type="file"' not in html


def test_publicar_bien_pone_el_tema_el_primero_con_autor_y_fecha(app, client):
    """US-07-AC-03."""
    entrar(client, crear_cuenta(app, 53))
    respuesta = client.post(NUEVO, data=VALIDO)
    assert respuesta.status_code == 302 and respuesta.headers["Location"].endswith("/foro")
    html = client.get("/foro").get_data(as_text=True)
    assert "Tema «Busco grupo de rol» publicado." in html
    assert html.index("Busco grupo de rol") < html.index("Normas del foro")
    assert "Por <strong>Usuario 53</strong>" in html


@pytest.mark.parametrize("datos, mensaje", [
    ({"titulo": "", "cuerpo": "Hola"}, "Escribe el título del tema."),
    ({"titulo": "Hola", "cuerpo": "  "}, "Escribe el mensaje del tema."),
])
def test_si_falta_un_campo_se_indica_y_se_conserva_lo_escrito(app, client, datos, mensaje):
    """US-07-AC-04."""
    entrar(client, crear_cuenta(app, 54))
    antes = total_temas(app)
    respuesta = client.post(NUEVO, data=datos)
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 400 and mensaje in html and 'aria-invalid="true"' in html
    assert "Hola" in html
    assert total_temas(app) == antes


# ---------- Quién no puede publicar (AC-05) ----------

def test_un_visitante_va_a_iniciar_sesion_y_no_se_guarda_nada(app, client):
    """US-07-AC-05."""
    antes = total_temas(app)
    for respuesta in (client.get(NUEVO), client.post(NUEVO, data=VALIDO)):
        assert respuesta.status_code == 302 and "/login" in respuesta.headers["Location"]
    assert total_temas(app) == antes


def test_con_la_sesion_caducada_tambien_va_a_iniciar_sesion(app, client):
    """US-07-AC-05: la cuenta de la sesión ya no existe."""
    entrar(client, 999)
    respuesta = client.post(NUEVO, data=VALIDO)
    assert respuesta.status_code == 302 and "/login" in respuesta.headers["Location"]


def test_una_cuenta_sin_verificar_no_puede_publicar(app, client):
    """US-07-AC-05."""
    entrar(client, crear_cuenta(app, 55, "pendiente"))
    antes = total_temas(app)
    for respuesta in (client.get(NUEVO), client.post(NUEVO, data=VALIDO)):
        assert respuesta.status_code == 403 and "pendiente de verificación" in respuesta.get_data(as_text=True)
    assert total_temas(app) == antes


def test_una_cuenta_bloqueada_no_puede_publicar(app, client):
    """US-07-AC-05 y US-10-AC-03: la sesión de una cuenta bloqueada se cierra y no se guarda nada."""
    bloqueada = crear_cuenta(app, 55, "bloqueada")
    antes = total_temas(app)
    entrar(client, bloqueada)
    respuesta = client.get(NUEVO)
    assert respuesta.status_code == 302 and "/login" in respuesta.headers["Location"]
    entrar(client, bloqueada)
    respuesta = client.post(NUEVO, data=VALIDO)
    assert respuesta.status_code == 302 and "/login" in respuesta.headers["Location"]
    assert total_temas(app) == antes


# ---------- Error al guardar (AC-06) ----------

def test_si_falla_el_guardado_avisa_y_conserva_el_texto(app, client, monkeypatch):
    """US-07-AC-06."""
    entrar(client, crear_cuenta(app, 56))

    def falla(*args, **kwargs):
        raise gestor_foro.ForoNoDisponible("fallo")

    monkeypatch.setattr(gestor_foro, "crearTema", falla)
    respuesta = client.post(NUEVO, data=VALIDO)
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 503
    assert "No se ha podido publicar el tema." in html and "Busco grupo de rol" in html


def test_pulsar_publicar_dos_veces_no_duplica_el_tema(app, client):
    """US-07-AC-06."""
    entrar(client, crear_cuenta(app, 57))
    client.post(NUEVO, data=VALIDO)
    client.post(NUEVO, data=VALIDO)
    assert total_temas(app) == 3


def test_el_texto_se_muestra_sin_ejecutar_html(app, client):
    """El mensaje es solo texto: el HTML que se escriba no se ejecuta."""
    entrar(client, crear_cuenta(app, 58))
    client.post(NUEVO, data={"titulo": "<script>alert(1)</script>", "cuerpo": "<b>hola</b>"})
    html = client.get("/foro/temas/3").get_data(as_text=True)
    assert "<script>alert(1)</script>" not in html and "&lt;b&gt;hola&lt;/b&gt;" in html
