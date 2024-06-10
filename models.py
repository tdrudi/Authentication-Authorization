from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)


class User(db.Model):
    """Users"""
    __tablename__ = "users"

    username = db.Column(db.String(20), nullable = False, unique = True, primary_key = True)
    password = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)
    feedback = db.relationship("Feedback", backref = "user", cascade = "all,delete")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user and hash password"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        user = cls(username = username, 
            password = hashed_utf8,
            email = email,
            first_name = first_name,
            last_name = last_name)
                
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Validate a user exist and the password is correct"""
        user = User.query.filter_by(username = username).first()

        """If user is valid"""
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            """User not valid"""
            return False
        
class Feedback(db.Model):
    """Feedback DB"""      
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.String(20), db.ForeignKey("users.username"), nullable = False)