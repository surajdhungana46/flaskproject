from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES
from wtforms import StringField,PasswordField,SubmitField,BooleanField ,HiddenField,IntegerField,TextAreaField,SelectField
from classflask.model import User
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError


class  RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(),Length(min=4,max=20)])
    email = StringField(label='Email', validators=[DataRequired(),Email()])
    password = PasswordField(label='New Password',  validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
class LoginForm(FlaskForm):
    email = StringField(label='Email',validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField(label='Login')
class AddProduct(FlaskForm):
    name = StringField('Name')
    price = IntegerField('Price')
    description = TextAreaField('Description')
    image = FileField('Image', validators=[FileAllowed(IMAGES, 'Only images are accepted.')])
class AddToCart(FlaskForm):
    quantity = IntegerField('Quantity')
    id = HiddenField('ID')

class Checkout(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone_number = StringField('Number')
    email = StringField('Email')
    address = StringField('Address')
    city = StringField('City')
    state = SelectField('State', choices=[('Bagmati', 'Kathmandu'), ('Gandaki', 'Pokhara'), ('koshi', 'Ithari')])
    payment_type = SelectField('Payment Type', choices=[('COD', 'Cash on Delivery'), ('OP', 'online Payment')])

