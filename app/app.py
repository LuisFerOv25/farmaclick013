from flask import Flask,abort
from flask import render_template
from flask import request,session
from datetime import date
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import make_response
from flask import jsonify
from datetime import timedelta
from os import listdir
from babel import numbers, dates
from datetime import date, datetime, time
from flask_babel import Babel, gettext, refresh; refresh()
from controller import *  # Importando mis Funciones
from bd import *  # Importando conexion BD
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import re
from flask import *
from flask import render_template
from datetime import date
from flask import request, session
import controller
from flask import Flask, url_for, redirect
import hashlib
import os
from flask import render_template,abort
from flask import Flask,request,url_for,redirect

from flask_babel import Babel, gettext, refresh; refresh()
import babel.dates

app = Flask(__name__)
app.secret_key = '97110c78ae51a45af397be6534caef90ebb9b1dcb3380af008f90b23a5d1616bf19bc29098105da20fe'
import os
import babel.dates

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.environ.setdefault('BABEL_DEFAULT_LOCALE', 'es')
babel = Babel(app)
    
def get_locale():
    return request.accept_languages.best_match(['en', 'es', 'de', 'fr'])

babel = Babel(app, locale_selector=get_locale)

sentry_sdk.init(
    dsn="https://47b422c23c014fec8d53ccc9dc0e3e61@o4504709798952960.ingest.sentry.io/4504709801443328",
    integrations=[
        FlaskIntegration(),
    ],
    traces_sample_rate=1.0
)










@app.route('/home_admin/')
def home_admin():
    translations = {
        'usrreg': gettext('Usuarios Registrados'),
        'titadm': gettext('Administradores'),
        'reg': gettext('Registrados'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    
    
    admin = controller.user_cant_admin()
    cliente = controller.user_cant_client()
    return render_template("home.html", admin=admin,cliente=cliente,dataLogin= dataLoginSesion(),
                           **dict(translations.items()))    


@app.route("/registrar_producto", methods=["POST"])
def registrar_producto():
    translations = {
        'usrreg': gettext('Usuarios Registrados'),
        'titadm': gettext('Administradores'),
        'reg': gettext('Registrados'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    cantidad = request.form["cantidad"]
    precio = request.form["precio"]
    proveedor = request.form["proveedor"]
    fecha_vencimiento = request.form["fecha_vencimiento"]
    categoria = request.form["categoria"]
    
    imagen = request.files['imagen']

    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        
        imagen.save(os.path.join(config['UPLOAD_FOLDER'], filename))
        imagename = filename
    controller.insertar_producto(nombre, descripcion, cantidad, precio,proveedor,fecha_vencimiento,imagename,categoria)
    # De cualquier modo, y si todo fue bien, redireccionar
    return render_template("home.html",dataLogin= dataLoginSesion(),**dict(translations.items()))

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/cuidado_personal/')
def cuidado_personal():
    translations = {
        'titadm': gettext('Administracion de productos de cuidado personal'),
        'descper': gettext('Esta sección permite operar sobre los productos de cuidado personal'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'adnom': gettext('Nombre'),
        'addes': gettext('Descripcion'),
        'adcant': gettext('Cantidad'),
        'adprec': gettext('Precio'),
        'adprov': gettext('Proveedor'),
        'adfech': gettext('Fecha Vencimiento'),
        'adimg': gettext('Imagen'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titedit': gettext('Edicion de datos'),
        'desedit': gettext('Esta sección permite operar sobre los productos'),
    }
    productos = controller.producto_personal()
    return render_template("cuidadopersonal.html", productos=productos,dataLogin= dataLoginSesion(),**dict(translations.items()))

@app.route("/cuidado_personal_pag/<number_page>")
def page_cuidado_p(number_page):
    translations = {
        'titadm': gettext('Administracion de productos de cuidado personal'),
        'descper': gettext('Esta sección permite operar sobre los productos de cuidado personal'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_page == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 1 LIMIT 0,10")
    if number_page == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 1 LIMIT 10,10")
    if number_page == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 20,10")
    if number_page == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 30,10")
        
    if number_page == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 40,10")
    if number_page == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 50,10")
    if number_page == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 60,10")
    if number_page == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 70,10")
    if number_page == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 80,10")
    if number_page == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 90,10")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('cuidadopersonal.html', productos=productos ,dataLogin= dataLoginSesion(),**dict(translations.items()))   
  
@app.route('/dermacosmetico/')
def dermacosmetico():
    translations = {
        'titderm': gettext('Administracion de productos dermacosmeticos'),
        'desderma': gettext('Esta sección permite operar sobre los productos para el cuidado y tratamiento de la piel'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'adnom': gettext('Nombre'),
        'addes': gettext('Descripcion'),
        'adcant': gettext('Cantidad'),
        'adprec': gettext('Precio'),
        'adprov': gettext('Proveedor'),
        'adfech': gettext('Fecha Vencimiento'),
        'adimg': gettext('Imagen'),
        'expl': gettext('Abrir Explorador'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titedit': gettext('Edicion de datos'),
        'desedit': gettext('Esta sección permite operar sobre los productos'),
    }
    productos = controller.producto_dermacosmetico()
    return render_template("dermacos.html", productos=productos,dataLogin= dataLoginSesion(),**dict(translations.items()))

@app.route("/dermacosmetico_pag/<number_pag>")
def dermacosmetico_pag(number_pag):
    translations = {
        'titderm': gettext('Administracion de productos dermacosmeticos'),
        'desderma': gettext('Esta sección permite operar sobre los productos para el cuidado y tratamiento de la piel'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 2 LIMIT 0,10")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 2 LIMIT 10,10")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 20,10")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 30,10")
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 40,10")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 50,10")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 60,10")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 70,10")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 80,10")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 90,10")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('dermacos.html', productos=productos ,dataLogin= dataLoginSesion(),**dict(translations.items())) 

@app.route('/nutricional/')
def nutricional():
    
    translations = {
        'titnut': gettext('Administracion de productos nutricionales'),
        'descnut': gettext('Esta sección permite operar sobre los productos nutricionales'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'adnom': gettext('Nombre'),
        'addes': gettext('Descripcion'),
        'adcant': gettext('Cantidad'),
        'adprec': gettext('Precio'),
        'adprov': gettext('Proveedor'),
        'adfech': gettext('Fecha Vencimiento'),
        'adimg': gettext('Imagen'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titedit': gettext('Edicion de datos'),
        'desedit': gettext('Esta sección permite operar sobre los productos'),
    }    
    
    productos = controller.producto_nutricional()
    return render_template("nutricional.html", productos=productos,dataLogin= dataLoginSesion(),**dict(translations.items()))

@app.route("/nutricional_pag/<number_pag>")
def nutricional_pag(number_pag):

    translations = {
        'titnut': gettext('Administracion de productos nutricionales'),
        'descnut': gettext('Esta sección permite operar sobre los productos nutricionales'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 3 LIMIT 0,10")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 3 LIMIT 10,10")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 20,10")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 30,10")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 40,10")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 50,10")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 60,10")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 70,10")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 80,10")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 90,10")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('nutricional.html', productos=productos ,dataLogin= dataLoginSesion(),**dict(translations.items()))
 
@app.route('/bebe/')
def bebe():
    
    translations = {
        'titbeb': gettext('Administracion de productos para bebé'),
        'descnut': gettext('Esta sección permite operar sobre los productos para el cuidado del bebé'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'adnom': gettext('Nombre'),
        'addes': gettext('Descripcion'),
        'adcant': gettext('Cantidad'),
        'adprec': gettext('Precio'),
        'adprov': gettext('Proveedor'),
        'adfech': gettext('Fecha Vencimiento'),
        'adimg': gettext('Imagen'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titedit': gettext('Edicion de datos'),
        'desedit': gettext('Esta sección permite operar sobre los productos'),
    }       
    
    productos = controller.producto_bebe()
    return render_template("bebe.html", productos=productos,dataLogin= dataLoginSesion(),**dict(translations.items()))

@app.route("/bebe_pag/<number_pag>")
def page_bebe(number_pag):
    translations = {
        'titbeb': gettext('Administracion de productos para bebé'),
        'descnut': gettext('Esta sección permite operar sobre los productos para el cuidado del bebé'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 4 LIMIT 0,10")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 4 LIMIT 10,10")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 20,10")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 30,10")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 40,10")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 50,10")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 60,10")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 70,10")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 80,10")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 90,10")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('bebe.html', productos=productos ,dataLogin= dataLoginSesion(),**dict(translations.items())) 

@app.route('/medicamento/')
def medicamento():
    translations = {
        'titmed': gettext('Administracion de medicamentos en general'),
        'descmed': gettext('Esta sección permite operar sobre medicamentos de diferentes tipos y/o presentaciones'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'adnom': gettext('Nombre'),
        'addes': gettext('Descripcion'),
        'adcant': gettext('Cantidad'),
        'adprec': gettext('Precio'),
        'adprov': gettext('Proveedor'),
        'adfech': gettext('Fecha Vencimiento'),
        'adimg': gettext('Imagen'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titedit': gettext('Edicion de datos'),
        'desedit': gettext('Esta sección permite operar sobre los productos'),  
    }  
    productos = controller.producto_medicamento()
    return render_template("medicamento.html", productos=productos,dataLogin= dataLoginSesion(),**dict(translations.items()))

@app.route("/medicamentos_pag/<number_pag>")
def medicamentos_pag(number_pag):
    translations = {
        'titmed': gettext('Administracion de medicamentos en general'),
        'descmed': gettext('Esta sección permite operar sobre medicamentos de diferentes tipos y/o presentaciones'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 5 LIMIT 0,10")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 5 LIMIT 10,10")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 20,10")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 30,10")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 40,10")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 50,10")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 60,10")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 70,10")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 80,10")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 90,10")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('medicamento.html', productos=productos ,dataLogin= dataLoginSesion(),**dict(translations.items()))


# Gestion de usuarios

@app.route('/gestionadmin/')
def gestionadmin():
    usuarios = controller.usuario_admin()
    translations = {
        'titgesadm': gettext('Panel de gestión de administradores'),
        'desgesadm': gettext('En este apartado esta diseñado para visualizar la informacion de los administrados registrados, asi como modificar y eliminar esta información'),
        'menuadm1': gettext('Lista de administradores'),
        'menuadm2': gettext('Adicionar app'),
        'adnom': gettext('Nombre'),
        'adape': gettext('Apellido'),
        'addire': gettext('Direccion'),
        'adtele': gettext('Telefono'),
        'adcorreo': gettext('Correo'),
        'adgener': gettext('Genero'),
        'adgenerm': gettext('Masculino'),
        'adgenefr': gettext('Femenino'),
        'adselopc': gettext('Seleccione una opcion'),
        'adimg': gettext('Imagen'),
        'adpass': gettext('Contraseña'),
        'adpass2': gettext('Repetir contraseña'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        
    } 
    return render_template("gestionadmin.html", usuarios=usuarios,dataLogin= dataLoginSesion(),**dict(translations.items()))

@app.route("/gestionadmin_pag/<number_pag>")
def gestionadmin_pag(number_pag):
    translations = {
        'titgesadm': gettext('Panel de gestión de administradores'),
        'desgesadm': gettext('En este apartado esta diseñado para visualizar la informacion de los administrados registrados, asi como modificar y eliminar esta información'),
        'menucl1': gettext('Lista de clientes'),
        'menucl2': gettext('Adicionar app'),
        'adnom': gettext('Nombre'),
        'adape': gettext('Apellido'),
        'addire': gettext('Direccion'),
        'adtele': gettext('Telefono'),
        'adcorreo': gettext('Correo'),
        'adgener': gettext('Genero'),
        'adgenerm': gettext('Masculino'),
        'adgenefr': gettext('Femenino'),
        'adselopc': gettext('Seleccione una opcion'),
        'adimg': gettext('Imagen'),
        'adpass': gettext('Contraseña'),
        'adpass2': gettext('Repetir contraseña'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        
    } 
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 0,10")
    if number_pag == '2':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 10,10")
    if number_pag == '3':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 20,10")
    if number_pag == '4':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 30,10")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 40,10")
    if number_pag == '6':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 50,10")
    if number_pag == '7':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 60,10")
    if number_pag == '8':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 70,10")
    if number_pag == '9':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 80,10")
    if number_pag == '10':
        cursor.execute("SELECT * FROM usuario where tipo_user = 1 LIMIT 90,10")
    usuarios = cursor.fetchall()
    conexion.commit()
    return render_template('gestionadmin.html', usuarios=usuarios ,dataLogin= dataLoginSesion(),**dict(translations.items()))


@app.route('/gestioncliente/')
def gestioncliente():
    translations = {
        'titgescl': gettext('Panel de gestión de clientes'),
        'desgescl': gettext('En este apartado esta diseñado para visualizar la informacion de los clientes, asi como modificar y eliminar la informacion almacenada'),
        'adnom': gettext('Nombre'),
        'adape': gettext('Apellido'),
        'addire': gettext('Direccion'),
        'adtele': gettext('Telefono'),
        'adcorreo': gettext('Correo'),
        'adgener': gettext('Genero'),
        'adimg': gettext('Imagen'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        
    }    
    
    usuarios = controller.usuario_cliente()
    return render_template("gestioncliente.html", usuarios=usuarios,dataLogin= dataLoginSesion(),**dict(translations.items()))

@app.route("/gestioncliente_pag/<number_pag>")
def gestioncliente_pag(number_pag):
    translations = {
        'titgescl': gettext('Panel de gestión de clientes'),
        'desgescl': gettext('En este apartado esta diseñado para visualizar la informacion de los clientes, asi como modificar y eliminar la informacion almacenada'),
        'adnom': gettext('Nombre'),
        'adape': gettext('Apellido'),
        'addire': gettext('Direccion'),
        'adtele': gettext('Telefono'),
        'adcorreo': gettext('Correo'),
        'adgener': gettext('Genero'),
        'adimg': gettext('Imagen'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        
    }  
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 0,10")
    if number_pag == '2':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 10,10")
    if number_pag == '3':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 20,10")
    if number_pag == '4':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 30,10")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 40,10")
    if number_pag == '6':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 50,10")
    if number_pag == '7':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 60,10")
    if number_pag == '8':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 70,10")
    if number_pag == '9':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 80,10")
    if number_pag == '10':
        cursor.execute("SELECT * FROM usuario where tipo_user = 2 LIMIT 90,10")
    usuarios = cursor.fetchall()
    conexion.commit()
    return render_template('gestioncliente.html', usuarios=usuarios ,dataLogin= dataLoginSesion(),**dict(translations.items()))


@app.route("/formulario_editar_producto/<int:id_producto>")
def editar_producto(id_producto):
    translations = {
        'titmed': gettext('Administracion de medicamentos en general'),
        'descmed': gettext('Esta sección permite operar sobre medicamentos de diferentes tipos y/o presentaciones'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'adnom': gettext('Nombre'),
        'addes': gettext('Descripcion'),
        'adcant': gettext('Cantidad'),
        'adprec': gettext('Precio'),
        'adprov': gettext('Proveedor'),
        'adfech': gettext('Fecha Vencimiento'),
        'adimg': gettext('Imagen'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbnomp': gettext('Nombre'),
        'tbcan': gettext('Cantidad disponible'),
        'tbprec': gettext('Precio'),
        'tbfech': gettext('Fecha de Vencimiento'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titedit': gettext('Edicion de datos'),
        'desedit': gettext('Esta sección permite operar sobre los productos'),  
    }  
    # Obtener el juego por ID
    productos = controller.obtener_producto_por_id(id_producto)
    return render_template("editar_producto.html", productos=productos,dataLogin= dataLoginSesion(),**dict(translations.items()))


@app.route("/formulario_editar_usuario/<int:id>")
def editar_usuario(id):
    translations = {
        'titgesadm': gettext('Panel de gestión de administradores'),
        'desgesadm': gettext('En este apartado esta diseñado para visualizar la informacion de los administrados registrados, asi como modificar y eliminar esta información'),
        'menuprodl': gettext('Lista de productos'),
        'menuproda': gettext('Adicionar producto'),
        'adnom': gettext('Nombre'),
        'adape': gettext('Apellido'),
        'addire': gettext('Direccion'),
        'adtele': gettext('Telefono'),
        'adcorreo': gettext('Correo'),
        'adgener': gettext('Genero'),
        'adgenerm': gettext('Masculino'),
        'adgenefr': gettext('Femenino'),
        'adselopc': gettext('Seleccione una opcion'),
        'adimg': gettext('Imagen'),
        'adpass': gettext('Contraseña'),
        'adpass2': gettext('Repetir contraseña'),
        'btncan': gettext('Cancelar'),
        'btnsav': gettext('Guardar'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'expl': gettext('Abrir Explorador'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titeditusu': gettext('Edicion de datos'),
        'deseditusu': gettext('En este apartado esta diseñado para modificar la informacion almacenada de los usuarios'),        
    } 
    # Obtener el juego por ID
    usuarios = controller.obtener_usuario_por_id(id)
    return render_template("editar_usuario.html", usuarios=usuarios,dataLogin= dataLoginSesion(),**dict(translations.items()))


@app.route("/actualizar_producto", methods=["POST"])
def actualizar_producto():
    translations = {
        'usrreg': gettext('Usuarios Registrados'),
        'titadm': gettext('Administradores'),
        'reg': gettext('Registrados'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    id_producto = request.form["id_producto"]
    nombre = request.form["nombre"]
    cantidad = request.form["cantidad"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    fecha_vencimiento = request.form["fecha_vencimiento"]
    imagen = request.files["imagen"]
    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        
        imagen.save(os.path.join(config['UPLOAD_FOLDER'], filename))
        imagename = filename    
    controller.actualizar_producto(nombre, descripcion,cantidad ,precio,fecha_vencimiento,imagename,id_producto )
    return render_template("home.html",dataLogin= dataLoginSesion(),**dict(translations.items()))


@app.route("/actualizar_usuario", methods=["POST"])
def actualizar_usuario():
    translations = {
        'usrreg': gettext('Usuarios Registrados'),
        'titadm': gettext('Administradores'),
        'reg': gettext('Registrados'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    translations = {
        'usrreg': gettext('Usuarios Registrados'),
        'titadm': gettext('Administradores'),
        'reg': gettext('Registrados'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }    
    id = request.form["id"]
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    correo = request.form["correo"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    genero = request.form["genero"]
    imagen = request.files["imagen"]
        

    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        
        imagen.save(os.path.join(config['UPLOAD_FOLDER'], filename))
        imagename = filename
    controller.actualizar_usuario(nombre, apellido, correo,direccion,telefono,genero,imagename,id)
    return render_template("home.html",dataLogin= dataLoginSesion(),**dict(translations.items()))


@app.route("/eliminar_producto", methods=["POST"])
def eliminar_producto():
    translations = {
        'usrreg': gettext('Usuarios Registrados'),
        'titadm': gettext('Administradores'),
        'reg': gettext('Registrados'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'txthelp': gettext('Ayuda'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'infogen': gettext('A traves de esta seccion el app tiene los permisos para visualizar la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),

    }
    controller.eliminar_producto(request.form["id_producto"])
    return render_template("home.html",dataLogin= dataLoginSesion(),**dict(translations.items()))


@app.route("/eliminar_usuario", methods=["POST"])
def eliminar_usuario():
    controller.eliminar_usuario(request.form["id"])
    return render_template("home.html",dataLogin= dataLoginSesion())


@app.route('/registro_admin', methods=['GET', 'POST'])
def registerUserr():
    msg = ''
    conexion = obtener_conexion()
    if request.method == 'POST':
        tipo_user = request.form['tipo_user']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        password = request.form['password']
        repite_password = request.form['repite_password']
        genero = request.form['genero']
        create_at = date.today()
        imagen = request.files['imagen']
        create_at = date.today()
        #current_time = datetime.datetime.now()

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuario WHERE correo = %s', (correo,))
        account = cursor.fetchone()
        cursor.close()  # cerrrando conexion SQL

        if account:
            msg = 'Ya existe el Email!'
        elif password != repite_password:
            msg = 'Disculpa, las clave no coinciden!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', correo):
            msg = 'Disculpa, formato de Email incorrecto!'
        elif not correo or not password or not password or not repite_password:
            msg = 'El formulario no debe estar vacio!'
        else:
            # La cuenta no existe y los datos del formulario son válidos,
            password_encriptada = generate_password_hash(
                password, method='sha256')
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            if imagen and allowed_file(imagen.filename):
                filename = secure_filename(imagen.filename)
                
                rut= imagen.save(os.path.join(config['UPLOAD_FOLDER'], filename))
                imagename = str(UPLOAD_FOLDER+'/'+filename)           
            cursor.execute('INSERT INTO usuario (tipo_user, nombre, apellido, correo,direccion,telefono, password,genero, create_at,imagen) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (tipo_user, nombre, apellido, correo, direccion,telefono, password_encriptada, genero, create_at,imagename))
            conexion.commit()
            cursor.close()
            msg = 'Cuenta creada correctamente!'

        return render_template('login.html', msjAlert= msg, typeAlert=1)
    return render_template('login.html', dataLogin= dataLoginSesion(), msjAlert = msg, typeAlert=0)



@app.route('/imagen/<int:id>')
def mostrar_imagen(id):
    datalogin=dataLoginSesion
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = "SELECT imagen FROM usuario WHERE id = %s"
    values = (id,)
    cursor.execute(query, datalogin.id,)
    resultado = cursor.fetchone()
    cursor.close()
    if resultado is not None:
        ruta = resultado[0]
        return render_template('base_admin.html', ruta=ruta)
    else:
        return 'La imagen no existe'
    
@app.route('/gestionpedido/')
def gestionpedido():
    translations = {
        'titgesp': gettext('Administracion de pedidos'),
        'desges': gettext('A traves de esta seccion se visualiza la informacion de los pedidos realizados por los clientes'),
        'adnomp': gettext('Nombre'),
        'adapep': gettext('Apellido'),
        'addirep': gettext('Direccion'),
        'adtelep': gettext('Telefono'),
        'adcorreop': gettext('Correo'),
        'addirp': gettext('Direccion'),
        'adciudp': gettext('Ciudad'),
        'addeparp': gettext('Departamento'),
        'adpaisp': gettext('Pais'),
        'adestp': gettext('Estado'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'txthelp': gettext('Ayuda'),

        'infogen': gettext('A traves de esta seccion se visualiza la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titedit': gettext('Edicion de datos'),
        'desedit': gettext('Esta sección permite operar sobre los productos'),
    }
    pedidos = controller.gestion_pedido()
    return render_template("gestionpedido.html", pedidos=pedidos,dataLogin= dataLoginSesion(),**dict(translations.items()))

@app.route("/gestionpedido_pag/<number_pag>")
def gestionpedido_pag(number_pag):
    translations = {
        'titgesp': gettext('Administracion de pedidos'),
        'desges': gettext('A traves de esta seccion se visualiza la informacion de los pedidos realizados por los clientes'),
        'adnomp': gettext('Nombre'),
        'adapep': gettext('Apellido'),
        'addirep': gettext('Direccion'),
        'adtelep': gettext('Telefono'),
        'adcorreop': gettext('Correo'),
        'addirp': gettext('Direccion'),
        'adciudp': gettext('Ciudad'),
        'addeparp': gettext('Departamento'),
        'adpaisp': gettext('Pais'),
        'adestp': gettext('Estado'),
        'tbmod': gettext('Modificar'),
        'tbel': gettext('Eliminar'),
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),
        'txthelp': gettext('Ayuda'),
        'infogen': gettext('A traves de esta seccion se visualiza la cantidad de clientes y administradores registrados, asi como realizar operaciones de registro, modificacion y eliminacion de los productos ofrecidos por la farmacia, adicionalmente es capaz de generar reportes de ventas'),
        'titedit': gettext('Edicion de datos'),
        'desedit': gettext('Esta sección permite operar sobre los productos'),
    }
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM pedido LIMIT 0,10")
    if number_pag == '2':
        cursor.execute("SELECT * FROM pedido LIMIT 10,10")
    if number_pag == '3':
        cursor.execute("SELECT * FROM pedido LIMIT 20,10")
    if number_pag == '4':
        cursor.execute("SELECT * FROM pedido LIMIT 30,10")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM pedido LIMIT 40,10")
    if number_pag == '6':
        cursor.execute("SELECT * FROM pedido LIMIT 50,10")
    if number_pag == '7':
        cursor.execute("SELECT * FROM pedido LIMIT 60,10")
    if number_pag == '8':
        cursor.execute("SELECT * FROM pedido LIMIT 70,10")
    if number_pag == '9':
        cursor.execute("SELECT * FROM pedido LIMIT 80,10")
    if number_pag == '10':
        cursor.execute("SELECT * FROM pedido LIMIT 90,10")
    pedidos = cursor.fetchall()
    conexion.commit()
    return render_template('gestionpedido.html', pedidos=pedidos ,dataLogin= dataLoginSesion(),**dict(translations.items()))

#/////////////////




# Rutas para login y recuperacion de cuenta
@app.route('/login/')
def login():
    translations = {
        'titlog': gettext('Registra tu cuenta y accede a nuestros servicios'),
        'welcome': gettext('Bienvenido de vuelta!'),
        'descwel': gettext('Para mantenerse conectado con nosotros, inicie sesión con su información personal'),
        'plhnom': gettext('Nombre'),
        'plhape': gettext('Apellido'),
        'plhcorr': gettext('Correo'),
        'plhdir': gettext('Direccion'),
        'plhtel': gettext('Telefono'),
        'plhpass': gettext('Contraseña'),
        'plhpass2': gettext('Repite contraseña'),
        'plhgen': gettext('Seleccione genero'),
        'plhgenm': gettext('Masculino'),
        'plhgenf': gettext('Femenino'),
        'sincu': gettext('Aun no tienes cuenta?'),
        'olvcon': gettext('Olvidaste tu contraseña?'),
        'txtlogin': gettext('Iniciar Sesión'),
        'textreg': gettext('Registrate'),
        'descreg': gettext('Para mantenerse conectado con nosotros, inicie sesión con su información personal'),
        'footdes': gettext('Descubre la comodidad de cuidar tu salud desde casa con FarmaClick'),
        'footnos': gettext('Nosotros'),
        'footqui': gettext('¿Quiénes somos?'),
        'footpreg': gettext('Preguntas Frecuentes'),
        'footpol': gettext('Políticas y Términos de Uso'),
        'footpole': gettext('Políticas de Envíos'),
        'foottrab': gettext('Trabaja con nosotros'),
        'footeni': gettext('Enlaces de interés'),
        'footsuper': gettext('Superintendencia de industria y comercio'),
        'footsuperf': gettext('Superintendencia financiera'),
        'footcped': gettext('Cómo hacer un pedido en TDV'),
        'foottitco': gettext('Contáctenos'),
        'footdir': gettext('Ipiales Nariño, CALLE 234A'),
        'footcorr': gettext('farmaclick@farma.com.co'),
        'footnum1': gettext('+ 57 3217655433'),
        'footnum2': gettext(' + 57 3146785432'),
        'footsigred': gettext('Síguenos en nuestras redes sociales'),   
        'footderech': gettext('Todos los derechos reservados')     
       
        }

    return render_template('login.html',**dict(translations.items()))

@app.route('/registro/')
def registro():
    return render_template("registro.html")

#Registrando una cuenta de Usuario
@app.route('/registro-usuario', methods=['GET', 'POST'])
def registerUser():
    
    translations = {
        'titlog': gettext('Registra tu cuenta y accede a nuestros servicios'),
        'welcome': gettext('Bienvenido de vuelta!'),
        'descwel': gettext('Para mantenerse conectado con nosotros, inicie sesión con su información personal'),
        'plhnom': gettext('Nombre'),
        'plhape': gettext('Apellido'),
        'plhcorr': gettext('Correo'),
        'plhdir': gettext('Direccion'),
        'plhtel': gettext('Telefono'),
        'plhpass': gettext('Contraseña'),
        'plhpass2': gettext('Repite contraseña'),
        'plhgen': gettext('Seleccione genero'),
        'plhgenm': gettext('Masculino'),
        'plhgenf': gettext('Femenino'),
        'sincu': gettext('Aun no tienes cuenta?'),
        'olvcon': gettext('Olvidaste tu contraseña?'),
        'txtlogin': gettext('Iniciar Sesión'),
        'textreg': gettext('Registrate'),
        'descreg': gettext('Para mantenerse conectado con nosotros, inicie sesión con su información personal'),
        'footdes': gettext('Descubre la comodidad de cuidar tu salud desde casa con FarmaClick'),
        'footnos': gettext('Nosotros'),
        'footqui': gettext('¿Quiénes somos?'),
        'footpreg': gettext('Preguntas Frecuentes'),
        'footpol': gettext('Políticas y Términos de Uso'),
        'footpole': gettext('Políticas de Envíos'),
        'foottrab': gettext('Trabaja con nosotros'),
        'footeni': gettext('Enlaces de interés'),
        'footsuper': gettext('Superintendencia de industria y comercio'),
        'footsuperf': gettext('Superintendencia financiera'),
        'footcped': gettext('Cómo hacer un pedido en TDV'),
        'foottitco': gettext('Contáctenos'),
        'footdir': gettext('Ipiales Nariño, CALLE 234A'),
        'footcorr': gettext('farmaclick@farma.com.co'),
        'footnum1': gettext('+ 57 3217655433'),
        'footnum2': gettext(' + 57 3146785432'),
        'footsigred': gettext('Síguenos en nuestras redes sociales'),   
        'footderech': gettext('Todos los derechos reservados')    
       
        }
    
    msg = ''
    conexion = obtener_conexion()
    if request.method == 'POST':
        tipo_user                   =2
        nombre                      = request.form['nombre']
        apellido                    = request.form['apellido']
        correo                       = request.form['correo']
        direccion                       = request.form['direccion']
        telefono                       = request.form['telefono']
        password                    = request.form['password']
        repite_password             = request.form['repite_password']
        genero                        = request.form['genero']
        create_at                   = date.today()
        #current_time = datetime.datetime.now()
        # Comprobando si ya existe la cuenta de Usuario con respecto al correo
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuario WHERE correo = %s', (correo,))
        account = cursor.fetchone()
        cursor.close() #cerrrando conexion SQL
          
        if account:
            msg = 'Ya existe el Email!'
        elif password != repite_password:
            msg = 'Disculpa, las clave no coinciden!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', correo):
            msg = 'Disculpa, formato de Email incorrecto!'
        elif not nombre or not apellido or not correo or not direccion or not telefono or not genero or not password or not repite_password:
            abort(400)
            msg = 'El formulario no debe estar vacio!'
        else:
            # La cuenta no existe y los datos del formulario son válidos,
            password_encriptada = generate_password_hash(password, method='sha256')
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute('INSERT INTO usuario (tipo_user, nombre, apellido, correo,direccion,telefono, password,genero, create_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (tipo_user, nombre, apellido, correo,direccion,telefono, password_encriptada, genero, create_at))
            conexion.commit()
            cursor.close()
            msg = 'Cuenta creada correctamente!'

        return render_template('login.html',**dict(translations.items()))
        
    return render_template('login.html',**dict(translations.items()))

    
# Cerrar session del usuario
@app.route('/logout')
def logout():
    translations = {
        'titlog': gettext('Registra tu cuenta y accede a nuestros servicios'),
        'welcome': gettext('Bienvenido de vuelta!'),
        'descwel': gettext('Para mantenerse conectado con nosotros, inicie sesión con su información personal'),
        'plhnom': gettext('Nombre'),
        'plhape': gettext('Apellido'),
        'plhcorr': gettext('Correo'),
        'plhdir': gettext('Direccion'),
        'plhtel': gettext('Telefono'),
        'plhpass': gettext('Contraseña'),
        'plhpass2': gettext('Repite contraseña'),
        'plhgen': gettext('Seleccione genero'),
        'plhgenm': gettext('Masculino'),
        'plhgenf': gettext('Femenino'),
        'sincu': gettext('Aun no tienes cuenta?'),
        'olvcon': gettext('Olvidaste tu contraseña?'),
        'txtlogin': gettext('Iniciar Sesión'),
        'textreg': gettext('Registrate'),
        'descreg': gettext('Para mantenerse conectado con nosotros, inicie sesión con su información personal'),
        'footdes': gettext('Descubre la comodidad de cuidar tu salud desde casa con FarmaClick'),
        'footnos': gettext('Nosotros'),
        'footqui': gettext('¿Quiénes somos?'),
        'footpreg': gettext('Preguntas Frecuentes'),
        'footpol': gettext('Políticas y Términos de Uso'),
        'footpole': gettext('Políticas de Envíos'),
        'foottrab': gettext('Trabaja con nosotros'),
        'footeni': gettext('Enlaces de interés'),
        'footsuper': gettext('Superintendencia de industria y comercio'),
        'footsuperf': gettext('Superintendencia financiera'),
        'footcped': gettext('Cómo hacer un pedido en TDV'),
        'foottitco': gettext('Contáctenos'),
        'footdir': gettext('Ipiales Nariño, CALLE 234A'),
        'footcorr': gettext('farmaclick@farma.com.co'),
        'footsigred': gettext('Síguenos en nuestras redes sociales'),   
        'footderech': gettext('Todos los derechos reservados')     
       
        }
    msgClose = ''
    # Eliminar datos de sesión, esto cerrará la sesión del usuario
    session.pop('conectado', None)
    session.pop('id', None)
    session.pop('correo', None)
    msgClose ="La sesión fue cerrada correctamente"
    return render_template('./login.html', msjAlert = msgClose, typeAlert=1,**dict(translations.items()))



@app.route('/dashboard', methods=['GET', 'POST'])
def loginUsser():
    conexion = obtener_conexion()
    noOfItems = 0
    translations = {
        'titlog': gettext('Registra tu cuenta y accede a nuestros servicios'),
        'welcome': gettext('Bienvenido de vuelta!'),
        'descwel': gettext('Para mantenerse conectado con nosotros, inicie sesión con su información personal'),
        'plhnom': gettext('Nombre'),
        'plhape': gettext('Apellido'),
        'plhcorr': gettext('Correo'),
        'plhdir': gettext('Direccion'),
        'plhtel': gettext('Telefono'),
        'plhpass': gettext('Contraseña'),
        'plhpass2': gettext('Repite contraseña'),
        'plhgen': gettext('Seleccione genero'),
        'plhgenm': gettext('Masculino'),
        'plhgenf': gettext('Femenino'),
        'sincu': gettext('Aun no tienes cuenta?'),
        'olvcon': gettext('Olvidaste tu contraseña?'),
        'txtlogin': gettext('Iniciar Sesión'),
        'textreg': gettext('Registrate'),
        'descreg': gettext('Para mantenerse conectado con nosotros, inicie sesión con su información personal'),
        'usrreg': gettext('Usuarios Registrados'),
        'titadm': gettext('Administradores'),
        'reg': gettext('Registrados'),
        'titcli': gettext('Clientes'),
        'footdes': gettext('Descubre la comodidad de cuidar tu salud desde casa con FarmaClick'),
        'footnos': gettext('Nosotros'),
        'footqui': gettext('¿Quiénes somos?'),
        'footpreg': gettext('Preguntas Frecuentes'),
        'footpol': gettext('Políticas y Términos de Uso'),
        'footpole': gettext('Políticas de Envíos'),
        'foottrab': gettext('Trabaja con nosotros'),
        'footeni': gettext('Enlaces de interés'),
        'footsuper': gettext('Superintendencia de industria y comercio'),
        'footsuperf': gettext('Superintendencia financiera'),
        'footcped': gettext('Cómo hacer un pedido en TDV'),
        'foottitco': gettext('Contáctenos'),
        'footdir': gettext('Ipiales Nariño, CALLE 234A'),
        'footcorr': gettext('farmaclick@farma.com.co'),
        'footnum1': gettext('+ 57 3217655433'),
        'footnum2': gettext(' + 57 3146785432'),
        'footsigred': gettext('Síguenos en nuestras redes sociales'),   
        'footderech': gettext('Todos los derechos reservados'),  
        'panel': gettext('Panel de control'),
        'gesp': gettext('Gestion producto'),
        'cuidp': gettext('Cuidado personal'),
        'dermaco': gettext('Dermacosmeticos'),
        'pnutri': gettext('Nutricionales'),
        'pbebe': gettext('Bebé'),
        'medip': gettext('Medicamentos'),
        'gesusu': gettext('Gestion usuarios'),
        'adminp': gettext('Administrador'),
        'clientep': gettext('Cliente'),
        'pedidosp': gettext('Pedidos'),
        'revisarp': gettext('Revisar pedidos'),              
        }
 
     
    if 'conectado' in session:
        
        
        
        correo = session['correo']
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM usuario WHERE correo = %s", (correo,))
        userId = cursor.fetchone()[0]
        cursor.fetchall()
        cursor.execute("SELECT count(id_producto) FROM carrito WHERE id = %s", (userId, ))
        noOfItems = cursor.fetchone()[0]  
    
        if session['tipo_user'] == 1:
            return render_template('./home.html', dataLogin = dataLoginSesion(),**dict(translations.items()))
        else:
            return render_template('./homecliente.html', dataLogin = dataLoginSesion(),noOfItems=noOfItems)
        
    else:
        msg = ''
        if request.method == 'POST' and 'correo' in request.form and 'password' in request.form:
            correo      = str(request.form['correo'])
            password   = str(request.form['password'])
            
            # Comprobando si existe una cuenta
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuario WHERE correo = %s", [correo])
            account = cursor.fetchone()

            if account:
                if check_password_hash(account['password'],password):
                    # Crear datos de sesión, para poder acceder a estos datos en otras rutas 
                    session['conectado']        = True
                    session['id']               = account['id']
                    session['tipo_user']        = account['tipo_user']
                    session['nombre']           = account['nombre']
                    session['apellido']         = account['apellido']
                    session['correo']           = account['correo']
                    session['direccion']        = account['direccion']
                    session['telefono']         = account['telefono']
                    session['genero']           = account['genero']
                    session['create_at']        = account['create_at'],
                    session['imagen']           = account['imagen']

                    msg = "Ha iniciado sesión correctamente."
                    if session['tipo_user'] == 1:
                        render_template('./home.html', msjAlert = msg, typeAlert=1, dataLogin = dataLoginSesion(),noOfItems=noOfItems,**dict(translations.items()))
                    else:
                        return render_template('./homecliente.html', msjAlert = msg, typeAlert=1, dataLogin = dataLoginSesion(),noOfItems=noOfItems) 
                else:
                    msg = 'Datos incorrectos, por favor verfique!'
                    return render_template('login.html', msjAlert = msg, typeAlert=0,**dict(translations.items()))
            else:
                return render_template('login.html', msjAlert = msg, typeAlert=0,**dict(translations.items()))
                
    return render_template('login.html', msjAlert = 'Debe iniciar sesión.', typeAlert=0,**dict(translations.items()))


#/////////////////


@app.route("/agregar")
def agregar():
    conexion = obtener_conexion()
    if 'correo' not in session:
        return redirect(url_for('login'))
    else:
        
        productId = int(request.args.get('productId'))
        with conexion.cursor() as cursor:
            
            cursor.execute("SELECT id FROM usuario WHERE correo = %s", (session['correo'], ))
            usuario = cursor.fetchone()[0]
            cursor.fetchall()
            # Buscar si el producto ya está en el carrito del usuario
            cursor.execute("SELECT cantidad FROM carrito WHERE id = %s AND id_producto = %s", (usuario, productId))
            result = cursor.fetchone()
            if result:
                # Si el producto ya está en el carrito, aumentar la cantidad en 1
                cantidad = result[0] + 1
                cursor.fetchall()
                cursor.execute("UPDATE carrito SET cantidad = %s WHERE id = %s AND id_producto = %s", (cantidad, usuario, productId))
            else:
                # Si el producto no está en el carrito, agregarlo con cantidad 1
                cursor.fetchall()
                cursor.execute("INSERT INTO carrito (id, id_producto, cantidad) VALUES (%s, %s, %s)", (usuario, productId, 1))
            conexion.commit() 
            msg = "Added successfully"
            # Reducir el stock del producto en la base de datos
            cursor.execute('''UPDATE producto SET cantidad = cantidad - 1 WHERE id_producto = %s''', (productId,))                
            conexion.commit()         
            
    conexion.close()
    return redirect(url_for('homecliente'))
    
@app.route("/carrito")
def carrito():
    conexion = obtener_conexion()
    noOfItems = 0
    conexion = obtener_conexion()
    correo = session['correo']
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM usuario WHERE correo = %s", (correo,))
    userId = cursor.fetchone()[0]
    cursor.fetchall()
    cursor.execute("SELECT count(id_producto) FROM carrito WHERE id = %s", (userId, ))
    noOfItems = cursor.fetchone()[0]    
    if 'correo' not in session:
        return redirect(url_for('login'))
   # loggedIn, firstName, noOfItems = getLoginDetails()
    correo = session['correo']
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id FROM usuario WHERE correo = %s", (correo, ))
        usuario = cursor.fetchone()[0]
        cursor.fetchall()
        cursor.execute("SELECT carrito.id,producto.id_producto, producto.nombre, producto.precio, producto.imagen, carrito.cantidad FROM producto, carrito WHERE producto.id_producto = carrito.id_producto AND carrito.id = %s", (usuario, ))
        
        productos = cursor.fetchall()
        
    totalPrice = 0
    for row in productos:
        totalPrice += row[3] * row[5]
    return render_template("cart.html", productos = productos, totalPrice=totalPrice, noOfItems=noOfItems)

@app.route("/eliminar")
def eliminar():
    conexion = obtener_conexion()
    if 'correo' not in session:
        return redirect(url_for('login'))
    correo = session['correo']
    productId = int(request.args.get('productId'))
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id FROM usuario WHERE correo = %s", (correo, ))
        id = cursor.fetchone()[0]
        cursor.fetchall()
        try:
            # Buscar si el producto ya está en el carrito del usuario
            cursor.execute("SELECT cantidad FROM carrito WHERE id = %s AND id_producto = %s AND cantidad > 0", (id, productId))
            result = cursor.fetchone()
            if result:
                            
                cursor.execute("UPDATE carrito SET cantidad = cantidad - 1 WHERE id = %s AND id_producto = %s AND cantidad > 0", (id, productId))
                cursor.fetchall()
                conexion.commit()
                cursor.execute('''UPDATE producto SET cantidad = cantidad + 1 WHERE id_producto = %s''', (productId,))  
                cursor.fetchall()
                conexion.commit()
                msg = "removed successfully"              
            else:
                 cursor.execute("DELETE FROM carrito WHERE id = %s AND id_producto = %s", (id, productId))
                 conexion.commit()

        except:
            conexion.rollback()
            msg = "error occured"
    conexion.close()
    return redirect(url_for('homecliente'))

@app.route("/checkout")
def checkout():
    id = request.args.get('id')
    return render_template("checkout.html",id=id)


@app.route('/pasarelacompra', methods=['POST'])
def pasarelacompra():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    telefono = request.form['telefono']
    correo = request.form['correo']
    direccion = request.form['direccion']
    ciudad = request.form['ciudad']
    departamento = request.form['departamento']
    pais = request.form['pais']
    estado = 'pendiente'
    id_user = session['id']
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "INSERT INTO pedido (nombre, apellido, telefono, correo, direccion, ciudad, departamento, pais, estado,id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (nombre, apellido, telefono, correo, direccion, ciudad, departamento, pais, estado,id_user)
    cursor.execute(query, values)
    conexion.commit()
    return render_template('checkout.html',id_user=id_user)

#/////////////////




@app.route('/')
def index():
  productos = controller.datosMedicamentosHomeNoLogin()
  return render_template("inicio.html", productos=productos)



# ACTUALIZAR DATOS CLIENTE
@app.route("/actualizarDatosCliente", methods=["POST"])
def actualizarDatosCliente():
    id = request.form["id"]
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    correo = request.form["correo"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    genero = request.form["genero"]
    controller.actualizarDatosCliente(nombre, apellido, correo, direccion, telefono, genero, id)
    return render_template("homecliente.html",dataLogin= dataLoginSesion())


# Home app
@app.route('/homecliente/')
def homecliente():
    noOfItems = 0
    conexion = obtener_conexion()
    correo = session['correo']
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM usuario WHERE correo = %s", (correo,))
    userId = cursor.fetchone()[0]
    cursor.fetchall()
    cursor.execute("SELECT count(id_producto) FROM carrito WHERE id = %s", (userId, ))
    noOfItems = cursor.fetchone()[0]    
    productos = controller.datosMedicamentosHome()
    return render_template("homecliente.html", productos=productos,dataLogin= dataLoginSesion(),noOfItems=noOfItems)


# Medicamentos app
@app.route('/medicamentoscliente/')
def medicamentoscliente():
  productos = controller.datosMedicamentos()
  return render_template("medicamentos.html", productos=productos,dataLogin= dataLoginSesion())


# Datos app
@app.route('/datoscliente/')
def datoscliente():
    return render_template('datoscliente.html', dataLogin= dataLoginSesion())

# Cuidado personal
@app.route('/cuidadopersonalclient/')
def cuidadopersonalclient():
  productos = controller.datosCuidadoPersonal()
  return render_template("cuidadopersonalclient.html", productos=productos,dataLogin= dataLoginSesion())

# Dermacosmeticos
@app.route('/dermacosmetica/')
def dermacosmetica():
  productos = controller.datosDermacosmetica()
  return render_template("dermacosmetica.html", productos=productos,dataLogin= dataLoginSesion())


# Nutricionales
@app.route('/nutricionales/')
def nutricionales():
  productos = controller.datosNutricional()
  return render_template("nutricionales.html", productos=productos,dataLogin= dataLoginSesion())

# Bebe
@app.route('/bebemed/')
def bebemed():
  productos = controller.datosBebe()
  return render_template("bebemed.html", productos=productos,dataLogin= dataLoginSesion())


# Inicio app
@app.route('/inicio/')
def inicio():
    return render_template("inicio.html")


# PAGINACION 

#Pag. Medicamentos 
@app.route("/pag_medicamentos/<number_pag>")
def pag_medicamentos(number_pag):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 5 LIMIT 0,12")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 5 LIMIT 12,12")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 24,12")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 36,12")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 48,12")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 60,12")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 72,12")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 84,12")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 96,12")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 5 LIMIT 108,12")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('medicamentos.html', productos=productos) 

#Pag. Cuidado personal

@app.route("/pag_cuidado_personal/<number_pag>")
def pag_cuidado_personal(number_pag):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 1 LIMIT 0,12")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 1 LIMIT 12,12")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 24,12")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 36,12")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 48,12")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 60,12")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 72,12")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 84,12")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 96,12")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 1 LIMIT 108,12")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('cuidadopersonalclient.html', productos=productos ,dataLogin= dataLoginSesion()) 

#Pag. Dermacosmética

@app.route("/pag_dermacosmetica/<number_pag>")
def pag_dermacosmetica(number_pag):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 2 LIMIT 0,12")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 2 LIMIT 12,12")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 24,12")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 36,12")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 48,12")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 60,12")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 72,12")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 84,12")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 96,12")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 2 LIMIT 108,12")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('dermacosmetica.html', productos=productos ,dataLogin= dataLoginSesion()) 

#Pag. Nutricionales

@app.route("/pag_nuticional/<number_pag>")
def pag_nuticional(number_pag):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 3 LIMIT 0,12")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 3 LIMIT 12,12")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 24,12")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 36,12")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 48,12")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 60,12")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 72,12")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 84,12")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 96,12")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 3 LIMIT 108,12")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('nutricionales.html', productos=productos ,dataLogin= dataLoginSesion()) 

#Pag. Bebé

@app.route("/pag_bebe/<number_pag>")
def pag_bebe(number_pag):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if number_pag == '1':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 4 LIMIT 0,12")
    if number_pag == '2':
        cursor.execute("SELECT * FROM producto WHERE CATEGORIA = 4 LIMIT 12,12")
    if number_pag == '3':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 24,12")
    if number_pag == '4':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 36,12")
        
    if number_pag == '5':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 48,12")
    if number_pag == '6':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 60,12")
    if number_pag == '7':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 72,12")
    if number_pag == '8':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 84,12")
    if number_pag == '9':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 96,12")
    if number_pag == '10':
        cursor.execute("SELECT * FROM producto where CATEGORIA = 4 LIMIT 108,12")
    productos = cursor.fetchall()
    conexion.commit()
    return render_template('nutricionales.html', productos=productos ,dataLogin= dataLoginSesion()) 


@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        # Obtener el término de búsqueda del usuario
        busqueda = request.form['busqueda']
        
        # Crear una consulta para buscar en la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        consulta = "SELECT * FROM producto WHERE nombre LIKE '%{}%'".format(busqueda)
        cursor.execute(consulta)
        
        # Obtener los resultados de la consulta
        resultados = cursor.fetchall()
        
        if len(resultados) == 0:
            # Si no se encontraron resultados, mostrar un mensaje
            mensaje = "No se encontraron productos para '{}'. Intente con otra búsqueda.".format(busqueda)
            return render_template('base_cliente_registrado.html', mensaje=mensaje)
        else:
            # Si se encontraron resultados, mostrarlos
            return render_template('base_cliente_registrado.html', resultados=resultados)
    
    # Si la solicitud es GET, mostrar la página de búsqueda
    return render_template('base_cliente_registrado.html')



@app.route('/buscarN', methods=['GET', 'POST'])
def buscarN():
    if request.method == 'POST':
        # Obtener el término de búsqueda del usuario
        busqueda = request.form['busqueda']
        
        # Crear una consulta para buscar en la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        consulta = "SELECT * FROM producto WHERE nombre LIKE '%{}%'".format(busqueda)
        cursor.execute(consulta)
        
        # Obtener los resultados de la consulta
        resultados = cursor.fetchall()
        
        if len(resultados) == 0:
            # Si no se encontraron resultados, mostrar un mensaje
            mensaje = "No se encontraron productos para '{}'. Intente con otra búsqueda.".format(busqueda)
            return render_template('base_cliente_no_registrado.html', mensaje=mensaje)
        else:
            # Si se encontraron resultados, mostrarlos
            return render_template('base_cliente_no_registrado.html', resultados=resultados)
    
    # Si la solicitud es GET, mostrar la página de búsqueda
    return render_template('base_cliente_no_registrado.html')


error_codes = [
    400, 401, 403, 404, 405, 406, 408, 409, 410, 411, 412, 413, 414, 415,
    416, 417, 418, 422, 428, 429, 431, 451, 500, 501, 502, 503, 504, 505
]
for code in error_codes:
    @app.errorhandler(code)
    def client_error(error):
        return render_template('error.html', error=error), error.code

#/////////////////
if __name__ == '__main__':
    app.run(debug=True, port=5913)


