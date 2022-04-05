from app.models.sqlite import db_sqlite
from app.models.mysql import db_mysql

def init_models(app):
    db_sqlite.init_app(app)
    db_mysql.init_app(app)
