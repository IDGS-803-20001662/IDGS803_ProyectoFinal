from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import User
from sqlalchemy import or_, and_
from . import db

usuario = Blueprint('usuario',  __name__, url_prefix='/usuario')

#MOSTRAR ROL
@usuario.route("/usuarios")
@login_required
@roles_required('ADMINISTRADOR')
def usuarios():
    usuarios = User.query.filter(User.status=='1', User.rfc != "").all()
    return render_template('/usuario/usuarios.html', usuarios = usuarios)

#MOSTRAR ROL
@usuario.route("/usuariosinactivos")
@login_required
@roles_required('ADMINISTRADOR')
def usuariosinactivos():
    usuarios = User.query.filter(User.status=='0', User.rfc != "").all()
    return render_template('/usuario/usuariosinactivos.html', usuarios = usuarios)

@usuario.route("/clientes")
@login_required
@roles_required('ADMINISTRADOR')
def clientes():
    usuarios = User.query.filter(User.status=='1', User.rfc == "").all()
    return render_template('/usuario/clientes.html', usuarios = usuarios)

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
            User.telefono.ilike(f'%{parametro}%'),
            User.email.ilike(f'%{parametro}%')
        )).all()

    return render_template('/usuario/usuariosencontrados.html', usuarios = usuarios)

#AGREGAR ROL
@usuario.route('/registrousuario', methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def registrousuario():
    if request.method == 'POST':
        dia = request.form.get('dia')
        mes = request.form.get('mes')
        annio = request.form.get('annio')
        fecha_nacimiento = annio+"-"+mes+"-"+dia
        rol = request.form.get('rol')

        usuario = User(nombre = request.form.get('nombre').upper(),
                       apellido_paterno = request.form.get('apellido_paterno').upper(),
                       apellido_materno = request.form.get('apellido_materno').upper(),
                       domicilio = request.form.get('domicilio').upper(),
                       fecha_nacimiento = fecha_nacimiento,
                       rfc = request.form.get('rfc').upper(),
                       telefono = request.form.get('telefono'),
                       email = request.form.get('correo'),
                       password = request.form.get('password'))
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
        fecha_nacimiento=usuario.fecha_nacimiento
        dia=fecha_nacimiento[8:10]
        mes=fecha_nacimiento[5:8]
        annio=fecha_nacimiento[:5]
    
    if request.method == 'POST':
        dia = request.form.get('dia')
        mes = request.form.get('mes')
        annio = request.form.get('annio')
        fecha_nacimiento = annio+"-"+mes+"-"+dia
        rol = request.form.get('rol')
        # password = request.form.get('password')

        
        id = request.form.get('id')
        usuario = db.session.query(User).filter(User.id == id).first()
        usuario.nombre = request.form.get('nombre')
        usuario.apellido_paterno = request.form.get('apellido_paterno')
        usuario.apellido_materno = request.form.get('apellido_materno')
        usuario.domicilio = request.form.get('domicilio')
        usuario.rfc = request.form.get('rfc')
        usuario.telefono = request.form.get('telefono')
        usuario.email = request.form.get('correo')
        usuario.fecha_nacimiento = fecha_nacimiento

        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for("usuario.usuarios"))
    
    return render_template("/usuario/modificarusuario.html", id=usuario.id, nombre=usuario.nombre, apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno, domicilio=usuario.domicilio, rfc=usuario.rfc, dia=dia, mes=mes, annio=annio,
        telefono=usuario.telefono, correo=usuario.email)

#AGREGAR ROL
@usuario.route("/eliminarusuario", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def eliminarusuario():

    if request.method == 'GET':
        id =  request.args.get('id')
        usuario = db.session.query(User).filter(User.id == id).first()
        fecha_nacimiento=usuario.fecha_nacimiento
        dia=fecha_nacimiento[8:10]
        mes=fecha_nacimiento[5:8]
        annio=fecha_nacimiento[:5]
    
    if request.method == 'POST':
        usuario = db.session.query(User).filter(User.id == id).first()
        usuario.nombre = request.form.get('nombre')
        usuario.apellido_paterno = request.form.get('apellido_paterno')
        usuario.apellido_materno = request.form.get('apellido_materno')
        usuario.domicilio = request.form.get('domicilio')
        usuario.rfc = request.form.get('rfc')
        usuario.telefono = request.form.get('telefono')
        usuario.email = request.form.get('correo')
        usuario.fecha_nacimiento = fecha_nacimiento

        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for("usuario.usuarios"))
    
    return render_template("/proveedor/eliminarusuario.html", id=usuario.id, nombre=usuario.nombre, apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno, domicilio=usuario.domicilio, rfc=usuario.rfc, dia=dia, mes=mes, annio=annio,
        telefono=usuario.telefono, correo=usuario.email)

