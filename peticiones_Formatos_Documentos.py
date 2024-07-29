from flask import Blueprint, request, render_template, jsonify, session
from werkzeug.utils import secure_filename
import uuid
import os
from conexion import *
from googleapiclient.http import MediaFileUpload
from auth2 import build_service

# Construir el servicio de Google Drive
service = build_service()
formatos_ruta = Blueprint('formatos2', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'xls', 'xlsx'}

formatos_ruta.config = {'UPLOAD_FOLDER': UPLOAD_FOLDER}

# Asegúrate de que el directorio de subidas exista
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Función para subir archivo a OneDrive
def subir_archivoN(ruta_archivo, nombre_nuevo, id_folder):
    try:
        # Metadatos del archivo
        file_metadata = {
            'name': nombre_nuevo,
            'parents': [id_folder]
        }

        media = MediaFileUpload(ruta_archivo, resumable=True)
        archivo = service.files().create(body=file_metadata, media_body=media, fields='id').execute()   
        file_id = archivo.get('id')
        return file_id

    except Exception as e:
        print(f"Error al subir el archivo: {str(e)}")
        return None

# Verifica si la extensión del archivo está permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def verificar_autenticacion():
    # Verificar si 'usuario_id' está en la sesión
    if 'usuario_id' not in session:
        # Redireccionar a la página de login si no está autenticado
        return False
    return True

@formatos_ruta.route('/formatos2/')
def home():
    if not verificar_autenticacion():
            return render_template('Login.html') 
    return render_template('Formatos.html')

@formatos_ruta.route('/upload_and_add', methods=['POST'])
def upload_and_add():
    if 'file' not in request.files:
        return jsonify(success=False, message='No se subio ningun archivo')
    
    file = request.files['file']
    nombre_formato = request.form.get('nombre_formato', '').strip()
    fecha_actualizacion = request.form['fecha_actualizacion']
    observacion = request.form['observacion']
    carrera_id = request.form['carrera_id']

    if not nombre_formato or not fecha_actualizacion or not carrera_id:
        return jsonify(success=False, message='Faltan campos por completar')
    
    id_folder = '1-KZqvvcRAM-n1h-OEC6ICHUgENCJdoTl'  # Reemplaza esto con tu ID de carpeta en Google Drive

    if file.filename == '':
        return jsonify(success=False, message='No seleccionaste ningun archivo . ')
    
    if file and allowed_file(file.filename):
        secure_name = secure_filename(file.filename)
        file_path = os.path.join(formatos_ruta.config['UPLOAD_FOLDER'], secure_name)
        file.save(file_path)
        
        # Subir archivo a OneDrive y obtener el ID
        id_onedrive = subir_archivoN(file_path, nombre_formato, id_folder)
        
        # Eliminar el archivo después de subirlo
        os.remove(file_path)
        
        client = connect_to_mongodb()
        try:
            if client:
                db = client.AlexaGestor
                collection_formatos = db.formatos
                collection_carreras = db.carreras
                
                carrera = collection_carreras.find_one({"_id": carrera_id})
                if not carrera:
                    return "id_carrera no existe", 400
                
                formato_id = str(uuid.uuid4())

                formatos = {
                    "_id": formato_id,
                    "nombre_formato": nombre_formato,
                    "fecha_actualizacion": fecha_actualizacion,
                    "observacion": observacion,
                    "carrera_id": carrera_id,
                    "id_onedrive": id_onedrive  # Agrega el ID de OneDrive aquí
                }
                
                result = collection_formatos.insert_one(formatos)
                if result:
                    return jsonify(success=True)
                else:
                    return jsonify(success=False, message=f'Ha surgido un error al agregar al docente {nombre_formato}.')
        except Exception as e:
            return jsonify(success=False)
        finally:
            client.close()
    else:
        return jsonify(success=False, message='Tipo de archivo no permitido.')

@formatos_ruta.route('/obtener_carreras')
def obtener_carreras():
    client = connect_to_mongodb()
    try:
        if client:
            db = client.AlexaGestor
            collection_carreras = db.carreras
            carreras = list(collection_carreras.find())
            carreras = [{'_id': str(carrera['_id']), 'nombre_carrera': carrera['nombre_carrera']} for carrera in carreras]
            return jsonify(carreras)
    except Exception as e:
        print("error")
    finally:
        client.close()

@formatos_ruta.route('/api/formatos', methods=['GET'])
def obtener_formatos():
    client = connect_to_mongodb()
    try:
        db = client.AlexaGestor
        collection_formatos= db.formatos
        collection_carreras = db.carreras

        formatos = list(collection_formatos.find({}))
        
        for formato in formatos:
            carrera_id = formato.get("carrera_id")
            
            carrera = collection_carreras.find_one({"_id": carrera_id}, {"_id": 0, "nombre_carrera": 1})
            
            formato["nombre_carrera"] = carrera["nombre_carrera"] if carrera else "Desconocido"
        
        return jsonify({"formatos": formatos}), 200
    except Exception as e:
        print("error obtener")
    finally:
        client.close()

@formatos_ruta.route('/eliminar/formato/<_id>', methods=['DELETE'])
def delete_formato(_id):
    client = connect_to_mongodb()
    try:
        db = client.AlexaGestor
        collection = db.formatos

        # Buscar el documento en la base de datos para obtener el ID de archivo de OneDrive
        formato = collection.find_one({"_id": _id})
        
        # Obtener el ID de archivo de OneDrive
        id_onedrive = formato.get("id_onedrive")
        
        # Eliminar el documento de la base de datos
        result = collection.delete_one({"_id": _id})
        if result.deleted_count == 1:
            # Eliminar archivo de OneDrive si existe ID de OneDrive
            if id_onedrive:
                borrar_formatodrive(id_onedrive)
            return jsonify(success=True)
        else:
            return jsonify(success=False, message=f'Ha surgido un problema al eliminar al formato')
    except Exception as e:
        print("error")
    finally:
        client.close()

def borrar_formatodrive(id_archivo):
    service = build_service()
    
    try:
        # Llamar al método files().delete() para eliminar el archivo
        service.files().delete(fileId=id_archivo).execute()
        print("Archivo eliminado exitosamente.")
        return True
    except Exception as error:
        print(f"Error al borrar archivo de Google Drive: {error}")
        return False
