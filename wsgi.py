from app.app import create_app, envinfo
#

application_cloudmemo = create_app()

@application_cloudmemo.template_global('get_memotypes')
def get_memotypes():
    from app.models.mysql import MemoType
    return MemoType.query.all()

if __name__ == '__main__':

    # envinfo()
    application_cloudmemo.run(host='0.0.0.0', port=5200)
