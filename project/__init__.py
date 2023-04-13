import os
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from .models import Usuario, Rol
userDataStore = SQLAlchemyUserDatastore(db, Usuario, Rol)

def create_app():
    app=Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24) # Clave aleatoria
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://gestor_sushicat:sushicatadmin@localhost/bd_sushicat'
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512' # SALT
    app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'

    db.init_app(app)
    @app.before_first_request
    def create_all():
        db.create_all()
    
    #Conectar modelos al SQLALCHEMY
    security = Security(app, userDataStore)

    #Registramos las rutas para auth, main y admin
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .producto import producto as producto_blueprint
    app.register_blueprint(producto_blueprint)

    from .materia import producto as producto_blueprint
    app.register_blueprint(producto_blueprint)

    from .finanzas import finanzas as finanzas_blueprint
    app.register_blueprint(finanzas_blueprint)

    return app
