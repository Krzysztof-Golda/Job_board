from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "databse.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "helloworld"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)
    
    from .views import views
    app.register_blueprint(views, url_prefix="/")
    
    from .auth import auth
    app.register_blueprint(auth, url_prefix="/")
    
    from .models import User, Job
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.sign_in"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    @app.errorhandler(404)
    def page_not_found(error):
        log_in = url_for("auth.sign_in")
        register = url_for("auth.sign_up")
        return render_template("404.html", login=log_in, register=register), 404
    
    return app

def create_database(app):
    if not path.exists("aplication/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")