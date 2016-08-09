from flask import Flask, jsonify, request, render_template, Response
from flask_mongoengine import MongoEngine
from flask_dotenv import DotEnv

import json

from models import *


env = DotEnv()
app = Flask(__name__)
app.config['DEBUG'] = True
env.init_app(app)
db = MongoEngine(app)

Student.drop_collection()
student1 = Student(name='Tri Ahmad Irfan',
				   major='Computer Science',
				   school='University of Indonesia',
				   resume_url='http://google.com',
				   linkedin_url='http://google.com',
				   photo_url='http://google.com',
				   headline='Back-end developer at Quint')
student1.save()

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/students")
def students():
	students = Student.objects().first()
	return Response(json.dumps(students.serialize()), mimetype='application/json')

if __name__ == "__main__":
    app.run()
