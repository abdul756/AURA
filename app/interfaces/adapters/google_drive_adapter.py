import pathway as pw
class GoogleDriveAdapter:
    def __init__(self, service_user_credentials_file, refresh_interval=30):
        self.service_user_credentials_file = service_user_credentials_file
        self.refresh_interval = refresh_interval

    def read_files(self, object_id):
        files = pw.io.gdrive.read(object_id=object_id, service_user_credentials_file=self.service_user_credentials_file, refresh_interval=30)
        # Assume this method uses pw.io.gdrive.read to fetch files from Google Drive
        return files
