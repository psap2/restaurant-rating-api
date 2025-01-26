from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RestaurantRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to the User model
    restaurant_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False) 
    cuisine_type = db.Column(db.String(50), nullable=False)
    meal_date = db.Column(db.DateTime, default=datetime.utcnow)  # Defaults to current time
    review = db.Column(db.Text, nullable=True)  # Optional review text
    calories = db.Column(db.Integer, nullable=True)  # Optional nutritional data

    user = db.relationship('User', backref='ratings', lazy=True)  # Relationship to the User model

def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()