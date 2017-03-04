import json

from zeus import app
from zeus.utils import auth


class Helper:
    def __init__(self):
        self.app = app.test_client()
        self.user_type = ''

    def set_type(self, user_type):
        self.user_type = user_type

    def login(self, email, password):
        return self.app.post('/'+self.user_type+'/login', data=json.dumps(dict(
            email=email,
            password=password
        )), content_type='application/json')

    def logout(self):
        return self.app.get('/'+self.user_type+'/logout')

    def register(self, email, password):
        return self.app.post('/'+self.user_type+'/register', data=json.dumps(dict(
            email=email,
            password=password
        )), content_type='application/json')

    def get_token_data(self, data):
        token = json.loads(data)['token']
        return auth.decode_token(token)

    def post(self, url, data, headers=None):
        return self.app.post(url, data=json.dumps(data), content_type='application/json', headers=headers)

    def get(self, url, headers=None):
        return self.app.get(url, headers=headers)

    def delete(self, url, headers=None):
        return self.app.delete(url, headers=headers)

    def put(self, url, data, headers=None):
        return self.app.put(url, data=json.dumps(data), content_type='application/json', headers=headers)
