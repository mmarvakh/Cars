from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask import Flask, render_template, request, redirect, flash, url_for, json, session
from forms import LoginForm, AddAutoForm, AddStaffForm, StatusOfAuto
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse
from flask_migrate import Migrate
from config import Config
from time import sleep

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import *


def date_and_time():
    dat = datetime.today().strftime("%Y.%m.%d, %H:%M:%S")
    return dat


@login.user_loader
def load_user(id):
    return Staff.query.get(int(id))


# Страница входа в систему
@app.route('/login', methods=['POST', 'GET'])
def login():
    title = "Вход в систему"

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = Staff.query.filter_by(user_login=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Неверный логин или пароль")
            return redirect(url_for('login'))
        login_user(user, remember=False)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        next_page = next_page[1::]
        return redirect(next_page)

    return render_template("login.html", form=form, title=title)


@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))


# Главная страница
@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    title = 'Учёт состояния автопарка'

    form_status = StatusOfAuto()
    types = Types.query.order_by(Types.id).all()

    if current_user.user_post == "Уборщик":
        cars = Cars.query.order_by(Cars.last_cleaning).all()
    elif current_user.user_post == "Техник":
        cars = Cars.query.order_by(Cars.last_repairing).all()
    else:
        cars = Cars.query.order_by(Cars.id).all()

    if form_status.validate_on_submit():
        if form_status.clean_status.data == "Не убрано" or form_status.tech_status.data == "Не обслужено":
            return redirect(url_for('index'))

        id_request = request.form["id"]

        car_in_base = db.session.query(Cars).filter_by(id=int(id_request)).first()

        try:
            note = Accounting(date=date_and_time(), id_car=id_request, id_staff=current_user.id)
            db.session.add(note)
            db.session.commit()

            if current_user.user_post == "Уборщик":
                select_status = form_status.clean_status.data
                car_in_base.clean_status = select_status
                car_in_base.last_cleaning = date_and_time()
            elif current_user.user_post == "Техник":
                select_status = form_status.tech_status.data
                car_in_base.tech_status = select_status
                car_in_base.last_repairing = date_and_time()

            car_in_base.last_staff_id = current_user.id

            if (select_status == "Обслужено" and car_in_base.clean_status == "Убрано") or (
                    select_status == "Убрано" and car_in_base.tech_status == "Обслужено"):
                car_in_base.car_status = "Готово"

            db.session.commit()

            return redirect(url_for('index'))
        except:
            return "<h3>Ошибка при внесении изменений в базу данных.</h3>"

    session['car_type'] = 'any'
    session['clean_status'] = 'any'
    session['tech_status'] = 'any'

    return render_template("index.html", current_user=current_user, cars=cars, form_status=form_status,
                           types=types, title=title)


# Панель администратора
@app.route('/admin-panel', methods=['POST', 'GET'])
@login_required
def admin_panel():
    title = 'Панель администратора'

    if current_user.user_post != 'Администратор':
        return redirect(url_for('index'))

    form_cars = AddAutoForm()
    form_staff = AddStaffForm()

    if form_cars.validate_on_submit():
        selected_type = form_cars.type.data
        plate_number = form_cars.plate_number.data

        new_car = Cars(car_type=selected_type, car_plate_number=plate_number)

        try:
            db.session.add(new_car)
            db.session.commit()

            return redirect(url_for('admin_panel'))
        except:
            return "<h3>Ошибка при добавлении авто в базу данных. Проверьте правильность написания госномера. " \
                   "Если Вы уверены, что написан номер верно, " \
                   "то данный номер уже содержится в базе данных автопарка</h3>"

    if form_staff.validate_on_submit():
        user_name = form_staff.user_name.data
        user_login = form_staff.user_login.data
        password = form_staff.user_password.data
        user_post = form_staff.user_post.data

        new_staff = Staff(user_name=user_name, user_login=user_login, user_post=user_post)
        new_staff.set_password(password)

        try:
            db.session.add(new_staff)
            db.session.commit()

            sleep(3)

            personal_info = Personal(staff_id=Staff.query.filter_by(user_login=login).first().id,
                                     birth_day=form_staff.birth_day.data, gender=form_staff.gender.data)
            db.session.add(personal_info)
            db.session.commit()

            return redirect(url_for('admin_panel'))
        except:
            return "<h3>Ошибка при добавлении пользователя в базу данных. " \
                   "Проверьте правильность написания имени и логина. " \
                   "Если Вы уверены, что написаны они верно, " \
                   "то данный(ое) логин / имя уже содержится в базе данных автопарка</h3>"

    return render_template('admin.html', form_cars=form_cars, form_staff=form_staff, current_user=current_user,
                           title=title)


# Личный кабинет
@app.route('/personal/<user_login>', methods=["POST", "GET"])
@login_required
def personal(user_login):
    title = 'Личный кабинет'
    
    info = Personal.query.filter_by(staff_id=current_user.id).first()
    user = Staff.query.filter_by(user_login=user_login).first_or_404()

    if current_user.user_post == "Администратор":
        notes = Accounting.query.order_by(Accounting.date.desc()).all()
    else:
        notes = Accounting.query.filter_by(id_staff=current_user.id).order_by(Accounting.date.desc()).all()

    return render_template('personal.html', current_user=current_user, user=user, notes=notes, info=info, title=title)


# Обработчик фильтров
@app.route('/query-filter', methods=["GET"])
def query_filter():
    current_key = ''
    current_value = ''

    for elem in request.args:
        current_key = elem
        current_value = request.args[elem]

    session[current_key] = current_value

    query = '''SELECT * FROM cars WHERE'''

    for key in session:
        if key == 'car_type' or key == 'clean_status' or key == 'tech_status' or key == 'car_status':
            if session[key] != 'any':
                query += " {key}='{value}' AND".format(key=key, value=session[key])

    query = query.strip(' WHERE')
    query = query.strip(' AND')

    cars = db.session.execute(query).fetchall()

    return render_template('query.html', cars=cars)


if __name__ == '__main__':
    app.run()
