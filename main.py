
import importlib


def run_backend_service():
    """Dynamically imports and runs the run() function from app/app.py."""
    
    # Dynamically import the app module
    app_api = importlib.import_module("app.app")  # Use the package.module notation
    
    # Call the run() function
    app_api.run()
    print("Finished running run() from app/app.py.")

def main():
    # # Create a thread for the backend service
    # backend_service_thread = threading.Thread(target=run_backend_service, daemon=True)
    run_backend_service()



if __name__ == "__main__":
    main()
