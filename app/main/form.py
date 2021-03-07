from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Write a brief bio about you.',validators = [Required()])
    submit = SubmitField('Save')

class BlogForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    category = SelectField('Category', choices=[('Technology','Technology'),('Job','Job'),('Advertisement','Advertisement')],validators=[Required()])
    post = TextAreaField('Your Blog', validators=[Required()])
    submit = SubmitField('Blog')

class CommentForm(FlaskForm):
    comment = TextAreaField('Leave a comment',validators=[Required()])
    submit = SubmitField('Comment')

