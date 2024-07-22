from conexion import *
import unicodedata

import uuid


from pymongo import MongoClient

# Supongo que ya tienes la conexión establecida, aquí se omite la conexión por simplicidad
client = connect_to_mongodb() # Sustituye 'tu_uri_de_conexion' con tu URI de conexión real
db = client.AlexaGestor
docentes_collection = db.docentes

# Datos para insertar
datos_docentes = [
    {"nombre_docente": "Oscar Armando", "apellido_docente": "González López"},
    {"nombre_docente": "Jorge Sergio", "apellido_docente": "Herrera Tapia"},
    {"nombre_docente": "Luzmila Benilda", "apellido_docente": "López Reyes"},
    {"nombre_docente": "Mike Paolo", "apellido_docente": "Machuca Avalos"},
    {"nombre_docente": "Adriana Virginia", "apellido_docente": "Macias Espinales"},
    {"nombre_docente": "Luis Jacinto", "apellido_docente": "Mendoza Cuzme"},
    {"nombre_docente": "Henry Neurio", "apellido_docente": "Mero Briones"},
    {"nombre_docente": "Winther Abel", "apellido_docente": "Molina Loor"},
    {"nombre_docente": "Robert Wilfrido", "apellido_docente": "Moreira Centeno"},
    {"nombre_docente": "Jorge Aníbal", "apellido_docente": "Moya Delgado"},
    {"nombre_docente": "Dolores Esperanza", "apellido_docente": "Muñoz Verduga"},
    {"nombre_docente": "Joffre Edgardo", "apellido_docente": "Panchana Flores"},
    {"nombre_docente": "Jonny Vicente", "apellido_docente": "Pérez Veliz"},
    {"nombre_docente": "Luigi Fabian", "apellido_docente": "Pihuave Calderón"},
    {"nombre_docente": "Jorge Iván", "apellido_docente": "Pincay Ponce"},
    {"nombre_docente": "Patricia Alexandra", "apellido_docente": "Quiroz Palma"},
    {"nombre_docente": "Jose Jacinto", "apellido_docente": "Reyes Cárdenas"},
    {"nombre_docente": "Fabricio Javier", "apellido_docente": "Rivadeneira Zambrano"},
    {"nombre_docente": "Alex Andrés", "apellido_docente": "Santamaria Philco"},
    {"nombre_docente": "Hiraida Monserrate", "apellido_docente": "Santana Cedeño"},
    {"nombre_docente": "Juan Carlos", "apellido_docente": "Sendon Varela"},
    {"nombre_docente": "Sandra Jackeline", "apellido_docente": "Soledispa Pereira"},
    {"nombre_docente": "Rubén Antonio", "apellido_docente": "Zamora Cusme"},
    {"nombre_docente": "Junior Jose", "apellido_docente": "Zamora Mendoza"},
    {"nombre_docente": "Willian Jesús", "apellido_docente": "Zamora Mero"},
    {"nombre_docente": "Jharol Antonio", "apellido_docente": "Ormaza Sabando"},
    {"nombre_docente": "Mariuxi Alexandra", "apellido_docente": "Bruzza Moncayo"},
    {"nombre_docente": "Cesar Eduardo", "apellido_docente": "Cedeño Cedeño"},
    {"nombre_docente": "Pedro Pablo", "apellido_docente": "Pihuave Mendoza"},
    {"nombre_docente": "Rubén Darío", "apellido_docente": "Solorzano Cadena"}
]

# Insertar documentos
for dato in datos_docentes:
    docente_id = str(uuid.uuid4())
    docentes = {
        "_id": docente_id,
        "nombre_docente": dato["nombre_docente"],
        "apellido_docente": dato["apellido_docente"]
    }
    docentes_collection.insert_one(docentes)

print("Documentos insertados con éxito.")
client.close()