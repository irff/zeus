from flask import Flask, jsonify, request, render_template, Response
from flask_mongoengine import MongoEngine
from flask_dotenv import DotEnv

import json

from models import *
from seeds import Seeder

env = DotEnv()
app = Flask(__name__)
app.config['DEBUG'] = True
env.init_app(app)
db = MongoEngine(app)

seeder = Seeder()
seeder.seed()

# ROUTE TESTING
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/students")
def students():
    students = Student.objects().first()
    return Response(json.dumps(students.serialize()), mimetype='application/json')

@app.route("/users")
def users():
    users = User.objects().first()
    return Response(json.dumps(users.serialize()), mimetype='application/json')

@app.route("/companies")
def companies():
    companies = Company.objects().first()
    return Response(json.dumps(companies.serialize()), mimetype='application/json')

@app.route("/applications")
def applications():
    applications = Application.objects().first()
    return Response(json.dumps(applications.serialize()), mimetype='application/json')


if __name__ == "__main__":
    app.run()
