from mongoengine import *
import datetime
from flask_login import UserMixin

class User(Document, UserMixin):
    email = StringField(unique=True, max_length=255)
    password = StringField(max_length=255)
    created_at = DateTimeField(default=datetime.datetime.now())

    def serialize(self):
        return {
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Student(Document):
    name = StringField(max_length=255)
    major = StringField(max_length=255)
    school = StringField(max_length=255)
    resume_url = URLField()
    linkedin_url = URLField()
    photo_url = URLField()
    headline = StringField(max_length=255)
    
    def serialize(self):
        return {
            'name': self.name,
            'major': self.major,
            'school': self.school,
            'resume_url': self.resume_url,
            'linkedin_url': self.linkedin_url,
            'photo_url': self.photo_url,
            'headline': self.headline
        }

class CompanyPhoto(EmbeddedDocument):
    img = ImageField()

    def serialize(self):
        return self.img.read().encode('base64')

class Company(Document):
    name = StringField(max_length=255)
    office_locations = ListField(ReferenceField('OfficeLocation'))
    job_posts = ListField(ReferenceField('JobPost'))
    industry = StringField(max_length=255)
    website = URLField()
    logo_url = URLField()
    photos = EmbeddedDocumentListField('CompanyPhoto')
    contact_person = ReferenceField('ContactPerson')

    def serialize(self):
        def to_json(items):
            json_obj = []
            for item in items:
                json_obj.append(item.serialize())
            return json_obj

        return {
            'name': self.name,
            'office_locations': to_json(self.office_locations),
            'job_posts': to_json(self.job_posts),
            'industry': self.industry,
            'website': self.website,
            'logo_url': self.logo_url,
            'photos': to_json(self.photos),
            'contact_person': self.contact_person.serialize()
        }

class OfficeLocation(Document):
    name = StringField(max_length=255)
    address = StringField(max_length=255)
    location = GeoPointField()

    def serialize(self):
        return {
            'name': self.name,
            'address': self.address,
            'location': self.location
        }

class ContactPerson(Document):
    name = StringField(max_length=255)
    role = StringField(max_length=255)
    phone = StringField(max_length=255)
    email = EmailField()

    def serialize(self):
        return {
            'name': self.name,
            'role': self.role,
            'phone': self.phone,
            'email': self.email
        }

class InternshipSchedule(EmbeddedDocument):
    start_at = DateTimeField()
    end_at = DateTimeField()

    def serialize(self):
        return {
            'start_at': self.start_at.isoformat(),
            'end_at': self.end_at.isoformat()
        }
    
class JobPost(Document):
    role = StringField(max_length=255)
    why_us = StringField()
    salary = IntField()
    technical_requirements = ListField(StringField(max_length=255))
    internship_schedule = EmbeddedDocumentField('InternshipSchedule')
    tasks = ListField(StringField(max_length=255))
    skills_gained = ListField(StringField(max_length=255))
    experiences_gained = ListField(StringField(max_length=255))
    contact_person = ReferenceField('ContactPerson')

    def serialize(self):
        return {
            'role': self.role,
            'why_us': self.why_us,
            'salary': self.salary,
            'technical_requirements': self.technical_requirements,
            'internship_schedule': self.internship_schedule.serialize(),
            'tasks': self.tasks,
            'skills_gained': self.skills_gained,
            'experiences_gained': self.experiences_gained,
            'contact_person': self.contact_person.serialize()
        }

class Application(Document):
    job_post = ReferenceField('JobPost')
    student = ReferenceField('Student')
    applied_at = DateTimeField(default=datetime.datetime.now)
    status = StringField(max_length=255)

    def serialize(self):
        return {
            'job_post': self.job_post.serialize(),
            'student': self.student.serialize(),
            'applied_at': self.applied_at.isoformat(),
            'status': self.status
        }
