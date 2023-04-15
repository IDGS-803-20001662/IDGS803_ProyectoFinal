from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import User, Role
from . import db, userDataStore

auth = Blueprint('auth', __name__, url_prefix='/security')

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
        return redirect(url_for('auth.login'))
    #Si los datos son correctos le creamos un usuario y accesa
    login_user(user, remember = remember)

    if user.id == 1:
        return redirect(url_for('proveedor.verproveedores'))
    
    return redirect(url_for('main.index'))

@auth.route('/registro')
def registro():
    return render_template('/security/registro.html')

@auth.route('/registro', methods = ['POST'])
def registro_post():
    email = request.form.get('correo')
    password = request.form.get('contrasennia')
    nombre = request.form.get('nombre').upper()
    apellido_paterno = request.form.get('apellido_paterno').upper()
    apellido_materno = request.form.get('apellido_materno').upper()
    domicilio = request.form.get('domicilio').upper()
    dia = request.form.get('dia')
    mes = request.form.get('mes')
    annio = request.form.get('annio')
    telefono = request.form.get('telefono')
    rfc = ""
    fecha_nacimiento = annio+"-"+mes+"-"+dia

    #Consultamos si ya está registrado
    user = User.query.filter_by(email=email).first()

    #Si ya está registrado, redireccionamos a registro
    if user:
        flash('El correo electrónico ya existe')
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


    return redirect(url_for('auth.login'))

@auth.route("/recuperarcontrasennia", methods = ['GET', 'POST'])
def recuperarcontraseña():
    
    if request.method == 'POST':
        email =  request.form.get('correo')
        password = request.form.get('contrasennia')
        
        usuario = db.session.query(User).filter(User.email == email).first()
        if usuario:
            usuario.password = generate_password_hash(password, method='sha256')
        else:
            flash('El usuario y/o la contraseña son incorrectos')

        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for("auth.login"))
    
    return render_template("/security/recuperarcontrasennia.html")

@auth.route('/logout')
@login_required
def logout():
    #Cerramos la sesión
    logout_user()
    return redirect(url_for('main.index'))