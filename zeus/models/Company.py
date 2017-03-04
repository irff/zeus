from mongoengine import *
from util import derefer
from werkzeug.security import generate_password_hash, check_password_hash


class Company(Document):
    name = StringField(max_length=255, required=True)
    category = StringField(max_length=255, required=True)
    location = StringField(max_length=255)
    logo_url = URLField(required=True)
    header_img_url = URLField()
    website = URLField(required=True)
    description = StringField(required=True)

    def serialize(self):
        return {
            'name': self.name,
            'category': self.category,
            'location': self.location,
            'logo_url': self.logo_url,
            'header_img_url': self.header_img_url,
            'website': self.website,
            'description': self.description
        }


class UserCompany(Document):
    email = StringField(unique=True, max_length=255, required=True)
    password = StringField(max_length=255, required=True)
    company = ReferenceField('Company', reverse_delete_rule=NULLIFY)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        if len(password) > 0:
            self.password = generate_password_hash(password)

    def serialize(self):
        return {
            'email': self.email,
            'company': derefer(self.company),
            'created_at': self.id.generation_time.isoformat()
        }
