from flask import request
from app.lib.mylib import afterrequestlog

def load_middleware(app):

    @app.before_request
    def process_before():
        pass

    @app.after_request
    @afterrequestlog
    def process_after(response):
        return response

