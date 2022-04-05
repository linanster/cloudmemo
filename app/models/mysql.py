from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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
        t1 = MemoType(1, 'Cloud Publish')
        t2 = MemoType(2, 'Cloud Accident')
        t3 = MemoType(3, 'CTC Verification Test')
        db_mysql.session.add_all([t1, t2, t3])
        db_mysql.session.commit()

class MemoRecord(MyBaseModel):
    __bind_key__ = 'mysql_gecloudmemo_memorecord'
    __tablename__ = 'memorecord'
    typecode = db_mysql.Column(db_mysql.Integer, db_mysql.ForeignKey(MemoType.code), nullable=False) 
    time = db_mysql.Column(db_mysql.DateTime, default=datetime.now(), nullable=False)
    summary = db_mysql.Column(db_mysql.String(200), nullable=False)
    comment = db_mysql.Column(db_mysql.String(200), nullable=True)
    type = db_mysql.relationship('MemoType', backref='records')
    def __init__(self, typecode, summary, comment='', time = datetime.now()):
        self.typecode = typecode
        self.time = time
        self.summary = summary
        self.comment = comment        
    @staticmethod
    def seed():
        r1 = MemoRecord(1, 'summary1', 'comment1')
        r2 = MemoRecord(2, 'summary2', 'comment2')
        r3 = MemoRecord(3, 'summary3', 'comment3')
        db_mysql.session.add_all([r1, r2, r3])
        db_mysql.session.commit()

class MemoFile(MyBaseModel):
    __bind_key__ = 'mysql_gecloudmemo_memofile'
    __tablename__ = 'memofile'
    memorecordid = db_mysql.Column(db_mysql.Integer, db_mysql.ForeignKey(MemoRecord.id), nullable=False) 
    filename = db_mysql.Column(db_mysql.String(200), nullable=False)
    memorecord = db_mysql.relationship('MemoRecord', backref='files')
    def __init__(self, memorecordid, filename):
        self.memorecordid = memorecordid
        self.filename = filename
    @staticmethod
    def seed():
        f1 = MemoFile(1, 'a1.txt')
        f2 = MemoFile(1, 'a2.txt')
        f3 = MemoFile(2, 'b.txt')
        f4 = MemoFile(3, 'c.txt')
        db_mysql.session.add_all([f1, f2, f3, f4])
        db_mysql.session.commit()


