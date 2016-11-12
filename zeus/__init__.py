from flask import Flask
from flask_dotenv import DotEnv
from mongoengine import connect
from celery import Celery
from flask_mail import Mail
from flask_cors import CORS

app = Flask('Quint API', template_folder='zeus/views')
env = DotEnv()
env.init_app(app)
app.secret_key = 'QuintDev'
CORS(app, origins=['https://*.quint.id', 'https://quint.id'])
# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.zoho.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'notification@quint.id'
app.config['MAIL_PASSWORD'] = '@x8Wh@MZ'
app.config['MAIL_DEFAULT_SENDER'] = ('Notification from Quint', 'notification@quint.id')
app.config['TESTING'] = False
# initiate celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# initiate connection to database
connect('quint')

# initiate mail
mail = Mail(app)

import api.student
import api.job_post
import api.company