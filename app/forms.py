from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class ArmiesQuantity(Form):
    quantity = StringField('quantity', validators=[DataRequired()])
