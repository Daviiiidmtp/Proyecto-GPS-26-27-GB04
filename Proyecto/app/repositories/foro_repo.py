"""Consultas SQL sobre la tabla `temas` del foro."""
from app.db import get_db

COLUMNAS = ("SELECT t.id, t.titulo, t.cuerpo, t.usuario_id, t.fecha_hora, u.nombre_usuario AS autor "
            "FROM temas t JOIN usuarios u ON u.id = t.usuario_id")


def listar_temas():
    """Todos los temas, del más reciente al más antiguo."""
    return get_db().execute(COLUMNAS + " ORDER BY t.fecha_hora DESC, t.id DESC").fetchall()


def obtener_tema(id_tema):
    """Un tema por su id, o None si no existe."""
    return get_db().execute(COLUMNAS + " WHERE t.id = ?", (id_tema,)).fetchone()


def buscar_igual_reciente(usuario_id, titulo, cuerpo, desde):
    """Id de un tema idéntico del mismo autor publicado a partir de `desde`, o None.

    Sirve para no guardar dos veces el mismo tema si se pulsa «Publicar» de nuevo.
    """
    fila = get_db().execute(
        "SELECT id FROM temas WHERE usuario_id = ? AND titulo = ? AND cuerpo = ? AND fecha_hora >= ? "
        "ORDER BY id DESC LIMIT 1",
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
    """Respuestas de un tema, de la más antigua a la más reciente, con el nombre del autor."""
    return get_db().execute(
        "SELECT r.id, r.cuerpo, r.usuario_id, r.fecha_hora, u.nombre_usuario AS autor "
        "FROM respuestas r JOIN usuarios u ON u.id = r.usuario_id "
        "WHERE r.tema_id = ? ORDER BY r.fecha_hora, r.id",
        (id_tema,),
    ).fetchall()


def buscar_respuesta_igual_reciente(id_tema, usuario_id, cuerpo, desde):
    """Id de una respuesta idéntica del mismo autor en el mismo tema publicada a partir de `desde`, o None.

    Sirve para no guardar dos veces la misma respuesta si se pulsa «Responder» de nuevo.
    """
    fila = get_db().execute(
        "SELECT id FROM respuestas WHERE tema_id = ? AND usuario_id = ? AND cuerpo = ? AND fecha_hora >= ? "
        "ORDER BY id DESC LIMIT 1",
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
