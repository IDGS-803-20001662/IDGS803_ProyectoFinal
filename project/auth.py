from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import User
from . import db, userDataStore

auth = Blueprint('auth', __name__, url_prefix='/security')

@auth.route('/login')
def login():
    return render_template('/security/login.html')

@auth.route('/login', methods = ['POST'])
def login_post():
    correo = request.form.get('correo')
    contrasennia = request.form.get('contrasennia')
    remember = True if request.form.get('remember') else False

    #Consultamos la existencia del usuario
    user = User.query.filter_by(correo=correo).first()

    #Verificamos y tomamos el password, se hashea y se compara con el registrado
    if not user or not check_password_hash(user.contrasennia, contrasennia):
        flash('El usuario y/o la contraseña son incorrectos')
        return redirect(url_for('auth.login'))
    #Si los datos son correctos le creamos un usuario y accesa
    login_user(user, remember = remember)

    #if user.id == 1:
    #    return redirect(url_for('admin.administracion'))
    #
    #return redirect(url_for('admin.productos'))

@auth.route('/registro')
def registro():
    return render_template('/security/registro.html')

#@auth.route('/registro', methods = ['POST'])
#def registro_post():
    correo = request.form.get('email')
    contrasennia = request.form.get('password')
    nombre = request.form.get('name')
    apellido_paterno = request.form.get('lastname')

    #Consultamos si ya está registrado
    user = User.query.filter_by(email=email).first()

    #Si ya está registrado, redireccionamos a registro
    if user:
        flash('El correo electrónico ya existe')
        return redirect(url_for('auth.register'))
    
    #Sino, creamos un usuario y hasheamos la contraseña
    userDataStore.create_user(name=name, lastname=lastname, email=email, password=generate_password_hash(password, method='sha256'))
    
    #Añadimos el usuario a la bd
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    #Cerramos la sesión
    logout_user()
    return redirect(url_for('main.index'))