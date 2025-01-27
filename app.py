from flask import Flask, render_template, url_for, redirect, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from models import User, RestaurantRating, db
from forms import RegisterForm, LoginForm, RestaurantRatingForm
import requests

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
    #query parameters
    search_query = request.args.get('search', '')
    if search_query:
        ratings = RestaurantRating.query.filter(
            RestaurantRating.user_id == current_user.id,
            (RestaurantRating.restaurant_name.ilike(f'%{search_query}%') |
             RestaurantRating.cuisine_type.ilike(f'%{search_query}%'))
        ).order_by(RestaurantRating.meal_date.desc()).all()
    else:
        ratings = RestaurantRating.query.filter_by(user_id=current_user.id).order_by(RestaurantRating.meal_date.desc()).all()
    
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

@app.route('/public_ratings', methods=['GET'])
def all_ratings():
    # getting query parameters
    search_query = request.args.get('search', '')
    cuisine_type = request.args.get('cuisine_type', '')
    min_rating = request.args.get('min_rating', '')
    query = RestaurantRating.query
    if search_query:
        query = query.filter(
            RestaurantRating.restaurant_name.ilike(f'%{search_query}%') |
            RestaurantRating.cuisine_type.ilike(f'%{search_query}%') |
            RestaurantRating.review.ilike(f'%{search_query}%') 
        )
    if cuisine_type:
        query = query.filter(RestaurantRating.cuisine_type.ilike(cuisine_type))
    if min_rating:
        query = query.filter(RestaurantRating.rating >= int(min_rating))
    all_ratings = query.order_by(RestaurantRating.meal_date.desc()).all()

    return render_template('public_ratings.html', ratings=all_ratings)

@app.route('/edit_rating/<int:rating_id>', methods=['GET', 'POST'])
def edit_rating(rating_id):
    
    rating = RestaurantRating.query.get_or_404(rating_id)

    form = RestaurantRatingForm(obj=rating) 

    if form.validate_on_submit():
        rating.restaurant_name = form.restaurant_name.data
        rating.cuisine_type = form.cuisine_type.data
        rating.rating = form.rating.data
        rating.review = form.review.data
        rating.meal_date = form.meal_date.data
        rating.calories = form.calories.data
        rating.is_anonymous = form.is_anonymous.data

        db.session.commit()
        return redirect(url_for('dashboard'))
    
    return render_template('edit_rating.html', form=form, rating_id = rating_id)

#Aggregation
@app.route('/aggregated/display/average_ratings', methods=['GET'])
def display_average_ratings():
    results = (
        db.session.query(
            RestaurantRating.cuisine_type,
            db.func.avg(RestaurantRating.rating).label('average_rating')
        )
        .group_by(RestaurantRating.cuisine_type)
        .all()
    )
    
    data = []
    for r in results:
        data.append({'cuisine_type': r[0], 'average_rating': round(r[1], 2)})

    return render_template('plain_display.html', data=data)

@app.route('/aggregated/top_restaurants/<int:user_id>', methods=['GET'])
def top_restaurants_by_month(user_id):

    results = (
        db.session.query(
            db.func.strftime('%Y-%m', RestaurantRating.meal_date).label('month'),
            RestaurantRating.restaurant_name,
            db.func.max(RestaurantRating.rating).label('top_rating')
        )
        .filter(RestaurantRating.user_id == user_id)
        .group_by('month', RestaurantRating.restaurant_name)
        .order_by('month')
        .all()
    )

    data =[]
    for r in results:
        data.append({'month': r[0], 'restaurant_name': r[1], 'rating': r[2]})

    return render_template('plain_display.html', data=data)

@app.route('/aggregated/popular_cuisines', methods=['GET'])
def popular_cuisine_types():
    results = (
        db.session.query(
            RestaurantRating.cuisine_type,
            db.func.count(RestaurantRating.id).label('review_count')
        )
        .group_by(RestaurantRating.cuisine_type)
        .order_by(db.func.count(RestaurantRating.id).desc())
        .all()
    )

    data = [{'cuisine_type': r[0], 'review_count': r[1]} for r in results]
    return render_template('plain_display.html', data=data)


if __name__ == '__main__':

    with app.app_context():
        db.create_all() 

    app.run(debug=True)