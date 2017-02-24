from mongoengine import *
from util import derefer
from werkzeug.security import generate_password_hash, check_password_hash


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
    email = EmailField(unique=True)

    def serialize(self):
        return {
            'name': self.name,
            'role': self.role,
            'phone': self.phone,
            'email': self.email
        }


class Company(Document):
    name = StringField(max_length=255, required=True)
    logo_url = URLField(required=True)
    category = StringField(max_length=255, required=True)
    company_address = StringField(required=True)
    website = URLField(required=True)
    background_img_url = URLField()
    description = StringField(required=True)
    contact_person = EmbeddedDocumentField('ContactPerson')

    def serialize(self):
        return {
            'name': self.name,
            'logo_url': self.logo_url,
            'category': self.category,
            'company_address': self.company_address,
            'website': self.website,
            'background_img_url': self.background_img_url,
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
