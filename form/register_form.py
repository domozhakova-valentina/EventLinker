from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, StringField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    email = EmailField('Your Email', validators=[DataRequired(message="Это поле является обязательным."),
                                                 Email(message="Неверный адрес электронной почты.")])
    password = PasswordField('Password', validators=[DataRequired(message="Это поле является обязательным.")])
    password_again = PasswordField('Repeat your password',
                                   validators=[DataRequired(message="Это поле является обязательным.")])
    name = StringField("Your Name", validators=[DataRequired(message="Это поле является обязательным.")])
    about = TextAreaField('About you')  # краткое описание пользователя, не обязательно
    photo = FileField('Avatar', default='...')  # иконка пользователя, если не укажет, то по умолчанию будет
    submit = SubmitField('Register')
