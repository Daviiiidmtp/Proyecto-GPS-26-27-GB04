"""Gestor Usuario (EP-04 Usuarios)."""


def crearUsuario(usuario):
    """Activa una cuenta de cliente con email sintético y contraseña. -> bool. US-09"""
    raise NotImplementedError("Pendiente: US-09 Registro de usuario")


def cambiarRol(idUsuario, rol):
    """Cambia el rol de un usuario (cliente, moderador, admin). -> bool. US-10"""
    raise NotImplementedError("Pendiente: US-10 Moderar foro y bloquear cuentas")


def getRolUsuario(idUsuario):
    """Rol del usuario. -> str. Lo usan los métodos @Admin y @Moderador. US-09"""
    raise NotImplementedError("Pendiente: US-09 Registro de usuario")


# ---------- @Admin @Moderador ----------

def banearUsuario(idUsuario):
    """@Admin @Moderador. Bloquea una cuenta. -> bool. US-10"""
    raise NotImplementedError("Pendiente: US-10 Moderar foro y bloquear cuentas")
