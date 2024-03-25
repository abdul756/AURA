from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from config.application_config import ApplicationConfig
import io

SERVICE_ACCOUNT_FILE = ApplicationConfig.SERVICE_ACCOUNT_CREDENTIALS_FILE
SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_ID = ApplicationConfig.GOOGLE_DRIVE_OBJECT_ID

def upload_file_to_drive(file_name, file_type, file_content):
    credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # Build the Google Drive service
    service = build('drive', 'v3', credentials=credentials)

    # Convert the UploadedFile to a byte stream
    file_stream = io.BytesIO()
    file_content.seek(0)  # Move to the beginning of the UploadedFile
    file_stream.write(file_content.read())  # Write UploadedFile content to the stream
    file_stream.seek(0)  # Move to the beginning of the byte stream

    # Use MediaIoBaseUpload with the byte stream
    media = MediaIoBaseUpload(file_stream, mimetype=file_type, resumable=True)
    
    # Prepare the file upload
    
    file_metadata = {
        'name': file_name,
        'parents': [FOLDER_ID]  # Specify the folder ID you want to upload files to
    }
    
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return file.get('id')