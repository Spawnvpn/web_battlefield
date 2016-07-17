from flask import Flask
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware

app = Flask(__name__)
app.config.from_object('config')


class BeakerSessionInterface(SessionInterface):

    def open_session(self, app, request):
        session = request.environ['beaker.session']
        return session

    def save_session(self, app, session, response):
        session.save()

session_opts = {
    'session.type': 'ext:memcached',
    'session.url': '127.0.0.1:11211',
    'session.data_dir': './cache',
}

app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
app.session_interface = BeakerSessionInterface()
from app import views