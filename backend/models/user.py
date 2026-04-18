from config.config import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), unique = False, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')

    def __repr__(self):
        return f"User('{self.user_name}', '{self.email}', '{self.image_file}')"
    
    def to_json(self):
        return {
            "id": self.id,
            "userName": self.user_name,
            "email": self.email
        }