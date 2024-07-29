from flask import Flask, session, redirect, url_for, jsonify
from datetime import timedelta

from peticiones_login import login_ruta
from peticiones_login_contraseña import logincontraseña_ruta
from peticiones_Comunidades import comunidades_ruta
from peticiones_home import home_ruta
from peticiones_Horarios_Distribucion import horarios_ruta
from peticiones_Eventos import eventos_ruta
from peticiones_Carreras import carreras_ruta
from peticiones_Docentes import docentes_ruta
from peticiones_Formatos_Documentos import formatos_ruta
from peticiones_Proceso_Academicos import procesos_ruta
from peticiones_PerfilDocente_Gemeni import perfil_ruta
from peticiones_usuarios import user_ruta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para manejar sesiones en Flask
app.permanent_session_lifetime = timedelta(minutes=35)

# Función para verificar si el usuario está autenticado
def verificar_autenticacion():
    if 'usuario_id' not in session:
        # Redireccionar a la página de sesión expirada si no está autenticado
        return redirect(url_for('login.home'))
        

@app.before_request
def before_request():
    session.permanent = True
    verificar_autenticacion()

@app.route('/session_expired')
def session_expired():
    if session.get('usuario_id') is None:  # Verifica si la sesión ha expirado
        return jsonify(success=False, message='Tu sesión ha expirado. Por favor, inicia sesión nuevamente.')
    # No retorna nada si la sesión está activa
    return jsonify(success=True)
# Registrar los Blueprints en la aplicación principal
app.register_blueprint(login_ruta)
app.register_blueprint(logincontraseña_ruta)
app.register_blueprint(home_ruta)
app.register_blueprint(comunidades_ruta)
app.register_blueprint(horarios_ruta)
app.register_blueprint(eventos_ruta)
app.register_blueprint(carreras_ruta)
app.register_blueprint(docentes_ruta)
app.register_blueprint(formatos_ruta)
app.register_blueprint(procesos_ruta)
app.register_blueprint(perfil_ruta)
app.register_blueprint(user_ruta)

if __name__ == '__main__':
    app.run(debug=False, port=8082)