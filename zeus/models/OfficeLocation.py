from mongoengine import *

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