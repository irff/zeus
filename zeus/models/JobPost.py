from mongoengine import *
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
    is_published = BooleanField()
    fee = EmbeddedDocumentField('Fee')
    currency = StringField(max_length=10, choices='IDR')
    term = StringField(max_length=20, choices=('jam', 'hari', 'minggu', 'bulan'))

    def serialize(self):
        return {
            'is_published': self.is_published,
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
    category = StringField(choices=('business', 'product', 'engineering', 'design', 'marketing'), required=True)
    location = StringField(max_length=255, required=True)
    job_schedule = EmbeddedDocumentField('JobSchedule')
    salary = EmbeddedDocumentField('Salary')
    technical_requirements = ListField(StringField(max_length=255), required=True)
    tasks = ListField(StringField(max_length=255), required=True)
    experiences_gained = ListField(StringField(max_length=255))
    status = ListField(StringField(max_length=255), required=True)
    is_open = BooleanField()
    company = ReferenceField('Company', reverse_delete_rule=NULLIFY, required=True)
    job_type = StringField(choices=('internship', 'full-time', 'part-time', 'fresh graduate'), required=True)

    def serialize(self):
        return {
            'id': str(self.id),
            'role': self.role,
            'category': self.category,
            'location': self.location,
            'job_schedule': derefer(self.job_schedule),
            'salary': derefer(self.salary),
            'technical_requirements': self.technical_requirements,
            'tasks': self.tasks,
            'experiences_gained': self.experiences_gained,
            'status': self.status,
            'company': derefer(self.company),
            'created_at': self.id.generation_time.isoformat()
        }

    def get_summary(self):
        return {
            'id': str(self.id),
            'role': self.role,
            'status': self.status
        }
