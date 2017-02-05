from flask import jsonify, request
from zeus import app
from functools import wraps
import jwt
from datetime import datetime, timedelta

def extract_data(header):
    try:
        header_type, value = tuple(header['Authorization'].split())
        data = jwt.decode(value, app.secret_key)
    except Exception:
        return None
    return data

def require_token(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        data = extract_data(request.headers)
        if(data == None):
            return jsonify({
                'message': 'There is no token/token is not valid'
            }), 401
        return func(*args, **kwargs)
    return decorated_func

def privilege(role):
    def check_privilege(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            data = extract_data(request.headers)
            if(data['role'] == role):
                return func(*args, **kwargs)
            return jsonify({
                'message': 'Unauthorized. Only {0} can access this endpoint'.format(role)
            }), 401
        return decorated_func
    return check_privilege

def same_property(prop_id):
    def functors(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            data = extract_data(request.headers)
            if(data[prop_id] == kwargs[prop_id]):
                return func(*args, **kwargs)
            return jsonify({
                'message': 'Unauthorized. Only the resource owner can access this endpoint'
            }), 401
        return decorated_func
    return functors

def create_token(data):
    data['exp'] = datetime.utcnow() + timedelta(days=365)
    token = jwt.encode(data, app.secret_key, algorithm='HS256')
    return token

def decode_token(token):
    return jwt.decode(token, app.secret_key)