def init_ext(app):
    from app.ext.loginmanager import login_manager
    from app.ext.bootstrap import bootstrap
    login_manager.init_app(app)
    bootstrap.init_app(app)
    
