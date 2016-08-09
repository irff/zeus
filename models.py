from mongoengine import *

class User(Document):
	email = StringField(unique=True, max_length=255)
	password = StringField(max_length=255)
	created_at = DateTimeField()

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

class Company(Document):
	name = StringField(max_length=255)
	office_locations = ListField(ReferenceField('OfficeLocation'))
	job_posts = ListField(ReferenceField('JobPost'))
	industry = StringField(max_length=255)
	website = URLField()
	logo_url = URLField()
	photos = ListField(ImageField())
	contact_person = ReferenceField('ContactPerson')

class OfficeLocation(Document):
	name = StringField(max_length=255)
	address = StringField(max_length=255)
	location = GeoPointField()

class ContactPerson(Document):
	name = StringField(max_length=255)
	role = StringField(max_length=255)
	phone = StringField(max_length=255)
	email = EmailField()

class InternshipSchedule(EmbeddedDocument):
	start_at = DateTimeField()
	end_at = DateTimeField()
	
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


class Application(Document):
	job_post = ReferenceField('JobPost')
	student = ReferenceField('Student')
	applied_at = DateTimeField()
	status = StringField(max_length=255)