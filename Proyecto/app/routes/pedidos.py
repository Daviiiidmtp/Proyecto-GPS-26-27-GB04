"""Confirmar la compra simulada y ver el resultado del pedido (US-17).

El resumen y el método de pago están en /cesta/checkout (GB04-109). La lógica está en
gestor_catalogo.realizarCompra (GB04-107): no se cobra nada ni se piden datos de pago reales.
"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.gestores import gestor_catalogo

bp = Blueprint("pedidos", __name__)


@bp.route("/cesta/confirmar", methods=["POST"])
def confirmar():
    """US-17-AC-03: confirma la compra simulada, vacía la cesta y muestra el resultado."""
    cesta = session.get("cesta")
    cesta = dict(cesta) if isinstance(cesta, dict) else {}
    codigo = request.form.get("codigo", "")
    try:
        pedido = gestor_catalogo.realizarCompra(cesta, request.form.get("metodo_pago"), codigo,
                                                session.get("usuario_id"))
    except gestor_catalogo.CompraInvalida as error:
        # US-17-AC-04: no se crea el pedido ni se cambia el stock. Se dice qué corregir
        flash(str(error), "error")
        if error.motivo in ("cesta_vacia", "no_disponible"):
            return redirect(url_for("cesta.ver_cesta"))
        return redirect(url_for("cesta.checkout"))
    except gestor_catalogo.CatalogoNoDisponible:
        # US-17-AC-06: se informa y se puede reintentar. La cesta se conserva
        flash("No se ha podido completar la compra. No se ha cobrado nada ni se ha cambiado el stock. "
              "Vuelve a intentarlo.", "error")
        return redirect(url_for("cesta.checkout"))
    # La compra ya está hecha: se vacía la cesta. Si se vuelve a confirmar con el mismo
    # código, el gestor devuelve el mismo pedido sin descontar más stock (US-17-AC-07)
    session["cesta"] = {}
    session.modified = True
    return redirect(url_for("pedidos.ver_pedido", codigo=pedido["codigo"]))


@bp.route("/pedidos/<codigo>")
def ver_pedido(codigo):
    """US-17-AC-03: resultado del pedido simulado con un mensaje explícito de éxito."""
    try:
        pedido = gestor_catalogo.getPedido(codigo)
    except gestor_catalogo.CatalogoNoDisponible:
        return render_template("cesta/pedido.html", pedido=None, error=True), 503
    if pedido is None:
        return render_template("cesta/pedido.html", pedido=None, error=False), 404
    return render_template("cesta/pedido.html", pedido=pedido, error=False)
