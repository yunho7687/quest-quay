from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from wtforms import TextAreaField
from wtforms.validators import Length
import sqlalchemy as sa
from app import db
from app.models import User
from flask_wtf.file import FileField, FileAllowed, FileRequired

import app
import os


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
    uploadFile = FileField('Upload Avatar', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == self.username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
    uploadFile = FileField('Upload Image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])

# class EmptyFormLikeComment(FlaskForm):
#     like_comment = SubmitField('Like')
    

# class EmptyFormSavePost(FlaskForm):
#     like_comment = SubmitField('Unlike')


class PostForm(FlaskForm):
    title=StringField('Title',validators=[
        DataRequired(), Length(min=1, max=50)])
    post = TextAreaField('Quest', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')
    uploadFile = FileField('Upload Image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired(), Length(
        min=1, max=140)], render_kw={"placeholder": "Title, contnet"})
    submit=SubmitField('Search')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment:', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit',id='submit-comment')
    uploadFile = FileField('Upload Image',validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    
class UploadForm(FlaskForm):
    uploadFile = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])