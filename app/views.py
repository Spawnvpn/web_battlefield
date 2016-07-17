from app import app
from flask import session, render_template, redirect, request
from forms import ArmiesQuantity
from app import battle


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    session.clear()
    form = ArmiesQuantity()
    if request.method == 'POST':
        session['army_quantity'] = form.data
        return redirect('/form')
    return render_template('index.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    try:
        session['armies_units']
    except KeyError:
        session['armies_units'] = list()
        session['armies_squads'] = list()
        session['armies_strategy'] = list()

    if request.method == 'POST':
        session['armies_units'].append(request.form['units'])
        session['armies_squads'].append(request.form['squads'])
        session['armies_strategy'].append(request.form['strategy'])
        if len(session['armies_units']) == int(session['army_quantity']['quantity']):
            print(session['armies_units'], session['armies_squads'],
                  session['armies_strategy'])
            go = battle.Battlefield(quan_armies=int(session['army_quantity']['quantity']),
                                    units=session['armies_units'], squads=session['armies_squads'],
                                    strategy=session['armies_strategy'])
            go.start()
            session['winner'] = go.winner
            return '/result'
    return render_template('form.html', quantity=session['army_quantity']['quantity'])


@app.route('/result', methods=['GET', 'POST'])
def result():
    winner = session['winner']
    return render_template("result.html", winner=winner)
