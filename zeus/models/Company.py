from mongoengine import *
from datetime import datetime
from util import derefer, to_json
from werkzeug.security import generate_password_hash, check_password_hash
        
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
