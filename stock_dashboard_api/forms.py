from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class EmailForm(FlaskForm):
    sender = StringField('From:', validators=[DataRequired()])
    recipient = StringField('To:', validators=[DataRequired(), Email()])
    submit = SubmitField('Send!')
