from mongoengine import *
from datetime import datetime
from util import derefer, update_modified
from StudyReference import StudyReference

@update_modified.apply
class Application(Document):
    job_post = ReferenceField('JobPost', reverse_delete_rule=NULLIFY, unique_with='student')
    student = ReferenceField('Student', reverse_delete_rule=NULLIFY)
    applied_at = DateTimeField(default=datetime.now)
    status = StringField(max_length=255, choices=('Diterima', 'Ditolak', 'Resume sedang direview', 'Menunggu wawancara/tes', 'Hasil sedang direview'), default='Resume sedang direview')
    updated_at = DateTimeField()


    def serialize(self):
        return {
            'job_post': derefer(self.job_post),
            'student': derefer(self.student),
            'applied_at': self.applied_at.isoformat(),
            'status': self.status,
            'updated_at': self.updated_at.isoformat()
        }

    def serialize_for_student(self):
        study_references = StudyReference.objects(category=self.job_post.category).first()
        return {
            'status': self.status,
            'salary': self.job_post.salary.serialize(),
            'job_detail': {
                'role': self.job_post.role,
                'company': {
                    'logo_url': self.job_post.company.logo_url,
                    'name': self.job_post.company.name,
                    'company_address': self.job_post.company.company_address
                },
                'study_references': study_references.serialize_topics()
            },
            'updated_at': self.updated_at.isoformat()
        }
