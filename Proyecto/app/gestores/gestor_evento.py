"""Gestor Evento (EP-02 Eventos)."""


def getEventosDisponibles(tipoEvento=None):
    """Próximos eventos; si se indica tipoEvento, solo los de ese tipo. -> list. US-04
    En el diagrama son dos métodos con el mismo nombre; en Python es uno
    con el parámetro opcional."""
    raise NotImplementedError("Pendiente: US-04 Ver calendario de eventos")


def apuntarmeEnEvento(idEvento, idUsuario):
    """Inscribe a un usuario verificado en un evento. -> bool. US-05"""
    raise NotImplementedError("Pendiente: US-05 Inscribirse en evento")


# ---------- @Admin ----------

def crearEvento(evento):
    """@Admin. Publica un evento nuevo. -> bool. US-06"""
    raise NotImplementedError("Pendiente: US-06 Añadir evento")
