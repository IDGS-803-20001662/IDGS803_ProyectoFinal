from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import Compra, Pedido, DetallePedido
from sqlalchemy import or_
from . import db

compra = Blueprint("compra", __name__, url_prefix='/compra')

@compra.route("/compras")
@login_required
@roles_accepted('ADMINISTRADOR','ALMACENISTA')
def compras():
    compras = Compra.query.all()
    return render_template("/compra/compras.html", compras=compras)

@compra.route("/buscarcompra", methods = ['GET', 'POST'])
@login_required
@roles_accepted('ADMINISTRADOR','ALMACENISTA')
def buscarcompra():
    if request.method == 'POST':
        parametro =  request.form['parametro']
        parametro = parametro.upper()
        print(parametro)

        compras = Compra.query.filter(or_(
            Compra.id.ilike(f'%{parametro}%'),
            Compra.fecha.ilike(f'%{parametro}%'),
            Compra.pedido_id.ilike(f'%{parametro}%'),
            Compra.user_id.ilike(f'%{parametro}%'),
            Compra.total.ilike(f'%{parametro}%')
        )).all()
    return render_template("compra/comprasencontradas.html", compras=compras)

@compra.route("/verdetalles", methods = ['GET'])
@login_required
@roles_accepted('ADMINISTRADOR','ALMACENISTA')
def verdetalles():
    if request.method == "GET":
        id=request.args.get("id")
        pedido = db.session.query(Pedido).filter(Pedido.id == id).first()
        detalles = DetallePedido.query.filter_by(pedido_id=id).all()

    return render_template("/compra/verdetalles.html", pedido=pedido, detalles=detalles)