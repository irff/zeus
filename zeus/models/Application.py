from mongoengine import *
from datetime import datetime
from util import derefer


class Application(Document):
    job_post = ReferenceField('JobPost', reverse_delete_rule=NULLIFY, unique_with='student')
    student = ReferenceField('Student', reverse_delete_rule=NULLIFY)
    applied_at = DateTimeField(default=datetime.now)
    status = StringField(max_length=255, choices=('Diterima', 'Ditolak', 'Resume sedang direview', 'Menunggu wawancara/tes', 'Hasil sedang direview'), default='Resume sedang direview')


    def serialize(self):
        return {
            'job_post': derefer(self.job_post),
            'student': derefer(self.student),
            'applied_at': self.applied_at.isoformat(),
            'status': self.status
        }

