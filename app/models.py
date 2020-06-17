from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash=db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
class Post(db.Model):
    __tablename__="posts"
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50), index=True)
    last_name = db.Column(db.String(100), index=True)
    phone = db.Column(db.String(12))
    email = db.Column(db.String(120), index=True, unique=True)
    note =db.Column(db.String(280))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return "<Post> {}, email:{}".format(self.body,self.email)