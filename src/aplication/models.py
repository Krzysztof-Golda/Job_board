from sqlalchemy.sql.expression import null
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), unique=True)    
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    job_card = db.relationship("Job", backref='user', passive_deletes=True)
    
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(150), nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    job_level = db.Column(db.String(150), nullable=False)
    date_expire = db.Column(db.String(150), nullable=False)
    job_city = db.Column(db.String(150), nullable=True)
    salary_from = db.Column(db.String(150), nullable=True)
    salary_to = db.Column(db.String(150), nullable=True)
    job_url = db.Column(db.String(150), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    owner = db.Column(db.Integer, db.ForeignKey('user.id', on_delete="CASCADE"), nullable=False)