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
