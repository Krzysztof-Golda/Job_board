from flask import Blueprint, url_for, request, redirect, flash, render_template
from flask_login import login_required, current_user, confirm_login
from .scraper import PracujScrap
from .models import Job, User
from . import db
from datetime import datetime
import werkzeug

views = Blueprint("views", __name__)

# index page
@views.route("/")
def home():
    log_in = url_for("auth.sign_in")
    register = url_for("auth.sign_up")
    
    if confirm_login():
        return redirect(url_for("views.user_board"))
    else:
        return render_template("index.html", login=log_in, register=register)

# User's board
@views.route("/board", methods=["POST", "GET"])
@login_required
def user_board():
    logout = url_for("auth.logout")
    add_job = url_for("views.add_job")
    job_cards = Job.query.all()
    user_cards = [card_job for card_job in job_cards if card_job.owner == current_user.id]
    
    return render_template("jobs_board.html", user=current_user.username, logout=logout, add_job=add_job, job_cards=user_cards, pracuj_img="pracuj_log.svg")

# Add job's card
@views.route("/add-job", methods=["POST", "GET"])
@login_required
def add_job():
    job_board = url_for("views.user_board")
    
    # wysłanie formularza
    if request.method == "POST":
        # formularz automatyczny
        if request.form.get("auto-url-job"):
            # wybranie przycisku pracuj
            if request.form.get("job-scrap") == "pracuj":
                job_url = request.form.get("auto-url-job")
                scrappy = PracujScrap(job_url)
                # sprawdzenie poprawności linku
                if not scrappy.bad_url:
                    scrap_result = scrappy.result_soup
                    job_name = scrap_result.get("job_name")
                    company_name = scrap_result.get("company_name")
                    job_level = scrap_result.get("job_level")
                    date_expire = scrap_result.get("offer_expire_date")
                    job_city = scrap_result.get("work_place")
                    
                    salary_from = scrap_result.get("salary_from")
                    salary_to = scrap_result.get("salary_to")
                    
                    
                    if scrap_result.get("salary_from") == None:
                        job_card = Job(job_name=str(job_name), company_name=str(company_name), job_level=str(job_level), date_expire=str(date_expire),job_city=str(job_city), job_url=job_url, owner=current_user.id)
                    else:
                        job_card = Job(job_name=str(job_name), company_name=str(company_name), job_level=str(job_level), date_expire=str(date_expire),job_city=str(job_city), salary_from=str(salary_from), salary_to=str(salary_to), job_url=job_url, owner=current_user.id)
                    
                    flash("Zapisano ofertę", category="info")
                    db.session.add(job_card)
                    db.session.commit()
            else:
                flash("Nie wybrano opcji pracuj.pl", category="error")
        
        # manualne wpisywanie danych     
        elif request.form.get("manual-form"):
            job_url = request.form.get("job-url")
            job_name = request.form.get("job-name")
            company_name = request.form.get("company-name")
            job_level = request.form.get("job-level")
            date_expire = request.form.get("job-date")
            job_city = request.form.get("city-job")
            
            salary_from = request.form.get("salary-from")
            salary_to = request.form.get("salary-to")
            
            if not salary_from and not salary_to:
                job_card = Job(job_name=str(job_name), company_name=str(company_name), job_level=str(job_level), date_expire=str(date_expire),job_city=str(job_city), job_url=job_url, owner=current_user.id)
            else:
                job_card = Job(job_name=str(job_name), company_name=str(company_name), job_level=str(job_level), date_expire=str(date_expire),job_city=str(job_city), salary_from=str(salary_from), salary_to=str(salary_to), job_url=job_url, owner=current_user.id)
            flash("Zapisano ofertę", category="info")
            db.session.add(job_card)
            db.session.commit()
            
    return render_template("job_add.html", board=job_board, user=current_user.username)

# User's account
@views.route("/<username>", methods=["GET", "POST"])
@login_required
def user_account(username):
    job_board = url_for("views.user_board")
    logout = url_for("auth.logout")
    user_mail = current_user.email
    
    if username != current_user.username:
        flash("Nie masz uprawnień do przeglądania danych innych użytkowników.") 
        return redirect(url_for("views.user_board"))
    
    looking_user = User.query.filter_by(username=username).first()
    if looking_user.id == current_user.id:
        if request.method == "POST":
            if request.form.get("delete-account") != "delete":
                new_username = request.form.get("username")
                new_email = request.form.get("email")
                if request.form.get("password") == request.form.get("password-repeat"):
                    new_password = request.form.get("password")
                else:
                    flash("Powtórzone hasło nie jest identyczne")
                
                if new_username:    
                    looking_user.username = new_username
                if new_email:
                    looking_user.email = new_email
                if new_password:
                    looking_user.password = new_password
                db.session.commit()
            else:
                flash("Konto zostało usunięte")
                db.session.delete(looking_user)
                db.session.commit()  
        return render_template("user.html", user=username, board=job_board, logout=logout, email=user_mail)
    else:
        flash("Nie masz uprawnień do przeglądania danych innych użytkowników.") 
        return redirect(url_for("views.user_board"))

@views.route("/delete/<int:card_id>")
@login_required
def delete(card_id):
    
    deleted_card = Job.query.get(int(card_id))
    
    if not deleted_card:
        flash("Wybrana karta nie istnieje.")
    else:
        if current_user.id == deleted_card.owner:
            db.session.delete(deleted_card)
            db.session.commit()
            flash("Karta usunieta.")
        else:
            flash("Nie masz uprawnień do skasowania tej karty.")
            
    return redirect(url_for("views.user_board"))

