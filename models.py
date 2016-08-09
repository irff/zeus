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
