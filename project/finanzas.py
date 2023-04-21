from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import Gasto
from sqlalchemy import or_, create_engine, text
import datetime
from . import db

finanzas = Blueprint('finanzas', __name__, url_prefix='/finanzas')
fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
annio_actual = datetime.datetime.now().year

engine = create_engine('mysql+mysqldb://gestor_sushicat:sushicatadmin@localhost/bd_sushicat')

@finanzas.route("/gastos")
@login_required
@roles_accepted('ADMINISTRADOR')
def vercostos():
    gastos = Gasto.query.filter_by(status='1').all()
    return render_template('/finanzas/gastos.html', gastos = gastos, annio_actual = annio_actual)

@finanzas.route("/gastosinactivos")
@login_required
@roles_accepted('ADMINISTRADOR')
def vercostosinactivos():
    gastos = Gasto.query.filter_by(status='0').all()
    return render_template('/finanzas/gastosinactivos.html', gastos = gastos)

@finanzas.route("/buscargasto", methods=["GET", "POST"])
@login_required
@roles_accepted('ADMINISTRADOR')
def buscargasto():
    if request.method == 'POST':
        parametro =  request.form['parametro']
        parametro = parametro.upper()
        print(parametro)

        gastos = Gasto.query.filter(or_(
            Gasto.id.ilike(f'%{parametro}%'),
            Gasto.descripcion.ilike(f'%{parametro}%'),
            Gasto.costo.ilike(f'%{parametro}%'),
            Gasto.fecha.ilike(f'%{parametro}%'),
        )).all()

    return render_template('/finanzas/gastosencontrados.html', gastos = gastos)

@finanzas.route('/registrogasto', methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def registrogasto():
    if request.method == 'POST':
        gasto1 = Gasto(descripcion = request.form.get('descripcion'),
                       costo = request.form.get('costo'),
                       fecha = request.form.get('fecha'))
        db.session.add(gasto1)
        db.session.commit()
        return redirect(url_for("finanzas.vercostos"))
    
    return render_template('/finanzas/registrogasto.html', fecha_actual = fecha_actual)

@finanzas.route("/modificargasto", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def modificargasto():

    if request.method == 'GET':
        id =  request.args.get('id')
        gasto1 = db.session.query(Gasto).filter(Gasto.id == id).first()
    
    if request.method == 'POST':
        id = request.form.get('id')
        gasto1 = db.session.query(Gasto).filter(Gasto.id == id).first()
        gasto1.descripcion = request.form.get('descripcion')
        gasto1.costo = request.form.get('costo')
        gasto1.fecha = request.form.get('fecha')
        db.session.add(gasto1)
        db.session.commit()
        return redirect(url_for("finanzas.vercostos"))
    
    return render_template("/finanzas/modificargasto.html", id=gasto1.id, descripcion=gasto1.descripcion, costo=gasto1.costo,
        fecha=gasto1.fecha, fecha_actual = fecha_actual)

@finanzas.route("/eliminargasto", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def eliminar():

    if request.method == 'GET':
        id =  request.args.get('id')
        gasto1 = db.session.query(Gasto).filter(Gasto.id == id).first()
    
    if request.method == 'POST':
        id = request.form.get('id')
        gasto1 = db.session.query(Gasto).filter(Gasto.id == id).first()
        gasto1.descripcion = request.form.get('descripcion')
        gasto1.costo = request.form.get('costo')
        gasto1.fecha = request.form.get('fecha')
        gasto1.status = False
        db.session.add(gasto1)
        db.session.commit()
        return redirect(url_for("finanzas.vercostos"))
    
    return render_template("/finanzas/eliminargasto.html", id=gasto1.id, descripcion=gasto1.descripcion, costo=gasto1.costo,
        fecha=gasto1.fecha, fecha_actual = fecha_actual)

@finanzas.route("/ganancias", methods = ['GET', 'POST'])
@login_required
@roles_required('ADMINISTRADOR')
def ganancias():
    if request.method == "POST":
        connection = engine.raw_connection()
        try:
            annio = int(request.form["annio"])
            cursor_obj = connection.cursor()
            cursor_obj.callproc("reporte_ganancias", [annio])
            reporte = list(cursor_obj.fetchall())
            cursor_obj.close()
            connection.commit()
        finally:
            connection.close()
    return render_template("/finanzas/ganancias.html", reporte = reporte, annio = annio)