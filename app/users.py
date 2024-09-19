import os
from datisbase import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
import logging
from functools import wraps
from flask import redirect, session, url_for
# Configure logging
logging.basicConfig(level=logging.DEBUG)


def add_user(name, password):
    sql = text("INSERT INTO users (name, password) VALUES (:name, :password)")
    params = {"name": name, "password": password}
    
    try:
        db.session.execute(sql, params)
        db.session.commit()
        return "User added successfully"
    except Exception as e:
        db.session.rollback()
        return f"Error adding user: {e}"


def login(name, password):
    sql = text("SELECT password, id, role FROM users WHERE name=:name")
    result = db.session.execute(sql, {"name": name})
    user = result.fetchone()
    
    if not user:
        return False
    if not check_password_hash(user[0], password):
        
        return False
    
    session["user_id"] = user[1]
    session["user_name"] = name
    session["user_role"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()
    return True


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["user_role"]

def register(name, password, role):
    hash_value = generate_password_hash(password)
    try:
        # Insert new user into the database
        sql = "INSERT INTO users (name, password, role) VALUES (:name, :password, :role)"
        logging.debug(f"SQL: {sql} | Params: {name}, {hash_value}, {role}")
        db.session.execute(text(sql), {"name": name, "password": hash_value, "role": role})
        db.session.commit()

        create_role_sql = text(f"CREATE ROLE {name} LOGIN PASSWORD '{password}'")
        db.session.execute(create_role_sql)
        db.session.commit()

        # Grant DELETE permissions only on the users table
        grant_sql = text("GRANT DELETE ON ALL TABLES IN SCHEMA public TO "+name)
        db.session.execute(grant_sql, {"name": name})
        db.session.commit()

        logging.debug(f"Delete permission granted on users table to user: {name}")
    except Exception as e:
        logging.error(f"Error during registration: {e}")
        return False

    return login(name, password)

def get_user_by_username(username):
    sql = text("SELECT id FROM users WHERE name = :username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    return user  # Returns None if no user is found

def delete_user(name):
    try:
        sql = "DELETE FROM users WHERE name=:name"
        db.session.execute(text(sql), {"name": name})
        db.session.commit()
        return True
    except Exception as e:
        logging.error(f"Error deleting user {name}: {e}")
        return False


def user_id():
    return session.get("user_id", 0)

def require_role(role):
    if role > session.get("user_role", 0):
        abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)