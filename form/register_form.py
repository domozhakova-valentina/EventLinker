from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import PasswordField, EmailField, SubmitField, StringField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    email = EmailField('Your Email', validators=[DataRequired(message="Это поле является обязательным."),
                                                 Email(message="Неверный адрес электронной почты.")])
    password = PasswordField('Password', validators=[DataRequired(message="Это поле является обязательным."),
                                                     Length(min=5, max=12,
                                                            message="Пароль должен содержать от 5 до 12 символов.")])
    password_again = PasswordField('Repeat your password',
                                   validators=[DataRequired(message="Это поле является обязательным."),
                                               EqualTo('password', message="Пароль не совпал с паролем выше!")])
    name = StringField("Your Name", validators=[DataRequired(message="Это поле является обязательным."),
                                                Length(min=3, max=20,
                                                       message="Имя должно содержать от 3 до 20 символов.")])
    about = TextAreaField('About you', description='О пользователе ничего не известно.')  # краткое описание пользователя, не обязательно
    photo = FileField('Avatar', default='...',
                      validators=[FileAllowed(['jpg', 'png', 'svg'],
                                              message='Принимаются файлы в расширение .jpg, .png и .svg'), ])  # иконка пользователя, если не укажет, то по умолчанию будет
    submit = SubmitField('Register')
