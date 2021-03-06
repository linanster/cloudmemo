from flask import Flask
from app.models import init_models
from app.views import init_views
from app.ext import init_ext
# from app.apis import init_apis
from app.mymiddleware import load_middleware

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('mysettings.py')
    init_models(app)
    init_views(app)
    init_ext(app)
    # init_apis(app)
    load_middleware(app)
    return app

def envinfo():
    import sys
    print('==sys.version==',sys.version)
    print('==sys.executable==',sys.executable)

