import unittest

from zeus import app
from zeus.tests.Helper import Helper


class CompanyLoginTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.helper = Helper()
        self.helper.set_type('companies')

    def test_login(self):
        def valid_credential():
            rv = self.helper.login('genturwt@quint.id', 'quint-dev')
            self.assertIn('success', rv.data)

        def wrong_email():
            rv = self.helper.login('ags@quint.id', 'quint-dev')
            self.assertIn('invalid', rv.data)

        def wrong_password():
            rv = self.helper.login('genturwt@quint.id', 'quint')
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
            self.helper.login('genturwt@quint.id', 'quint-dev')
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
            rv = self.helper.register('genturwt@quint.id', 'quint')
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
