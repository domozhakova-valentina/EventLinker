from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import Length


class AddComment(FlaskForm):
    text_comment = StringField('Комментарий', default='Добавить комментарий',
                               validators=[Length(min=1, max=170, message="Возможно от 1 до 170 символов")])
    submit = SubmitField('Отправить')
