from flask import Flask, jsonify, request, render_template, Response, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_dotenv import DotEnv
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

import json

from models import *
from seeds import Seeder

env = DotEnv()
login_manager = LoginManager()
app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'QuintDev'
env.init_app(app)
login_manager.init_app(app)
db = MongoEngine(app)

# LOGIN, LOGOUT, REGISTER
@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({
        'status': 'Unauthorized Area'
    }), 401

@app.route("/login", methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.objects(email=email).first()

    if user == None or not check_password_hash(user.password, password):
        return jsonify({
            'status': 'invalid credentials'
        }), 403
    else:
        login_user(user)
        return jsonify({
            'status': 'logged in successfully'
        }), 200

@app.route("/logout")
def logout():
    logout_user()
    return jsonify({
        'status': 'logged out successfully'
    }), 200

@app.route("/register", methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']

    try:
        user = User(email=email, password=generate_password_hash(password))
        user.save()
        return jsonify({
            'status': 'account created'
        }), 201
    except NotUniqueError:
        return jsonify({
            'status': 'email already exist'
        }), 403

# ROUTE TESTING
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/students")
def students():
    students = Student.objects().first()
    return jsonify(students.serialize()), 200

@app.route("/users")
def users():
    users = User.objects().first()
    return jsonify(users.serialize()), 200

@app.route("/companies")
def companies():
    companies = Company.objects().first()
    return jsonify(companies.serialize()), 200

@app.route("/applications")
def applications():
    applications = Application.objects().first()
    return jsonify(applications.serialize()), 200

if __name__ == "__main__":
    app.run()
