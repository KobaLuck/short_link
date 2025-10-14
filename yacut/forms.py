from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(message='Вы не ввели полную ссылку!'),
                    URL(message='Вы ввели не ссылку!')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16, message='Длина не более 16 символов!'),
            Optional(),
            Regexp('^[A-Za-z0-9]*$',
                   message='Можно использовать только буквы и цифры')
        ]
    )
    submit = SubmitField('Создать')


class FileUploadForm(FlaskForm):
    files = MultipleFileField(
        'Выберите файлы',
        validators=[DataRequired(message='Выберите хотя бы один файл')]
    )
    submit = SubmitField('Загрузить')
