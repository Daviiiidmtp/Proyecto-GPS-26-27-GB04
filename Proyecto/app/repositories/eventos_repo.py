"""Consultas SQL sobre la tabla `eventos`."""
from app.db import get_db


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
