from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import MateriaPrima, Proveedor
from sqlalchemy import or_
from . import db

materia = Blueprint('materia', __name__, url_prefix='/materia')

@materia.route("/materias")
@login_required
@roles_accepted('ADMINISTRADOR','ALMACENISTA')
def materias():
    materias = MateriaPrima.query.filter_by(status='1').all()
    proveedores = Proveedor.query.filter_by(status='1').all()
    return render_template('/materia/materias.html', materias=materias, proveedores=proveedores)

@materia.route("/materiasinactivas")
@login_required
@roles_accepted('ADMINISTRADOR','ALMACENISTA')
def materiasinactivas():
    materias = MateriaPrima.query.filter_by(status='0').all()
    proveedores = Proveedor.query.filter_by(status='1').all()
    return render_template('/materia/materiasinactivas.html', materias=materias, proveedores=proveedores)

@materia.route("/buscarmateria", methods = ['GET', 'POST'])
@login_required
@roles_accepted('ADMINISTRADOR','ALMACENISTA')
def buscarmateria():
    if request.method == 'POST':
        parametro =  request.form['parametro']
        parametro = parametro.upper()
        print(parametro)

        materias = MateriaPrima.query.filter(or_(
            MateriaPrima.id.ilike(f'%{parametro}%'),
            MateriaPrima.nombre.ilike(f'%{parametro}%'),
            MateriaPrima.descripcion.ilike(f'%{parametro}%'),
            MateriaPrima.perecidad.ilike(f'%{parametro}%'),
            MateriaPrima.medida.ilike(f'%{parametro}%'),
            MateriaPrima.precio.ilike(f'%{parametro}%')
        )).all()
        proveedores = Proveedor.query.filter_by(status='1').all()
    return render_template('/materia/materiasencontradas.html', materias=materias, proveedores=proveedores)

@materia.route("/registrarmateria", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def registrarmateria():

    proveedores = Proveedor.query.filter_by(status='1').all()

    if request.method == 'POST':
        #ingresar proveedor por id
        mat = MateriaPrima(nombre = request.form.get('nombre').upper(),
                           descripcion = request.form.get('descripcion').upper(),
                           perecidad = request.form.get('perecidad').upper(),
                           cant_min = request.form.get('cant_min'),
                           cant_max = request.form.get('cant_max'),
                           medida = request.form.get('medida').upper(),
                           precio = request.form.get('precio'),
                           proveedor_id = request.form.get('proveedor'))
        db.session.add(mat)
        db.session.commit()
        return redirect(url_for("materia.materias"))
    
    return render_template('/materia/registrarmateria.html', proveedores=proveedores)

@materia.route("/modificarmateria", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def modificarmateria():

    if request.method == 'GET':
        id =  request.args.get('id')
        mat = db.session.query(MateriaPrima).filter(MateriaPrima.id == id).first()
        proveedores = Proveedor.query.filter_by(status='1').all()
    
    if request.method == 'POST':
        id = request.form.get('id')
        mat = db.session.query(MateriaPrima).filter(MateriaPrima.id == id).first()
        mat.nombre = request.form.get('nombre').upper()
        mat.descripcion = request.form.get('descripcion').upper()
        mat.perecidad = request.form.get('perecidad').upper()
        mat.cant_min = request.form.get('cant_min')
        mat.cant_max = request.form.get('cant_max')
        mat.medida = request.form.get('medida').upper()
        mat.precio = request.form.get('precio')
        mat.proveedor_id = request.form.get('proveedor')
        db.session.add(mat)
        db.session.commit()
        return redirect(url_for("materia.materias"))
    
    return render_template("/materia/modificarmateria.html", id=mat.id, nombre=mat.nombre, descripcion=mat.descripcion,
        perecidad=mat.perecidad, cant_min=mat.cant_min, cant_max=mat.cant_max, medida=mat.medida, precio=mat.precio,
        proveedor_id=mat.proveedor_id, proveedor_empresa=mat.proveedor.empresa, proveedores=proveedores)

@materia.route("/eliminarmateria", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def eliminarmateria():

    if request.method == 'GET':
        id =  request.args.get('id')
        mat = db.session.query(MateriaPrima).filter(MateriaPrima.id == id).first()
        proveedores = Proveedor.query.filter_by(status='1').all()

    if request.method == 'POST':
        id = request.form.get('id')
        mat = db.session.query(MateriaPrima).filter(MateriaPrima.id == id).first()
        mat.nombre = request.form.get('nombre').upper()
        mat.descripcion = request.form.get('descripcion').upper()
        mat.perecidad = request.form.get('perecidad').upper()
        mat.cant_min = request.form.get('cant_min')
        mat.cant_max = request.form.get('cant_max')
        mat.medida = request.form.get('medida').upper()
        mat.precio = request.form.get('precio')
        mat.proveedor_id = request.form.get('proveedor')
        mat.status = False
        db.session.add(mat)
        db.session.commit()
        return redirect(url_for("materia.materias"))

    return render_template("/materia/eliminarmateria.html", id=mat.id, nombre=mat.nombre, descripcion=mat.descripcion,
        perecidad=mat.perecidad, cant_min=mat.cant_min, cant_max=mat.cant_max, medida=mat.medida, precio=mat.precio,
        proveedor_id=mat.proveedor_id, proveedor_empresa=mat.proveedor.empresa, proveedores=proveedores)

