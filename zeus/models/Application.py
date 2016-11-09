from mongoengine import *
from datetime import datetime
from util import derefer


class Application(Document):
    job_post = ReferenceField('JobPost', reverse_delete_rule=NULLIFY)
    student = ReferenceField('Student', reverse_delete_rule=NULLIFY)
    applied_at = DateTimeField(default=datetime.now)
    status = StringField(max_length=255, choices=('Accepted', 'Rejected', 'Pending'), default='Pending')


    def serialize(self):
        return {
            'job_post': derefer(self.job_post),
            'student': derefer(self.student),
            'applied_at': self.applied_at.isoformat(),
            'status': self.status
        }

