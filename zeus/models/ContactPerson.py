from mongoengine import *
from datetime import datetime

class ContactPerson(Document):
    name = StringField(max_length=255)
    role = StringField(max_length=255)
    phone = StringField(max_length=255)
    email = EmailField(unique=True)

    def serialize(self):
        return {
            'name': self.name,
            'role': self.role,
            'phone': self.phone,
            'email': self.email
        }