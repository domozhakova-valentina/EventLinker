from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(message="Это поле является обязательным."),
                                            Email(message="Неверный адрес электронной почты.")])
    password = PasswordField('Password', validators=[DataRequired(message="Это поле является обязательным.")])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Login')
