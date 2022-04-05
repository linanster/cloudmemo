from app.app import create_app, envinfo
#

app = create_app()

@app.template_global('get_memotypes')
def get_memotypes():
    from app.models.mysql import MemoType
    return MemoType.query.all()

if __name__ == '__main__':

    # envinfo()
    app.run(host='0.0.0.0', port=9000)
