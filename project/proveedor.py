from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import Proveedor
from . import db

proveedor = Blueprint('proveedor', __name__, url_prefix='/proveedor')

@proveedor.route("/proveedores")
@login_required
@roles_accepted('ADMINISTRADOR','ALMACENISTA')
def verproveedores():
    proveedores = Proveedor.query.all()
    return render_template('/proveedor/proveedores.html', proveedores = proveedores)

