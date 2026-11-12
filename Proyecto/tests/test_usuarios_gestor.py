"""Pruebas de la lógica y los datos del registro de usuario (US-09, GB04-85)."""
import pytest

from app.db import get_db
from app.gestores import gestor_usuario as g


def datos(**cambios):
    base = {"codigo_invitacion": "INV-HOBBIT-001", "email": "frodo@comarca.test",
            "nombre_usuario": "Frodo", "contrasena": "anillo1234", "contrasena2": "anillo1234"}
    base.update(cambios)
    return base


def motivos(app, **cambios):
    with app.app_context(), pytest.raises(g.RegistroInvalido) as error:
        g.crearUsuario(datos(**cambios))
    return " ".join(error.value.motivos)


def test_sin_invitacion_valida_no_se_crea_la_cuenta(app):
    """US-09-AC-01."""
    assert "invitación" in motivos(app, codigo_invitacion="")
    assert "no existe" in motivos(app, codigo_invitacion="INV-FALSA")


def test_las_contrasenas_deben_coincidir_y_tener_8_caracteres(app):
    """US-09-AC-02."""
    assert "8 caracteres" in motivos(app, contrasena="corta", contrasena2="corta")
    assert "no coinciden" in motivos(app, contrasena2="otra12345")


def test_el_email_debe_ser_valido_y_unico(app):
    """US-09-AC-03."""
    assert "formato" in motivos(app, email="no-es-un-email")
    assert "Ya existe" in motivos(app, email="admin@hobbit.test")


def test_un_alta_valida_crea_cuenta_pendiente_con_hash(app):
    """US-09-AC-04 y contraseña con hash, nunca en texto plano."""
    with app.app_context():
        token = g.crearUsuario(datos())
        fila = get_db().execute("SELECT * FROM usuarios WHERE email = 'frodo@comarca.test'").fetchone()
    assert token
    assert fila["estado"] == "pendiente" and fila["rol"] == "cliente"
    assert fila["hash_contrasena"] != "anillo1234"


def test_no_se_puede_entrar_antes_de_verificar(app):
    """US-09-AC-05."""
    with app.app_context():
        g.crearUsuario(datos())
        with pytest.raises(g.AccesoDenegado, match="pendiente"):
            g.iniciarSesion("frodo@comarca.test", "anillo1234")


def test_tras_verificar_la_cuenta_queda_activa_y_puede_entrar(app):
    """US-09-AC-05."""
    with app.app_context():
        token = g.crearUsuario(datos())
        assert g.verificarCuenta(token) is True
        usuario = g.iniciarSesion("Frodo@Comarca.test", "anillo1234")
    assert usuario["rol"] == "cliente"


def test_una_invitacion_solo_activa_una_cuenta(app):
    """US-09-AC-06."""
    with app.app_context():
        g.crearUsuario(datos())
    assert "ya se ha utilizado" in motivos(app, email="sam@comarca.test")
    assert "ya se ha utilizado" in motivos(app, codigo_invitacion="INV-HOBBIT-900")
    assert "revocada" in motivos(app, codigo_invitacion="INV-HOBBIT-999")


def test_el_enlace_de_verificacion_solo_sirve_una_vez(app):
    """US-09-AC-06."""
    with app.app_context():
        token = g.crearUsuario(datos())
        g.verificarCuenta(token)
        with pytest.raises(g.VerificacionInvalida):
            g.verificarCuenta(token)
        with pytest.raises(g.VerificacionInvalida):
            g.verificarCuenta("token-inventado")


def test_contrasena_incorrecta_no_entra(app):
    with app.app_context(), pytest.raises(g.AccesoDenegado, match="no son correctos"):
        g.iniciarSesion("admin@hobbit.test", "otra-cosa")


def test_las_cuentas_iniciales_tienen_su_rol(app):
    with app.app_context():
        assert g.iniciarSesion("admin@hobbit.test", "Admin-Hobbit-2026")["rol"] == "admin"
        assert g.getRolUsuario(2) == "moderador"
        assert g.getRolUsuario(999) is None
