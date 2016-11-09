from flask_oauthlib.client import OAuth
from flask import session
from zeus import env

oauth = OAuth()
linkedin = oauth.remote_app('linkedin',
    authorize_url='https://www.linkedin.com/oauth/v2/authorization',
    access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
    consumer_key=env.app.config['LINKEDIN_ID'],
    consumer_secret=env.app.config['LINKEDIN_SECRET'],
    request_token_url=None
)

@linkedin.tokengetter
def get_linkedin_token():
    return session.get('linkedin_token')

def save_token(token):
	session['linkedin_token'] = (token, '')