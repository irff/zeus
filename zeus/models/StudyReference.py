from mongoengine import *
from datetime import datetime
from util import derefer, update_modified, to_json

class Reference(EmbeddedDocument):
    title = StringField()
    ref_url = StringField()

    def serialize(self):
        return {
            'title': self.title,
            'ref_url': self.ref_url
        }

class Topic(EmbeddedDocument):
    name = StringField()
    contents = EmbeddedDocumentListField('Reference')

    def serialize(self):
        return {
            'name': self.name,
            'contents': to_json(self.contents)
        }


class StudyReference(Document):
    category = ReferenceField('Category', reverse_delete_rule=NULLIFY)
    topics = EmbeddedDocumentListField('Topic')

    def serialize(self):
        return {
            'category': derefer(self.category),
            'topics': to_json(self.topics)
        }

    def serialize_topics(self):
        return to_json(self.topics)