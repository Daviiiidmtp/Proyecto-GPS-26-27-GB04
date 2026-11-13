"""Pruebas de la lógica y los datos de la inscripción en eventos (US-05, GB04-92)."""
import sqlite3
import threading
from datetime import datetime

import pytest

from app.db import get_db
from app.gestores import gestor_evento
from app.repositories import eventos_repo

HOY = datetime(2026, 11, 11, 10, 0)
TORNEO = 1      # 12 de 32 plazas libres
COMPLETO = 3    # 0 plazas
PASADO = 7      # ya celebrado
OCULTO = 8      # no publicado
ADMIN = 1


def crear_cuenta(app, id_usuario, estado="activa"):
    with app.app_context():
        get_db().execute(
            "INSERT INTO usuarios (id, email, nombre_usuario, hash_contrasena, rol, estado) "
            "VALUES (?, ?, ?, 'x', 'cliente', ?)",
            (id_usuario, f"usuario{id_usuario}@comarca.test", f"Usuario {id_usuario}", estado))
        get_db().commit()
    return id_usuario


def inscribir(app, id_evento, id_usuario):
    with app.app_context():
        return gestor_evento.apuntarmeEnEvento(id_evento, id_usuario, ahora=HOY)


def motivo(app, id_evento, id_usuario):
    with pytest.raises(gestor_evento.InscripcionDenegada) as error:
        inscribir(app, id_evento, id_usuario)
    return error.value.motivo


def plazas(app, id_evento):
    with app.app_context():
        return get_db().execute("SELECT plazas_disponibles FROM eventos WHERE id = ?", (id_evento,)).fetchone()[0]


def inscripciones(app, id_evento):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM inscripciones WHERE evento_id = ?", (id_evento,)).fetchone()[0]


def test_una_inscripcion_confirmada_resta_una_plaza(app):
    """US-05-AC-03."""
    assert inscribir(app, TORNEO, ADMIN) is True
    assert plazas(app, TORNEO) == 11
    assert inscripciones(app, TORNEO) == 1


def test_sin_sesion_no_se_puede_inscribir(app):
    """US-05-AC-01."""
    assert motivo(app, TORNEO, None) == "sin_sesion"
    assert motivo(app, TORNEO, 999) == "sin_sesion"
    assert plazas(app, TORNEO) == 12


@pytest.mark.parametrize("estado", ["pendiente", "bloqueada"])
def test_una_cuenta_sin_verificar_o_bloqueada_no_se_puede_inscribir(app, estado):
    """US-05-AC-01: se indica el motivo y no se consume plaza."""
    usuario = crear_cuenta(app, 50, estado)
    assert motivo(app, TORNEO, usuario) == estado
    assert plazas(app, TORNEO) == 12


def test_el_mensaje_explica_como_continuar(app):
    """US-05-AC-01."""
    with app.app_context(), pytest.raises(gestor_evento.InscripcionDenegada) as error:
        gestor_evento.apuntarmeEnEvento(TORNEO, None, ahora=HOY)
    assert "Inicia sesión" in str(error.value)


def test_no_se_puede_inscribir_dos_veces(app):
    """US-05-AC-04: la segunda vez avisa y no consume otra plaza."""
    inscribir(app, TORNEO, ADMIN)
    assert motivo(app, TORNEO, ADMIN) == "ya_inscrito"
    assert plazas(app, TORNEO) == 11
    assert inscripciones(app, TORNEO) == 1


def test_evento_completo_o_pasado_no_admite_inscripciones(app):
    """US-05-AC-06."""
    assert motivo(app, COMPLETO, ADMIN) == "completo"
    assert motivo(app, PASADO, ADMIN) == "pasado"
    assert plazas(app, COMPLETO) == 0


def test_evento_que_no_existe_o_no_publicado(app):
    assert motivo(app, 12345, ADMIN) == "no_existe"
    assert motivo(app, OCULTO, ADMIN) == "no_existe"


def test_con_la_ultima_plaza_solo_entra_una_de_varias_peticiones_a_la_vez(app):
    """US-05-AC-05: solo se confirma una, las demás reciben aforo completo y nunca hay plazas negativas."""
    with app.app_context():
        get_db().execute("UPDATE eventos SET plazas_disponibles = 1 WHERE id = ?", (TORNEO,))
        get_db().commit()
    usuarios = [crear_cuenta(app, 60 + n) for n in range(6)]
    resultados = []
    salida = threading.Barrier(len(usuarios))

    def pedir(id_usuario):
        with app.app_context():
            salida.wait()
            try:
                resultados.append(gestor_evento.apuntarmeEnEvento(TORNEO, id_usuario, ahora=HOY))
            except gestor_evento.InscripcionDenegada as error:
                resultados.append(error.motivo)

    hilos = [threading.Thread(target=pedir, args=(u,)) for u in usuarios]
    for hilo in hilos:
        hilo.start()
    for hilo in hilos:
        hilo.join()

    assert resultados.count(True) == 1
    assert resultados.count("completo") == len(usuarios) - 1
    assert plazas(app, TORNEO) == 0
    assert inscripciones(app, TORNEO) == 1


def test_si_falla_la_base_de_datos_no_se_confirma_ninguna_plaza(app, monkeypatch):
    """US-05-AC-07: se avisa del error y se puede volver a intentar."""
    def falla(*args):
        raise sqlite3.OperationalError("base de datos no disponible")

    monkeypatch.setattr(eventos_repo, "inscribir", falla)
    with app.app_context(), pytest.raises(gestor_evento.EventosNoDisponibles):
        gestor_evento.apuntarmeEnEvento(TORNEO, ADMIN, ahora=HOY)
    assert plazas(app, TORNEO) == 12
    monkeypatch.undo()
    assert inscribir(app, TORNEO, ADMIN) is True


def test_si_falla_al_guardar_la_inscripcion_se_devuelve_la_plaza(app):
    """La plaza y la inscripción se guardan juntas: si falla una, no se guarda ninguna."""
    with app.app_context():
        get_db().execute("DROP TABLE inscripciones")
        get_db().commit()
        with pytest.raises(gestor_evento.EventosNoDisponibles):
            gestor_evento.apuntarmeEnEvento(TORNEO, ADMIN, ahora=HOY)
    assert plazas(app, TORNEO) == 12


def test_getEventosInscritos_devuelve_los_eventos_del_usuario(app):
    """Lo usa la interfaz para mostrar «Inscrito» (US-05-AC-02)."""
    inscribir(app, TORNEO, ADMIN)
    inscribir(app, 2, ADMIN)
    with app.app_context():
        assert gestor_evento.getEventosInscritos(ADMIN) == {TORNEO, 2}
        assert gestor_evento.getEventosInscritos(None) == set()
