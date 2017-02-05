from mongoengine import *
from datetime import datetime
from util import derefer, update_modified

class Category(Document):
    name = StringField()