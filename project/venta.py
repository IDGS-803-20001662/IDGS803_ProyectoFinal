from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import Venta, Pedido, DetallePedido
from sqlalchemy import or_
from . import db

venta = Blueprint("venta", __name__, url_prefix='/venta')

@venta.route("/ventas")
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def ventas():
    ventas = Venta.query.all()
    return render_template("/venta/ventas.html", ventas=ventas)

@venta.route("/buscarventa", methods = ['GET', 'POST'])
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def buscarventa():
    if request.method == 'POST':
        parametro =  request.form['parametro']
        parametro = parametro.upper()
        print(parametro)

        ventas = Venta.query.filter(or_(
            Venta.id.ilike(f'%{parametro}%'),
            Venta.fecha.ilike(f'%{parametro}%'),
            Venta.pedido_id.ilike(f'%{parametro}%'),
            Venta.user_id.ilike(f'%{parametro}%'),
            Venta.total.ilike(f'%{parametro}%')
        )).all()
    return render_template("venta/ventasencontradas.html", ventas=ventas)

@venta.route("/verdetalles", methods = ['GET'])
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def verdetalles():
    if request.method == "GET":
        id=request.args.get("id")
        pedido = db.session.query(Pedido).filter(Pedido.id == id).first()
        detalles = DetallePedido.query.filter_by(pedido_id=id).all()

    return render_template("/venta/verdetalles.html", pedido=pedido, detalles=detalles)