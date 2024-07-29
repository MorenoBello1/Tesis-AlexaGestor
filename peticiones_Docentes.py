from flask import Blueprint,Flask, request, jsonify, render_template,session
from conexion import *
import re
import uuid



docentes_ruta = Blueprint('docentes', __name__)

def verificar_autenticacion():
    # Verificar si 'usuario_id' está en la sesión
    if 'usuario_id' not in session:
        # Redireccionar a la página de login si no está autenticado
        return False
    return True
# Ruta principal que renderiza un archivo HTML
@docentes_ruta.route('/docentes/')
def home():
    if not verificar_autenticacion():
            return render_template('Login.html') 
    return render_template('Docentes.html')

# Ruta para manejar solicitudes GET a /api/data
@docentes_ruta.route('/obtener_docentes', methods=['GET'])
def get_docentes():
    client = connect_to_mongodb()
    try:
        db = client.AlexaGestor
        collection = db.docentes
        docentes = list(collection.find({}, {"_id": 1, "nombre_docente": 1, "apellido_docente": 1}))
        return jsonify(docentes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        client.close()

# Ruta para manejar solicitudes PUT a /api/data
@docentes_ruta.route('/agregar/docente', methods=['PUT'])
def add_docente():
    data = request.get_json()
    print("Datos recibidos:", data)
    nombre_docente = data.get("nombre_docente", "").strip()
    apellido_docente = data.get("apellido_docente", "").strip()
    correo = data.get("correo", "").strip().lower()

    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+[.][a-zA-Z0-9._%+-]+@uleam\.edu\.ec$")

    if not EMAIL_REGEX.match(correo):
        return jsonify(success=False, message='El correo debe ser válido, contener un punto antes del @ y terminar en @uleam.edu.ec')
    if not nombre_docente or not apellido_docente or not correo:
        return jsonify(success=False, message='Faltan campos por completar')

    client = connect_to_mongodb()

    try:
        db = client.AlexaGestor
        collection = db.docentes

        # Generar un ID único
        docente_id = str(uuid.uuid4())

        docentes = {
            "_id": docente_id,
            "nombre_docente": nombre_docente,
            "apellido_docente": apellido_docente,
            "correo": correo
        }
        result = collection.insert_one(docentes)
        
        if result.inserted_id:
            return jsonify(success=True, message=f'Docente {nombre_docente} agregado exitosamente.')
        else:
            return jsonify(success=False, message=f'Ha surgido un error al agregar al docente {nombre_docente}.')
    except Exception as e:
        print("Error:", e)
        return jsonify(success=False)
    finally:
        client.close()

@docentes_ruta.route('/eliminar/docente/<_id>', methods=['DELETE'])
def delete_docente(_id):
    client = connect_to_mongodb()
    try:
        db = client.AlexaGestor
        collection = db.docentes
        result = collection.delete_one({"_id": _id})
        if result.deleted_count == 1:
            return jsonify(success=True)
        else:
            return jsonify(success=False, message=f'Ha surgido un problema al eliminar al docente.')
    except Exception as e:
        return jsonify(success=False)
    finally:
        client.close()

@docentes_ruta.route('/api/docentes', methods=['GET'])
def obtener_docentes():
    try:
        client = connect_to_mongodb()
        db = client.AlexaGestor
        collection = db.docentes

        # Excluir el campo "_id" de los resultados
        resultados = collection.find({})

        # Convertir los resultados a una lista de diccionarios
        docentes = [docente for docente in resultados]

        # Cerrar la conexión con MongoDB
        client.close()

        # Devolver los resultados como JSON
        return jsonify({"docentes": docentes}), 200

    except Exception as e:
        print("error")
