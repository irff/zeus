from mongoengine import *

class UserStudent(Document):
    email       = EmailField(unique=True, max_length=255, required=True)
    password    = StringField(max_length=255, required=True)
    student     = ReferenceField('Student', reverse_delete_rule=NULLIFY)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        if(len(password) < 6):
            raise ValidationError('Password length is less than 6')
        self.password = generate_password_hash(password)

    def serialize(self):
        return {
            'email'     : self.email,
            'student'   : derefer(self.student),
            'created_at': self.id.generation_time.isoformat()
        }