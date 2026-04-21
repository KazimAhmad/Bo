import os
import uuid
from werkzeug.utils import secure_filename

def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

def save_image(file, upload_folder, allowed_extensions):
    if not file:
        return None, "No file provided"

    if file.filename == "":
        return None, "Empty filename"

    if not allowed_file(file.filename, allowed_extensions):
        return None, "Invalid file type"

    filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"

    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    return filename, None

def delete_image(filename, upload_folder):
    if not filename:
        return None, "No file provided"

    if filename == "":
        return None, "Empty filename"
    
    filepath = os.path.join(upload_folder, filename)
    os.remove(filepath)
