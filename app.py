from flask import Flask, render_template, url_for, redirect
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from models import User, RestaurantRating, db
from forms import RegisterForm, LoginForm, RestaurantRatingForm

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

bcrypt = Bcrypt(app)
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    ratings = RestaurantRating.query.filter_by(user_id=current_user.id).order_by(RestaurantRating.visit_date.desc()).all()
    total_ratings = len(ratings)
    avg_rating = sum(rating.rating for rating in ratings) / total_ratings if ratings else 0
    
    return render_template('dashboard.html', 
                           username=current_user.username, 
                           ratings=ratings,
                           total_ratings=total_ratings,
                           avg_rating=round(avg_rating, 2))



@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/add_rating', methods=['GET', 'POST'])
@login_required
def add_rating():
    form = RestaurantRatingForm()
    if form.validate_on_submit():
        new_rating = RestaurantRating(
            user_id=current_user.id,
            restaurant_name=form.restaurant_name.data,
            rating=form.rating.data,
            cuisine_type=form.cuisine_type.data,
            meal_date = form.meal_date.data, 
            review =form.review.data,
            calories = form.calories.data,
            is_anonymous = form.is_anonymous.data
        )
        db.session.add(new_rating)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_rating.html', form=form)

if __name__ == '__main__':

    with app.app_context():
        db.create_all() 

    app.run(debug=True)