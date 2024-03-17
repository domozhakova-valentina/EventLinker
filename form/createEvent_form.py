from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, SubmitField
from wtforms.validators import Length, DataRequired
from flask_wtf.file import FileAllowed


class CreateForm(FlaskForm):
    photo = FileField('Фотография события',
                      default='...',
                      validators=[FileAllowed(['jpg', 'png'],
                                              message='Принимаются файлы в расширение .jpg и .png'), ])  # фотография карточки, если не укажет, то по умолчанию будет
    mini_description = TextAreaField("Имя и вводное описание мероприятия:",
                                     validators=[DataRequired(message="Это поле является обязательным."),
                                                 Length(max=140, message='Слишком длинно')])
    description = TextAreaField("Полное описание:", validators=[Length(min=50, message='Слишком маленькое описание')])
    submit = SubmitField('Create')
