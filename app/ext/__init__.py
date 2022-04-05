def init_ext(app):
    from app.ext.loginmanager import login_manager
    login_manager.init_app(app)
    
