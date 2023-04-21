from flask import Blueprint, render_template
from flask import Blueprint, render_template
from .models import Producto

main = Blueprint('main',__name__)

@main.route('/')
def index():
    productos = Producto.query.filter_by(status='1').all()
    return render_template('index.html', productos=productos)

@main.route('/contacto')
def contacto():
    return render_template('contacto.html')

@main.route('/conocenos')
def conocenos():
    return render_template('conocenos.html')

@main.route('/terminosycondiciones')
def terminosycondiciones():
    return render_template('terminos.html')

@main.route('/avisolegal')
def avisolegal():
    return render_template('aviso.html')