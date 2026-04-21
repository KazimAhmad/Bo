from config.config import app
from flask import send_from_directory
from pathlib import Path
from config.constants import media_uploads, allowed_extensions

BASE_DIR = Path("image_uploads").resolve().parent
IMAGES_DIR = BASE_DIR / media_uploads

@app.route("/images/<path:filename>", methods = ["GET"])
def images(filename):
    print((IMAGES_DIR / "image.jpg").exists())
    return send_from_directory(IMAGES_DIR, filename)