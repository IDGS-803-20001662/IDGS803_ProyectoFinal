from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import MateriaPrima, Producto, Receta, Pedido, User, DetallePedido
from sqlalchemy import or_
from . import db
from werkzeug.utils import secure_filename
import os
import base64

pedido = Blueprint('pedido', __name__, url_prefix='/pedido')

# ADMINISTRACION GENERAL DE PEDIDOS DE CLIENTES
@pedido.route("/pedidoscliente")
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def pedidoscliente():
    pedidos = Pedido.query.filter_by(tipo_pedido = "1").all()
    return render_template("/pedido/pedidoscliente.html", pedidos=pedidos)

#Buscar por estatus
@pedido.route("/pedidosestatuscliente", methods = ['GET', 'POST'])
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def pedidosestatuscliente():
   if request.method == 'POST':
        parametro =  request.form['parametro']
        print(parametro)
        pedidos = Pedido.query.filter_by(tipo_pedido = "1", status=parametro).all()

        return render_template("/pedido/pedidosestatuscliente.html", pedidos=pedidos)

#Buscar por tipo de entrega
@pedido.route("/pedidosentregacliente", methods = ['GET', 'POST'])
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def pedidosentregacliente():
    if request.method == 'POST':
        parametro =  request.form['parametro']
        print(parametro)
        pedidos = Pedido.query.filter_by(tipo_pedido = "1",tipo_entrega=parametro).all()

        return render_template("/pedido/pedidosentregacliente.html", pedidos=pedidos)
    
# ADMINISTRACION GENERAL DE PEDIDOS A PROVEEDOR
@pedido.route("/pedidoscliente")
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def pedidoscliente():
    pedidos = Pedido.query.filter_by(tipo_pedido = "1").all()
    return render_template("/pedido/pedidoscliente.html", pedidos=pedidos)

#Buscar por estatus
@pedido.route("/pedidosestatuscliente", methods = ['GET', 'POST'])
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def pedidosestatuscliente():
   if request.method == 'POST':
        parametro =  request.form['parametro']
        print(parametro)
        pedidos = Pedido.query.filter_by(tipo_pedido = "1", status=parametro).all()

        return render_template("/pedido/pedidosestatuscliente.html", pedidos=pedidos)

#Buscar por tipo de entrega
@pedido.route("/pedidosentregacliente", methods = ['GET', 'POST'])
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def pedidosentregacliente():
    if request.method == 'POST':
        parametro =  request.form['parametro']
        print(parametro)
        pedidos = Pedido.query.filter_by(tipo_pedido = "1",tipo_entrega=parametro).all()

        return render_template("/pedido/pedidosentregacliente.html", pedidos=pedidos)


# ADMINISTRACION GENERAL DE DETALLES DE PEDIDOS DE CLIENTES

@pedido.route("/detallescliente", methods = ['GET', 'POST'])
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def detallescliente():
    if request.method == "GET":
        id =  request.args.get('id')
        pedido = db.session.query(Pedido).filter(Pedido.id == id).first()
        detalles = DetallePedido.query.filter_by(pedido_id=id).all()

    if request.method == 'POST':
        return redirect(url_for("pedido.pedidoscliente"))
    
    return render_template("/pedido/detallescliente.html", pedido=pedido, detalles=detalles)

