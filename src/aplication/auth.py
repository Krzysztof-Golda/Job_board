from flask import Blueprint, render_template, redirect, request, url_for, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


# Sign in
@auth.route("/sign-in", methods=["POST", "GET"])
def sign_in():
    index = url_for("views.home")
    register = url_for("auth.sign_up")
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()
        
        
        if user:
            if check_password_hash(user.password, password):
                flash("Zalogowano", category="info")
                login_user(user, remember=True)
                return redirect(url_for("views.user_board"))
            else:
                flash("Nieprawidłowe hasło.", category="error")
                
        else:
            flash("Nieporawna nazwa użytkownika", category="error")
               
    return render_template("sign_in.html", index=index, register=register)

# Loguot
@auth.route("/logut")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))  

# Sign up
@auth.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    index = url_for("views.home")
    sign_in = url_for("auth.sign_in")
    
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_passwd = request.form.get("repeat-password")
        
        email_exist = User.query.filter_by(email=email).first()
        username_exist = User.query.filter_by(username=username).first()
        
        if email_exist:
            flash("Ten email jest już zajęty.", category="error")
        elif username_exist:
            flash("Ta nazwa użytkownika jest już zajęta.", category="error")
        elif password != confirm_passwd:
            flash("Powtórzone hasło nie jest identyczne", category="error")
        elif len(username) < 5:
            flash("Nazwa użytkownika jest za krótka.", category="error")
        elif len(password) < 5:
            flash("Hasło jest za krótkie.", category="error")
        elif len(email) < 4:
            flash("Nie prawidłowy email", "error")
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Konto zostało poprawnie utworzone.", category="info")
            
            return redirect(url_for("views.home"))
        
    return render_template("sign_up.html", index=index, login=sign_in)