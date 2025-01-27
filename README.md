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