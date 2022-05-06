def init_views(app):
    from app.views.blue_main import blue_main
    from app.views.blue_memo import blue_memo
    from app.views.blue_auth import blue_auth
    from app.views.blue_log import blue_log
    app.register_blueprint(blue_main)
    app.register_blueprint(blue_memo)
    app.register_blueprint(blue_auth)
    app.register_blueprint(blue_log)
