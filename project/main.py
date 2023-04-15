from flask import Blueprint, render_template

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