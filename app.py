from flask import Flask, jsonify, request, render_template, Response, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_dotenv import DotEnv
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_oauthlib.provider import OAuth2Provider

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
oauth = OAuth2Provider(app)

Seeder().seed()

@login_manager.user_loader
def load_user(user_id):
    user = UserStudent.objects(id=user_id).first()
    if(user == None):
        user = UserCompany.objects(id=user_id).first()
    return user

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({
        'status': 'Unauthorized Area'
    }), 401

# STUDENT LOGIN, LOGOUT, REGISTER
@app.route("/students/login", methods=['POST'])
def student_login():
    form = LoginForm.from_json(request.json)
    if(not form.validate()):
        return jsonify(form.serialize_error()), 403

    email = request.json['email']
    password = request.json['password']

    user = UserStudent.objects(email=email).first()
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

@app.route("/students/logout")
def student_logout():
    logout_user()
    return jsonify({
        'status': 'logged out successfully'
    }), 200

@app.route("/students/register", methods=['POST'])
def student_register():
    form = RegistrationForm.from_json(request.json)
    try:
        if(not form.validate()):
            return jsonify(form.serialize_error()), 403
        
        email = request.json['email']
        password = request.json['password']
        user = UserStudent(email=email, password=generate_password_hash(password))
        user.save()
        return jsonify({
            'status': 'account created'
        }), 201
    except NotUniqueError:
        return jsonify({
            'status': 'email already exist'
        }), 403

# COMPANY LOGIN, LOGOUT, REGISTER
@app.route("/companies/login", methods=['POST'])
def company_login():
    form = LoginForm.from_json(request.json)
    if(not form.validate()):
        return jsonify(form.serialize_error()), 403

    email = request.json['email']
    password = request.json['password']

    user = UserCompany.objects(email=email).first()
    if user == None or not check_password_hash(user.password, password):
        return jsonify({
            'status': 'invalid credentials'
        }), 403
    else:
        login_user(user)
        return jsonify({
            'user_id': str(user.id),
            'name': user.company.name,
            'status': 'logged in successfully'
        }), 200

@app.route("/companies/logout")
def company_logout():
    logout_user()
    return jsonify({
        'status': 'logged out successfully'
    }), 200

@app.route("/companies/register", methods=['POST'])
def company_register():
    form = RegistrationForm.from_json(request.json)
    try:
        if(not form.validate()):
            return jsonify(form.serialize_error()), 403
        
        email = request.json['email']
        password = request.json['password']
        user = UserCompany(email=email, password=generate_password_hash(password))
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

# COMPANY CRUD
@app.route("/companies", methods=['GET'])
def get_companies():
    companies = Company.objects().all()
    companies_json = []
    for company in companies:
        companies_json.append(company.serialize())
    return jsonify({
        'companies': companies_json,
        'status': 'success'
    }), 200

@app.route("/companies", methods=['POST'])
def add_company():
    req = request.json
    data = req
    data['office_locations'] = []
    for item_id in req['office_locations']:
        off_loc = OfficeLocation.objects(id=item_id).first()
        data['office_locations'].append(off_loc)

    data['contact_person'] = ContactPerson.objects(id=data['contact_person']).first()
    new_company = Company(**data)
    new_company.save()

    return jsonify({
        'status': 'company profile successfully posted'
    }), 201

@app.route("/companies/<company_id>", methods=['PUT'])
def modify_company(company_id):
    req = request.json
    data = req
    data['office_locations'] = []
    data['job_posts'] = []

    for item_id in req['office_locations']:
        off_loc = OfficeLocation.objects(id=item_id).first()
        data['office_locations'].append(off_loc)

    for item_id in req['job_posts']:
        job_post = JobPost.objects(id=item_id).first()
        data['job_posts'].append(job_post)
    data['contact_person'] = ContactPerson.objects(id=data['contact_person']).first()
    company = Company.objects(id=job_id).modify(**data)

    return jsonify({
        'company': company.serialize(),
        'status': 'company successfully modified'
    }), 200

@app.route("/companies/<company_id>", methods=['DELETE'])
def delete_company(company_id):
    Company.objects(id=company_id).delete()
    return jsonify({
        'status': 'company successfully deleted'
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
    users = UserStudent.objects().first()
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
