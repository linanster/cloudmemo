from app.models.sqlite import db_sqlite

def init_models(app):
    db_sqlite.init_app(app)
