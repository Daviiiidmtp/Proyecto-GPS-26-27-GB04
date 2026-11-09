"""Gestión Foro (EP-03 Foro)."""


def getTema(idTema):
    """Un tema con sus mensajes. -> dict. US-07 y US-08"""
    raise NotImplementedError("Pendiente: US-07 Crear tema en foro")


def crearTema(titulo):
    """Crea un tema y devuelve su id. -> int. US-07"""
    raise NotImplementedError("Pendiente: US-07 Crear tema en foro")


def anadirComentario(idUsuario, idTema, comentario):
    """Responde en un tema. -> bool. US-08"""
    raise NotImplementedError("Pendiente: US-08 Responder en foro")


def eliminarMensaje(idMensaje):
    """@Admin @Moderador. Retira un mensaje. -> bool. US-10"""
    raise NotImplementedError("Pendiente: US-10 Moderar foro y bloquear cuentas")
