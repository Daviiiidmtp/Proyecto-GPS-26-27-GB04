"""Pruebas de la pantalla para responder en el foro (US-08, GB04-112)."""
import pytest

from app.db import get_db
from app.gestores import gestor_foro

MAZOS = 2
TEMA = f"/foro/temas/{MAZOS}"
RESPONDER = f"/foro/temas/{MAZOS}/responder"


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


def total_respuestas(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM respuestas").fetchone()[0]


# ---------- Respuestas públicas (AC-01) ----------

def test_un_visitante_ve_las_respuestas_pero_no_el_formulario(client):
    """US-08-AC-01."""
    html = client.get(TEMA).get_data(as_text=True)
    assert "Respuestas (1)" in html and "El de bosque aguanta mejor" in html
    assert "Por <strong>Administración</strong>" in html and "09/11/2026 a las 11:15" in html
    assert 'name="cuerpo"' not in html and "iniciar sesión" in html


def test_un_tema_sin_respuestas_lo_dice(client):
    assert "Todavía no hay respuestas." in client.get("/foro/temas/1").get_data(as_text=True)


def test_una_cuenta_activa_ve_el_formulario_sin_adjuntos(app, client):
    """US-08-AC-01: solo texto."""
    entrar(client, crear_cuenta(app, 50))
    html = client.get(TEMA).get_data(as_text=True)
    assert '<label for="cuerpo">Tu respuesta</label>' in html and 'type="file"' not in html


@pytest.mark.parametrize("estado", ["pendiente", "bloqueada"])
def test_una_cuenta_sin_verificar_o_bloqueada_no_ve_el_formulario(app, client, estado):
    """US-08-AC-01."""
    entrar(client, crear_cuenta(app, 51, estado))
    html = client.get(TEMA).get_data(as_text=True)
    assert 'name="cuerpo"' not in html and "Tu cuenta no puede responder" in html


# ---------- Publicar (AC-02 y AC-03) ----------

def test_responder_bien_pone_la_respuesta_al_final_con_autor_y_fecha(app, client):
    """US-08-AC-03."""
    entrar(client, crear_cuenta(app, 52))
    respuesta = client.post(RESPONDER, data={"cuerpo": "Yo uso el de niebla."})
    assert respuesta.status_code == 302 and "/foro/temas/2#respuesta-" in respuesta.headers["Location"]
    html = client.get(TEMA).get_data(as_text=True)
    assert "Respuesta publicada." in html and "Respuestas (2)" in html
    assert html.index("El de bosque aguanta mejor") < html.index("Yo uso el de niebla.")
    assert "Por <strong>Usuario 52</strong>" in html


def test_una_respuesta_vacia_se_indica_y_no_se_publica(app, client):
    """US-08-AC-02."""
    entrar(client, crear_cuenta(app, 53))
    antes = total_respuestas(app)
    respuesta = client.post(RESPONDER, data={"cuerpo": "   "})
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 400
    assert "Escribe el texto de la respuesta." in html and 'aria-invalid="true"' in html
    assert total_respuestas(app) == antes


# ---------- Tema que no existe (AC-04) ----------

def test_responder_en_un_tema_que_no_existe_lo_dice(app, client):
    """US-08-AC-04."""
    entrar(client, crear_cuenta(app, 54))
    respuesta = client.post("/foro/temas/999/responder", data={"cuerpo": "Hola"})
    assert respuesta.status_code == 404
    assert "Este tema ya no está disponible." in respuesta.get_data(as_text=True)
    assert total_respuestas(app) == 1


# ---------- Quién no puede responder (AC-05) ----------

def test_un_visitante_va_a_iniciar_sesion_y_no_se_guarda_nada(app, client):
    """US-08-AC-05."""
    respuesta = client.post(RESPONDER, data={"cuerpo": "Hola"})
    assert respuesta.status_code == 302 and "/login" in respuesta.headers["Location"]
    assert total_respuestas(app) == 1


def test_con_la_sesion_caducada_tambien_va_a_iniciar_sesion(client):
    """US-08-AC-05."""
    entrar(client, 999)
    respuesta = client.post(RESPONDER, data={"cuerpo": "Hola"})
    assert respuesta.status_code == 302 and "/login" in respuesta.headers["Location"]


@pytest.mark.parametrize("estado, texto", [("pendiente", "pendiente de verificación"), ("bloqueada", "está bloqueada")])
def test_una_cuenta_sin_verificar_o_bloqueada_no_puede_responder(app, client, estado, texto):
    """US-08-AC-05."""
    entrar(client, crear_cuenta(app, 55, estado))
    respuesta = client.post(RESPONDER, data={"cuerpo": "Hola"})
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 403 and texto in html and "No se ha guardado ninguna respuesta." in html
    assert total_respuestas(app) == 1


# ---------- Error al guardar (AC-05) ----------

def test_si_falla_el_guardado_avisa_y_conserva_el_texto(app, client, monkeypatch):
    """US-08-AC-05."""
    entrar(client, crear_cuenta(app, 56))

    def falla(*args, **kwargs):
        raise gestor_foro.ForoNoDisponible("fallo")

    monkeypatch.setattr(gestor_foro, "anadirComentario", falla)
    respuesta = client.post(RESPONDER, data={"cuerpo": "Yo uso el de niebla."})
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 503
    assert "No se ha podido publicar la respuesta." in html and "Yo uso el de niebla." in html


def test_pulsar_responder_dos_veces_no_duplica_la_respuesta(app, client):
    """US-08-AC-05."""
    entrar(client, crear_cuenta(app, 57))
    client.post(RESPONDER, data={"cuerpo": "Yo uso el de niebla."})
    client.post(RESPONDER, data={"cuerpo": "Yo uso el de niebla."})
    assert total_respuestas(app) == 2


def test_el_texto_se_muestra_sin_ejecutar_html(app, client):
    entrar(client, crear_cuenta(app, 58))
    client.post(RESPONDER, data={"cuerpo": "<script>alert(1)</script>"})
    html = client.get(TEMA).get_data(as_text=True)
    assert "<script>alert(1)</script>" not in html and "&lt;script&gt;" in html
