from flask_bootstrap import SwitchField
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, URL, Length


class NewCafeForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    map_url = StringField(label='Map URL', validators=[DataRequired(), URL()])
    img_url = StringField(label='Image URL', validators=[DataRequired(), URL()])
    location = StringField(label='Location', validators=[DataRequired()])
    seats = StringField(label='Number of seats (Example: 10-15)', validators=[DataRequired(), Length(min=1)])
    coffee_price = DecimalField(label='Coffee price', validators=[DataRequired()], places=2)
    has_sockets = SwitchField(label='Has sockets for laptop charging?')
    has_wifi = SwitchField(label='Has Wi-Fi?')
    has_toilet = SwitchField(label='Has toilet?')
    can_take_calls = SwitchField(label='Can take calls?')
    submit = SubmitField('Submit')
