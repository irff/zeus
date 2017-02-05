from flask import Flask
from flask_dotenv import DotEnv
from mongoengine import connect
from celery import Celery
from flask_mail import Mail
from flask_cors import CORS

app = Flask('Quint API', template_folder='zeus/html')
env = DotEnv()
env.init_app(app)
app.secret_key = 'QuintDev'
CORS(app, origins=['https://*.quint.id', 'https://quint.id'])

app.config['CELERY_BROKER_URL'] = env.app.config['REDIS_CELERY_URL']
app.config['CELERY_RESULT_BACKEND'] = env.app.config['REDIS_CELERY_URL']

app.config['MAIL_SERVER'] = env.app.config['MAIL_SERVER']
app.config['MAIL_PORT'] = env.app.config['MAIL_PORT']
app.config['MAIL_USE_TLS'] = env.app.config['MAIL_USE_TLS']
app.config['MAIL_USERNAME'] = env.app.config['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = env.app.config['MAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = (env.app.config['MAIL_SENDER_NAME'], env.app.config['MAIL_USERNAME'])
app.config['TESTING'] = env.app.config['TESTING']

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(env.app.config)

connect(env.app.config['MONGODB_DB'])

mail = Mail(app)

import api.student
import api.job_post
import api.company
