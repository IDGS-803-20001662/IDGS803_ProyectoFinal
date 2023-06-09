from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import User, Role
from sqlalchemy import or_, and_
from . import db, userDataStore
from datetime import datetime
from .logg import Logger

usuario = Blueprint('usuario',  __name__, url_prefix='/usuario')
log = Logger("usuario")

#MOSTRAR ROL
@usuario.route("/usuarios")
@login_required
@roles_required('ADMINISTRADOR')
def usuarios():
    usuarios = User.query.filter(User.status=='1', User.rfc != "").all()
    if not usuarios:
        log.critical('El módulo de Usuarios no ha cargado la información de los usuarios')
    return render_template('/usuario/usuarios.html', usuarios = usuarios)

#MOSTRAR ROL
@usuario.route("/usuariosinactivos")
@login_required
@roles_required('ADMINISTRADOR')
def usuariosinactivos():
    usuarios = User.query.filter(User.status=='0', User.rfc != "").all()
    if not usuarios:
        log.critical('El módulo de Usuarios no ha cargado la información de los usuarios inactivos')
    return render_template('/usuario/usuariosinactivos.html', usuarios = usuarios)

@usuario.route("/clientes")
@login_required
@roles_required('ADMINISTRADOR')
def clientes():
    usuarios = User.query.filter(User.status=='1', User.rfc == "").all()
    if not usuarios:
        log.critical('El módulo de Usuarios no ha cargado la información de los clientes')
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

        if not usuarios:
            log.exception('El módulo de Usuarios no ha cargado la información de los usuarios coincidentes')

    return render_template('/usuario/usuariosencontrados.html', usuarios = usuarios)

#AGREGAR ROL
@usuario.route('/registrousuario', methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def registrousuario():
    if request.method == 'POST':
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        rol = request.form.get('rol')
        nombre = request.form.get('nombre').upper()
        apellido_paterno = request.form.get('apellido_paterno').upper()
        apellido_materno = request.form.get('apellido_materno').upper()
        domicilio = request.form.get('domicilio').upper()
        fecha_nacimiento = fecha_nacimiento
        rfc = request.form.get('rfc').upper()
        telefono = request.form.get('telefono')
        email = request.form.get('correo')
        password = request.form.get('contrasennia')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('El correo electrónico ya existe')
            log.error("El correo {} ya existe, el usuario no puede ser registrado".format(email))
            return redirect(url_for('usuario.registrousuario'))
        
        userDataStore.create_user(nombre=nombre, apellido_paterno=apellido_paterno, email=email,apellido_materno=apellido_materno,
                               domicilio=domicilio, fecha_nacimiento=fecha_nacimiento, telefono=telefono, rfc=rfc,
                              password=generate_password_hash(password, method='sha256'))
        db.session.commit()

        ultimo_usuario = User.query.order_by(User.id.desc()).first()
        roles = rol
        rol = Role.query.filter_by(id=roles).first()
        ultimo_usuario.roles.append(rol)
        db.session.commit()
        log.debug('El usuario {} fue registrado por el usuario {}'.format(email, current_user.email))

        return redirect(url_for("usuario.usuarios"))
    
    return render_template('/usuario/registrousuario.html', fecha_actual=datetime.now())

#AGREGAR ROL
@usuario.route("/modificarusuario", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def modificarusuario():

    if request.method == 'GET':
        id =  request.args.get('id')
        usuario = db.session.query(User).filter(User.id == id).first()
        for role in usuario.roles:
            rol = role.name
            rol_pasado = role.id
    
    if request.method == 'POST':
        id = request.form.get('id')
        usuario = db.session.query(User).filter(User.id == id).first()
        usuario.nombre = request.form.get('nombre')
        usuario.apellido_paterno = request.form.get('apellido_paterno')
        usuario.apellido_materno = request.form.get('apellido_materno')
        usuario.domicilio = request.form.get('domicilio')
        usuario.rfc = request.form.get('rfc')
        usuario.telefono = request.form.get('telefono')
        usuario.email = request.form.get('correo')
        usuario.fecha_nacimiento = request.form.get('fecha_nacimiento')
        rol_n = request.form.get('rol')
        rol_pasado = request.form.get('rol_p')

        db.session.add(usuario)
        db.session.commit()
        log.warning('El usuario {} fue modificado por el usuario {}'.format(usuario.email, current_user.email))

        roles_ = rol_n
        rol_n = Role.query.filter_by(id=roles_).first()
        rol_p = Role.query.filter_by(id=rol_pasado).first()
        usuario.roles.append(rol_n)
        db.session.commit()
        usuario.roles.remove(rol_p)
        db.session.commit()

        return redirect(url_for("usuario.usuarios"))
    
    return render_template("/usuario/modificarusuario.html", id=usuario.id, nombre=usuario.nombre, apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno, domicilio=usuario.domicilio, rfc=usuario.rfc, fecha_nacimiento=usuario.fecha_nacimiento,
        telefono=usuario.telefono, correo=usuario.email, rol=rol, rol_id=rol_pasado, fecha_actual=datetime.now())

@usuario.route("/eliminarusuario", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def eliminarusuario():

    if request.method == 'GET':
        id =  request.args.get('id')
        usuario = db.session.query(User).filter(User.id == id).first()
        for role in usuario.roles:
            rol = role.name
    
    if request.method == 'POST':
        id =  request.form.get('id')
        usuario = db.session.query(User).filter(User.id == id).first()
        usuario.nombre = request.form.get('nombre')
        usuario.apellido_paterno = request.form.get('apellido_paterno')
        usuario.apellido_materno = request.form.get('apellido_materno')
        usuario.domicilio = request.form.get('domicilio')
        usuario.rfc = request.form.get('rfc')
        usuario.telefono = request.form.get('telefono')
        usuario.email = request.form.get('correo')
        usuario.fecha_nacimiento = request.form.get('fecha_nacimiento')
        usuario.status = False

        db.session.add(usuario)
        db.session.commit()
        log.warning('El usuario {} fue eliminado por el usuario {}'.format(usuario.email, current_user.email))
        return redirect(url_for("usuario.usuarios"))
    
    return render_template("/usuario/eliminarusuario.html", id=usuario.id, nombre=usuario.nombre, apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno, domicilio=usuario.domicilio, rfc=usuario.rfc, fecha_nacimiento=usuario.fecha_nacimiento,
        telefono=usuario.telefono, correo=usuario.email, rol=rol)

@usuario.route("/modificarperfil", methods = ['GET', 'POST'])
@login_required
def modificarperfil():

    if request.method == 'GET':
        id =  current_user.id
        usuario = db.session.query(User).filter(User.id == id).first()
    
    if request.method == 'POST':
        
        id = current_user.id
        usuario = db.session.query(User).filter(User.id == id).first()
        usuario.nombre = request.form.get('nombre')
        usuario.apellido_paterno = request.form.get('apellido_paterno')
        usuario.apellido_materno = request.form.get('apellido_materno')
        usuario.domicilio = request.form.get('domicilio')
        usuario.rfc = ""
        usuario.telefono = request.form.get('telefono')
        usuario.email = request.form.get('correo')
        usuario.fecha_nacimiento = request.form.get('fecha_nacimiento')

        db.session.add(usuario)
        db.session.commit()
        log.warning('El usuario {} modificó su perfil'.format(current_user.email))
        return redirect(url_for("main.index")) # revisar direccion
    
    return render_template("/usuario/modificarperfil.html", nombre=usuario.nombre, apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno, domicilio=usuario.domicilio, rfc=usuario.rfc, fecha_nacimiento=usuario.fecha_nacimiento,
        telefono=usuario.telefono, correo=usuario.email, fecha_actual=datetime.now())

@usuario.route("/cambiarcontrasennia", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def cambiarcontraseña():

    if request.method == 'GET':
        id =  request.args.get('id')
        usuario = db.session.query(User).filter(User.id == id).first()
    
    if request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('contrasennia')
        
        usuario = db.session.query(User).filter(User.id == id).first()
        usuario.password = generate_password_hash(password, method='sha256')

        db.session.add(usuario)
        db.session.commit()
        log.warning('El usuario {} cambió la contraseña del usuario {}'.format(usuario.email, current_user.email))
        return redirect(url_for("usuario.usuarios"))
    
    return render_template("/usuario/cambiarcontrasennia.html", correo=usuario.email, id=usuario.id)

