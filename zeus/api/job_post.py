from flask import request, jsonify
from zeus import app
from zeus.models import *
from zeus.utils import auth


@app.route("/jobs", methods=['GET'])
@auth.require_token
def get_jobs():
    jobs = JobPost.objects(is_open=True)
    jobs_json = []
    for job in jobs:
        jobs_json.append(job.serialize())
    jobs_json = sorted(jobs_json, key=lambda job: job['created_at'], reverse=True)
    return jsonify(jobs_json), 200

# @app.route("/jobs/<job_id>")
# @auth.require_token
# def get_job(job_id):
#     job = JobPost.objects(id=job_id).first()
#     return jsonify(job.serialize()), 200

# @app.route("/jobs/<job_id>", methods=['PUT'])
# @auth.require_token
# def modify_job(job_id):
#     data = request.json
#     data['internship_schedule'] = InternshipSchedule(**data['internship_schedule'])
#     data['contact_person'] = ContactPerson.objects(id=data['contact_person']).first()
#     job = JobPost.objects(id=job_id).modify(**data)

#     return jsonify({
#         'job': job.serialize(),
#         'status': 'job successfully modified'
#     }), 200

# @app.route("/jobs/<job_id>", methods=['DELETE'])
# @auth.require_token
# def delete_job(job_id):
#     JobPost.objects(id=job_id).delete()
#     return jsonify({
#         'status': 'job successfully deleted'
#     }), 200
