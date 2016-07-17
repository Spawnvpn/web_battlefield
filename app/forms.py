from flask.ext.wtf import Form
from wtforms import StringField
from wtforms import validators


class ArmiesQuantity(Form):
    quantity = StringField('quantity', validators=[validators.InputRequired])
