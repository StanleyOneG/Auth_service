from flask import Flask, request
from gevent import monkey

monkey.patch_all()

import logging
from flask_wtf import CSRFProtect
from flask_restful import Resource, Api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)
csrf = CSRFProtect(app)


@app.before_request
def csrf_protect():
    if (
        request.method == 'POST'
        and request.url_root
        == 'http://sprint06_auth_api:5050',  # TODO: вынести host в env файл
    ):
        # exempt the URL from CSRF protection
        csrf.exempt(request.url)


class TestHelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, World!'}


api.add_resource(TestHelloWorld, '/hello')


app.run(
    debug=True, host='sprint06_auth_api', port='8000'
)  # TODO: вынести host в env файл
