from mongoengine import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from util import derefer

class Experiences(EmbeddedDocument):
    achievement_num = IntField(default=0)
    project_num     = IntField(default=0)
    work_num        = IntField(default=0)

    def serialize(self):
        return {
            'achievement_num' : self.achievement_num,
            'project_num'     : self.project_num,
            'work_num'        : self.work_num
        }
class Student(Document):
    first_name      = StringField(max_length=255, required=True)
    last_name       = StringField(max_length=255)
    major           = StringField(max_length=255, required=True)
    university      = StringField(max_length=255, required=True)
    resume_url      = URLField(required=True)
    linkedin_url    = URLField()
    photo_url       = URLField()
    headline        = StringField(max_length=255)
    experiences     = EmbeddedDocumentField('Experiences')

    def serialize(self):
        return {
            'first_name'    : self.first_name,
            'last_name'     : self.last_name,   
            'major'         : self.major,
            'university'    : self.university,
            'resume_url'    : self.resume_url,
            'linkedin_url'  : self.linkedin_url,
            'photo_url'     : self.photo_url,
            'headline'      : self.headline,
            'experiences'   : derefer(self.experiences)
        }
