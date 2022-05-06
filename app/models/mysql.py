from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dateutil import tz
#
db_mysql = SQLAlchemy(use_native_unicode='utf8')

class MyBaseModel(db_mysql.Model):
    __abstract__ = True
    id = db_mysql.Column(db_mysql.Integer, nullable=False, autoincrement=True, primary_key=True)
    def save(self):
        try:
            db_mysql.session.add(self)
            db_mysql.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def delete(self):
        try:
            db_mysql.session.delete(self)
            db_mysql.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

class MemoType(MyBaseModel):
    __bind_key__ = 'mysql_gecloudmemo_memotype'
    __tablename__ = 'memotype'
    code = db_mysql.Column(db_mysql.Integer, nullable=False, unique=True)
    name = db_mysql.Column(db_mysql.String(100), nullable=False)
    def __init__(self, code, name):
        self.code = code
        self.name = name
    @staticmethod
    def seed():
        t1 = MemoType(1, 'Xlink NPI Development')
        t2 = MemoType(2, 'Xlink Cloud Release')
        t3 = MemoType(3, 'Xlink Cloud Accident')
        t4 = MemoType(4, 'CTC Test')
        t5 = MemoType(5, 'US Support')
        t6 = MemoType(6, 'Meeting and Discusstion')
        t7 = MemoType(7, 'Miscellaneous')
        db_mysql.session.add_all([t1, t2, t3, t4, t5, t6, t7])
        db_mysql.session.commit()

class MemoRecord(MyBaseModel):
    __bind_key__ = 'mysql_gecloudmemo_memorecord'
    __tablename__ = 'memorecord'
    typecode = db_mysql.Column(db_mysql.Integer, db_mysql.ForeignKey(MemoType.code), nullable=False) 
    time = db_mysql.Column(db_mysql.DateTime, nullable=False)
    summary = db_mysql.Column(db_mysql.String(500), nullable=False)
    author = db_mysql.Column(db_mysql.String(50), nullable=True)
    type = db_mysql.relationship('MemoType', backref='records')
    def __init__(self, typecode, summary, author):
        self.typecode = typecode
        self.time = datetime.now(tz.gettz('Asia/Shanghai'))
        self.summary = summary
        self.author = author
    @staticmethod
    def seed():
        pass

class MemoFile(MyBaseModel):
    __bind_key__ = 'mysql_gecloudmemo_memofile'
    __tablename__ = 'memofile'
    memorecordid = db_mysql.Column(db_mysql.Integer, db_mysql.ForeignKey(MemoRecord.id), nullable=False) 
    filename = db_mysql.Column(db_mysql.String(200), nullable=False)
    deleted = db_mysql.Column(db_mysql.Boolean)
    memorecord = db_mysql.relationship('MemoRecord', backref='files')
    def __init__(self, memorecordid, filename, deleted):
        self.memorecordid = memorecordid
        self.filename = filename
        self.deleted = deleted
    @staticmethod
    def seed():
        pass

class MemoComment(MyBaseModel):
    __bind_key__ = 'mysql_gecloudmemo_memocomment'
    __tablename__ = 'memocomment'
    memorecordid = db_mysql.Column(db_mysql.Integer, db_mysql.ForeignKey(MemoRecord.id), nullable=False)
    comment = db_mysql.Column(db_mysql.Text, nullable=True)
    memorecord = db_mysql.relationship('MemoRecord', backref='comments')
    def __init__(self, memorecordid, comment):
        self.memorecordid = memorecordid
        self.comment = comment
    @staticmethod
    def seed():
        pass

