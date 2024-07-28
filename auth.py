from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Directorio de las credenciales
directorio_credenciales = "credentials_module.json"


def login():
    gauth = GoogleAuth()
    
    # Cargar credenciales desde el archivo
    try:
        gauth.LoadCredentialsFile(directorio_credenciales)
    except Exception as e:
        print(f"Error al cargar el archivo de credenciales: {e}")

    if gauth.credentials is None:
        # No se encontraron credenciales, autenticando de forma local
        print("No se encontraron credenciales. Realizando autenticación local.")
        gauth.LocalWebserverAuth()  # Requiere intervención del usuario
    elif gauth.access_token_expired:
        try:
            # Intentar refrescar el token de acceso
            print("Token de acceso expirado. Intentando refrescar.")
            gauth.Refresh()
        except Exception as e:
            print(f"Error al refrescar el token de acceso: {e}")
            print("Fallo al refrescar el token. Realizando autenticación local.")
            gauth.LocalWebserverAuth()  # Reautenticar si falla el refresco
    else:
        # Credenciales válidas
        print("Token de acceso válido.")
        gauth.Authorize()

    # Guardar las credenciales actualizadas
    try:
        gauth.SaveCredentialsFile(directorio_credenciales)
    except Exception as e:
        print(f"Error al guardar el archivo de credenciales: {e}")

    return GoogleDrive(gauth)