"""Pruebas de la pantalla de añadir evento (US-06, GB04-114)."""
import pytest

from app.db import get_db
from app.gestores import gestor_evento

NUEVO = "/admin/eventos/nuevo"
VALIDO = {"titulo": "Torneo de Navidad", "tipo": "torneo", "fecha": "2030-12-20", "hora": "17:30", "capacidad": "24"}


def entrar(client, id_usuario=1, rol="admin"):
    with client.session_transaction() as sesion:
        sesion["usuario_id"] = id_usuario
        sesion["nombre_usuario"] = "Administración" if rol == "admin" else "Moderación"
        sesion["rol"] = rol


def total_eventos(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM eventos").fetchone()[0]


def con(**cambios):
    return {**VALIDO, **cambios}


# ---------- Formulario y menú (AC-01) ----------

def test_el_administrador_ve_el_formulario_con_todos_los_campos(client):
    """US-06-AC-01."""
    entrar(client)
    html = client.get(NUEVO).get_data(as_text=True)
    for campo in ["titulo", "tipo", "fecha", "hora", "capacidad"]:
        assert f'<label for="{campo}">' in html
    assert 'type="date"' in html and 'type="time"' in html and "Publicar evento" in html


def test_solo_el_administrador_ve_el_enlace_del_menu(client):
    assert 'href="/admin/eventos/nuevo"' not in client.get("/eventos").get_data(as_text=True)
    entrar(client)
    assert 'href="/admin/eventos/nuevo"' in client.get("/eventos").get_data(as_text=True)


# ---------- Publicar (AC-02) ----------

def test_publicar_bien_lleva_al_calendario_con_el_evento_y_sus_plazas(app, client):
    """US-06-AC-02."""
    entrar(client)
    respuesta = client.post(NUEVO, data=VALIDO)
    assert respuesta.status_code == 302 and respuesta.headers["Location"].endswith("/eventos")
    html = client.get("/eventos").get_data(as_text=True)
    assert "Evento «Torneo de Navidad» publicado en el calendario con 24 plazas libres." in html
    assert "Torneo de Navidad" in html and "20/12/2030" in html
    with app.app_context():
        fila = get_db().execute("SELECT plazas_totales, plazas_disponibles FROM eventos WHERE titulo = 'Torneo de Navidad'").fetchone()
    assert tuple(fila) == (24, 24)


# ---------- Datos que hay que corregir (AC-03) ----------

@pytest.mark.parametrize("datos, mensaje", [
    (con(titulo=""), "Escribe el título del evento."),
    (con(fecha="2020-01-01"), "La fecha y la hora del evento deben ser futuras."),
    (con(capacidad="0"), "La capacidad debe ser un número entero mayor que 0."),
    (con(capacidad="2,5"), "La capacidad debe ser un número entero mayor que 0."),
])
def test_un_dato_incorrecto_se_indica_y_no_se_publica(app, client, datos, mensaje):
    """US-06-AC-03."""
    entrar(client)
    antes = total_eventos(app)
    respuesta = client.post(NUEVO, data=datos)
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 400
    assert "No se ha publicado el evento." in html and mensaje in html and 'aria-invalid="true"' in html
    assert total_eventos(app) == antes


def test_tras_un_error_se_conservan_los_datos_escritos(client):
    """US-06-AC-03."""
    entrar(client)
    html = client.post(NUEVO, data=con(capacidad="0")).get_data(as_text=True)
    assert 'value="Torneo de Navidad"' in html and 'value="2030-12-20"' in html and 'value="17:30"' in html
    assert '<option value="torneo" selected>' in html


# ---------- Quién no puede crear eventos (AC-04) ----------

def test_un_visitante_va_a_iniciar_sesion_y_no_se_guarda_nada(app, client):
    """US-06-AC-04."""
    antes = total_eventos(app)
    for respuesta in (client.get(NUEVO), client.post(NUEVO, data=VALIDO)):
        assert respuesta.status_code == 302 and "/login" in respuesta.headers["Location"]
    assert "Necesitas una sesión de administrador para crear eventos." in client.get("/login").get_data(as_text=True)
    assert total_eventos(app) == antes


@pytest.mark.parametrize("rol", ["moderador", "cliente"])
def test_un_moderador_o_un_cliente_no_pueden_crear_eventos(app, client, rol):
    """US-06-AC-04."""
    entrar(client, 2, rol)
    antes = total_eventos(app)
    for respuesta in (client.get(NUEVO), client.post(NUEVO, data=VALIDO)):
        html = respuesta.get_data(as_text=True)
        assert respuesta.status_code == 403 and "Solo un administrador de la tienda puede crear eventos." in html
    assert total_eventos(app) == antes


def test_con_la_sesion_caducada_va_a_iniciar_sesion_al_guardar(app, client):
    """US-06-AC-04: la sesión dice admin pero la cuenta ya no existe. El gestor lo comprueba al guardar."""
    entrar(client, 999)
    antes = total_eventos(app)
    respuesta = client.post(NUEVO, data=VALIDO)
    assert respuesta.status_code == 302 and "/login" in respuesta.headers["Location"]
    assert total_eventos(app) == antes


# ---------- Error al guardar (AC-05) ----------

def test_si_falla_el_guardado_avisa_y_conserva_los_datos(client, monkeypatch):
    """US-06-AC-05."""
    entrar(client)

    def falla(*args, **kwargs):
        raise gestor_evento.EventosNoDisponibles("fallo")

    monkeypatch.setattr(gestor_evento, "crearEvento", falla)
    respuesta = client.post(NUEVO, data=VALIDO)
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 503
    assert "No se ha podido guardar el evento. Vuelve a intentarlo." in html and 'value="Torneo de Navidad"' in html
