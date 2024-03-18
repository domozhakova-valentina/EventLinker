from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import Length


class AddComment(FlaskForm):
    text_comment = StringField('Комментарий', validators=[Length(min=1, max=170, message="Возможно от 1 до 170 символов")],
                               render_kw={"placeholder": "Добавить комментарий", "aria-label": "Добавить комментарий"})
    submit = SubmitField('Отправить')
