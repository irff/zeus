from mongoengine import signals
from datetime import datetime
from functools import wraps

def handler(event):
    def decorator(fn):
    	@wraps(fn)
        def apply(cls):
            event.connect(fn, sender=cls)
            return cls

        fn.apply = apply
        return fn

    return decorator

def derefer(data):
    if data == None:
        return ""
    else:
        return data.serialize()

def to_json(items):
    json_obj = []
    for item in items:
        json_obj.append(derefer(item))
    return json_obj


@handler(signals.pre_save)
def update_modified(sender, document):
	document.updated_at = datetime.now()
