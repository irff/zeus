from wtforms import Form, BooleanField, StringField, PasswordField, validators
import wtforms_json

wtforms_json.init()

class RegistrationForm(Form):
    email = StringField('Email', [
        validators.Email('Not a valid email address'),
        validators.DataRequired()
    ])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])

    def serialize_error(self):
        return {
            'email': self.email.errors,
            'password': self.password.errors,
        }

class LoginForm(Form):
    email = StringField('Email', [
        validators.Email('Not a valid email address'),
        validators.DataRequired()
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])

    def serialize_error(self):
        return {
            'email': self.email.errors,
            'password': self.password.errors
        }