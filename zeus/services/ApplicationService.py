from zeus.models import Application, StatusHistory, UserStudent
from zeus.utils import mailer, mapper

class ApplicationService:

    def modify_status(self, company_id, application_id, current_status, email_rejected_content):
        application = Application.objects(id=application_id, company=company_id).first()
        if application is None:
            return

        prev_status = application.status

        if prev_status == 'REJECTED' or prev_status == 'ACCEPTED':
            return

        application.status = current_status
        application.is_new = False
        application.save()

        email = UserStudent.objects(student=application.student.id).first().email
        student = application.student
        company = application.company
        job_post = application.job_post

        if email_rejected_content == '' and current_status != 'REJECTED':
            mailer.send_updated_status.delay(to=[email], data={
                'prev_status': mapper.map_status(prev_status, 'student'),
                'current_status': mapper.map_status(current_status, 'student'),
                'student': student,
                'company': company,
                'job_post': job_post
            })
        elif email_rejected_content != '' and current_status == 'REJECTED':
            mailer.send_updated_status.delay(to=[email], data={
                'prev_status': mapper.map_status(prev_status, 'student'),
                'current_status': mapper.map_status(current_status, 'student'),
                'student': student,
                'company': company,
                'job_post': job_post,
                'email_rejected_content': email_rejected_content
            })

    def send_resume_read(self,company_id, application_id):
        application = Application.objects(id=application_id, company=company_id).first()
        if application is None or not application.is_new:
            return

        prev_status_history = StatusHistory({'status': application.status})
        application.status_histories.append(prev_status_history)

        application.is_new = False
        application.status = 'RESUME_REVIEWED'

        email = UserStudent.objects(student=application.student.id).first().email
        student = application.student
        company = application.company
        job_post = application.job_post

        mailer.send_resume_read.delay(to=[email], data={
            'student': student,
            'company': company,
            'job_post': job_post
        })
