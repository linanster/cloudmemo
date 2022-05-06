from flask_script import Manager
from app.app import create_app, envinfo
#

app = create_app()
manager = Manager(app)

@manager.command
def hello():
    print('hello')

@manager.command
def env():
    envinfo()

@manager.command
def createdb_sqlite(table=False, data=False):
    "--table --data"
    from app.models.sqlite import db_sqlite, User
    if table:
        db_sqlite.create_all(bind='sqlite_user_user')
        print('==create sqlite tables==: user')
    if data:
        User.seed()
        print('==initialize sqlite data==')

@manager.command
def deletedb_sqlite(table=False, data=False):
    "--table --data"
    from app.models.sqlite import db_sqlite, User
    if table:
        db_sqlite.drop_all(bind='sqlite_user_user')
        print('==delete sqlite tables==')
        return
    if data:
        User.query.delete()
        db_sqlite.session.commit()
        print('==delete sqlite data==')

@manager.command
def createdb_mysql(table=False, data=False):
    "--table --data"
    from app.models.mysql import db_mysql, MemoType, MemoRecord, MemoFile, MemoComment
    if table:
        db_mysql.create_all(bind='mysql_gecloudmemo_memotype')
        db_mysql.create_all(bind='mysql_gecloudmemo_memorecord')
        db_mysql.create_all(bind='mysql_gecloudmemo_memofile')
        db_mysql.create_all(bind='mysql_gecloudmemo_memocomment')
        print('==create mysql tables==: memotype, memorecord, memofile, memocomment')
    if data:
        MemoType.seed()
        print('==insert data==: memotype')

@manager.command
def deletedb_mysql(table=False, data=False):
    "--table --data"
    from app.models.mysql import db_mysql, MemoType, MemoRecord, MemoFile
    if table:
        db_mysql.drop_all(bind='mysql_gecloudmemo_memocomment')
        db_mysql.drop_all(bind='mysql_gecloudmemo_memofile')
        db_mysql.drop_all(bind='mysql_gecloudmemo_memorecord')
        db_mysql.drop_all(bind='mysql_gecloudmemo_memotype')
        print('==delete mysql tables==')
        return
    if data:
        MemoComment.query.delete()
        MemoFile.query.delete()
        MemoRecord.query.delete()
        MemoType.query.delete()
        db_mysql.session.commit()
        print('==delete mysql datas==')


# python3 manage.py runserver -h 0.0.0.0 -p 5000 -r -d
if __name__ == '__main__':

    manager.run()
