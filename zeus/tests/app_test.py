import json
import unittest

from utils.seeds import *
from zeus.models import *
from zeus.tests.Helper import Helper

seed()

class StudentLoginTest(unittest.TestCase):
    def setUp(self):
        self.helper = Helper()
        self.endpoint = '/students/login'

    def login(self, data):
        return self.helper.post(self.endpoint, data);

    def test_login_with_valid_credential(self):
        rv = self.login({
            'email': 'genturwt@gmail.com',
            'password': 'quint-dev'
        })
        token = self.helper.get_token_data(rv.data)
        self.assertIn('student_id', token)
        self.assertIn('user_id', token)
        self.assertIn('name', rv.data)

    def test_login_with_invalid_email(self):
        rv = self.login({
            'email': 'ags@hmail.com',
            'password': 'quint-dev'
        })
        self.assertEqual(403, rv.status_code)
        self.assertIn('email', rv.data)

    def test_login_with_invalid_password(self):
        rv = self.login({
            'email': 'genturwt@gmail.com',
            'password': 'quint'
        })
        self.assertEqual(403, rv.status_code)
        self.assertIn('password', rv.data)

    def test_login_with_empty_email(self):
        rv = self.login({
            'password': 'quint-dev'
        })
        self.assertEqual(400, rv.status_code)
        self.assertIn('email', rv.data)

    def test_login_with_empty_password(self):
        rv = self.login({
            'email': 'genturwt@gmail.com'
        })
        self.assertEqual(400, rv.status_code)
        self.assertIn('password', rv.data)

class StudentRegisterTest(unittest.TestCase):
    def setUp(self):
        self.helper = Helper()
        self.endpoint = '/students/register'

    def register(self, data):
        return self.helper.post(self.endpoint, data);

    def test_register_with_valid_credentials(self):
        rv = self.register({
            'email': 'tri@quint.dev',
            'password': 'testing-lalala'
        })
        self.assertIn('token', rv.data)
        token = json.loads(rv.data)['token']
        self.assertEqual(200, rv.status_code)

    def test_register_with_duplicate_email(self):
        rv = self.register({
            'email': 'genturwt@gmail.com',
            'password': 'quint'
        })
        self.assertEqual(403, rv.status_code)

    def test_register_with_invalid_email(self):
        rv = self.register({
            'email': 'kenny',
            'password': 'quint'
        })
        self.assertEqual(403, rv.status_code)

    def test_register_with_empty_password(self):
        rv = self.register({
            'email': 'quint@dev.it'
        })
        self.assertEqual(400, rv.status_code)

    def test_register_with_empty_email(self):
        rv = self.register({
            'password': 'quint'
        })
        self.assertEqual(400, rv.status_code)

class StudentTest(unittest.TestCase):
    def setUp(self):
        self.helper = Helper()
        self.helper.set_type('students')
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
        self.helper.set_type('students')
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