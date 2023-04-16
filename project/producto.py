from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import MateriaPrima, Producto, Receta
from sqlalchemy import or_
from . import db

producto = Blueprint('producto', __name__, url_prefix='/producto')

@producto.route("/productos")
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def productos():
    productos = Producto.query.filter_by(status='1').all()
    return render_template('/producto/productos.html', productos=productos)

@producto.route("/productosinactivos")
@login_required
@roles_accepted('ADMINISTRADOR','VENDEDOR')
def productosinactivos():
    productos = Producto.query.filter_by(status='0').all()
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

    return render_template('/producto/productosencontrados.html', productos=productos)

@producto.route("/registrarproducto", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def registrarproducto():

    materias = MateriaPrima.query.filter_by(status='1').all()

    # confirmar que se registró la receta
    if request.method == 'POST':
        flash('No olvide registrar la receta del producto')
        prod = Producto(nombre = request.form.get('nombre').upper(),
                        descripcion = request.form.get('descripcion').upper(),
                        preparacion = request.form.get('preparacion').upper(),
                        url = request.form.get('url'),
                        merma_esperada = request.form.get('merma_esperada'),
                        precio = request.form.get('precio'))
        db.session.add(prod)
        db.session.commit() 

        return redirect(url_for("producto.productos"))
    
    return render_template('/producto/registrarproducto.html')

@producto.route("/guardarreceta", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def guardarreceta():

    if request.method == "GET":
        id =  request.args.get('id')
        producto = db.session.query(Producto).filter(Producto.id == id).first()
        materias = MateriaPrima.query.filter_by(status='1').all()

    if request.method == 'POST':
        return redirect(url_for("producto.productos"))
    
    return render_template("/producto/guardarreceta.html", id_producto=producto.id, nombre_producto=producto.nombre, 
                           descripcion_producto=producto.descripcion,preparacion_producto=producto.preparacion, imagen_producto=producto.url,
                           materias=materias)


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
        prod.nombre = request.form.get('nombre').upper()
        prod.descripcion = request.form.get('descripcion').upper()
        prod.preparacion = request.form.get('preparacion').upper()
        prod.url = request.form.get('url'),
        prod.merma_esperada = request.form.get('merma_esperada')
        prod.precio = request.form.get('precio')
        db.session.add(prod)
        db.session.commit()
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
        # ELIMINAR RECETAS
        return redirect(url_for("producto.productos"))
    
    return render_template("/producto/eliminarproducto.html", id=prod.id, nombre=prod.nombre, descripcion=prod.descripcion,
        preparacion=prod.preparacion, url=prod.url, merma_esperada=prod.merma_esperada, precio=prod.precio)
