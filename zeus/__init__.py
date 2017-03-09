from flask import Flask
from flask_dotenv import DotEnv
from mongoengine import connect
from celery import Celery
from flask_mail import Mail
from flask_cors import CORS
# from minio import Minio
# from minio.error import ResponseError

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
app.config['CURRENT_HOST'] = env.app.config['STAGING_HOST'] if env.app.config['TESTING'] else env.app.config['PROD_HOST']

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(env.app.config)

connect(env.app.config['MONGODB_DB'])

mail = Mail(app)

# minio_client = Minio(env.app.config['MINIO_ENDPOINT'],
#                access_key=env.app.config['MINIO_ACCESS_KEY'],
#                secret_key=env.app.config['MINIO_SECRET_KEY'],
#                secure=(env.app.config['MINIO_SECURE'] == 'True'))
#
# try:
#     minio_client.make_bucket('companies', location='us-east-1')
# except ResponseError as err:
#     print(err)

import api.student
import api.job_post
import api.company
import api.category
