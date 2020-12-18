from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, validators
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class AddAutoForm(FlaskForm):
    type = SelectField('Тип', choices=[("choose", "Выберите"), ("Автобус", "Автобус"), ("Трамвай", "Трамвай"), ("Троллейбус", "Троллейбус"), ("Маршрутка", "Маршрутка")], validate_choice=True)
    plate_number = StringField('Госномер', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class AddStaffForm(FlaskForm):
    user_name = StringField('Имя', validators=[DataRequired()])
    birth_day = DateField('Дата рождения', format='%d-%m-%Y', validators=(validators.Optional(),))
    gender = SelectField('Пол', choices=[("choose", "Выберите"), ("М", "М"), ("Ж", "Ж")], validate_choice=True)
    user_login = StringField('Логин', validators=[DataRequired()])
    user_password = PasswordField('Пароль', validators=[DataRequired()])
    user_post = SelectField('Должность', choices=[("choose", "Выберите"), ("Уборщик", "Уборщик"), ("Техник", "Техник"), ("Администратор сайта", "Администратор")], validate_choice=False)
    submit = SubmitField('Добавить')


class StatusOfAuto(FlaskForm):
    clean_status = SelectField('Статус уборки', choices=[("Не убрано", "Не убрано"), ("Убрано", "Убрано")], validate_choice=False)
    tech_status = SelectField('Статус обслуживания', choices=[("Не обслужено", "Не обслужено"), ("Обслужено", "Обслужено")], validate_choice=False)
    submit = SubmitField("Внести изменения")
