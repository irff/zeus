from zeus import celery
from zeus import app
from zeus import mail
from flask_mail import Message
from flask import render_template

@celery.task
def send_applied_job(**kwargs):
    with app.app_context():
        data = kwargs['data']
        student = data['student']
        job_post = data['job_post']
        body = render_template('email.html', **data)
        recipients = kwargs['to']
        subject = 'Quint - Pendaftar Internship ({0}, {1})'.format(student.name, job_post.role)
        cc = ['firza@quint.id']
        message = Message(html=body, recipients=recipients, subject=subject, cc=cc)
        mail.send(message)

# celery debugger
def get_celery_worker_status():
    ERROR_KEY = "ERROR"
    try:
        from celery.task.control import inspect
        insp = inspect()
        d = insp.stats()
        if not d:
            d = { ERROR_KEY: 'No running Celery workers were found.' }
    except IOError as e:
        from errno import errorcode
        msg = "Error connecting to the backend: " + str(e)
        if len(e.args) > 0 and errorcode.get(e.args[0]) == 'ECONNREFUSED':
            msg += ' Check that the Redis server is running.'
        d = { ERROR_KEY: msg }
    except ImportError as e:
        d = { ERROR_KEY: str(e)}
    return d