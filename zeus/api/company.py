from datetime import *
from flask import request, jsonify

from zeus import app
from zeus.models import *
from zeus.services import application as _application, company as _company
from zeus.utils import auth, upload


@app.route("/companies/login", methods=['POST'])
def company_login():
    email = request.json['email']
    password = request.json['password']

    user = UserCompany.objects(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({}), 403
    else:
        company_id = str(user.company.id) if user.company is not None else ''
        token = auth.create_token({
            'exp': datetime.utcnow() + timedelta(days=365),
            'user_id': str(user.id),
            'company_id': company_id,
            'role': 'company'
        })
        return jsonify({
            'token': token,
            'company_id': company_id
        }), 200


@app.route("/companies/register", methods=['POST'])
def company_register():
    try:
        email = request.json['email']
        password = request.json['password']
        user = UserCompany(email=email)
        user.set_password(password)
        user.save()
        token = auth.create_token({
            'exp': datetime.utcnow() + timedelta(days=365),
            'user_id': str(user.id),
            'role': 'company'
        })
        return jsonify({
            'token': token
        }), 200
    except NotUniqueError:
        return jsonify({
            'status': 'email already exist'
        }), 403
    except ValidationError:
        return jsonify(), 403


@app.route("/companies", methods=['POST'])
@auth.require_token
@auth.privilege('company')
def add_company():
    try:
        token_data = auth.extract_data(request.headers)
        data = request.json
        user = UserCompany.objects(id=token_data['user_id']).first()
        new_company = Company(**data)
        new_company.save()
        user.company = new_company
        user.save()
        token = auth.create_token({
            'exp': datetime.utcnow() + timedelta(days=365),
            'user_id': str(user.id),
            'company_id': str(user.company.id),
            'role': 'company'
        })
        return jsonify({
            'token': token,
            'company_id': str(new_company.id)
        }), 201
    except (InvalidQueryError, FieldDoesNotExist):
        return jsonify(), 400


@app.route("/companies/<company_id>")
@auth.require_token
@auth.same_property('company_id')
def get_company(company_id):
    token_data = auth.extract_data(request.headers)
    company = _company.get_company(company_id)

    token = auth.create_token({
        'exp': datetime.utcnow() + timedelta(days=365),
        'user_id': token_data['user_id'],
        'company_id': token_data['company_id'],
        'role': 'company'
    })
    return jsonify({
        'token': token,
        'company': company
    }), 200


@app.route("/companies/<company_id>", methods=['PUT'])
@auth.require_token
@auth.privilege('company')
@auth.same_property('company_id')
def modify_company(company_id):
    try:
        token_data = auth.extract_data(request.headers)
        data = request.json
        _company.modify_company(company_id, data)

        token = auth.create_token({
            'exp': datetime.utcnow() + timedelta(days=365),
            'user_id': token_data['user_id'],
            'company_id': token_data['company_id'],
            'role': 'company'
        })
        return jsonify({
            'token': token
        }), 200
    except InvalidQueryError:
        return jsonify(), 400


@app.route("/companies/<company_id>/applications")
@auth.require_token
@auth.privilege('company')
@auth.same_property('company_id')
def get_jobs_applications(company_id):
    try:
        token_data = auth.extract_data(request.headers)
        is_new_application = bool(request.args.get('new')) == True
        applications = _company.get_jobs_applications(company_id=company_id, is_new_application=is_new_application)

        token = auth.create_token({
            'exp': datetime.utcnow() + timedelta(days=365),
            'user_id': token_data['user_id'],
            'company_id': token_data['company_id'],
            'role': 'company'
        })
        return jsonify({
            'token': token,
            'applications': applications
        }), 200
    except (InvalidQueryError, FieldDoesNotExist):
        return jsonify(), 400


@app.route("/companies/<company_id>/applications/<application_id>/resume-read", methods=['POST'])
@auth.require_token
@auth.privilege('company')
@auth.same_property('company_id')
def send_resume_read(company_id, application_id):
    try:
        token_data = auth.extract_data(request.headers)
        _application.send_resume_read(company_id, application_id)

        token = auth.create_token({
            'exp': datetime.utcnow() + timedelta(days=365),
            'user_id': token_data['user_id'],
            'company_id': token_data['company_id'],
            'role': 'company'
        })
        return jsonify({
            'token': token
        }), 200
    except InvalidQueryError:
        return jsonify(), 400


@app.route("/companies/<company_id>/applications/<application_id>/status", methods=['PUT'])
@auth.require_token
@auth.privilege('company')
@auth.same_property('company_id')
def modify_status(company_id, application_id):
    try:
        token_data = auth.extract_data(request.headers)
        current_status = request.json['status']
        email_rejected_subject = ''
        if 'email_rejected_subject' in request.json:
            email_rejected_subject = request.json['email_rejected_subject']
        email_rejected_content = ''
        if 'email_rejected_content' in request.json:
            email_rejected_content = request.json['email_rejected_content']
        _application.modify_status(company_id, application_id, current_status, email_rejected_subject, email_rejected_content)

        token = auth.create_token({
            'exp': datetime.utcnow() + timedelta(days=365),
            'user_id': token_data['user_id'],
            'company_id': token_data['company_id'],
            'role': 'company'
        })
        return jsonify({
            'token': token
        }), 200
    except InvalidQueryError:
        return jsonify(), 400


@app.route("/companies/<company_id>/jobs", methods=['POST'])
@auth.require_token
@auth.privilege('company')
@auth.same_property('company_id')
def company_add_job(company_id):
    token_data = auth.extract_data(request.headers)
    data = request.json
    job = _company.add_job(company_id=company_id, data=data)

    token = auth.create_token({
        'exp': datetime.utcnow() + timedelta(days=365),
        'user_id': token_data['user_id'],
        'company_id': token_data['company_id'],
        'role': 'company'
    })
    return jsonify({
        'token': token,
        'job_id': str(job.id)
    }), 201


@app.route("/companies/<company_id>/statistics")
@auth.require_token
@auth.privilege('company')
@auth.same_property('company_id')
def get_statistics(company_id):
    token_data = auth.extract_data(request.headers)
    statistics = _company.get_statistics(company_id)

    token = auth.create_token({
        'exp': datetime.utcnow() + timedelta(days=365),
        'user_id': token_data['user_id'],
        'company_id': token_data['company_id'],
        'role': 'company'
    })
    return jsonify({
        'token': token,
        'statistics': statistics
    }), 200


# @app.route("/companies/<company_id>/upload/logo", methods=['POST'])
# def company_upload_logo(company_id):
#     file_name = '{0}_logo'.format(company_id)
#     logo_path = upload.upload(request.files, company_id, file_name)
#
#     if logo_path == 'failed':
#         return jsonify({
#             'error': 'failed'
#         }), 400
#     else:
#         return jsonify({
#             'logo_path': logo_path
#         }), 200
#
# @app.route("/companies/<company_id>/upload/header", methods=['POST'])
# def company_upload_logo(company_id):
#     file_name = '{0}_header'.format(company_id)
#     header_path = upload.upload(request.files, company_id, file_name)
#
#     if header_path == 'failed':
#         return jsonify({
#             'error': 'failed'
#         }), 400
#     else:
#         return jsonify({
#             'header_path': header_path
#         }), 200

# @app.route("/companies")
# @auth.require_token
# def get_companies():
#     companies = Company.objects().all()
#     companies_json = []
#     for company in companies:
#         companies_json.append(company.serialize())
#     return jsonify({
#         'companies': companies_json,
#         'status': 'success'
#     }), 200

# @app.route("/companies/<company_id>", methods=['PUT'])
# @auth.require_token
# def modify_company(company_id):
#     req = request.json
#     data = req
#     data['office_locations'] = []
#     data['job_posts'] = []

#     for item_id in req['office_locations']:
#         off_loc = OfficeLocation.objects(id=item_id).first()
#         data['office_locations'].append(off_loc)

#     for item_id in req['job_posts']:
#         job_post = JobPost.objects(id=item_id).first()
#         data['job_posts'].append(job_post)
#     data['contact_person'] = ContactPerson.objects(id=data['contact_person']).first()
#     company = Company.objects(id=company_id).modify(**data)

#     return jsonify({
#         'company': company.serialize(),
#         'status': 'company successfully modified'
#     }), 200

# @app.route("/companies/<company_id>", methods=['DELETE'])
# @auth.require_token
# def delete_company(company_id):
#     Company.objects(id=company_id).delete()
#     return jsonify({
#         'status': 'company successfully deleted'
#     }), 200