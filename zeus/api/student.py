from flask import request, jsonify, url_for, render_template
from zeus import app
from zeus.models import *
from zeus.utils.linkedin_api import *
from datetime import *
from zeus.utils import auth
from zeus.utils import mailer
from zeus.utils.mailer import *
import os
import jwt

@app.route("/students/login", methods=['POST'])
def student_login():
    email = request.json['email']
    password = request.json['password']

    user = UserStudent.objects(email=email).first()
    if user == None or not user.check_password(password):
        return jsonify({}), 403
    else:
        student_id = str(user.student.id) if user.student != None else ''
        token = jwt.encode({
            'exp': datetime.utcnow() + timedelta(days=365),
            'user_id': str(user.id),
            'student_id': student_id
        }, app.secret_key, algorithm='HS256')
        return jsonify({
            'token': token,
            'student_id': student_id
        }), 200


@app.route("/students/login/linkedin")
def student_linkedin_login():
    return linkedin.authorize(callback=url_for('student_linkedin_authorized', _external=True))

@app.route("/students/authorize/linkedin")
def student_linkedin_authorized():
    resp = linkedin.authorized_response()
    if request.args['code'] is None:
        return render_template('linkedin-redirect.html', data={})

    save_token(resp['access_token'])
    fields = '(id,first-name,picture-url,last-name,public-profile-url,headline,email-address)'
    resp = linkedin.get(
        'https://api.linkedin.com/v1/people/~:'+fields+'?format=json',
    )

    data = dict(
        first_name = resp.data['firstName'],
        last_name = resp.data['lastName'],
        photo_url = resp.data['pictureUrl'],
        linkedin_url = resp.data['publicProfileUrl'],
        headline = resp.data['headline']
    )

    email = resp.data['emailAddress']
    user = UserStudent.objects(email=email).first()
    if(user == None):
        student = Student(**data)
        student.save()
        user = UserStudent(email=email, student=student)
        user.set_password(os.urandom(12))
        user.save()
    token = jwt.encode({
        'exp': datetime.utcnow() + timedelta(minutes=30),
        'student_id': str(user.student.id)
    }, app.secret_key, algorithm='HS256')
    data = {
        'student_id': str(user.student.id),
        'token': token
    }
    return render_template('linkedin-redirect.html', data=data)

@app.route("/students/register", methods=['POST'])
def student_register():
    try:
        email = request.json['email']
        password = request.json['password']
        user = UserStudent(email=email)
        user.set_password(password)
        user.save()
        token = jwt.encode({
            'exp': datetime.utcnow() + timedelta(days=365),
            'user_id': str(user.id)
        }, app.secret_key, algorithm='HS256')
        return jsonify({
            'token': token,
        }), 200
    except NotUniqueError:
        return jsonify({
            'status': 'email already exist'
        }), 403
    except ValidationError:
        return jsonify(), 403

@app.route("/students", methods=['POST'])
@auth.require_token
def add_student():
    try:
        token_data = auth.extract_data(request.headers)
        data = request.json
        user = UserStudent.objects(id=token_data['user_id']).first()
        student = Student(**data)
        student.save()
        user.student = student
        user.save()
        token = jwt.encode({
            'exp': datetime.utcnow() + timedelta(days=365),
            'user_id': str(user.id),
            'student_id': str(user.student.id)
        }, app.secret_key, algorithm='HS256')
        return jsonify({
            'student_id': str(user.student.id)
        }), 204
    except (InvalidQueryError, FieldDoesNotExist):
        return jsonify(), 400

@app.route("/students/<student_id>", methods=['PUT'])
@auth.require_token
@auth.same_property('student_id')
def modify_student(student_id):
    try:
        data = request.json
        student = Student.objects(id=student_id).modify(**data)
        return jsonify(), 204
    
    except InvalidQueryError:
        return jsonify(), 400

# @app.route("/students/<student_id>", methods=['DELETE'])
# @auth.require_token
# @auth.same_property('student_id')
# def delete_student(student_id):
#     UserStudent.objects(student=student_id).delete()
#     Student.objects(id=student_id).delete()
#     return jsonify(), 204

@app.route("/students/<student_id>/jobs")
@auth.require_token
@auth.same_property('student_id')
def get_student_jobs(student_id):
    applications = Application.objects(student=student_id).all()
    data = []
    for application in applications:
        data.append(str(application.job_post.id))
    return jsonify({'jobs_id':data}), 200

@app.route("/students/<student_id>/jobs", methods=['POST'])
@auth.require_token
@auth.same_property('student_id')
def apply_job(student_id):
    job_id = request.json['job_id']
    application = Application(student=student_id, job_post=job_id)
    application.save()
    company = JobPost.objects(id=job_id).first().company
    user_company = UserCompany.objects(company=company).only('email').first()
    student = Student.objects(id=student_id).first()
    mailer.send_applied_job.delay(to=[user_company.email], data={
        'resume_url': student.resume_url
    })
    return jsonify(), 204