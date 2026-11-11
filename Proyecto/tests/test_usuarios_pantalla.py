"""Pruebas de las pantallas de registro, verificación e inicio de sesión (US-09, GB04-86)."""
import re

from app.gestores import gestor_usuario

VALIDO = {"codigo_invitacion": "INV-HOBBIT-002", "email": "sam@comarca.test", "nombre_usuario": "Sam",
          "contrasena": "patatas123", "contrasena2": "patatas123"}


def registrar(client, **cambios):
    return client.post("/registro", data={**VALIDO, **cambios})


def enlace_de(html):
    return re.search(r'href="(/verificar/[^"]+)"', html).group(1)


def test_el_formulario_pide_los_datos(client):
    """US-09-AC-02."""
    html = client.get("/registro").get_data(as_text=True)
    for campo in ["codigo_invitacion", "email", "nombre_usuario", "contrasena", "contrasena2"]:
        assert f'name="{campo}"' in html


def test_los_errores_se_muestran_con_su_motivo(client):
    """US-09-AC-01 a 03: se explica el motivo y no se crea la cuenta."""
    respuesta = registrar(client, codigo_invitacion="INV-FALSA", contrasena2="otra-cosa")
    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 400
    assert "No se ha creado la cuenta" in html
    assert "no existe" in html and "no coinciden" in html
    assert "patatas123" not in html


def test_alta_valida_muestra_el_correo_simulado(client):
    """US-09-AC-04."""
    html = registrar(client).get_data(as_text=True)
    assert "correo de confirmación" in html
    assert "no se envía ningún correo real" in html
    assert "/verificar/" in html


def test_no_se_puede_entrar_sin_verificar_y_si_despues(client):
    """US-09-AC-05."""
    enlace = enlace_de(registrar(client).get_data(as_text=True))
    antes = client.post("/login", data={"email": "sam@comarca.test", "contrasena": "patatas123"})
    assert "pendiente de verificación" in antes.get_data(as_text=True)

    assert "Tu cuenta está activa" in client.get(enlace).get_data(as_text=True)
    despues = client.post("/login", data={"email": "sam@comarca.test", "contrasena": "patatas123"}, follow_redirects=True)
    assert "Has iniciado sesión" in despues.get_data(as_text=True)


def test_el_enlace_solo_sirve_una_vez(client):
    """US-09-AC-06."""
    enlace = enlace_de(registrar(client).get_data(as_text=True))
    client.get(enlace)
    respuesta = client.get(enlace)
    assert respuesta.status_code == 400
    assert "ya se ha utilizado" in respuesta.get_data(as_text=True)


def test_invitacion_usada_o_revocada(client):
    """US-09-AC-06."""
    assert "ya se ha utilizado" in registrar(client, codigo_invitacion="INV-HOBBIT-900").get_data(as_text=True)
    assert "revocada" in registrar(client, codigo_invitacion="INV-HOBBIT-999").get_data(as_text=True)


def test_cerrar_sesion(client):
    client.post("/login", data={"email": "admin@hobbit.test", "contrasena": "Admin-Hobbit-2026"})
    html = client.get("/logout", follow_redirects=True).get_data(as_text=True)
    assert "Has cerrado la sesión" in html


def test_si_falla_el_guardado_se_informa(client, monkeypatch):
    def falla(datos):
        raise gestor_usuario.UsuariosNoDisponibles("fallo")

    monkeypatch.setattr(gestor_usuario, "crearUsuario", falla)
    respuesta = registrar(client)
    assert respuesta.status_code == 503
    assert "No se ha podido completar el registro" in respuesta.get_data(as_text=True)


def test_el_menu_muestra_quien_ha_iniciado_sesion(client):
    """Tras iniciar sesión, el menú muestra el nombre y la opción de cerrar sesión."""
    antes = client.get("/").get_data(as_text=True)
    assert "Iniciar sesión" in antes and "Cerrar sesión" not in antes
    client.post("/login", data={"email": "admin@hobbit.test", "contrasena": "Admin-Hobbit-2026"})
    despues = client.get("/eventos").get_data(as_text=True)
    assert "Hola, Administración" in despues and "Cerrar sesión" in despues
    assert "Iniciar sesión" not in despues
