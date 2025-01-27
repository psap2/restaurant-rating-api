# Restaurant Ratings application API

### Overview
 Flask-based API allows users to register, log in, and manage restaurant ratings. It supports creating, viewing, editing, and deleting ratings, and while also allowing for aggregation of ratings to provide different insights.

 ### Design descions

- **RESTful Endpoints**: REST allows for clear and structured communication between client and server in a client-server architecture. Additionally, RESTful architecture uses standard HTTP methods like GET, POST, PUT, and DELETE, which are easy to understand and can be easily implemented across different platforms.
- **Flask**: Chosen for its simplicity and flexibility in building web applications and RESTFUL API.
- **SQLite**: Used because its a relational datbase management system that is lightweight, and easy for setup. Useful for managing more complex data, and data is more persistent even through the application closing. 
- **SQLAlchemy**: Allowed to query and interact with DB using Python instead of SQL. 
- **Flask-Login**: Manages user authentication, making it easier to handle user sessions and protect routes and sensitive personal information. 
- **Flask-Bcrypt**: Hashing capabilities to securely store user passwords.

## Starting up application

##### Clone the repository:
`git clone https://github.com/psap2/restaurant-rating-api`
##### Naviagte to directory
`cd restaurant-rating-api`
##### Activate Virtual Environment
`python3 -m venv env`

`source env/bin/activate`

##### Install dependencies
`pip install -r requirements.txt`

##### Set Up Environment Variables
- Create a `.env` file in your root directory. And add configuration key.

`SECRET_KEY=your_secret_key_here`

##### Initialize database in python shell
```
from app import app, db
with app.app_context():
db.create_all()
```

##### Run application
`python3 app.py`

## Endpoints

1. **Home (/)**
    - **Method**: GET
    - **Description**: Redirects to home page, or user dashboard if user is already authenticated from session token. 
    - **Parameters**: None
    - **Response**: Redirects to /dashboard if authenticated, otherwise renders home.html.
2. **Register (/register)**
    - **Method**: GET, POST
    - **Description**: Handles new user registration.
    - **Parameters**: `username` (string), `password` (string) from RegisterForm.
    - **Response**: Redirects to /login on successful registration, otherwise renders register.html with Registerform(GET).
3. **Login (/login)**
    - **Method**: GET, POST
    - **Description**: Handles user login.
    - **Parameters**: `username` (string), `password` (string) from LoginForm.
    - **Response**: Redirects to /dashboard on successful login, otherwise renders login.html with form(GET).
4. **Dashboard (/dashboard)**
    - **Method**: GET
    - **Description**: Displays user's dashboard with restaurant ratings.
    - **Parameters**: Optional query parameter `search` (string)
    - **Response**: Renders dashboard.html with ratings and user details. And optionally returns user's search query rating results.
5. **Logout (/logout)**
    - **Method**: GET
    - **Description**: Logs out the current user.
    - **Parameters**: None
    - **Response**: Redirects to /login.
6. **Add Rating (/add_rating)**
    - **Method**: GET, POST
    - **Description**: Allows authenticated users to add a restaurant rating.
    - **Parameters**: Form sumbission with fields for `restaurant_name`, `rating`, `cuisine_type`, `meal_date`, `review`, `calories`, `is_anonymous` from RestaurantRatingForm.
    - **Response**: Redirects to /dashboard on successful entry, otherwise renders add_rating.html with RestaurantRatingForm (GET).
7. **Public Ratings (/public_ratings)**
    - **Method**: GET
    - **Description**: Displays all ratings based on search and filters.
    - **Parameters**: Optional query parameters `search` by keywords, `cuisine_type`, `min_rating`.
    - **Response**: Renders public_ratings.html with optional filtered ratings from all resturant ratings.
8. **Edit Rating (/edit_rating/<rating_id>)**
    - **Method**: GET, POST
    - **Description**: Allows users to edit an existing rating.
    - **Parameters**: `rating_id` (int) from URL, form data same as old rating.
    - **Response**: Redirects to /dashboard on successful update, otherwise renders edit_rating.html (GET).
9. **Display Average Ratings (/aggregated/display/average_ratings)**
    - **Method**: GET
    - **Description**: Aggregates and displays average ratings per cuisine type.
    - **Parameters**: None
    - **Response**: Renders plain_display.html with average ratings.
10. **Top Restaurants by Month (/aggregated/top_restaurants/<user_id>)**
    - **Method**: GET
    - **Description**: Displays the highest rated restaurants per month for the user.
    - **Parameters**: `user_id` (int) retrieved from `current_user` from the session.
    - **Response**: Renders plain_display.html with results.
11. **Popular Cuisine Types (/aggregated/popular_cuisines)**
    - **Method**: GET
    - **Description**: Lists the most reviewed cuisine types.
    - **Parameters**: None
    - **Response**: Renders plain_display.html with cuisine types and review counts.

### Testing the API on Localhost Using a Web Browser

##### Start the flask application
`python3 app.py`

##### Test endpoints

- **Home (`/`)**
    - ***Steps***:
        1. Open your web browser and go to `http://127.0.0.1:5000/`.
        2. If logged in, you will be redirected to `/dashboard`. Otherwise, the home page will load with options to login/register.

- **Login (`/login`)**
    - ***Steps***:
        1. Go to `http://127.0.0.1:5000/login`. Also done by clicking on login button on home page.
        2. Enter a valid `username` and `password` for an existing user.
        3. Submit the form.
        4. If successful, you will be redirected to `/dashboard`. If unsuccessful, the page will reload with error messages.
    
- **Dashboard (`/dashboard`)**
    - ***Steps***:
        1. Navigate to `http://127.0.0.1:5000/dashboard` or through navigation bar on localhost (authentication required).
        2. View your personalized dashboard with your ratings.
        3. **Optional**: Test the search functionality by adding a query parameter to the URL:
            - Example: `http://127.0.0.1:5000/dashboard?search={any_keywords}` or using the search functionality on the page.
            - This filters the dashboard to show results matching the search term.

- **Add Rating (`/add_rating`)**
    - ***Steps***:
        1. Go to `http://127.0.0.1:5000/add_rating` or through navigation bar on localhost (authentication required).
        2. Fill out the form with:
            - `restaurant_name`
            - `rating`
            - `cuisine_type`
            - Optional fields: `meal_date`, `review`, `calories`, `is_anonymous`
        3. Submit the form.
        4. If successful, you will be redirected to `/dashboard` with the new rating displayed.

- **Public Ratings (`/public_ratings`)**
    - ***Steps***:
        1. Navigate to `http://127.0.0.1:5000/public_ratings` or through navigation bar on localhost .
        2. All public ratings will be displayed.
        3. **Optional**: Test filtering by adding query parameters, or by using the search features on localhost:
            - Example:
            - `http://127.0.0.1:5000/public_ratings?search=fries` 
            - `http://127.0.0.1:5000/public_ratings?cuisine_type=American`
            - `http://127.0.0.1:5000/public_ratings?min_rating=4`
        4. The results should match the applied filters.

- **Edit Rating (`/edit_rating/<rating_id>`)**
    - ***Steps***:
        1. Replace `<rating_id>` with the ID of a rating you want to edit (e.g., `http://127.0.0.1:5000/edit_rating/1`).
            - Additionally, this can be tested by simply clicking edit on the rating you want to edit in your dashboard.
        2. Modify the fields in the form and submit.
        3. You will be redirected to `/dashboard` with the updated rating displayed.

##### **Aggregation Endpoints**

- **Display Average Ratings (`/aggregated/display/average_ratings`)**
    - ***Steps***:
        1. Go to `http://127.0.0.1:5000/aggregated/display/average_ratings`.
        2. The browser will display a list of cuisine types with their average ratings.

- **Top Restaurants by Month (`/aggregated/top_restaurants/<user_id>`)**
    - ***Steps****:
        1. Replace `<user_id>` with a valid user ID (e.g., `http://127.0.0.1:5000/aggregated/top_restaurants/1`).
        2. The browser will display the highest-rated restaurants per month for that user.

- **Popular Cuisine Types (`/aggregated/popular_cuisines`)**
    - **Steps**:
        1. Go to `http://127.0.0.1:5000/aggregated/popular_cuisines`.
        2. The browser will display a list of cuisine types with their review counts, sorted by popularity.

---