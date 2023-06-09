from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, current_user
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import User, Role
from . import db, userDataStore
from .logg import Logger
from datetime import datetime

auth = Blueprint('auth', __name__, url_prefix='/security')
log = Logger('auth')

@auth.route('/login')
def login():
    return render_template('/security/login.html')

@auth.route('/login', methods = ['POST'])
def login_post():
    email = request.form.get('correo')
    password = request.form.get('contrasennia')
    remember = True if request.form.get('remember') else False

    #Consultamos la existencia del usuario
    user = User.query.filter(User.email==email, User.status=='1').first()

    #Verificamos y tomamos el password, se hashea y se compara con el registrado
    if not user or not check_password_hash(user.password, password):
        flash('El usuario y/o la contraseña son incorrectos')
        log.error('Usuario {} no encontrado o la contraseña es incorrecta'.format(email))
        return redirect(url_for('auth.login'))
    
    #Si los datos son correctos le creamos un usuario y accesa
    login_user(user, remember = remember)

    if "ADMINISTRADOR" in [role.name for role in user.roles]:
        log.debug('Usuario {} logueado como Administrador'.format(current_user.email))
        return redirect(url_for('usuario.usuarios'))
    
    if "ALMACENISTA" in [role.name for role in user.roles]:
        log.debug('Usuario {} logueado como Alamcenista'.format(current_user.email))
        return redirect(url_for('materia.materias'))
    
    if "VENDEDOR" in [role.name for role in user.roles]:
        log.debug('Usuario {} logueado como Vendedor'.format(current_user.email))
        return redirect(url_for('producto.productos'))
    
    if "CLIENTE" in [role.name for role in user.roles]:
        log.debug('Usuario {} logueado como Cliente'.format(current_user.email))
    return redirect(url_for('main.index'))

@auth.route('/registro')
def registro():
    return render_template('/security/registro.html', fecha_actual=datetime.now())

@auth.route('/registro', methods = ['POST'])
def registro_post():
    email = request.form.get('correo')
    password = request.form.get('contrasennia')
    nombre = request.form.get('nombre').upper()
    apellido_paterno = request.form.get('apellido_paterno').upper()
    apellido_materno = request.form.get('apellido_materno').upper()
    domicilio = request.form.get('domicilio').upper()
    telefono = request.form.get('telefono')
    rfc = ""
    fecha_nacimiento = request.form.get('fecha_nacimiento')

    #Consultamos si ya está registrado
    user = User.query.filter_by(email=email).first()

    #Si ya está registrado, redireccionamos a registro
    if user:
        flash('El correo electrónico ya existe')
        log.error('El correo {} ya está registrado con una cuenta'.format(email))
        return redirect(url_for('auth.registro'))
    
    #Sino, creamos un usuario y hasheamos la contraseña
    userDataStore.create_user(nombre=nombre, apellido_paterno=apellido_paterno, email=email,apellido_materno=apellido_materno,
                               domicilio=domicilio, fecha_nacimiento=fecha_nacimiento, telefono=telefono, rfc=rfc,
                              password=generate_password_hash(password, method='sha256'))
    
    #Añadimos el usuario a la bd
    db.session.commit()
    #Añadimos el rol
    ultimo_usuario = User.query.order_by(User.id.desc()).first()
    roles = "4"
    rol = Role.query.filter_by(id=roles).first()
    ultimo_usuario.roles.append(rol)
    db.session.commit()
    log.debug('Usuario {} registrado como Cliente'.format(email))

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    log.debug('Usuario {} cerró su sesión'.format(current_user.email))
    #Cerramos la sesión
    logout_user()
    return redirect(url_for('main.index'))