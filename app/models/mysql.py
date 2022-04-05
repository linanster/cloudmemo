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
        t2 = MemoType(2, 'Xlink Cloud Update')
        t3 = MemoType(3, 'Xlink Cloud Accident')
        t4 = MemoType(4, 'CTC Local Verification Test')
        t5 = MemoType(5, 'US Request Support')
        t6 = MemoType(6, 'Other')
        db_mysql.session.add_all([t1, t2, t3, t4, t5, t6])
        db_mysql.session.commit()

class MemoRecord(MyBaseModel):
    __bind_key__ = 'mysql_gecloudmemo_memorecord'
    __tablename__ = 'memorecord'
    typecode = db_mysql.Column(db_mysql.Integer, db_mysql.ForeignKey(MemoType.code), nullable=False) 
    time = db_mysql.Column(db_mysql.DateTime, default=datetime.now(tz.gettz('Asia/Shanghai')), nullable=False)
    summary = db_mysql.Column(db_mysql.String(500), nullable=False)
    # comment = db_mysql.Column(db_mysql.String(5000), nullable=True)
    comment = db_mysql.Column(db_mysql.Text, nullable=True)
    type = db_mysql.relationship('MemoType', backref='records')
    def __init__(self, typecode, summary, comment='', time = datetime.now(tz.gettz('Asia/Shanghai'))):
        self.typecode = typecode
        self.time = time
        self.summary = summary
        self.comment = comment        
    @staticmethod
    def seed():
        r1 = MemoRecord(5, 'Investigate Tim’s question', '2.1 google action binding errors\n2.2 detailed commands logs during google voice automation test environment')
        r2 = MemoRecord(1, 'Share location requests are being evaluated.')
        r3 = MemoRecord(6, 'Dr. Wang raised a requirement', 'need to develop a tool to record cloud service functionality and release log.')
        r4 = MemoRecord(2, 'Service optimization postpone', 'Service optimization bug has been fixed, postpone to next week to deploy.')
        r5 = MemoRecord(5, 'Validate Gina’s account', 'Validate Gina’s account about motion detection and person detection, test report has been sent out.')
        r6 = MemoRecord(5, 'Thermostat FW 12104 statistics have been sent out', 'Next week CTC hold a meeting to discuss usually used query requests.')
        r7 = MemoRecord(3, 'GCP DB3 server automatically restart on last Sunday', 'Do you think we need to further discussion or can we go on to do the Dual Write directly?\nIf need to discussion, can we have an online meeting, here I tentatively schedule this meeting on this Friday morning, from 9:00 AM to 9:45 AM, Shanghai time\nIf no need further discussion, we will directly start the Dual Write operations on Next Monday, from 14:30PM to 17:00PM, Shanghai time.')
        r8 = MemoRecord(4, 'Google Cloud Action issues discussion', )
        db_mysql.session.add_all([r1, r2, r3, r4, r5, r6, r7, r8])
        db_mysql.session.commit()

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
        # f1 = MemoFile(1, 'a1.txt', False)
        # f2 = MemoFile(1, 'a2.txt', False)
        # f3 = MemoFile(2, 'b.txt', False)
        # f4 = MemoFile(3, 'c.txt', False)
        # db_mysql.session.add_all([f1, f2, f3, f4])
        # db_mysql.session.commit()


