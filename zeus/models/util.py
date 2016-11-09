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