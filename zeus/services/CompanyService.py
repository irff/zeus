from datetime import *

from zeus.models import Application, Company, JobPost, JobSchedule, Category
from zeus.utils import mapper


class CompanyService:

    def add_job(self, company_id, data):
        start_at = datetime.strptime(data['job_schedule']['start_at'], '%d-%m-%Y')
        end_at = datetime.strptime(data['job_schedule']['end_at'], '%d-%m-%Y')
        job_schedule = JobSchedule(start_at=start_at, end_at=end_at)
        data['job_schedule'] = job_schedule
        data['status'] = mapper.map_generate_status(data['status'])
        data['is_open'] = True
        data['job_type'] = 'internship'
        category = Category.objects(name=data['category']).get()
        if category is None:
            category = Category(name=data['category'])
            category.save()
        data['category'] = category.id
        job = JobPost(**data)
        job.company = Company.objects(id=company_id).first()
        job.save()
        return job

    def get_applicants(self, job_id, is_new_application):
        if (is_new_application):
            applications = Application.objects(job_post=job_id, is_new=True).exclude('job_post').all()
        else:
            applications = Application.objects(job_post=job_id).exclude('job_post').all()
        applicants = []
        for application in applications:
            applicants.append(application.get_applicant())
        return applicants

    def get_company(self, company_id):
        company = Company.objects(id=company_id).first()
        return company.serialize()

    def get_jobs_applications(self, company_id, is_new_application):
        jobs = JobPost.objects(company=company_id, is_open=True).only('id', 'role', 'status').all()
        jobs_json = []
        for job in jobs:
            applicants = self.get_applicants(job.id, is_new_application)
            applicant_nums = len(applicants)
            job_json = job.get_summary()

            list_status = []
            for status in job_json['status']:
                list_status.append({
                    'text': mapper.map_status(status, 'company'),
                    'value':status
                })

            job_json['status'] = list_status
            job_json['applicants'] = applicants
            job_json['applicant_num'] = applicant_nums
            jobs_json.append(job_json)
        return jobs_json

    def get_statistics(self, company_id):
        jobs = JobPost.objects(company=company_id, is_open=True).only('id').all()
        job_num = len(jobs)
        applicant_num = 0
        accepted_num = 0
        rejected_num = 0
        for job in jobs:
            applicant_num += Application.objects(job_post=job.id).count()
            accepted_num += Application.objects(job_post=job.id, status='ACCEPTED').count()
            rejected_num += Application.objects(job_post=job.id, status='REJECTED').count()
        in_progress_num = applicant_num - accepted_num - rejected_num
        return {
            'job_num': job_num,
            'applicant_num': applicant_num,
            'accepted_num': accepted_num,
            'rejected_num': rejected_num,
            'in_progress_num': in_progress_num
        }

    def modify_company(self, company_id, data):
        Company.objects(id=company_id).modify(**data)
