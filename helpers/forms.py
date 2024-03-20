from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import InputRequired, ValidationError


# La clase LoginForm permanece igual
class LoginForm(FlaskForm):
    name = StringField(label="User Name:", validators=[InputRequired()])
    password = PasswordField(label="Password:", validators=[InputRequired()])
    submit = SubmitField(label="Sign in")


# Actualizaciones en la clase GameForm
class GameForm(FlaskForm):
    game_name = StringField(label="Game Name:", validators=[InputRequired()])
    genre = StringField(label="Genre:", validators=[InputRequired()])
    price = FloatField(label="Price:", validators=[InputRequired(message="This field cannot be empty.")])
    submit = SubmitField(label="Create Game")

    # Añadido un validador personalizado para el campo price
    def validate_price(form, field):
        if field.data is not None:
            try:
                float(field.data)
            except ValueError:
                raise ValidationError("Please enter a valid number for the price.")
