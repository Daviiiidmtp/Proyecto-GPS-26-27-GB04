"""Pantalla de la cesta y botón «Añadir a la cesta» del catálogo (US-16).

La cesta se guarda en la sesión del navegador como {"id del producto": cantidad}, porque
el checkout simulado no exige cuenta. La lógica está en gestor_catalogo (GB04-106).
"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.gestores import gestor_catalogo

bp = Blueprint("cesta", __name__)


def _cesta():
    """Copia de la cesta de la sesión, para no tocarla si la operación falla."""
    cesta = session.get("cesta")
    return dict(cesta) if isinstance(cesta, dict) else {}


def _guardar(cesta):
    session["cesta"] = cesta
    session.modified = True


def _volver():
    """Vuelve a la página desde la que se pulsó el botón, solo si es de esta web."""
    destino = request.form.get("volver", "")
    if destino.startswith("/") and not destino.startswith("//"):
        return redirect(destino)
    return redirect(url_for("catalogo.ver_catalogo"))


@bp.route("/cesta")
def ver_cesta():
    try:
        datos = gestor_catalogo.getCesta(_cesta())
    except gestor_catalogo.CatalogoNoDisponible:
        return render_template("cesta/cesta.html", datos=None, error=True), 503
    return render_template("cesta/cesta.html", datos=datos, error=False)


@bp.route("/cesta/anadir/<int:id_producto>", methods=["POST"])
def anadir(id_producto):
    """US-16-AC-01: añade unidades de un producto disponible."""
    cesta = _cesta()
    try:
        gestor_catalogo.anadirProductoCesta(id_producto, request.form.get("cantidad", "1"), cesta)
    except (gestor_catalogo.CantidadInvalida, gestor_catalogo.ProductoNoDisponible) as error:
        # US-16-AC-04: se dice qué artículo no se puede añadir y por qué
        flash(str(error), "error")
        return _volver()
    except gestor_catalogo.CatalogoNoDisponible:
        flash("No se ha podido añadir el producto a la cesta. Vuelve a intentarlo.", "error")
        return _volver()
    _guardar(cesta)
    producto = gestor_catalogo.getProducto(id_producto)
    flash(f"«{producto['nombre']}» añadido a la cesta.", "exito")
    return _volver()


@bp.route("/cesta/quitar/<int:id_producto>", methods=["POST"])
def quitar(id_producto):
    """US-16-AC-01: quita una unidad o el producto entero si no se indica cantidad."""
    cesta = _cesta()
    try:
        cambiado = gestor_catalogo.quitarProductoCesta(id_producto, cesta, request.form.get("cantidad") or None)
    except gestor_catalogo.CantidadInvalida as error:
        flash(str(error), "error")
        return redirect(url_for("cesta.ver_cesta"))
    if cambiado:
        _guardar(cesta)
        flash("Cesta actualizada.", "exito")
    return redirect(url_for("cesta.ver_cesta"))


@bp.route("/cesta/checkout")
def checkout():
    """Resumen de la compra simulada y elección del método de pago (US-17-AC-01 y AC-02).

    US-16-AC-03 y AC-04: con la cesta vacía o con artículos que no se pueden comprar,
    se vuelve a la cesta para corregirla. El formulario se confirma en /cesta/confirmar (GB04-110).
    """
    try:
        datos = gestor_catalogo.getCesta(_cesta())
    except gestor_catalogo.CatalogoNoDisponible:
        flash("No se ha podido comprobar la cesta. Vuelve a intentarlo.", "error")
        return redirect(url_for("cesta.ver_cesta"))
    if datos["vacia"]:
        flash("Tu cesta está vacía. Añade algún producto antes de tramitar el pedido.", "error")
        return redirect(url_for("cesta.ver_cesta"))
    if not datos["se_puede_comprar"]:
        flash("Hay artículos que no se pueden comprar. Corrige la cesta antes de tramitar el pedido.", "error")
        return redirect(url_for("cesta.ver_cesta"))
    # Cada vez que se abre el resumen hay un código nuevo. Si se confirma dos veces
    # con el mismo código, se devuelve el mismo pedido (US-17-AC-07).
    return render_template("cesta/checkout.html", datos=datos, metodos=gestor_catalogo.METODOS_PAGO,
                           codigo=gestor_catalogo.nuevoCodigoCompra())
