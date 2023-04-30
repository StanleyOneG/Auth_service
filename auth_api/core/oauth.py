from authlib.integrations.flask_client import OAuth
from flask import jsonify
from flask_restful import Resource
from core.config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    VK_CLIENT_ID,
    VK_CLIENT_SECRET,
)
from flask import current_app as app
from flask import request


oauth = OAuth()


google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'email profile'},
)


vk = oauth.register(
    name='vk',
    client_id=VK_CLIENT_ID,
    client_secret=VK_CLIENT_SECRET,
    access_token_url='https://oauth.vk.com/access_token',
    access_token_params=None,
    authorize_url='https://oauth.vk.com/authorize',
    authorize_params=None,
    api_base_url='https://api.vk.com/method/',
    client_kwargs={'scope': 'email'},
)


class GoogleOauth(Resource):
    def get(self):
        google = oauth.create_client('google')
        redirect_uri = 'http://localhost/api/v1/callback'
        return google.authorize_redirect(redirect_uri)


class VKOauth(Resource):
    def get(self):
        vk = oauth.create_client('vk')
        redirect_uri = 'http://localhost/api/v1/callback'
        return vk.authorize_redirect(redirect_uri)


class Callback(Resource):
    def get(self):
        google = oauth.create_client('google')
        token = google.authorize_access_token()
        resp = google.get('userinfo')
        if resp.status_code != 200:
            return jsonify({'error': 'Failed to fetch user info'})
        user_info = resp.json()
        return jsonify(user_info)
