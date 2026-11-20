"""Consultas SQL sobre la tabla `notificaciones` (US-11)."""
from app.db import get_db

COLUMNAS = ("SELECT n.id, n.evento_id, n.fecha_hora, n.leida, e.titulo, e.fecha_hora AS fecha_evento "
            "FROM notificaciones n JOIN eventos e ON e.id = n.evento_id")


def avisar_evento(evento_id, fecha_hora):
    """Crea una notificación no leída del evento para cada cuenta Cliente activa. Devuelve cuántas.

    No hace commit: se llama dentro de la operación que guarda el evento (eventos_repo.crear),
    así el evento y sus avisos se guardan juntos o no se guarda nada.
    INSERT OR IGNORE con UNIQUE (usuario_id, evento_id): no se crean duplicados (US-11-AC-01).
    """
    cursor = get_db().execute(
        "INSERT OR IGNORE INTO notificaciones (usuario_id, evento_id, fecha_hora) "
        "SELECT id, ?, ? FROM usuarios WHERE rol = 'cliente' AND estado = 'activa'",
        (evento_id, fecha_hora),
    )
    return cursor.rowcount


def listar_no_leidas(usuario_id):
    """Notificaciones sin leer de una cuenta, de la más reciente a la más antigua."""
    return get_db().execute(
        COLUMNAS + " WHERE n.usuario_id = ? AND n.leida = 0 ORDER BY n.fecha_hora DESC, n.id DESC",
        (usuario_id,),
    ).fetchall()


def contar_no_leidas(usuario_id):
    return get_db().execute(
        "SELECT COUNT(*) FROM notificaciones WHERE usuario_id = ? AND leida = 0", (usuario_id,)
    ).fetchone()[0]


def obtener(id_notificacion, usuario_id):
    """Una notificación de esa cuenta, o None si no existe o es de otra cuenta."""
    return get_db().execute(
        COLUMNAS + " WHERE n.id = ? AND n.usuario_id = ?", (id_notificacion, usuario_id)
    ).fetchone()


def marcar_leida(id_notificacion, usuario_id):
    """Marca la notificación como leída. Una leída no vuelve a estar sin leer (US-11-AC-04)."""
    db = get_db()
    with db:
        db.execute(
            "UPDATE notificaciones SET leida = 1 WHERE id = ? AND usuario_id = ?", (id_notificacion, usuario_id)
        )
