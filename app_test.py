import app
import unittest
import json
from seeds import *
from models import *

class Helper():
    def __init__(self):
        self.app = app.app.test_client()

    def login(self, email, password):
        return self.app.post('/login', data=json.dumps(dict(
            email=email,
            password=password
        )), content_type='application/json')

    def logout(self):
        return self.app.get('/logout')

    def register(self, email, password):
        return self.app.post('/register', data=json.dumps(dict(
            email=email,
            password=password
        )), content_type='application/json')

    def get_model(self, model):
        return self.app.get('/'+model)

    def post(self, url, data):
        return self.app.post(url, data=json.dumps(data), content_type='application/json')

    def get(self, url):
        return self.app.get(url)

    def delete(self, url):
        return self.app.delete(url)

    def put(self, url, data):
        return self.app.put(url, data=json.dumps(data), content_type='application/json')

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
            rv = self.helper.register('tri@quint.dev', 'quint')
            self.assertIn('created', rv.data)
        
        def duplicate_email():
            rv = self.helper.register('genturwt@gmail.com', 'quint')
            self.assertIn('exist', rv.data)

        def invalid_email():
            rv = self.helper.register('kenny', 'quint')
            self.assertIn('Not a valid email', rv.data)

        def empty_required_field():
            rv = self.helper.register('quint', '')
            self.assertIn('This field is required.', rv.data)
            rv = self.helper.register('', 'quint')
            self.assertIn('This field is required.', rv.data)

        valid_credential()
        duplicate_email()
        invalid_email()
        empty_required_field()

class JobPostTest(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.helper = Helper()

    def test_base(self):
        rv = self.helper.get('/jobs')
        self.assertIn('success', rv.data)

    def test_creation(self):
        contact_person = str(ContactPerson.objects().first().id)
        rv = self.helper.post('/jobs', {
            'role': "Software Engineer",
            'why_us': 'We are the top brand company in Indonesia',
            'salary': {
                'fee': 450000,
                'currency': '$',
                'term': 'month'
            },
            'technical_requirements': ['SQL', 'Python', 'CP Skills'],
            'internship_schedule': {
                'start_at': '2016-09-27 20:56:54.181914',
                'end_at': '2016-10-27 20:56:54.181914'
            },
            'tasks': ['Building Frontend', 'Building Backend'],
            'skills_gained': ['Hardwork', 'Relations'],
            'experiences_gained': ['Experience in Collaboration', 'Love from Quint'],
            'contact_person': contact_person
        })
        self.assertIn('success', rv.data)

    def test_modification(self):
        contact_person = str(ContactPerson.objects().first().id)
        job = JobPost.objects().first()
        job_id = str(job.id)
        rv = self.helper.put('/jobs/'+job_id, {
            'role': "Software Developer",
            'why_us': 'We are the top brand company in Indonesia',
            'salary': {
                'fee': 450000,
                'currency': '$',
                'term': 'month'
            },
            'technical_requirements': ['SQL', 'Python', 'CP Skills'],
            'internship_schedule': {
                'start_at': '2016-09-27 20:56:54.181914',
                'end_at': '2016-10-27 20:56:54.181914'
            },
            'tasks': ['Building Frontend', 'Building Backend'],
            'skills_gained': ['Hardwork', 'Relations'],
            'experiences_gained': ['Experience in Collaboration', 'Love from Quint'],
            'contact_person': contact_person
        })
        self.assertIn('success', rv.data)

    def test_deletion(self):
        job = JobPost.objects().first()
        job_id = str(job.id)
        rv = self.helper.delete('/jobs/'+job_id)


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
    unittest.main()
