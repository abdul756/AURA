import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ApplicationConfig(object):

    DATA_DIR = os.getenv("DATA_DIR", "data")
    
    OPEN_AI_API_KEY =  os.getenv("OPENAI_API_KEY")

    PATHWAY_REST_CONNECTOR_HOST = os.getenv("PATHWAY_REST_CONNECTOR_HOST")

    PATHWAY_REST_CONNECTOR_PORT = int(os.getenv("PATHWAY_REST_CONNECTOR_PORT"))

    GOOGLE_DRIVE_OBJECT_ID = os.getenv("GOOGLE_DRIVE_OBJECT_ID", "1YKu9D4HQEd_otZ7Pst-QJPXcyibdKtmX")

    SERVICE_ACCOUNT_CREDENTIALS_FILE = os.getenv("SERVICE_ACCOUNT_CREDENTIALS_FILE")

    NEWS_API_KEY = os.getenv("NEWS_API_KEY")