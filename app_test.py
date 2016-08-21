import app
import unittest
import json
from seeds import Seeder

class AuthTest(unittest.TestCase):

        
    def setUp(self):
        self.app = app.app.test_client()

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ))

    def logout(self):
        return self.app.get('/logout')

    def register(self, email, password):
        return self.app.post('/register', data=dict(
            email=email,
            password=password
        ))

    def test_login(self):
        def valid_credential():
            rv = self.login('genturwt@gmail.com', 'quint-dev')
            assert 'success' in rv.data

        def wrong_email():
            rv = self.login('ags@hmail.com', 'quint-dev')
            assert 'invalid' in rv.data

        def wrong_password():
            rv = self.login('genturwt@gmail.com', 'quint')
            assert 'invalid' in rv.data

        valid_credential()
        wrong_email()
        wrong_password()

    def test_logout(self):
        def with_login():
            self.login('genturwt@gmail.com', 'quint-dev')
            rv = self.logout()
            assert 'success' in rv.data
        
        def without_login():
            rv = self.logout()
            assert 'success' in rv.data

        with_login()
        without_login()

    def test_register(self):
        def valid_credential():
            rv = self.register('tri@quint.dev', 'quint')
            assert 'created' in rv.data
        
        def duplicate_email():
            rv = self.register('genturwt@gmail.com', 'quint')
            assert 'exist' in rv.data

        valid_credential()
        duplicate_email()

class ModelTest(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def get_model(self, model):
        rv = self.app.get('/'+model)
        data = json.loads(rv.data)
        assert len(data) != 0

    def test_student(self):
        self.get_model('students')

    def test_user(self):
        self.get_model('users')

    def test_company(self):
        self.get_model('companies')

    def test_application(self):
        self.get_model('applications')


if __name__ == '__main__':
    seeder = Seeder()
    seeder.seed()
    unittest.main()
