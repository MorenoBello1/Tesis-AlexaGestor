from google.oauth2 import service_account
from googleapiclient.discovery import build

# Ruta al archivo de credenciales de la cuenta de servicio
SERVICE_ACCOUNT_FILE =  'credentials.json'


# Alcance de la API de Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Crear las credenciales de la cuenta de servicio
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Construir el servicio de Google Drive
def build_service():
    return build('drive', 'v3', credentials=credentials)


