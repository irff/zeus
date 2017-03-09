from mongoengine import *

class Category(Document):
    name = StringField()

    def serialize(self):
        return self.name