"""Consultas SQL sobre la tabla `eventos`."""
from app.db import get_db
from app.repositories import notificaciones_repo


def listar_publicados_desde(fecha_hora, tipo=None):
    """Eventos publicados a partir de una fecha, del más próximo al más lejano."""
    sql = ("SELECT id, titulo, tipo, fecha_hora, plazas_totales, plazas_disponibles "
           "FROM eventos WHERE publicado = 1 AND fecha_hora >= ?")
    parametros = [fecha_hora]
    if tipo:
        sql += " AND tipo = ?"
        parametros.append(tipo)
    sql += " ORDER BY fecha_hora, titulo COLLATE NOCASE"
    return get_db().execute(sql, parametros).fetchall()


def obtener(id_evento):
    """Un evento publicado por su id, o None si no existe."""
    return get_db().execute(
        "SELECT id, titulo, tipo, fecha_hora, plazas_totales, plazas_disponibles "
        "FROM eventos WHERE id = ? AND publicado = 1",
        (id_evento,),
    ).fetchone()


def esta_inscrito(id_evento, id_usuario):
    return get_db().execute(
        "SELECT 1 FROM inscripciones WHERE evento_id = ? AND usuario_id = ?", (id_evento, id_usuario)
    ).fetchone() is not None


def eventos_de_usuario(id_usuario):
    """Ids de los eventos en los que está inscrito el usuario."""
    filas = get_db().execute(
        "SELECT evento_id FROM inscripciones WHERE usuario_id = ?", (id_usuario,)
    ).fetchall()
    return {fila["evento_id"] for fila in filas}


def inscribir(id_evento, id_usuario, fecha_hora):
    """Reserva una plaza y guarda la inscripción en una sola operación.

    La plaza solo se descuenta si queda alguna, así nunca hay plazas negativas.
    BEGIN IMMEDIATE bloquea la escritura: si llegan dos peticiones a la vez
    por la última plaza, la segunda espera y ya no la encuentra.
    Devuelve True si se ha reservado la plaza y False si el evento está completo.
    Si la cuenta ya estaba inscrita, salta sqlite3.IntegrityError y no se descuenta nada.
    """
    db = get_db()
    if not db.in_transaction:
        db.execute("BEGIN IMMEDIATE")
    try:
        cursor = db.execute(
            "UPDATE eventos SET plazas_disponibles = plazas_disponibles - 1 "
            "WHERE id = ? AND publicado = 1 AND plazas_disponibles > 0",
            (id_evento,),
        )
        if cursor.rowcount == 0:
            db.rollback()
            return False
        db.execute(
            "INSERT INTO inscripciones (evento_id, usuario_id, fecha_hora) VALUES (?, ?, ?)",
            (id_evento, id_usuario, fecha_hora),
        )
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise


def crear(titulo, tipo, fecha_hora, plazas, publicado_en=None):
    """Guarda un evento publicado con todas sus plazas libres y devuelve su id (US-06-AC-02).

    La capacidad inicial es el aforo total. Si se indica `publicado_en`, en la misma operación
    se crea una notificación para cada cuenta Cliente activa (US-11-AC-01).
    Se guarda en una sola operación: si algo falla, no queda nada a medias.
    """
    db = get_db()
    with db:
        cursor = db.execute(
            "INSERT INTO eventos (titulo, tipo, fecha_hora, plazas_totales, plazas_disponibles, publicado) "
            "VALUES (?, ?, ?, ?, ?, 1)",
            (titulo, tipo, fecha_hora, plazas, plazas),
        )
        if publicado_en is not None:
            notificaciones_repo.avisar_evento(cursor.lastrowid, publicado_en)
    return cursor.lastrowid
