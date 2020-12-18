from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5
from app import db


class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    car_type = db.Column(db.String(64), db.ForeignKey('types.type'))
    car_plate_number = db.Column(db.String(10), nullable=False, index=True, unique=True)
    car_status = db.Column(db.String(30), nullable=False, default='Не готово')
    last_cleaning = db.Column(db.DateTime, default=None)
    last_repairing = db.Column(db.DateTime, default=None)
    clean_status = db.Column(db.String(30), nullable=False, default='Не убрано')
    tech_status = db.Column(db.String(30), nullable=False, default='Не обслужено')
    last_staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), default=None)
    accounting = db.relationship('Accounting', backref='car', lazy='dynamic')


class Staff(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(64), index=True, nullable=False)
    user_login = db.Column(db.String(64), nullable=False, index=True, unique=True)
    user_post = db.Column(db.String(64), db.ForeignKey('posts.post'))
    password_hash = db.Column(db.String(128), nullable=True)
    cars = db.relationship('Cars', backref='staff', lazy='dynamic')
    note = db.relationship('Accounting', backref='staff', lazy='dynamic')
    personal = db.relationship('Personal', backref='staff', lazy='dynamic')

    def avatar(self, size):
        return 'https://www.gravatar.com/avatar/?d=identicon&s={}'.format(size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Accounting(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    id_car = db.Column(db.Integer, db.ForeignKey('cars.id'), default=None)
    id_staff = db.Column(db.Integer, db.ForeignKey('staff.id'), default=None)


class Types(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(64), nullable=False, index=True, unique=True)
    cars = db.relationship('Cars', backref='type', lazy='dynamic')


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post = db.Column(db.String(64), nullable=False, index=True, unique=True)
    staff = db.relationship('Staff', backref='post', lazy='dynamic')


class Personal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), default=None)
    birth_day = db.Column(db.Date, default=None)
    gender = db.Column(db.String(1), default=None)
