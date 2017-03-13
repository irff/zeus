from flask import jsonify, request

from zeus import app
from zeus.services import category as _category
from zeus.utils import auth
from zeus.models.StudyReference import *


@app.route("/references", methods=['POST'])
def save_reference():
    category = _category.get_or_create(request.json['category'])
    topic_list = []
    topic_dict = {}
    for topic in request.json['topics']:
        ref = Reference(title=topic['title'], ref_url=topic['ref_url'])
        if topic['topic'] not in topic_dict:
            topic_obj = Topic(name=topic['topic'])
            topic_dict[topic['topic']] = topic_obj
        else:
            topic_obj = topic_dict[topic['topic']]
        topic_obj.contents.append(ref)
    for name in topic_dict:
        topic_list.append(topic_dict[name])
    StudyReference(category=category, topics=topic_list).save()
    return jsonify({}), 200
