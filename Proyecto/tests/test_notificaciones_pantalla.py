"""Pruebas de la pantalla de notificaciones y de la ficha del evento (US-11, GB04-121)."""
from datetime import datetime

from app.db import get_db
from app.gestores import gestor_evento, gestor_notificacion

ADMIN = 1
EVENTO = {"titulo": "Torneo de Navidad", "tipo": "torneo", "fecha": "2099-12-20", "hora": "17:30", "capacidad": "24"}


def crear_cuenta(app, id_usuario, estado="activa"):
    with app.app_context():
        get_db().execute(
            "INSERT INTO usuarios (id, email, nombre_usuario, hash_contrasena, rol, estado) VALUES (?, ?, ?, 'x', 'cliente', ?)",
            (id_usuario, f"usuario{id_usuario}@comarca.test", f"Usuario {id_usuario}", estado))
        get_db().commit()
    return id_usuario


def entrar(client, id_usuario):
    with client.session_transaction() as sesion:
        sesion["usuario_id"] = id_usuario
        sesion["nombre_usuario"] = f"Usuario {id_usuario}"
        sesion["rol"] = "cliente"


def publicar(app, **cambios):
    with app.app_context():
        return gestor_evento.crearEvento({**EVENTO, **cambios}, ADMIN, ahora=datetime(2026, 11, 21, 10, 0))


def id_aviso(app, id_usuario):
    with app.app_context():
        return gestor_notificacion.getNotificaciones(id_usuario)[0]["id"]


# ---------- Campana (AC-02 y AC-07) ----------

def test_la_campana_muestra_el_numero_sin_leer(app, client):
    """US-11-AC-02."""
    entrar(client, crear_cuenta(app, 50))
    publicar(app)
    publicar(app, titulo="Partida de rol")
    html = client.get("/").get_data(as_text=True)
    assert 'href="/notificaciones"' in html and "Notificaciones (2)" in html


def test_sin_sesion_no_hay_campana(client):
    """US-11-AC-07."""
    assert 'href="/notificaciones"' not in client.get("/").get_data(as_text=True)


def test_si_falla_el_contador_la_campana_sale_sin_numero(app, client, monkeypatch):
    entrar(client, crear_cuenta(app, 50))

    def falla(*args, **kwargs):
        raise gestor_notificacion.NotificacionesNoDisponibles("fallo")

    monkeypatch.setattr(gestor_notificacion, "contarNoLeidas", falla)
    html = client.get("/").get_data(as_text=True)
    assert 'href="/notificaciones"' in html and "Notificaciones (" not in html


# ---------- Lista (AC-02, AC-04, AC-06 y AC-07) ----------

def test_la_lista_muestra_titulo_y_fecha(app, client):
    """US-11-AC-02."""
    entrar(client, crear_cuenta(app, 50))
    publicar(app)
    html = client.get("/notificaciones").get_data(as_text=True)
    assert "Torneo de Navidad" in html and "Sin leer" in html
    assert "Publicado el 21/11/2026 a las 10:00" in html and "20/12/2099 a las 17:30" in html


def test_sin_notificaciones_se_indica(app, client):
    """US-11-AC-04."""
    entrar(client, crear_cuenta(app, 50))
    html = client.get("/notificaciones").get_data(as_text=True)
    assert "No tienes notificaciones sin leer." in html


def test_sin_sesion_se_pide_iniciar_sesion(client):
    """US-11-AC-07."""
    respuesta = client.get("/notificaciones")
    assert respuesta.status_code == 302 and "/login" in respuesta.headers["Location"]
    html = client.get("/login").get_data(as_text=True)
    assert "Inicia sesión para ver tus notificaciones." in html


def test_si_falla_la_carga_se_muestra_un_error_con_reintento(app, client, monkeypatch):
    """US-11-AC-06."""
    entrar(client, crear_cuenta(app, 50))

    def falla(*args, **kwargs):
        raise gestor_notificacion.NotificacionesNoDisponibles("fallo")

    monkeypatch.setattr(gestor_notificacion, "getNotificaciones", falla)
    respuesta = client.get("/notificaciones")
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 503
    assert "no se han podido cargar tus notificaciones" in html and "Volver a intentarlo" in html
    assert "No tienes notificaciones sin leer" not in html


# ---------- Abrir (AC-03, AC-04 y AC-06) ----------

def test_abrir_lleva_a_la_ficha_y_la_marca_como_leida(app, client):
    """US-11-AC-03 y AC-04."""
    cliente = crear_cuenta(app, 50)
    entrar(client, cliente)
    id_evento = publicar(app)
    respuesta = client.post(f"/notificaciones/{id_aviso(app, cliente)}/abrir")
    assert respuesta.status_code == 302 and respuesta.headers["Location"].endswith(f"/eventos/{id_evento}")
    html = client.get(f"/eventos/{id_evento}").get_data(as_text=True)
    assert "Torneo de Navidad" in html and "Notificaciones (0)" in html
    assert "No tienes notificaciones sin leer." in client.get("/notificaciones").get_data(as_text=True)


def test_no_se_abre_la_notificacion_de_otra_cuenta(app, client):
    ana, bea = crear_cuenta(app, 50), crear_cuenta(app, 51)
    publicar(app)
    entrar(client, bea)
    assert client.post(f"/notificaciones/{id_aviso(app, ana)}/abrir").status_code == 404


def test_si_falla_al_abrir_sigue_sin_leer(app, client, monkeypatch):
    """US-11-AC-06."""
    cliente = crear_cuenta(app, 50)
    entrar(client, cliente)
    publicar(app)
    aviso = id_aviso(app, cliente)

    def falla(*args, **kwargs):
        raise gestor_notificacion.NotificacionesNoDisponibles("fallo")

    monkeypatch.setattr(gestor_notificacion, "abrirNotificacion", falla)
    html = client.post(f"/notificaciones/{aviso}/abrir", follow_redirects=True).get_data(as_text=True)
    assert "No se ha podido abrir la notificación. Sigue sin leer" in html and "Torneo de Navidad" in html


def test_abrir_sin_sesion_pide_iniciar_sesion(client):
    """US-11-AC-07."""
    respuesta = client.post("/notificaciones/1/abrir")
    assert respuesta.status_code == 302 and "/login" in respuesta.headers["Location"]


# ---------- Ficha del evento (AC-03 y AC-05) ----------

def test_la_ficha_permite_inscribirse_y_vuelve_a_la_ficha(app, client):
    """US-11-AC-03."""
    cliente = crear_cuenta(app, 50)
    entrar(client, cliente)
    id_evento = publicar(app)
    html = client.get(f"/eventos/{id_evento}").get_data(as_text=True)
    assert "Inscribirse" in html and "24 de 24 libres" in html
    respuesta = client.post(f"/eventos/{id_evento}/inscribirse", data={"volver": "ficha"})
    assert respuesta.headers["Location"].endswith(f"/eventos/{id_evento}")
    html = client.get(f"/eventos/{id_evento}").get_data(as_text=True)
    assert "Inscripción confirmada" in html and "Inscrito" in html and "23 de 24 libres" in html


def test_la_ficha_de_un_evento_completo_no_deja_inscribirse(app, client):
    """US-11-AC-05."""
    id_evento = publicar(app, capacidad="1")
    otro = crear_cuenta(app, 51)
    with app.app_context():
        gestor_evento.apuntarmeEnEvento(id_evento, otro)
    entrar(client, crear_cuenta(app, 50))
    html = client.get(f"/eventos/{id_evento}").get_data(as_text=True)
    assert "Este evento está completo" in html and "boton-inscribirse" not in html


def test_la_ficha_de_un_evento_pasado_sigue_disponible(app, client):
    """US-11-AC-05: los eventos de ejemplo ya celebrados se pueden abrir."""
    with app.app_context():
        get_db().execute("UPDATE eventos SET fecha_hora = '2020-01-01 18:00' WHERE id = 1")
        get_db().commit()
    entrar(client, crear_cuenta(app, 50))
    html = client.get("/eventos/1").get_data(as_text=True)
    assert "Ya celebrado" in html and "ya se ha celebrado" in html and "boton-inscribirse" not in html


def test_la_ficha_sin_sesion_pide_iniciar_sesion_para_inscribirse(app, client):
    id_evento = publicar(app)
    html = client.get(f"/eventos/{id_evento}").get_data(as_text=True)
    assert "iniciar sesión" in html and "boton-inscribirse" not in html


def test_un_evento_que_no_existe_da_404(client):
    assert client.get("/eventos/999").status_code == 404
