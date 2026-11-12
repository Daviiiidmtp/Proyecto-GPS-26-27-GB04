"""Lógica de la página de inicio."""
from app.repositories import ajustes_repo

NOMBRE_POR_DEFECTO = "El Hogar del Hobbit"


def datos_portada():
    """Prepara los datos que necesita la página de inicio."""
    return {
        "nombre_tienda": ajustes_repo.obtener("nombre_tienda") or NOMBRE_POR_DEFECTO,
        "lema": ajustes_repo.obtener("lema") or "",
    }
