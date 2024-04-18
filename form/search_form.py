from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField


class SearchForm(FlaskForm):
    search = StringField('Поиск', render_kw={"placeholder": "Поиск", "aria-label": "Поиск"})
    concert = BooleanField('Концерты')
    excursion = BooleanField('Экскурсии')
    sports = BooleanField('Спорт')
    attractions = BooleanField('Развлечения')
    for_kids = BooleanField('Для детей')
    studies = BooleanField('Учеба')
    other = BooleanField('Прочее')
    submit = SubmitField('Поиск и сортировка')

    def get_selected_event_types(self):
        selected_event_types = []
        if self.concert.data:
            selected_event_types.append('концерт')
        if self.excursion.data:
            selected_event_types.append('экскурсия')
        if self.sports.data:
            selected_event_types.append('спорт')
        if self.attractions.data:
            selected_event_types.append('развлечения')
        if self.for_kids.data:
            selected_event_types.append('для детей')
        if self.studies.data:
            selected_event_types.append('учеба')
        if self.other.data:
            selected_event_types.append('прочее')

        return selected_event_types if selected_event_types else ['концерт', 'экскурсия', 'спорт', 'развлечения',
                                                                  'для детей', 'учеба', 'прочее']

