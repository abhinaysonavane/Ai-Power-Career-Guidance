from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    school = db.Column(db.String(120), nullable=True)
    skills = db.Column(db.String(255), nullable=True)
    interests = db.Column(db.String(255), nullable=True)
    recommended = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<User {self.email}>"
