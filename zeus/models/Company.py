from mongoengine import *
from datetime import datetime
from util import derefer, to_json
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
        
class Company(Document):
    name = StringField(max_length=255, required=True)
    logo_url = URLField(required=True)
    company_address = StringField(required=True)
    background_img_url = URLField()
    website = URLField(required=True)
    category = StringField(max_length=255, required=True)

    def serialize(self):
        return {
            'name': self.name,
            'logo_url': self.logo_url,
            'background_img_url': self.background_img_url,
            'company_address': self.company_address,
            'category': self.category,
            'website': self.website
        }
        
class UserCompany(Document):
    email = StringField(unique=True, max_length=255, required=True)
    password = StringField(max_length=255, required=True)
    company = ReferenceField('Company', reverse_delete_rule=NULLIFY)
    created_at = DateTimeField(default=datetime.now())

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        if(len(password) > 0):
            self.password = generate_password_hash(password)

    def serialize(self):
        return {
            'email': self.email,
            'company': derefer(self.company),
            'created_at': self.created_at.isoformat()
        }


