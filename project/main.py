from flask import Blueprint, render_template
from flask import Blueprint, render_template
from .models import Producto

main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index.html')

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