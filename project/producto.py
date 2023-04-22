from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import MateriaPrima, Producto, Receta, AgregarForm, Carrito, Carrito_Producto
from sqlalchemy import or_
from . import db
from werkzeug.utils import secure_filename
import os
import base64
from .logg import Logger

producto = Blueprint('producto', __name__, url_prefix='/producto')
log = Logger("producto")

@producto.route("/productos")
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def productos():
    productos = Producto.query.filter_by(status='1').all()
    if not productos:
        log.critical('El módulo de Productos no ha cargado la información de los productos')
    return render_template('/producto/productos.html', productos=productos)

@producto.route("/productosinactivos")
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def productosinactivos():
    productos = Producto.query.filter_by(status='0').all()
    if not productos:
        log.critical('El módulo de Productos no ha cargado la información de los productos inactivos')
    return render_template('/producto/productosinactivos.html', productos=productos)

@producto.route("/buscarproducto", methods = ['GET', 'POST'])
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def buscarproducto():
    if request.method == 'POST':
        parametro =  request.form['parametro']
        parametro = parametro.upper()
        print(parametro)

        productos = Producto.query.filter(or_(
            Producto.id.ilike(f'%{parametro}%'),
            Producto.nombre.ilike(f'%{parametro}%'),
            Producto.descripcion.ilike(f'%{parametro}%'),
            Producto.preparacion.ilike(f'%{parametro}%'),
            Producto.url.ilike(f'%{parametro}%')
        )).all()

        if not productos:
            log.warning('El módulo de Productos no ha cargado la información de los productos coincidentes')

    return render_template('/producto/productosencontrados.html', productos=productos)

@producto.route("/registrarproducto", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def registrarproducto():

    if request.method == 'POST':
        imagen = request.files['imagen']
        if imagen:
            imagen_data = base64.b64encode(imagen.read()).decode('utf-8')

        prod = Producto(nombre = request.form.get('nombre').upper(),
                        descripcion = request.form.get('descripcion').upper(),
                        preparacion = request.form.get('preparacion').upper(),
                        url = imagen_data,
                        merma_esperada = request.form.get('merma_esperada'),
                        precio = request.form.get('precio'))
        db.session.add(prod)
        db.session.commit()
        log.debug('Se registró el producto {} por el usuario {}'.format(request.form.get('nombre').upper(), current_user.email))

        return redirect(url_for("producto.productos"))
    
    return render_template('/producto/registrarproducto.html')

@producto.route("/guardarreceta", methods = ['GET', 'POST'])
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def guardarreceta():

    if request.method == "GET":
        id =  request.args.get('id')
        producto = db.session.query(Producto).filter(Producto.id == id).first()
        materias = MateriaPrima.query.filter_by(status='1').all()
        recetas = Receta.query.filter_by(producto_id=id).all()

    if request.method == 'POST':
        return redirect(url_for("producto.productos"))
    
    return render_template("/producto/guardarreceta.html", id_producto=producto.id, nombre_producto=producto.nombre, 
                           descripcion_producto=producto.descripcion,preparacion_producto=producto.preparacion, imagen_producto=producto.url,
                           materias=materias, recetas=recetas)

@producto.route("/registraringrediente", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def registraringrediente():
    if request.method == "POST":
        id=request.form.get('producto_id_nuevo')
        materia = db.session.query(MateriaPrima).filter(MateriaPrima.id == request.form.get('materia_nueva')).first()
        receta = Receta(producto_id=request.form.get('producto_id_nuevo'),
                        materia_prima_id= materia.id,
                        cantidad=request.form.get('cant_nueva'),
                        medida=materia.medida)
        db.session.add(receta)
        db.session.commit()
        log.debug('Se registró un nuevo ingrediente en el producto {} por el usuario {}'.format(request.form.get('producto_id_nuevo'), current_user.email))

        producto = db.session.query(Producto).filter(Producto.id == id).first()
        materias = MateriaPrima.query.filter_by(status='1').all()
        recetas = Receta.query.filter_by(producto_id=id).all()

        return render_template('/producto/guardarreceta.html', id_producto=producto.id, nombre_producto=producto.nombre, 
                           descripcion_producto=producto.descripcion,preparacion_producto=producto.preparacion, 
                           imagen_producto=producto.url, materias=materias,recetas=recetas)
    
@producto.route("/eliminaringrediente", methods = ["GET"])
@login_required
@roles_required('ADMINISTRADOR')
def eliminaringrediente():
    if request.method == "GET":
        id=request.args.get("id")
        receta = db.session.query(Receta).filter(Receta.id == id).first()
        id_prod = receta.producto_id
        db.session.delete(receta)
        db.session.commit()
        log.warning('Se eliminó un ingrediente en el producto {} por el usuario {}'.format(id_prod, current_user.email))

        producto = db.session.query(Producto).filter(Producto.id == id_prod).first()
        materias = MateriaPrima.query.filter_by(status='1').all()
        recetas = Receta.query.filter_by(producto_id=id_prod).all()
    return render_template('/producto/guardarreceta.html', id_producto=producto.id, nombre_producto=producto.nombre, 
                           descripcion_producto=producto.descripcion,preparacion_producto=producto.preparacion, 
                           imagen_producto=producto.url, materias=materias,recetas=recetas)

@producto.route("/modificarproducto", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def modificarproducto():

    if request.method == 'GET':
        id =  request.args.get('id')
        prod = db.session.query(Producto).filter(Producto.id == id).first()

    if request.method == 'POST':
        id = request.form.get('id')
        prod = db.session.query(Producto).filter(Producto.id == id).first()
        imagen = request.files['imagen']
        if imagen:
            imagen_data = base64.b64encode(imagen.read()).decode('utf-8')
            prod.url = imagen_data
        
        prod.nombre = request.form.get('nombre').upper()
        prod.descripcion = request.form.get('descripcion').upper()
        prod.preparacion = request.form.get('preparacion').upper()
        prod.merma_esperada = request.form.get('merma_esperada')
        prod.precio = request.form.get('precio')
        db.session.add(prod)
        db.session.commit()

        log.warning('Se modificó el producto {} por el usuario {}'.format(request.form.get('nombre').upper(), current_user.email))

        return redirect(url_for("producto.productos"))
    
    return render_template("/producto/modificarproducto.html", id=prod.id, nombre=prod.nombre, descripcion=prod.descripcion,
        preparacion=prod.preparacion, url=prod.url, merma_esperada=prod.merma_esperada, precio=prod.precio)

@producto.route("/eliminarproducto", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def eliminarproducto():

    if request.method == 'GET':
        id =  request.args.get('id')
        prod = db.session.query(Producto).filter(Producto.id == id).first()

    if request.method == 'POST':
        id = request.form.get('id')
        prod = db.session.query(Producto).filter(Producto.id == id).first()
        prod.nombre = request.form.get('nombre').upper()
        prod.descripcion = request.form.get('descripcion').upper()
        prod.preparacion = request.form.get('preparacion').upper()
        prod.url = request.form.get('url'),
        prod.merma_esperada = request.form.get('merma_esperada')
        prod.precio = request.form.get('precio')
        prod.status = False
        db.session.add(prod)
        db.session.commit()
        log.warning('Se eliminó el producto {} por el usuario {}'.format(request.form.get('nombre').upper(), current_user.email))
        
        recetas = Receta.query.filter_by(producto_id=id).all()
        for receta in recetas:
            db.session.delete(receta)
            db.session.commit()
        return redirect(url_for("producto.productos"))
    
    return render_template("/producto/eliminarproducto.html", id=prod.id, nombre=prod.nombre, descripcion=prod.descripcion,
        preparacion=prod.preparacion, url=prod.url, merma_esperada=prod.merma_esperada, precio=prod.precio)

@producto.route('/catalogo')
@login_required
@roles_required('CLIENTE')
def catalogo():
    productos_rs = Producto.query.filter_by(status='1').all()
    productos = []
    for p in productos_rs:
         producto = p.__dict__
         form = AgregarForm()
         form.id_producto.data = p.id
         producto['form'] = form
         productos.append(producto)
    return render_template('/producto/catalogo.html', nombre=current_user.nombre, productos=productos)

@producto.route('/catalogo', methods=['POST'])
@login_required
@roles_required('CLIENTE')
def agregar_producto_carrito():
    form = AgregarForm(request.form)
    if form.validate():
        carrito = Carrito.query.filter_by(id_user = current_user.id).first()
        if carrito:
             carritoTiene = carrito.carrito_tiene.filter_by(id_producto=form.id_producto.data).first()
             if carritoTiene:
                  carritoTiene.cantidad += form.cantidad.data
                  db.session.commit()
             else:
                  carritoProducto = Carrito_Producto(id_carrito = carrito.id,
                                                    id_producto = form.id_producto.data,
                                                    cantidad = form.cantidad.data)
                  db.session.add(carritoProducto)
                  db.session.commit()
        else:
            carrito = Carrito(id_user=current_user.id)
            db.session.add(carrito)
            db.session.commit()
            carritoProducto = Carrito_Producto(id_carrito = carrito.id,
                                            id_producto = form.id_producto.data,
                                            cantidad = form.cantidad.data)
            db.session.add(carritoProducto)
            db.session.commit()
    return redirect(url_for('producto.catalogo'))


@producto.route("/productos")
@login_required
@roles_required('CLIENTE')
def lista_productos():
	productos = Producto.query.filter_by(status='1').all()
	return render_template('catalogo.html',productos = productos)

@producto.route("/productos/<id_producto>")
@login_required
@roles_required('CLIENTE')
def desc_producto(id_producto):
	producto = Producto.query.get(id_producto)
	form = AgregarForm()
	return render_template('desc_producto.html',producto = producto, form = form)

@producto.route("/agregar/<id_producto>", methods=['GET', 'POST'])
@login_required
@roles_required('CLIENTE')
def agregar(id_producto):
	form = AgregarForm()
	if form.validate_on_submit():
		sumatotal = 0

		productos = session['productos']
		producto_nombre = db.session.query(Producto).filter(Producto.id == id).first()
		producto = [id_producto, producto_nombre.nombre, form.cantidad.data, producto_nombre.precio, form.cantidad.data*producto_nombre.precio, sumatotal, producto_nombre.url]
		productos.append(producto)
		session['productos'] = productos
		cantidad = form.cantidad.data
		producto = Producto.query.get(id_producto)
		return render_template('carrito.html', productos = session['productos'])
		productos = Producto.query.all()
	return render_template('catalogo.html',productos = productos)

