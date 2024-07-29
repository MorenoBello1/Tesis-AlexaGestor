from conexion import *
from flask import Blueprint, request, render_template,session


home_ruta = Blueprint('home', __name__)

# Ruta principal que renderiza un archivo HTML
def verificar_autenticacion():
    # Verificar si 'usuario_id' está en la sesión
    if 'usuario_id' not in session:
        # Redireccionar a la página de login si no está autenticado
        return False
    return True
@home_ruta.route('/home')
def home():
    if not verificar_autenticacion():
            return render_template('Login.html') 
    return render_template('home.html')
