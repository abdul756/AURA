import os
import datetime

def get_path(path, name):
    dir_path = os.path.join(
        path
    )
    create_folder_if_not_exists(dir_path)

    return os.path.join(dir_path, name)

def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    os.chmod(path, 0o777)