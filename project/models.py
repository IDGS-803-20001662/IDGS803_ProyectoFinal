from . import db
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
import datetime
from wtforms import StringField, PasswordField, BooleanField, IntegerField, HiddenField, SubmitField
from wtforms.validators import DataRequired, NumberRange

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(20), nullable=False)
    apellido_paterno = db.Column(db.String(30), nullable=False)
    apellido_materno = db.Column(db.String(30), nullable=True)
    domicilio = db.Column(db.String(150), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    telefono = db.Column(db.String(10), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean(), nullable=False, default = True)
    rfc = db.Column(db.String(13), nullable=True)
    active = db.Column(db.Boolean())
    create_date = db.Column(db.DateTime, default = datetime.datetime.now)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    pedido = db.relationship("Pedido", back_populates="user")
    venta = db.relationship("Venta", back_populates="user")
    compra = db.relationship("Compra", back_populates="user")

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(20), nullable=False)
    apellido_paterno = db.Column(db.String(30), nullable=False)
    apellido_materno = db.Column(db.String(30), nullable=True)
    direccion = db.Column(db.String(150), nullable=True)
    empresa = db.Column(db.String(20), nullable=False)
    rfc = db.Column(db.String(13), nullable=True)
    telefono = db.Column(db.String(10), nullable=True)
    correo = db.Column(db.String(50), nullable=True)
    status = db.Column(db.Boolean(), nullable=False, default = True)
    create_date = db.Column(db.DateTime, default = datetime.datetime.now)
    materia_prima = db.relationship("MateriaPrima", back_populates="proveedor")

class MateriaPrima(db.Model):
    __tablename__ = 'materia_prima'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nombre = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)
    perecidad =  db.Column(db.String(30), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    cant_min = db.Column(db.Integer, nullable=False)
    cant_max = db.Column(db.Integer, nullable=False)
    medida =  db.Column(db.String(20), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    proveedor_id = db.Column(db.Integer(), db.ForeignKey('proveedor.id'))
    status = db.Column(db.Boolean(), nullable=False, default = True)
    create_date = db.Column(db.DateTime, default = datetime.datetime.now)
    proveedor = db.relationship("Proveedor", back_populates="materia_prima")
    receta = db.relationship("Receta", back_populates="materia_prima")
    detalle_pedido = db.relationship("DetallePedido", back_populates="materia_prima")

class Receta(db.Model):
    __tablename__ = 'receta'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    producto_id = db.Column(db.Integer(), db.ForeignKey('producto.id'))
    materia_prima_id = db.Column(db.Integer(), db.ForeignKey('materia_prima.id'))
    cantidad = db.Column(db.Float, nullable=False)
    medida =  db.Column(db.String(20), nullable=False)
    materia_prima = db.relationship("MateriaPrima", back_populates="receta")
    producto = db.relationship("Producto", back_populates="receta")

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nombre = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)
    preparacion =  db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=True)
    merma_esperada = db.Column(db.Float, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean(), nullable=False, default = True)
    create_date = db.Column(db.DateTime, default = datetime.datetime.now)
    receta = db.relationship("Receta", back_populates="producto")
    detalle_pedido = db.relationship("DetallePedido", back_populates="producto")
    producto_en = db.relationship('Carrito_Producto', backref='Producto', lazy='dynamic')
    def __repr__(self):
	
      return '<Producto %r>' % (self.nombre)

class Gasto(db.Model):
    __tablename__ = 'gasto'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    descripcion = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=True)
    costo = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean(), nullable=False, default = True)

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    fecha = db.Column(db.DateTime, nullable=False, default = datetime.datetime.now)
    usuario_id = db.Column(db.Integer(), db.ForeignKey('user.id')) # cliente o almacenista
    domicilio_entrega = db.Column(db.String(250), nullable=True)
    tipo_entrega = db.Column(db.Boolean(), nullable=True) # 40 pesos por envio #DOMICILIO O EN RESTAURANTE
    forma_pago = db.Column(db.Boolean(), nullable=True) # por el momento puro efectivo
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer(), nullable=False, default = 1) #REGISTRADO, EN PROCESO, ENTREGADO, CANCELADO
    tipo_pedido = db.Column(db.Boolean(), nullable=False, default = True) #CLIENTE O PROVEEDOR
    user = db.relationship("User", back_populates="pedido")
    venta = db.relationship("Venta", back_populates="pedido")
    compra = db.relationship("Compra", back_populates="pedido")
    detalle_pedido = db.relationship("DetallePedido", back_populates="pedido")

class Venta(db.Model):
    __tablename__ = 'venta'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    fecha = db.Column(db.DateTime, nullable=False, default = datetime.datetime.now)
    pedido_id = db.Column(db.Integer(), db.ForeignKey('pedido.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    total = db.Column(db.Float, nullable=False)
    pedido = db.relationship("Pedido", back_populates="venta")
    user = db.relationship("User", back_populates="venta") #vendedor 

class Compra(db.Model):
    __tablename__ = 'compra'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    fecha = db.Column(db.DateTime, nullable=False, default = datetime.datetime.now)
    pedido_id = db.Column(db.Integer(), db.ForeignKey('pedido.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    total = db.Column(db.Float, nullable=False)
    pedido = db.relationship("Pedido", back_populates="compra")
    user = db.relationship("User", back_populates="compra") # almacenista

class DetallePedido(db.Model):
    __tablename__ = 'detalle_pedido'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    pedido_id = db.Column(db.Integer(), db.ForeignKey('pedido.id'))
    producto_id = db.Column(db.Integer(), db.ForeignKey('producto.id'))
    materia_prima_id = db.Column(db.Integer(), db.ForeignKey('materia_prima.id'))
    medida = db.Column(db.String(20), nullable=True)
    cantidad = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    pedido = db.relationship("Pedido", back_populates="detalle_pedido")
    producto = db.relationship("Producto", back_populates="detalle_pedido")
    materia_prima = db.relationship("MateriaPrima", back_populates="detalle_pedido")

class Carrito(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
	carrito_tiene = db.relationship('Carrito_Producto', backref='Carrito', lazy='dynamic')

	# def __init__(self, id_user):
	# 	self.id_user = id_user
	# 	self.fecha = datetime.now()

	def __repr__(self):
		return '<Carrito %r>' % (self.id)

class Carrito_Producto(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_carrito = db.Column(db.Integer, db.ForeignKey('carrito.id'))
	id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'))
	cantidad = db.Column(db.Integer)
	producto = db.relationship('Producto', lazy=True, uselist=False)

	def __repr__(self):
		return '<Carrito_Producto %r>' % (self.id)
        
class AgregarForm(FlaskForm):
    cantidad = IntegerField("Cantidad", validators=[DataRequired("Se requiere la cantidad"),
                                                     NumberRange(min=1, message="El valor debe de ser igual o mayor a 1")])
    id_producto = HiddenField('id producto')
    save = SubmitField('Agregar')
