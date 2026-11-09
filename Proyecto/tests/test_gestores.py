"""Comprueba que existen los gestores del diagrama de clases con sus métodos."""
import pytest

from app.gestores import (gestor_catalogo, gestor_evento, gestor_foro,
                          gestor_soporte, gestor_usuario)

METODOS = {
    gestor_catalogo: ["getProductos", "getProducto", "getProductosPorNombre",
                      "getProductosPorTipo", "getProductosDisponibles",
                      "anadirProductoCesta", "realizarCompra", "getCesta",
                      "crearProducto", "cambiarStock"],
    gestor_evento: ["getEventosDisponibles", "apuntarmeEnEvento", "crearEvento"],
    gestor_foro: ["getTema", "crearTema", "anadirComentario", "eliminarMensaje"],
    gestor_usuario: ["crearUsuario", "cambiarRol", "getRolUsuario", "banearUsuario"],
    gestor_soporte: ["reportarIncidencia"],
}


@pytest.mark.parametrize("gestor, metodos", METODOS.items(), ids=lambda x: getattr(x, "__name__", ""))
def test_cada_gestor_tiene_los_metodos_del_diagrama(gestor, metodos):
    for metodo in metodos:
        assert callable(getattr(gestor, metodo, None)), f"Falta {gestor.__name__}.{metodo}"
