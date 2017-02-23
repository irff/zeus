from flask import request, jsonify
from zeus import app
from zeus.models import *
from datetime import *
from zeus.utils import auth

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
            'company_id': company_id
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
            'user_id': str(user.id)
        })
        return jsonify({
            'token': token,
        }), 200
    except NotUniqueError:
        return jsonify({
            'status': 'email already exist'
        }), 403
    except ValidationError:
        return jsonify(), 403


@app.route("/companies", methods=['POST'])
@auth.require_token
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
            'company_id': str(user.company.id)
        })
        return jsonify({
            'company_id': str(new_company.id),
            'token': token
        }), 201
    except (InvalidQueryError, FieldDoesNotExist):
        return jsonify(), 400


@app.route("/companies/<company_id>/jobs", methods=['POST'])
@auth.require_token
@auth.same_property('company_id')
def add_job(company_id):
    data = request.json
    contact_person = ContactPerson.objects(email=data['contact_person']['email']).first()
    if(contact_person == None):
        contact_person = ContactPerson(**data['contact_person'])
        contact_person.save()
    start_at = datetime.strptime(data['job_schedule']['start_at'], '%d-%m-%Y')
    end_at = datetime.strptime(data['job_schedule']['end_at'], '%d-%m-%Y')
    job_schedule = JobSchedule(start_at=start_at, end_at=end_at)
    data['contact_person'] = contact_person
    data['job_schedule'] = job_schedule
    job = JobPost(**data)
    job.company = Company.objects(id=company_id).first()
    job.save()
    return jsonify({
        'job_id': str(job.id)
    }), 200
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