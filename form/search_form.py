from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    search = StringField('Поиск', render_kw={"placeholder": "Поиск", "aria-label": "Поиск"})
    submit = SubmitField('Поиск по описанию')
