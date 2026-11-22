"""Consultas SQL sobre la tabla `temas` del foro."""
from app.db import get_db

COLUMNAS = ("SELECT t.id, t.titulo, t.cuerpo, t.usuario_id, t.fecha_hora, u.nombre_usuario AS autor "
            "FROM temas t JOIN usuarios u ON u.id = t.usuario_id")

# US-10: los mensajes retirados por moderación no se muestran a nadie
TEMA_VISIBLE = ("NOT EXISTS (SELECT 1 FROM mensajes_retirados m "
                "WHERE m.tipo = 'tema' AND m.mensaje_id = t.id)")
RESPUESTA_VISIBLE = ("NOT EXISTS (SELECT 1 FROM mensajes_retirados m "
                     "WHERE m.tipo = 'respuesta' AND m.mensaje_id = r.id)")


def listar_temas():
    """Todos los temas no retirados, del más reciente al más antiguo."""
    return get_db().execute(COLUMNAS + " WHERE " + TEMA_VISIBLE + " ORDER BY t.fecha_hora DESC, t.id DESC").fetchall()


def obtener_tema(id_tema):
    """Un tema no retirado por su id, o None si no existe o está retirado."""
    return get_db().execute(COLUMNAS + " WHERE t.id = ? AND " + TEMA_VISIBLE, (id_tema,)).fetchone()


def buscar_igual_reciente(usuario_id, titulo, cuerpo, desde):
    """Id de un tema idéntico del mismo autor publicado a partir de `desde`, o None.

    Sirve para no guardar dos veces el mismo tema si se pulsa «Publicar» de nuevo.
    """
    fila = get_db().execute(
        "SELECT t.id FROM temas t WHERE t.usuario_id = ? AND t.titulo = ? AND t.cuerpo = ? AND t.fecha_hora >= ? "
        "AND " + TEMA_VISIBLE + " ORDER BY t.id DESC LIMIT 1",
        (usuario_id, titulo, cuerpo, desde),
    ).fetchone()
    return fila["id"] if fila else None


def crear_tema(titulo, cuerpo, usuario_id, fecha_hora):
    """Guarda un tema y devuelve su id, que asigna la base de datos.

    Se guarda en una sola operación: si algo falla, no queda nada a medias.
    """
    db = get_db()
    with db:
        cursor = db.execute(
            "INSERT INTO temas (titulo, cuerpo, usuario_id, fecha_hora) VALUES (?, ?, ?, ?)",
            (titulo, cuerpo, usuario_id, fecha_hora),
        )
    return cursor.lastrowid


# ---------- Respuestas (US-08) ----------

def listar_respuestas(id_tema):
    """Respuestas no retiradas de un tema, de la más antigua a la más reciente, con el nombre del autor."""
    return get_db().execute(
        "SELECT r.id, r.cuerpo, r.usuario_id, r.fecha_hora, u.nombre_usuario AS autor "
        "FROM respuestas r JOIN usuarios u ON u.id = r.usuario_id "
        "WHERE r.tema_id = ? AND " + RESPUESTA_VISIBLE + " ORDER BY r.fecha_hora, r.id",
        (id_tema,),
    ).fetchall()


def buscar_respuesta_igual_reciente(id_tema, usuario_id, cuerpo, desde):
    """Id de una respuesta idéntica del mismo autor en el mismo tema publicada a partir de `desde`, o None.

    Sirve para no guardar dos veces la misma respuesta si se pulsa «Responder» de nuevo.
    """
    fila = get_db().execute(
        "SELECT r.id FROM respuestas r WHERE r.tema_id = ? AND r.usuario_id = ? AND r.cuerpo = ? "
        "AND r.fecha_hora >= ? AND " + RESPUESTA_VISIBLE + " ORDER BY r.id DESC LIMIT 1",
        (id_tema, usuario_id, cuerpo, desde),
    ).fetchone()
    return fila["id"] if fila else None


def crear_respuesta(id_tema, cuerpo, usuario_id, fecha_hora):
    """Guarda una respuesta y devuelve su id, que asigna la base de datos.

    Se guarda en una sola operación: si algo falla, no queda nada a medias.
    """
    db = get_db()
    with db:
        cursor = db.execute(
            "INSERT INTO respuestas (tema_id, cuerpo, usuario_id, fecha_hora) VALUES (?, ?, ?, ?)",
            (id_tema, cuerpo, usuario_id, fecha_hora),
        )
    return cursor.lastrowid


# ---------- Moderación (US-10) ----------

TABLAS = {"tema": "temas", "respuesta": "respuestas"}


def existe_mensaje(tipo, id_mensaje):
    """True si el tema o la respuesta existe, aunque esté retirado."""
    return get_db().execute(
        f"SELECT 1 FROM {TABLAS[tipo]} WHERE id = ?", (id_mensaje,)
    ).fetchone() is not None


def esta_retirado(tipo, id_mensaje):
    return get_db().execute(
        "SELECT 1 FROM mensajes_retirados WHERE tipo = ? AND mensaje_id = ?", (tipo, id_mensaje)
    ).fetchone() is not None


def retirar(tipo, id_mensaje, usuario_id, fecha_hora):
    """Apunta el mensaje como retirado. Devuelve True si se ha retirado ahora y False si ya lo estaba.

    INSERT OR IGNORE con UNIQUE (tipo, mensaje_id): si dos moderadores lo retiran a la vez,
    solo cuenta la primera vez y no se duplica nada (US-10-AC-07).
    """
    db = get_db()
    with db:
        cursor = db.execute(
            "INSERT OR IGNORE INTO mensajes_retirados (tipo, mensaje_id, usuario_id, fecha_hora) VALUES (?, ?, ?, ?)",
            (tipo, id_mensaje, usuario_id, fecha_hora),
        )
    return cursor.rowcount == 1
