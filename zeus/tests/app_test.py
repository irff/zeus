import unittest
import json
from utils.seeds import *
from zeus.models import *
from zeus import app

seed()
class Helper():
    def __init__(self):
        self.app = app.test_client()

    def setType(self, user_type):
        self.user_type = user_type;

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

    def get_model(self, model):
        return self.app.get('/'+model)

    def post(self, url, data, headers=None):
        return self.app.post(url, data=json.dumps(data), content_type='application/json', headers=headers)

    def get(self, url, headers=None):
        return self.app.get(url, headers=headers)

    def delete(self, url, headers=None):
        return self.app.delete(url, headers=headers)

    def put(self, url, data, headers=None):
        return self.app.put(url, data=json.dumps(data), content_type='application/json', headers=headers)

class StudentAuthTest(unittest.TestCase):

    def setUp(self):
        self.helper = Helper()
        self.helper.setType('students')

    def test_login_with_valid_credential(self):
        rv = self.helper.login('genturwt@gmail.com', 'quint-dev')
        self.assertIn('token', rv.data)

    def test_login_with_invalid_email(self):
        rv = self.helper.login('ags@hmail.com', 'quint-dev')
        self.assertEqual(403, rv.status_code)

    def test_login_with_invalid_password(self):
        rv = self.helper.login('genturwt@gmail.com', 'quint')
        self.assertEqual(403, rv.status_code)

    def test_register_with_valid_credentials(self):
        rv = self.helper.register('tri@quint.dev', 'quint')
        self.assertIn('token', rv.data)
        token = json.loads(rv.data)['token']
        data = {
            'name': 'Gentur Waskito T',
            'major': 'Computer Science',
            'school': 'UI - Indonesia',
            'headline': 'Mata Pancing'
        }
        rv = self.helper.post('/students', data, {
            'Authorization': 'Bearer ' + token
        })
        
    def test_register_with_duplicate_email(self):
        rv = self.helper.register('genturwt@gmail.com', 'quint')
        self.assertEqual(403, rv.status_code)

    def test_register_with_invalid_email(self):
        rv = self.helper.register('kenny', 'quint')
        self.assertEqual(403, rv.status_code)

    def test_register_with_empty_credential(self):
        rv = self.helper.register('quint@dev.it', '')
        self.assertEqual(403, rv.status_code)
        rv = self.helper.register('', 'quint')
        self.assertEqual(403, rv.status_code)

class StudentTest(unittest.TestCase):
    def setUp(self):
        self.helper = Helper()
        self.helper.setType('students')
        data = json.loads(self.helper.login('genturwt@gmail.com', 'quint-dev').data)
        self.id = data['student_id']
        self.token = data['token']

    def test_modify_student(self):
        data = {
            'first_name': 'Kenny',
            'last_name': 'Ganteng',
            'experiences': {
                'project_num': 1
            }
        }
        rv = self.helper.put('/students/'+ self.id, data, {
            'Authorization': 'Bearer ' + self.token
        })
        self.assertEqual(204, rv.status_code)

    def test_modify_other_student(self):
        data = {
            'name': 'Kenny Ganteng'
        }
        rv = self.helper.put('/students/' + "123", data, {
            'Authorization': 'Bearer ' + self.token
        })
        self.assertEqual(401, rv.status_code)

    def test_modify_without_token(self):
        data = {
            'name': 'Kenny Ganteng'
        }
        rv = self.helper.put('/students/' + self.id, data, {})
        self.assertEqual(401, rv.status_code)

    # def test_delete_student(self):
    #     rv = self.helper.delete('/students/'+ self.id, {
    #         'Authorization': 'Bearer ' + self.token
    #     })
    #     self.assertEqual(204, rv.status_code)
    #     seedStudent()
    #     seedUserStudent()

    # def test_delete_another_student(self):
    #     rv = self.helper.delete('/students/'+ "123", {
    #         'Authorization': 'Bearer ' + self.token
    #     })
    #     self.assertEqual(401, rv.status_code)

    # def test_delete_without_token(self):
    #     rv = self.helper.delete('/students/'+ "123", {})
    #     self.assertEqual(401, rv.status_code)

class ApplicationTest(unittest.TestCase):
    def setUp(self):
        self.helper = Helper()
        self.helper.setType('students')
        data = json.loads(self.helper.login('genturwt@gmail.com', 'quint-dev').data)
        self.id = data['student_id']
        self.token = data['token']

    def test_apply_job(self):
        job_id = JobPost.objects(role='Marketing Division').first().id
        rv = self.helper.post('/students/' + self.id + '/jobs', {
            'job_id': str(job_id)
        }, {
            'Authorization': 'Bearer ' + self.token
        })
        self.assertEqual(204, rv.status_code)

    def test_apply_all_jobs(self):
        rv = self.helper.get('/students/' + self.id + '/jobs', {
            'Authorization': 'Bearer ' + self.token
        })
        self.assertIn('jobs', rv.data)
# class CompanyAuthTest(unittest.TestCase):

#     def setUp(self):
#         self.app = app.test_client()
#         self.helper = Helper()
#         self.helper.setType('companies')

#     def test_login(self):
#         def valid_credential():
#             rv = self.helper.login('genturwt@quint.id', 'quint-dev')
#             self.assertIn('success', rv.data)

#         def wrong_email():
#             rv = self.helper.login('ags@quint.id', 'quint-dev')
#             self.assertIn('invalid', rv.data)

#         def wrong_password():
#             rv = self.helper.login('genturwt@quint.id', 'quint')
#             self.assertIn('invalid', rv.data)

#         def invalid_email():
#             rv = self.helper.login('kenny', 'quint')
#             self.assertIn('Not a valid email', rv.data)

#         def empty_required_field():
#             rv = self.helper.login('quint', '')
#             self.assertIn('This field is required.', rv.data)
#             rv = self.helper.login('', 'quint')
#             self.assertIn('This field is required.', rv.data)

#         valid_credential()
#         wrong_email()
#         wrong_password()
#         invalid_email()
#         empty_required_field()

#     def test_logout(self):
#         def with_login():
#             self.helper.login('genturwt@quint.id', 'quint-dev')
#             rv = self.helper.logout()
#             self.assertIn('success', rv.data)
        
#         def without_login():
#             rv = self.helper.logout()
#             self.assertIn('success', rv.data)

#         with_login()
#         without_login()

#     def test_register(self):
#         def valid_credential():
#             rv = self.helper.register('tri@quint.dev', 'quint')
#             self.assertIn('created', rv.data)
        
#         def duplicate_email():
#             rv = self.helper.register('genturwt@quint.id', 'quint')
#             self.assertIn('exist', rv.data)

#         def invalid_email():
#             rv = self.helper.register('kenny', 'quint')
#             self.assertIn('Not a valid email', rv.data)

#         def empty_required_field():
#             rv = self.helper.register('quint', '')
#             self.assertIn('This field is required.', rv.data)
#             rv = self.helper.register('', 'quint')
#             self.assertIn('This field is required.', rv.data)

#         valid_credential()
#         duplicate_email()
#         invalid_email()
#         empty_required_field()

# class JobPostTest(unittest.TestCase):
#     def setUp(self):
#         self.app = app.test_client()
#         self.helper = Helper()

#     def test_base(self):
#         rv = self.helper.get('/jobs')
#         self.assertIn('success', rv.data)

#     def test_creation(self):
#         contact_person = str(ContactPerson.objects().first().id)
#         rv = self.helper.post('/jobs', {
#             'role': "Software Engineer",
#             'why_us': 'We are the top brand company in Indonesia',
#             'salary': {
#                 'fee': 450000,
#                 'currency': '$',
#                 'term': 'month'
#             },
#             'technical_requirements': ['SQL', 'Python', 'CP Skills'],
#             'internship_schedule': {
#                 'start_at': '2016-09-27 20:56:54.181914',
#                 'end_at': '2016-10-27 20:56:54.181914'
#             },
#             'tasks': ['Building Frontend', 'Building Backend'],
#             'skills_gained': ['Hardwork', 'Relations'],
#             'experiences_gained': ['Experience in Collaboration', 'Love from Quint'],
#             'contact_person': contact_person
#         })
#         self.assertIn('success', rv.data)

#     def test_modification(self):
#         contact_person = str(ContactPerson.objects().first().id)
#         job = JobPost.objects().first()
#         job_id = str(job.id)
#         rv = self.helper.put('/jobs/'+job_id, {
#             'role': "Software Developer",
#             'why_us': 'We are the top brand company in Indonesia',
#             'salary': {
#                 'fee': 450000,
#                 'currency': '$',
#                 'term': 'month'
#             },
#             'technical_requirements': ['SQL', 'Python', 'CP Skills'],
#             'internship_schedule': {
#                 'start_at': '2016-09-27 20:56:54.181914',
#                 'end_at': '2016-10-27 20:56:54.181914'
#             },
#             'tasks': ['Building Frontend', 'Building Backend'],
#             'skills_gained': ['Hardwork', 'Relations'],
#             'experiences_gained': ['Experience in Collaboration', 'Love from Quint'],
#             'contact_person': contact_person
#         })
#         self.assertIn('success', rv.data)

#     def test_deletion(self):
#         job = JobPost.objects().first()
#         job_id = str(job.id)
#         rv = self.helper.delete('/jobs/'+job_id)

# class CompanyTest(unittest.TestCase):
#     def setUp(self):
#         self.app = app.test_client()
#         self.helper = Helper()

#     def test_base(self):
#         rv = self.helper.get('/companies')
#         self.assertIn('success', rv.data)

#     def test_creation(self):
#         contact_person = str(ContactPerson.objects().first().id)
#         rv = self.helper.post('/companies', {
#             'name': 'Quint Dev Ops',
#             'industry': 'Technology',
#             'website': 'http://quint.id',
#             'logo_url': 'http://quint.id/companies/logo.png',
#             'contact_person': contact_person
#         })
#         self.assertIn('success', rv.data)

#     def test_modification(self):
#         contact_person = str(ContactPerson.objects().first().id)
#         company = Company.objects().first()
#         company_id = str(company.id)
#         rv = self.helper.post('/companies', {
#             'name': 'Quint Dev Ops v2',
#             'industry': 'Technology',
#             'website': 'http://quint.id',
#             'logo_url': 'http://quint.id/companies/logo.png',
#             'contact_person': contact_person
#         })
#         self.assertIn('success', rv.data)

#     def test_deletion(self):
#         company = Company.objects().first()
#         company_id = str(company.id)
#         rv = self.helper.delete('/companies/'+company_id)