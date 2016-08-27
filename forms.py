from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    email = StringField('Email', [
        validators.Email('Not a valid email address'),
        validators.DataRequired()
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm_password', 'Field must be equal to Confirm Password')
    ])
    confirm_password = PasswordField('Confirm Password')

    def serialize_error(self):
        return {
            'email': self.email.errors,
            'password': self.password.errors,
            'confirm_password': self.confirm_password.errors
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
