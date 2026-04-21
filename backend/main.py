import sys
sys.path.append("../config/config.py")
sys.path.append("../requests/auth.py")
sys.path.append("../requests/post.py")

from config.config import db, app
from requests import auth, post

def requests_files():
    auth()
    post()

# to run only when called this and not on the import because the import runs all the file
if __name__ == "__main__":
    with app.app_context():
        # to create all the models defined in the models in the database and only if they are not already been created
        db.create_all()
    app.run(debug=True)
    requests_files()
