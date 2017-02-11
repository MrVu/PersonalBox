from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NewFolder(FlaskForm):
    folder = StringField('folder', validators=[DataRequired()])
    submit = SubmitField()


class FileUpload(FlaskForm):
    upload_file = FileField(validators=[FileRequired()])
    submit = SubmitField()
