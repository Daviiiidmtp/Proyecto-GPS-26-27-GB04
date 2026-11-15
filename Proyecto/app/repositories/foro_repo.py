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
