from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField

class PostForm(FlaskForm):
    title = StringField('Title',
                    validators=[DataRequired(), Length(max=80)])
    
    # content = TextAreaField('Content', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])

    submit = SubmitField('Post')

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Search")