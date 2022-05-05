from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
#
db_sqlite = SQLAlchemy(use_native_unicode='utf8')

class MyBaseModel(db_sqlite.Model):
    __abstract__ = True
    id = db_sqlite.Column(db_sqlite.Integer, nullable=False, autoincrement=True, primary_key=True)
    def save(self):
        try:
            db_sqlite.session.add(self)
            db_sqlite.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def delete(self):
        try:
            db_sqlite.session.delete(self)
            db_sqlite.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

class User(UserMixin, MyBaseModel):
    __bind_key__ = 'sqlite_user_user'
    __tablename__ = 'user'
    username = db_sqlite.Column(db_sqlite.String(100), nullable=False, unique=True, index=True)
    _password = db_sqlite.Column(db_sqlite.String(256), nullable=False)
    def __init__(self, username='nousername', password='nopassword'):
        self.username = username
        self._password = password

    @property
    def password(self):
        raise Exception('password is not accessible')
        # return self._password

    @password.setter
    def password(self, new_password):
        self._password = new_password

    def verify_password(self, password):
        return self._password == password

    @staticmethod
    def seed():
        user1 = User('user1', 'makeituptome')
        user2 = User('user2', '123456')
        seeds = [user1, user2]
        db_sqlite.session.add_all(seeds)
        db_sqlite.session.commit()

