from mongoengine import *
from datetime import datetime
from util import derefer, to_json


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
        return {
            'student': derefer(self.student),
            'applied_at': self.applied_at.isoformat(),
            'status': self.status
        }
