from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import User, Role, roles_users
from sqlalchemy import or_
from . import db

usuario = Blueprint('usuario',  __name__, url_prefix='/usuario')

#MOSTRAR ROL
@usuario.route("/usuarios")
@login_required
@roles_required('ADMINISTRADOR')
def usuarios():
    usuarios = User.query.filter_by(status='1').all()
    roles = roles_users.query.all()
    return render_template('/usuario/usuarios.html', usuarios = usuarios, roles = roles)

#MOSTRAR ROL
@usuario.route("/usuariosinactivos")
@login_required
@roles_required('ADMINISTRADOR')
def usuariosinactivos():
    usuarios = User.query.filter_by(status='0').all()
    roles = roles_users.query.all()
    return render_template('/usuario/usuariosinactivos.html', usuarios = usuarios, roles = roles)

#MOSTRAR ROL
@usuario.route("/buscarusuario", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def buscarusuario():
    if request.method == 'POST':
        parametro =  request.form['parametro']
        print(parametro)

        usuarios = User.query.filter(or_(
            User.id.ilike(f'%{parametro}%'),
            User.nombre.ilike(f'%{parametro}%'),
            User.apellido_paterno.ilike(f'%{parametro}%'),
            User.apellido_materno.ilike(f'%{parametro}%'),
            User.domicilio.ilike(f'%{parametro}%'),
            User.fecha_nacimiento.ilike(f'%{parametro}%'),
            User.rfc.ilike(f'%{parametro}%'),
            User.telefono.ilike(f'%{parametro}%'),
            User.email.ilike(f'%{parametro}%')
        )).all()
        roles = roles_users.query.all()

    return render_template('/usuario/usuariosencontrados.html', usuarios = usuarios, roles = roles)

#AGREGAR ROL
@usuario.route('/registrousuario', methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def registrousuario():
    if request.method == 'POST':
        usuario = User(nombre = request.form.get('nombre'),
                       apellido_paterno = request.form.get('apellido_paterno'),
                       apellido_materno = request.form.get('apellido_materno'),
                       domicilio = request.form.get('domicilio'),
                       fecha_nacimiento = request.form.get('fecha_nacimiento'),
                       rfc = request.form.get('rfc'),
                       telefono = request.form.get('telefono'),
                       correo = request.form.get('correo'))
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for("usuario.usuarios"))
    
    return render_template('/usuario/registrousuario.html')

#AGREGAR ROL
@usuario.route("/modificarusuario", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def modificarusuario():

    if request.method == 'GET':
        id =  request.args.get('id')
        usuario = db.session.query(User).filter(User.id == id).first()
    
    if request.method == 'POST':
        id = request.form.get('id')
        usuario = db.session.query(User).filter(User.id == id).first()
        prov.nombre = request.form.get('nombre')
        prov.apellido_paterno = request.form.get('apellido_paterno')
        prov.apellido_materno = request.form.get('apellido_materno')
        prov.direccion = request.form.get('direccion')
        prov.empresa = request.form.get('empresa')
        prov.rfc = request.form.get('rfc')
        prov.telefono = request.form.get('telefono')
        prov.correo = request.form.get('correo')
        db.session.add(prov)
        db.session.commit()
        return redirect(url_for("proveedor.verproveedores"))
    
    return render_template("/proveedor/modificarproveedor.html", id=prov.id, nombre=prov.nombre, apellido_paterno=prov.apellido_paterno,
        apellido_materno=prov.apellido_materno, direccion=prov.direccion, empresa=prov.empresa, rfc=prov.rfc,
        telefono=prov.telefono, correo=prov.correo)

#AGREGAR ROL
@proveedor.route("/eliminarproveedor", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def eliminar():

    if request.method == 'GET':
        id =  request.args.get('id')
        prov = db.session.query(Proveedor).filter(Proveedor.id == id).first()
    
    if request.method == 'POST':
        id = request.form.get('id')
        prov = db.session.query(Proveedor).filter(Proveedor.id == id).first()
        prov.nombre = request.form.get('nombre')
        prov.apellido_paterno = request.form.get('apellido_paterno')
        prov.apellido_materno = request.form.get('apellido_materno')
        prov.direccion = request.form.get('direccion')
        prov.empresa = request.form.get('empresa')
        prov.rfc = request.form.get('rfc')
        prov.telefono = request.form.get('telefono')
        prov.correo = request.form.get('correo')
        prov.status = False
        db.session.add(prov)
        db.session.commit()
        return redirect(url_for("proveedor.verproveedores"))
    
    return render_template("/proveedor/eliminarproveedor.html", id=prov.id, nombre=prov.nombre, apellido_paterno=prov.apellido_paterno,
        apellido_materno=prov.apellido_materno, direccion=prov.direccion, empresa=prov.empresa, rfc=prov.rfc,
        telefono=prov.telefono, correo=prov.correo)

