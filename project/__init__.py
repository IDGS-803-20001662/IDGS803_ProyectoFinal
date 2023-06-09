import os
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from .logg import Logger

db = SQLAlchemy()
from .models import User, Role
userDataStore = SQLAlchemyUserDatastore(db, User, Role)

def create_app():
    app=Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24) # Clave aleatoria
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://gestor_sushicat:sushicatadmin@localhost/bd_sushicat'
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512' # SALT
    app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'
    app.config['UPLOAD_FOLDER'] = 'static/img/' #FOLDER PARA GUARDAR IMAGENES
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    log = Logger('app')

    db.init_app(app)
    @app.before_first_request
    def create_all():
        db.create_all()
    
    #Conectar modelos al SQLALCHEMY
    security = Security(app, userDataStore)
    log.info('Servidor iniciado')

    #Registramos las rutas para auth, main y admin
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .usuario import usuario as usuario_blueprint
    app.register_blueprint(usuario_blueprint)

    from .proveedor import proveedor  as proveedor_blueprint
    app.register_blueprint(proveedor_blueprint)

    from .producto import producto as producto_blueprint
    app.register_blueprint(producto_blueprint)

    from .materia import materia as materia_blueprint
    app.register_blueprint(materia_blueprint)

    from .pedido import pedido as pedido_blueprint
    app.register_blueprint(pedido_blueprint)

    from .compra import compra as compra_blueprint
    app.register_blueprint(compra_blueprint)

    from .venta import venta as venta_blueprint
    app.register_blueprint(venta_blueprint)

    from .finanzas import finanzas as finanzas_blueprint
    app.register_blueprint(finanzas_blueprint)

    return app
