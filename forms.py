from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, URL, Length


class NewCafeForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    map_url = StringField(label='Map URL', validators=[DataRequired(), URL()])
    img_url = StringField(label='Image URL', validators=[DataRequired(), URL()])
    location = StringField(label='Location', validators=[DataRequired()])
    has_sockets = BooleanField(label='Has sockets for laptop charging?', validators=[DataRequired()])
    has_toilet = BooleanField(label='Has toilet?', validators=[DataRequired()])
    has_wifi = BooleanField(label='Has Wi-Fi?', validators=[DataRequired()])
    seats = IntegerField(label='Number of seats', validators=[DataRequired(), Length(min=1)])
    submit = SubmitField('Register this Cafe')
