from app import app
from flask import render_template, redirect, flash
from forms import ArmiesQuantity


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = ArmiesQuantity()
    if form.validate_on_submit():
        flash('Armies quantity="' + form.quantity.data)
        return redirect('/form')
    return render_template('index.html',
                           form=form)
