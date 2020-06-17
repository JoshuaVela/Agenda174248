from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Usuario:", validators=[DataRequired()])
    password = PasswordField("Contraseña:", validators=[DataRequired()])
    remember_me = BooleanField("Recordar Usuario")
    submit = SubmitField("Iniciar Sesion")

class SignUpForm(FlaskForm):
    username = StringField("Usuario:", validators=[DataRequired()])
    password = PasswordField("Contraseña:", validators=[DataRequired()])
    email = StringField("Correo: ", validators=[DataRequired()])
    submit = SubmitField("Iniciar Sesion")

class PostForm(FlaskForm):
    first_name = StringField("Nombre: ", validators=[DataRequired()])
    last_name = StringField("Apellidos: ", validators=[DataRequired()])
    phone = IntegerField("Numero: ", validators=[DataRequired()])
    email = StringField("Correo: ", validators=[DataRequired()])
    note = StringField("body", validators=[DataRequired()])
    submit = SubmitField("Registrar")