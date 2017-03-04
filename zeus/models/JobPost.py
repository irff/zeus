from mongoengine import *
from datetime import datetime
from util import derefer

class Fee(EmbeddedDocument):
    minimal = IntField()
    maximal = IntField()

    def serialize(self):
        return {
            'minimal': self.minimal,
            'maximal': self.maximal
        }

class Salary(EmbeddedDocument):
    fee = EmbeddedDocumentField('Fee')
    currency = StringField(max_length=10, choices=('IDR'))
    term = StringField(max_length=20, choices=('hari', 'jam', 'minggu', 'bulan'))

    def serialize(self):
        return {
            'fee': derefer(self.fee),
            'currency': self.currency,
            'term': self.term
        }
    
class JobSchedule(EmbeddedDocument):
    start_at = DateTimeField()
    end_at = DateTimeField()

    def serialize(self):
        return {
            'start_at': self.start_at,
            'end_at': self.end_at
        }
    
class JobPost(Document):
    role = StringField(max_length=255, required=True)
    why_us = StringField(required=True)
    salary = EmbeddedDocumentField('Salary')
    technical_requirements = ListField(StringField(max_length=255), required=True)
    job_schedule = EmbeddedDocumentField('JobSchedule')
    tasks = ListField(StringField(max_length=255), required=True)
    skills_gained = ListField(StringField(max_length=255))
    experiences_gained = ListField(StringField(max_length=255))
    contact_person = ReferenceField('ContactPerson', reverse_delete_rule=NULLIFY, required=True)
    company = ReferenceField('Company', reverse_delete_rule=NULLIFY, required=True)
    job_type = StringField(choices=('internship', 'full-time', 'part-time', 'fresh graduate'), required=True)
    category = ReferenceField('Category', reverse_delete_rule=NULLIFY)
    is_open = BooleanField(default=True)

    def serialize(self):
        return {
            'id': str(self.id),
            'role': self.role,
            'why_us': self.why_us,
            'salary': derefer(self.salary),
            'technical_requirements': self.technical_requirements,
            'job_schedule': derefer(self.job_schedule),
            'tasks': self.tasks,
            'skills_gained': self.skills_gained,
            'experiences_gained': self.experiences_gained,
            'contact_person': derefer(self.contact_person),
            'company': derefer(self.company),
            'job_type': self.job_type,
            'created_at': self.id.generation_time.isoformat()
        }

