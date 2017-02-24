from zeus.models import Application
from zeus.utils import mailer

class ApplicationService:

    def update_status(self, company_id, application_id, status):
        application = Application.objects(id=application_id, company=company_id).first()
        application.status = status
        application.is_new = False
        application.save()

        email = application.student.email
        status = application.status
        company = application.company
        job_post = application.job_post

        mailer.send_updated_status.delay(to=[email], data={
            'status': status,
            'company': company,
            'job_post': job_post
        })
