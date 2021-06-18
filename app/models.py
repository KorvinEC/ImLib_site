from flask_user import UserMixin
from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from app.init_app import db
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import Required


# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    # reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')

class Library(db.Model):
    __tablename__ = 'library'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    name = db.Column(db.String(50), nullable=False, server_default=u'')
    parent = db.Column(db.Integer(), nullable=True)

class Library_image(db.Model):
    __tablename__ = 'library_image'
    id = db.Column(db.Integer(), primary_key=True)
    library_id = db.Column(db.Integer(), db.ForeignKey('library.id', ondelete='CASCADE'))
    image_id = db.Column(db.Integer(), db.ForeignKey('images.id', ondelete='CASCADE'))

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False, server_default=u'')

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer(), primary_key=True)
    tag = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)

class Image_Tag(db.Model):
    __tablename__ = 'image_tag'
    id = db.Column(db.Integer(), primary_key=True)
    image_id = db.Column(db.Integer(), db.ForeignKey('images.id', ondelete='CASCADE'))
    tag_id = db.Column(db.Integer(), db.ForeignKey('tags.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))

# Define the User registration form
# It augments the Flask-User RegisterForm with additional fields
class MyRegisterForm(RegisterForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])


# Define the User profile form
class UserProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    submit = SubmitField('Save')
	
class ImageForm(FlaskForm):
	image = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'bmp', 'gif', 'jpeg', 'tif'], 'Images only!')
    ])

class TagForm(FlaskForm):
    tag = StringField('Tag', [validators.Length(max=50), validators.DataRequired()])

class LibraryForm(FlaskForm):
    library = StringField('Library', [validators.Length(max=50), validators.DataRequired()])

class SearchFrom(FlaskForm):
    tags = StringField('Tags', [validators.Length(max=50), validators.DataRequired()])

class NameChangeForm(FlaskForm):
    name = StringField('Name', [validators.Length(max=50), validators.DataRequired()])
    submit = SubmitField('Change')

class TagChangeForm(FlaskForm):
    tag = StringField('Tag', [validators.Length(max=50), validators.DataRequired()])
    tag_id = StringField('Image', [validators.Length(max=50), validators.DataRequired()])
    submit = SubmitField('Change')

class LibraryChangeForm(FlaskForm):
    library_name = StringField('Library_name', [validators.Length(max=50), validators.DataRequired()])
    library_id = StringField('library_id', [validators.Length(max=50), validators.DataRequired()])
    submit = SubmitField('Change')