from flask import Flask, jsonify, request, render_template, Response, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_dotenv import DotEnv
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

import json

from models import *
from seeds import Seeder
from forms import *

env = DotEnv()
login_manager = LoginManager()
app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'QuintDev'
env.init_app(app)
login_manager.init_app(app)
db = MongoEngine(app)

Seeder().seed()

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
    form = LoginForm.from_json(request.json)
    if(not form.validate()):
        return jsonify(form.serialize_error()), 403

    email = request.json['email']
    password = request.json['password']

    user = User.objects(email=email).first()
    if user == None or not check_password_hash(user.password, password):
        return jsonify({
            'status': 'invalid credentials'
        }), 403
    else:
        login_user(user)
        return jsonify({
            'user_id': str(user.id),
            'name': user.student.name,
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
    form = RegistrationForm.from_json(request.json)
    try:
        if(not form.validate()):
            return jsonify(form.serialize_error()), 403
        
        email = request.json['email']
        password = request.json['password']
        user = User(email=email, password=generate_password_hash(password))
        user.save()
        return jsonify({
            'status': 'account created'
        }), 201
    except NotUniqueError:
        return jsonify({
            'status': 'email already exist'
        }), 403

# JOB POST CRUD
@app.route("/jobs", methods=['GET'])
def get_jobs():
    jobs = JobPost.objects().all()
    jobs_json = []
    for job in jobs:
        jobs_json.append(job.serialize())
    return jsonify({
        'jobs': jobs_json,
        'status': 'success'
    }), 200

@app.route("/jobs", methods=['POST'])
def add_job():
    data = request.json
    data['internship_schedule'] = InternshipSchedule(**data['internship_schedule'])
    data['contact_person'] = ContactPerson.objects(id=data['contact_person']).first()
    new_job = JobPost(**data)
    new_job.save()

    return jsonify({
        'status': 'job successfully posted'
    }), 201

@app.route("/jobs/<job_id>", methods=['PUT'])
def modify_job(job_id):
    data = request.json
    data['internship_schedule'] = InternshipSchedule(**data['internship_schedule'])
    data['contact_person'] = ContactPerson.objects(id=data['contact_person']).first()
    job = JobPost.objects(id=job_id).modify(**data)

    return jsonify({
        'job': job.serialize(),
        'status': 'job successfully modified'
    }), 200

@app.route("/jobs/<job_id>", methods=['DELETE'])
def delete_job(job_id):
    JobPost.objects(id=job_id).delete()
    return jsonify({
        'status': 'job successfully deleted'
    }), 200



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
