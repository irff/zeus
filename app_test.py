import app
import unittest
import json
from seeds import Seeder

class Helper():
    def __init__(self):
        self.app = app.app.test_client()

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ))

    def logout(self):
        return self.app.get('/logout')

    def register(self, email, password, confirm_password):
        return self.app.post('/register', data=dict(
            email=email,
            password=password,
            confirm_password=confirm_password
        ))

    def get_model(self, model):
        return self.app.get('/'+model)

class AuthTest(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.helper = Helper()

    def test_login(self):
        def valid_credential():
            rv = self.helper.login('genturwt@gmail.com', 'quint-dev')
            self.assertIn('success', rv.data)

        def wrong_email():
            rv = self.helper.login('ags@hmail.com', 'quint-dev')
            self.assertIn('invalid', rv.data)

        def wrong_password():
            rv = self.helper.login('genturwt@gmail.com', 'quint')
            self.assertIn('invalid', rv.data)

        def invalid_email():
            rv = self.helper.login('kenny', 'quint')
            self.assertIn('Not a valid email', rv.data)

        def empty_required_field():
            rv = self.helper.login('quint', '')
            self.assertIn('This field is required.', rv.data)
            rv = self.helper.login('', 'quint')
            self.assertIn('This field is required.', rv.data)

        valid_credential()
        wrong_email()
        wrong_password()
        invalid_email()
        empty_required_field()

    def test_logout(self):
        def with_login():
            self.helper.login('genturwt@gmail.com', 'quint-dev')
            rv = self.helper.logout()
            self.assertIn('success', rv.data)
        
        def without_login():
            rv = self.helper.logout()
            self.assertIn('success', rv.data)

        with_login()
        without_login()

    def test_register(self):
        def valid_credential():
            rv = self.helper.register('tri@quint.dev', 'quint', 'quint')
            self.assertIn('created', rv.data)
        
        def duplicate_email():
            rv = self.helper.register('genturwt@gmail.com', 'quint', 'quint')
            self.assertIn('exist', rv.data)

        def password_not_match():
            rv = self.helper.register('kenny@quint.dev', 'quint', 'qui')
            self.assertIn('Field must be equal', rv.data)

        def invalid_email():
            rv = self.helper.register('kenny', 'quint', 'quint')
            self.assertIn('Not a valid email', rv.data)

        def empty_required_field():
            rv = self.helper.register('quint', '', 'quint')
            self.assertIn('This field is required.', rv.data)
            rv = self.helper.register('', 'quint', 'quint')
            self.assertIn('This field is required.', rv.data)

        valid_credential()
        duplicate_email()
        password_not_match()
        invalid_email()
        empty_required_field()

class ModelTest(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.helper = Helper()

    def test_student(self):
        rv = self.helper.get_model('students')
        self.assertIsNotNone(rv)

    def test_user(self):
        rv = self.helper.get_model('users')
        self.assertIsNotNone(rv)

    def test_company(self):
        rv = self.helper.get_model('companies')
        self.assertIsNotNone(rv)

    def test_application(self):
        rv = self.helper.get_model('applications')
        self.assertIsNotNone(rv)


if __name__ == '__main__':
    seeder = Seeder()
    seeder.seed()
    unittest.main()
