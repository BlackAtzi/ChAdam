from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class CreateForumForm(Form):
    forum_name = StringField('forum_name', validators=[DataRequired()])

class PostForm(Form):
    post = StringField('post_form', widget=TextArea(), validators=[DataRequired()])

class ImgForm(Form):
    postImg = StringField('img_form', widget=TextArea(), validators=[DataRequired()])