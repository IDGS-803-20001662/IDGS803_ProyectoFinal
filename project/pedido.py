from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import MateriaPrima, Producto, Receta, Pedido, User, DetallePedido, Compra, Venta
from sqlalchemy import or_
from . import db
from werkzeug.utils import secure_filename
import os
import base64
from datetime import datetime, timedelta

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

@pedido.route("/detallescliente", methods = ['GET', 'POST'])
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def detallescliente():
    if request.method == "GET":
        id =  request.args.get('id')
        pedido = db.session.query(Pedido).filter(Pedido.id == id).first()
        detalles = DetallePedido.query.filter_by(pedido_id=id).all()
        fecha_actual = datetime.now()
        fecha_val= pedido.fecha + timedelta(minutes=10)
        print(fecha_val)
        mostrar = 0
        if fecha_actual > fecha_val:
            mostrar = 1

    if request.method == 'POST':
        return redirect(url_for("pedido.pedidoscliente"))
    
    return render_template("/pedido/detallescliente.html", pedido=pedido, detalles=detalles, mostrar=mostrar)

@pedido.route("/prepararpedidocliente", methods = ['GET', 'POST'])
@login_required
@roles_required("VENDEDOR")
def prepararpedidocliente():
    if request.method == "GET":
        id=request.args.get("id")
        pedido = db.session.query(Pedido).filter(Pedido.id == id).first()
        detalles = DetallePedido.query.filter_by(pedido_id=id).all()
        fecha_actual = datetime.now()
        fecha_val= pedido.fecha + timedelta(minutes=10)
        print(fecha_val)
        mostrar = 0
        if fecha_actual > fecha_val:
            mostrar = 1
        pedido.status = "2"
        db.session.add(pedido)
        db.session.commit()
        return render_template("/pedido/detallescliente.html", pedido=pedido, detalles=detalles, mostrar=mostrar)

@pedido.route("/entregarpedidocliente", methods = ['GET', 'POST'])
@login_required
@roles_required("VENDEDOR")
def entregarpedidocliente():
    if request.method == "GET":
        id=request.args.get("id")
        pedido = db.session.query(Pedido).filter(Pedido.id == id).first()
        detalles = DetallePedido.query.filter_by(pedido_id=id).all()
        fecha_actual = datetime.now()
        fecha_val = pedido.fecha + timedelta(minutes=10)
        print(fecha_val)
        mostrar = 0
        if fecha_actual > fecha_val:
            mostrar = 1

        pedido.status = "3"
        db.session.add(pedido)
        db.session.commit()

        # MODIFICAR STOCK
        for detalle in detalles:
            prod = db.session.query(Producto).filter(Producto.id == detalle.producto.id).first()
            recetas = Receta.query.filter_by(producto_id=prod.id).all()

            for receta in recetas:
                materia = db.session.query(MateriaPrima).filter(MateriaPrima.id == receta.materia_prima.id).first()
                materia.stock = materia.stock - (receta.cantidad * detalle.cantidad)
                db.session.add(materia)
                db.session.commit()
        
        # AGREGAR VENTA EFECTUADA
        venta = Venta(pedido_id=pedido.id,
                        user_id= current_user.id,
                        total=pedido.total)
        db.session.add(venta)
        db.session.commit()

        return render_template("/pedido/detallescliente.html", pedido=pedido, detalles=detalles, mostrar=mostrar)



# ADMINISTRACION GENERAL DE DETALLES DE PEDIDOS A PROVEEDORES

@pedido.route("/pedidosprov")
@login_required
@roles_accepted('ADMINISTRADOR','ALMACENISTA')
def pedidosprov():
    pedidos = Pedido.query.filter_by(tipo_pedido = "0").all()
    return render_template("/pedido/pedidosprov.html", pedidos=pedidos)

#Buscar por estatus
@pedido.route("/pedidosestatusprov", methods = ['GET', 'POST'])
@login_required
@roles_accepted('ADMINISTRADOR','ALMACENISTA')
def pedidosestatusprov():
   if request.method == 'POST':
        parametro =  request.form['parametro']
        print(parametro)
        pedidos = Pedido.query.filter_by(tipo_pedido = "0", status=parametro).all()

        return render_template("/pedido/pedidosestatusprov.html", pedidos=pedidos)

@pedido.route("/detallesprov", methods = ['GET', 'POST'])
@login_required
@roles_accepted('ADMINISTRADOR','ALMACENISTA')
def detallesprov():
    if request.method == "GET":
        id=request.args.get("id")
        pedido = db.session.query(Pedido).filter(Pedido.id == id).first()
        detalles = DetallePedido.query.filter_by(pedido_id=id).all()
        fecha_actual = datetime.now()
        fecha_val= pedido.fecha + timedelta(minutes=10)
        print(fecha_val)
        mostrar = 0
        if fecha_val > fecha_actual:
            mostrar = 1


    if request.method == 'POST':
        return redirect(url_for("pedido.pedidosprov"))
    
    return render_template("/pedido/detallesprov.html", pedido=pedido, detalles=detalles, mostrar = mostrar)

@pedido.route("/registrardetalleprov", methods = ['POST'])
@login_required
@roles_accepted('ALMACENISTA')
def registrardetalleprov():
    materias = MateriaPrima.query.filter_by(status='1').all()

    if request.method == "POST":
        # COMPROBACIÓN DEL STOCK
        materia = MateriaPrima.query.filter_by(id=request.form.get('materia_nueva')).first()
        cantidad = request.form.get('cant_nueva')
        if (int(materia.stock) + int(cantidad)) < int(materia.cant_max):

            # REGISTRO DE PEDIDO
            ped = Pedido(usuario_id=current_user.id,
                        total=0,
                        tipo_pedido=False)
            db.session.add(ped)
            db.session.commit()

            # REGISTRO DE PRIMER DETALLE DE PEDIDO
            ultimo_pedido = Pedido.query.order_by(Pedido.id.desc()).first()

            det = DetallePedido(pedido_id = ultimo_pedido.id,
                                materia_prima_id = materia.id,
                                medida = materia.medida,
                                cantidad = cantidad,
                                subtotal = materia.precio)
            db.session.add(det)
            db.session.commit()

            # MODIFICACIÓN DEL TOTAL
            ultimo_pedido.total = materia.precio
            db.session.add(ultimo_pedido)
            db.session.commit()

            pedido = db.session.query(Pedido).filter(Pedido.id == ultimo_pedido.id).first()
            
            return redirect(url_for("pedido.modificarpedidoprov", id=pedido.id))

        else:
            flash("La cantidad solicitada sobrepasará el stock máximo del insumo")
            return redirect(url_for("/pedido/registrarpedidoprov"), materias=materias)
        
@pedido.route("/modificardetalleprov", methods = ['GET', 'POST'])
@login_required
@roles_accepted('ALMACENISTA')
def modificardetalleprov():
    materias = MateriaPrima.query.filter_by(status='1').all()

    if request.method == "POST":
        # COMPROBACIÓN DEL STOCK
        materia = MateriaPrima.query.filter_by(id=request.form.get('materia_nueva')).first()
        cantidad = request.form.get('cant_nueva')
        if (int(materia.stock) + int(cantidad)) < int(materia.cant_max):

            # REGISTRO DE DETALLE DE PEDIDO
            id_pedido = request.form.get('pedido_id')
            pedido = db.session.query(Pedido).filter(Pedido.id == id_pedido).first()

            det = DetallePedido(pedido_id = id_pedido,
                                materia_prima_id = materia.id,
                                medida = materia.medida,
                                cantidad = cantidad,
                                subtotal = materia.precio)
            db.session.add(det)
            db.session.commit()

            # MODIFICACIÓN DEL TOTAL
            pedido.total = pedido.total + materia.precio
            db.session.add(pedido)
            db.session.commit()
            
            
            return redirect(url_for('pedido.modificarpedidoprov', id=id_pedido))

        else:
            flash("La cantidad solicitada sobrepasará el stock máximo del insumo")
            return redirect(url_for('pedido.modificarpedidoprov', id=id_pedido))
        
@pedido.route("/eliminardetalleprov/<int:id>", methods = ["GET"])
@login_required
@roles_accepted('ALMACENISTA')
def eliminardetalleprov(id):
    if request.method == "GET":
        detalle = db.session.query(DetallePedido).filter(DetallePedido.id == id).first()
        id_pedido = detalle.pedido_id
        pedido = db.session.query(Pedido).filter(Pedido.id == id).first()

        # MODIFICACIÓN DEL TOTAL
        pedido.total = pedido.total - detalle.materia_prima.precio
        db.session.add(pedido)
        db.session.commit()

        db.session.delete(detalle)
        db.session.commit()

    return redirect(url_for('pedido.modificarpedidoprov', id=id_pedido))


@pedido.route("/modificarpedidoprov/<int:id>", methods = ['GET', 'POST'])
@login_required
@roles_accepted('ALMACENISTA')
def modificarpedidoprov(id):
    if request.method == "GET":
        #id = request.args.get('id')
        pedido = db.session.query(Pedido).filter(Pedido.id == id).first()
        materias = MateriaPrima.query.filter_by(status='1').all()
        detalles = DetallePedido.query.filter_by(pedido_id=id).all()
        fecha_actual = datetime.now()

    return render_template("/pedido/modificarpedidoprov.html", materias=materias, pedido=pedido, detalles=detalles, fecha_actual=fecha_actual)
   

@pedido.route("/registrarpedidoprov", methods = ['GET'])
@login_required
@roles_accepted('ALMACENISTA')
def registrarpedidoprov():
    if request.method == "GET":
        materias = MateriaPrima.query.filter_by(status='1').all()
    
    return render_template("/pedido/registrarpedidoprov.html", materias=materias)

@pedido.route("/hacerpedidoprov", methods = ['GET', 'POST'])
@login_required
@roles_required("ALMACENISTA")
def hacerpedidoprov():
    if request.method == "GET":
        id=request.args.get("id")
        pedido = db.session.query(Pedido).filter(Pedido.id == id).first()
        detalles = DetallePedido.query.filter_by(pedido_id=id).all()
        fecha_actual = datetime.now()
        fecha_val= pedido.fecha + timedelta(minutes=10)
        print(fecha_val)
        mostrar = 0
        if fecha_val > fecha_actual:
            mostrar = 1
        pedido.status = "2"
        db.session.add(pedido)
        db.session.commit()
        return render_template("/pedido/detallesprov.html", pedido=pedido, detalles=detalles, mostrar=mostrar)
    
@pedido.route("/entregarpedidoprov", methods = ['GET', 'POST'])
@login_required
@roles_required("ALMACENISTA")
def entregarpedidoprov():
    if request.method == "GET":
        id=request.args.get("id")
        pedido = db.session.query(Pedido).filter(Pedido.id == id).first()
        detalles = DetallePedido.query.filter_by(pedido_id=id).all()
        fecha_actual = datetime.now()
        fecha_val= pedido.fecha + timedelta(minutes=10)
        print(fecha_val)
        mostrar = 0
        if fecha_val > fecha_actual:
            mostrar = 1

        pedido.status = "3"
        db.session.add(pedido)
        db.session.commit()

        # MODIFICAR STOCK
        for detalle in detalles:
            mat = db.session.query(MateriaPrima).filter(MateriaPrima.id == detalle.materia_prima.id).first()
            mat.stock = detalle.cantidad + mat.stock
            db.session.add(mat)
            db.session.commit()
        
        # AGREGAR COMPRA EFECTUADA
        compra = Compra(pedido_id=pedido.id,
                        user_id= current_user.id,
                        total=pedido.total)
        db.session.add(compra)
        db.session.commit()

        return render_template("/pedido/detallesprov.html", pedido=pedido, detalles=detalles, mostrar=mostrar)
    
@pedido.route("/cancelarpedidoprov", methods = ['GET', 'POST'])
@login_required
@roles_required("ALMACENISTA")
def cancelarpedidoprov():
    if request.method == "GET":
        id=request.args.get("id")
        pedido = db.session.query(Pedido).filter(Pedido.id == id).first()
        detalles = DetallePedido.query.filter_by(pedido_id=id).all()
        fecha_actual = datetime.now()
        fecha_val= pedido.fecha + timedelta(minutes=10)
        print(fecha_val)
        mostrar = 0
        if fecha_val > fecha_actual:
            mostrar = 1
        pedido.status = "0"
        db.session.add(pedido)
        db.session.commit()
        return render_template("/pedido/detallesprov.html", pedido=pedido, detalles=detalles, mostrar=mostrar)

