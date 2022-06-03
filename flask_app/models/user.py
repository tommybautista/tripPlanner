from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import request, flash
import re
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "trip_planner2"
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register_user(cls, data):
        query = "INSERT INTO users(username, email, password) VALUES (%(username)s, %(email)s, %(password)s);" 
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE users SET username = %(username)s, email = %(email)s, password = %(password)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)    

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        user = cls(results[0])
        return user

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False        
        user = cls(results[0])
        return user

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_register(user):
        is_valid = True
        user_in_db = User.get_user_by_email(user)
        if user_in_db:
            flash("Email is associated with another account", 'danger')
            is_valid = False
        if len(user['username']) < 3:
            flash("Username must be at least 3 characters", "danger")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'danger')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "danger")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Password must match", "danger")
            is_valid = False            
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        user_in_db = User.get_user_by_email(user)
        if not user_in_db:
            flash("Email is not associated to an account", "danger")
            is_valid = False        
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "danger")
            is_valid = False          
        return is_valid

    @staticmethod
    def validate_update(user):
        is_valid = True
        user_in_db = User.get_user_by_email(user)
        if len(user['username']) < 3:
            flash("Username must be at least 3 characters", "danger")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'danger')
            is_valid = False

        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "danger")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Password must match", "danger")
            is_valid = False            
        return is_valid

