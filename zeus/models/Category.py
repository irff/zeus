from mongoengine import *

class Category(Document):
    name = StringField()
