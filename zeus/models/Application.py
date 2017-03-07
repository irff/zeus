from mongoengine import *
from datetime import datetime
from util import derefer, to_json
from StudyReference import StudyReference
from UserStudent import UserStudent
from zeus.utils import mapper

status_choices = (
    'WAIT_FOR_REVIEW',
    'RESUME_REVIEWED',
    'WAIT_FOR_PHONE',
    'PHONE_REVIEWED',
    'WAIT_FOR_ONLINE_TEST',
    'ONLINE_TEST_REVIEWED',
    'WAIT_FOR_SUBMISSION',
    'SUBMISSION_REVIEWED',
    'WAIT_FOR_ONSITE_TEST',
    'ONSITE_TEST_REVIEWED',
    'REJECTED',
    'ACCEPTED'
)

class StatusHistory(EmbeddedDocument):
    changed_at = DateTimeField(default=datetime.now)
    status = StringField(max_length=255, choices=status_choices)

    def serialize(self):
        return {
            'changed_at': self.changed_at.isoformat(),
            'status': self.status
        }


class Application(Document):
    job_post = ReferenceField('JobPost', reverse_delete_rule=NULLIFY, unique_with='student')
    student = ReferenceField('Student', reverse_delete_rule=NULLIFY)
    company = ReferenceField('Company', reverse_delete_rule=NULLIFY)
    applied_at = DateTimeField(default=datetime.now)
    status = StringField(max_length=255, choices=status_choices, default='WAIT_FOR_REVIEW')
    status_histories = ListField(EmbeddedDocumentField('StatusHistory'))
    is_new = BooleanField()

    def serialize(self):
        return {
            'job_post': derefer(self.job_post),
            'student': derefer(self.student),
            'company': derefer(self.company),
            'applied_at': self.applied_at.isoformat(),
            'status': self.status,
            'status_histories': to_json(self.status_histories)
        }

    def get_applicant(self):
        email = UserStudent.objects(student=self.student.id).first().email
        return {
            'id': self._id,
            'student': derefer(self.student),
            'email': email,
            'applied_at': self.applied_at.isoformat(),
            'status': self.status
        }

    def serialize_for_student(self):
        study_references = StudyReference.objects(category=self.job_post.category).first()
        return {
            'status': mapper.map_status(self.status, 'student'),
            'salary': self.job_post.salary.serialize(),
            'job_detail': {
                'role': self.job_post.role,
                'company': {
                    'logo_url': self.job_post.company.logo_url,
                    'name': self.job_post.company.name
                },
                'study_references': study_references.serialize_topics()
            },
            'updated_at': self.updated_at.isoformat()
        }
