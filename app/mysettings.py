SECRET_KEY = "youdonotknowme"
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = False

# SQLALCHEMY_DATABASE_URI = 'sqlite:///../sqlite/db4_hist.sqlite3'
SQLALCHEMY_BINDS = {
# 'mysql_myframework_stu1': 'mysql+pymysql://root1:123456@localhost:3306/myframework',
# 'mysql_myframework_stu2': 'mysql+pymysql://root1:123456@localhost:3306/myframework',
# 'sqlite_db1_sys': 'sqlite:///../sqlite/db1_sys.sqlite3',
# 'sqlite_db2_app': 'sqlite:///../sqlite/db2_app.sqlite3',
# 'sqlite_db3_auth': 'sqlite:///../sqlite/db3_auth.sqlite3',
# 'sqlite_db4_hist': 'sqlite:///../sqlite/db4_hist.sqlite3',
'sqlite_user_user': 'sqlite:///../sqlite/db1_user.sqlite3',
'mysql_gecloudmemo_memotype': 'mysql+pymysql://root1:123456@localhost:3306/gecloudmemo',
'mysql_gecloudmemo_memorecord': 'mysql+pymysql://root1:123456@localhost:3306/gecloudmemo',
'mysql_gecloudmemo_memofile': 'mysql+pymysql://root1:123456@localhost:3306/gecloudmemo',
'mysql_gecloudmemo_memocomment': 'mysql+pymysql://root1:123456@localhost:3306/gecloudmemo',
}

