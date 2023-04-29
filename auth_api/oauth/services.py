"""Abstract class for OAuth providers and services"""

import json
import secrets

from flask import url_for, redirect, request
from rauth import OAuth2Service

from core.config import configs

OAUTH_CREDENTIALS = {
        'google': {
            'id': '173135724631-iag1nja3t9bsuts21iqg6ihive2orhfr.apps.googleusercontent.com',
            'secret': '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'
        },
        'mail': {
            'id': '888193a485c54cbda9a46d024c78373b',
            'secret': '4a1190dec95b4d3eaaf09b20c12d3d3e'
        }
    }


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name) -> None:
        self.provider_name = provider_name
        credentials = OAUTH_CREDENTIALS[provider_name]
        self.client_id = credentials['id']
        self.client_secret = credentials['secret']
    def authorize(self):
        pass
    def callback(self):
        pass
    def get_callback_url(self):
        return url_for(f'{self.provider_name}oauthcallback',
                       _external=True)
    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class(provider_name=provider_name)
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class GoogleSignIn(OAuthSignIn):
    def __init__(self, provider_name) -> None:
        super(GoogleSignIn, self).__init__('google')
        self.service = OAuth2Service(
            client_id=self.client_id,
            client_secret=self.client_secret,
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            access_token_url='https://oauth2.googleapis.com/token',
            name='google',
            base_url='https://openidconnect.googleapis.com/v1/userinfo'
        )
    def authorize(self):
        return redirect(
            self.service.get_authorize_url(
                scope='email',
                response_type='code',
                redirect_uri=self.get_callback_url()
            )
        )
    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        callback_url = self.get_callback_url()
        print(f'+++++ REQUEST {request.__dict__} ++++++++')
        print(callback_url)
        oauth_session = self.service.get_auth_session(
            data={
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': callback_url
            },
            decoder=json.loads
        )
        print(f'============ {oauth_session} ==================')
        me = oauth_session.get('').json()
        login_email = me['email'].split('@')
        login = login_email[0]
        return (me['sub'], login, me['email'])


# class MailRuSignIn(OAuthSignIn):
#     def __init__(self, provider_name):
#         super(MailRuSignIn, self).__init__('mail')
#         self.service = OAuth2Service(name='mail',
#                                      client_id=self.client_id,
#                                      client_secret=self.client_secret,
#                                      authorize_url=self.auth_uri,
#                                      access_token_url=self.token_uri,
#                                      base_url=self.base_url)
#         self.state = secrets.token_urlsafe()

#     def authorize(self):
#         return redirect(self.service.get_authorize_url(
#             scope='email',
#             response_type='code',
#             redirect_uri=self.get_callback_url(),
#             state=self.state
#             )
#                         )

#     def callback(self):
#         if 'code' not in request.args:
#             return None, None, None
#         if request.args['state'] != self.state:
#             return None, None, None
#         oauth_session = self.service.get_auth_session(
#             data={
#                 'code': request.args['code'],
#                 'grant_type': 'authorization_code',
#                 'redirect_uri': self.get_callback_url()
#             },
#             decoder=json.loads
#         )
#         params = {
#             'access_token': oauth_session.access_token
#         }
#         me = oauth_session.get('', params=params).json()
#         login_email = me['email'].split('@')
#         login = login_email[0]
#         return (me['id'], login, me['email'])
