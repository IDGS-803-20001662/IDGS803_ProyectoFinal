from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import Proveedor
from sqlalchemy import or_
from . import db

proveedor = Blueprint('proveedor', __name__, url_prefix='/proveedor')

@proveedor.route("/proveedores")
@login_required
@roles_accepted('ADMINISTRADOR','ALMACENISTA')
def verproveedores():
    proveedores = Proveedor.query.filter_by(status='1').all()
    return render_template('/proveedor/proveedores.html', proveedores = proveedores)

@proveedor.route("/proveedoresinactivos")
@login_required
@roles_accepted('ADMINISTRADOR','ALMACENISTA')
def verproveedoresinactivos():
    proveedores = Proveedor.query.filter_by(status='0').all()
    return render_template('/proveedor/proveedoresinactivos.html', proveedores = proveedores)

@proveedor.route("/buscarproveedor", methods = ['GET', 'POST'])
@login_required
@roles_accepted('ADMINISTRADOR','ALMACENISTA')
def buscarproveedor():
    if request.method == 'POST':
        parametro =  request.form['parametro']
        parametro = parametro.upper()
        print(parametro)

        proveedores = Proveedor.query.filter(or_(
            Proveedor.id.ilike(f'%{parametro}%'),
            Proveedor.nombre.ilike(f'%{parametro}%'),
            Proveedor.apellido_paterno.ilike(f'%{parametro}%'),
            Proveedor.apellido_materno.ilike(f'%{parametro}%'),
            Proveedor.direccion.ilike(f'%{parametro}%'),
            Proveedor.empresa.ilike(f'%{parametro}%'),
            Proveedor.rfc.ilike(f'%{parametro}%'),
            Proveedor.telefono.ilike(f'%{parametro}%'),
            Proveedor.correo.ilike(f'%{parametro}%')
        )).all()

    return render_template('/proveedor/proveedoresencontrados.html', proveedores = proveedores)

@proveedor.route('/registroproveedor', methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def registroproveedor():
    if request.method == 'POST':
        prov = Proveedor(nombre = request.form.get('nombre').upper(),
                       apellido_paterno = request.form.get('apellido_paterno').upper(),
                       apellido_materno = request.form.get('apellido_materno').upper(),
                       direccion = request.form.get('direccion').upper(),
                       empresa = request.form.get('empresa').upper(),
                       rfc = request.form.get('rfc').upper(),
                       telefono = request.form.get('telefono').upper(),
                       correo = request.form.get('correo'))
        db.session.add(prov)
        db.session.commit()
        return redirect(url_for("proveedor.verproveedores"))
    
    return render_template('/proveedor/registroproveedor.html')

@proveedor.route("/modificarproveedor", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def modificarproveedor():

    if request.method == 'GET':
        id =  request.args.get('id')
        prov = db.session.query(Proveedor).filter(Proveedor.id == id).first()
    
    if request.method == 'POST':
        id = request.form.get('id')
        prov = db.session.query(Proveedor).filter(Proveedor.id == id).first()
        prov.nombre = request.form.get('nombre').upper()
        prov.apellido_paterno = request.form.get('apellido_paterno').upper()
        prov.apellido_materno = request.form.get('apellido_materno').upper()
        prov.direccion = request.form.get('direccion').upper()
        prov.empresa = request.form.get('empresa').upper()
        prov.rfc = request.form.get('rfc').upper()
        prov.telefono = request.form.get('telefono').upper()
        prov.correo = request.form.get('correo')
        db.session.add(prov)
        db.session.commit()
        return redirect(url_for("proveedor.verproveedores"))
    
    return render_template("/proveedor/modificarproveedor.html", id=prov.id, nombre=prov.nombre, apellido_paterno=prov.apellido_paterno,
        apellido_materno=prov.apellido_materno, direccion=prov.direccion, empresa=prov.empresa, rfc=prov.rfc,
        telefono=prov.telefono, correo=prov.correo)

@proveedor.route("/eliminarproveedor", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def eliminarproveedor():

    if request.method == 'GET':
        id =  request.args.get('id')
        prov = db.session.query(Proveedor).filter(Proveedor.id == id).first()
    
    if request.method == 'POST':
        id = request.form.get('id')
        prov = db.session.query(Proveedor).filter(Proveedor.id == id).first()
        prov.nombre = request.form.get('nombre').upper()
        prov.apellido_paterno = request.form.get('apellido_paterno').upper()
        prov.apellido_materno = request.form.get('apellido_materno').upper()
        prov.direccion = request.form.get('direccion').upper()
        prov.empresa = request.form.get('empresa').upper()
        prov.rfc = request.form.get('rfc').upper()
        prov.telefono = request.form.get('telefono').upper()
        prov.correo = request.form.get('correo')
        prov.status = False
        db.session.add(prov)
        db.session.commit()
        return redirect(url_for("proveedor.verproveedores"))
    
    return render_template("/proveedor/eliminarproveedor.html", id=prov.id, nombre=prov.nombre, apellido_paterno=prov.apellido_paterno,
        apellido_materno=prov.apellido_materno, direccion=prov.direccion, empresa=prov.empresa, rfc=prov.rfc,
        telefono=prov.telefono, correo=prov.correo)


