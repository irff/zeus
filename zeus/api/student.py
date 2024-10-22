from flask import request, jsonify, url_for, render_template
from zeus import app
from zeus.models import *
from zeus.utils.linkedin_api import *
from datetime import *
from zeus.utils import auth
from zeus.utils import mailer
from zeus.utils.mailer import *
import os

def get_user(email, password):
    user = UserStudent.objects(email=email).first()
    if user == None:
        raise ValueError('Invalid email')
    if not user.check_password(password):
        raise ValueError('Invalid password')
    name = user.student.first_name if user.student != None else user.email.split('@')[0]
    return (user, name)

@app.route("/students/login", methods=['POST'])
def student_login():
    try:
        email = request.json['email']
        password = request.json['password']
        user, name = get_user(email, password)
        student_id = str(user.student.id) if user.student != None else ''
        token = auth.create_token({
            'user_id': str(user.id),
            'student_id': student_id
        })
        return jsonify({
            'token': token,
            'student_id': student_id,
            'name': name
        }), 200
    except ValueError as e:
        return jsonify({'message': e.args}), 403
    except KeyError as e:
        message = 'Field cannot be empty: {0}'.format(e.args)
        return jsonify({'message': message}), 400

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
        headline = resp.data['headline'],
        major = 'empty',
        university = 'empty',
        resume_url = 'http://www.empty.com'
    )

    email = resp.data['emailAddress']
    user = UserStudent.objects(email=email).first()
    if(user == None):
        student = Student(**data)
        student.save()
        user = UserStudent(email=email, student=student)
        user.set_password(os.urandom(12))
        user.save()
    token = auth.create_token({
        'exp': datetime.utcnow() + timedelta(minutes=30),
        'student_id': str(user.student.id)
    })
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
        token = auth.create_token({
            'user_id': str(user.id)
        })
        return jsonify({
            'token': token,
            'user_id': str(user.id)
        }), 200
    except NotUniqueError:
        return jsonify({
            'status': 'email already exist'
        }), 403
    except ValidationError:
        return jsonify(), 403
    except KeyError as e:
        message = 'Field cannot be empty: {0}'.format(e.args)
        return jsonify({'message': message}), 400

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
        token = auth.create_token({
            'exp': datetime.utcnow() + timedelta(days=365),
            'user_id': str(user.id),
            'student_id': str(user.student.id)
        })
        return jsonify({
            'student_id': str(user.student.id),
            'token': token
        }), 200
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
    application.company = JobPost.objects(id=job_id).first().company
    application.is_new = True
    application.save()
    job_post = JobPost.objects(id=job_id).first()
    company = job_post.company
    email = UserCompany.objects(company=company).first().email
    student = Student.objects(id=student_id).first()
    student.email = UserStudent.objects(student=student_id).first().email
    mailer.send_applied_job.delay(to=[email], data={
        'student_mail': student.email,
        'student': student,
        'company': company,
        'job_post': job_post
    })
    return jsonify(), 204

@app.route("/students/<student_id>")
@auth.require_token
@auth.same_property('student_id')
def get_student(student_id):
    student = Student.objects(id=student_id).first()
    return jsonify(student.serialize()), 200

@app.route("/students/<student_id>/jobs/detail")
@auth.require_token
@auth.same_property('student_id')
def get_student_jobs_detail(student_id):
    applications = Application.objects(student=student_id).all()
    registered_num = Application.objects(student=student_id).count()
    accepted_num = Application.objects(student=student_id, status='ACCEPTED').count()
    rejected_num = Application.objects(student=student_id, status='REJECTED').count()
    processed_num = registered_num - accepted_num - rejected_num

    jobs = []
    for application in applications:
        jobs.append(application.serialize_for_student())
    return jsonify({
        'registered_num': registered_num,
        'processed_num': processed_num,
        'accepted_num': accepted_num,
        'rejected_num': rejected_num,
        'jobs': jobs
    })
# @app.route("/students/<student_id>", methods=['DELETE'])
# @auth.require_token
# @auth.same_property('student_id')
# def delete_student(student_id):
#     UserStudent.objects(student=student_id).delete()
#     Student.objects(id=student_id).delete()
#     return jsonify(), 204