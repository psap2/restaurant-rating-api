
from models import User, db
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, NumberRange, Optional
from wtforms.fields import DateField
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

class RestaurantRatingForm(FlaskForm):
    restaurant_name = StringField('Restaurant Name', validators=[InputRequired()])
    cuisine_type = SelectField('Cuisine Type', choices=[
        ('American', 'American'), 
        ('Italian', 'Italian'), 
        ('Chinese', 'Chinese'), 
        ('Mexican', 'Mexican'), 
        ('Indian', 'Indian'), 
        ('Other', 'Other')
    ], validators=[InputRequired()])
    rating = IntegerField('Rating', validators=[InputRequired(), NumberRange(min=1, max=5)])
    review = TextAreaField('Review', validators=[Optional()])
    calories = IntegerField('Calories', validators=[Optional()])
    is_anonymous = BooleanField('Post Anonymously', default=False)
    meal_date = DateField(
        'Meal Date', 
        format='%Y-%m-%d', 
        validators=[Optional()]
    )
    submit = SubmitField('Submit Rating')