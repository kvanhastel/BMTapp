from flask import Flask, render_template, json, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import TerugbetalingsForm, LoginForm, BasisloegenForm, DatabaseForm, RegistrationForm
from app.models import Gebruiker, Speler
from app.ziekenfonds import maak_document_ziekenfonds
import time, datetime
from werkzeug.urls import url_parse
from sqlalchemy import or_, and_
from functools import wraps
from app import db, importeerdata

import os

from . import app

basedir = os.path.abspath(os.path.dirname(__file__))

def login_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.rechten != "administrator":
            flash('geen rechten tot deze pagina', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
 

def login_werkgroep_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.rechten != "werkgroep" and current_user.rechten != "administrator":
            flash('geen rechten tot deze pagina', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def login_ploegkapitein_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('geen rechten tot deze pagina', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/terugbetalingsformulier', methods=['GET','POST'])
def terugbetalingsformulier():
    #return render_template('terugbetalingsformulier.html')
    terugbetaling_form = TerugbetalingsForm()

    # controle of download knop ingedrukt wordt
    if terugbetaling_form.validate_on_submit():
        # selecteer juiste speler aan de hand van ingevuld formulier
        selected_speler = Speler.query.filter(and_(Speler.firstname.ilike(terugbetaling_form.speler_voornaam.data),
                                                   Speler.lastname.ilike(terugbetaling_form.speler_familienaam.data))).first()
        # als de speler bestaat in database...
        if selected_speler is not None:
            if int(datetime.datetime.now().strftime("%m"))< 8:
                inschrijfdag = datetime.datetime(int(time.strftime("%Y"))-1, 8, 1)
            else:
                inschrijfdag = datetime.datetime(int(time.strftime("%Y")), 8, 1)
            # als de speler dit seizoen nog niet betaald heeft
            if selected_speler.datum_betaling < inschrijfdag:
                flash('Je betaling voor dit seizoen is nog niet geregistreerd', 'danger')
                return redirect(url_for('terugbetalingsformulier'))
            # als de speler dit seizoen betaald heeft
            if selected_speler.datum_betaling >= inschrijfdag:
                maak_document_ziekenfonds(selected_speler, terugbetaling_form.ziekenfonds.data)
                flash('Document aangemaakt', 'success')
                return redirect(url_for('downloadformulier')) # extra variabele speler meegeven en javascript plaatsen in downloadformulier
        # als de speler niet in database zit
        else:
            flash('Je bent geen lid of je hebt je naam verkeerd ingegeven', 'danger')
            return redirect(url_for('terugbetalingsformulier'))
    return render_template('terugbetalingsformulier.html', terugbetaling_form=terugbetaling_form)

@app.route('/downloadformulier')
def downloadformulier():
    return render_template('downloadformulier.html')

@app.route('/ploegopstellingsformulier')
#@login_ploegkapitein_required
def ploegopstellingsformulier():
    return render_template('ploegopstellingsformulier.html')

@app.route('/reservespelers')
#@login_ploegkapitein_required
def reservespelers():
    return render_template('reservespelers.html')

@app.route('/basisploegen')
#@login_werkgroep_required
@login_admin_required
def basisploegen():
    aanmaak_basisploegen_form = BasisloegenForm()
    basisploegen_form = BasisloegenForm()
    return render_template('basisploegen.html', basisploegen_form=basisploegen_form, aanmaak_basisploegen_form=aanmaak_basisploegen_form)

@app.route('/spelerslijst')
#@login_ploegkapitein_required
@login_admin_required
def spelerslijst():
    #spelers = Speler.query.all()
    # filter om alleen competitiespelers te selecteren
    spelers = Speler.query.filter(
        (Speler.role =='Speler') | (Speler.role == 'Uitgeleende speler')).filter(or_(Speler.typename == 'Competitiespeler',
                                                                                     Speler.typename == 'Jeugd')).filter(Speler.website == 'http://www.interclub.be').all()
    return render_template('spelerslijst.html', spelers=spelers)

# route voor speler pagina
@app.route('/speler/<string:memberid>/')
#@login_ploegkapitein_required
@login_admin_required
def speler(memberid):
        s = Speler.query.filter_by(memberid=memberid).first()
        return render_template('speler.html', s=s)

@app.route('/administratie', methods=['GET', 'POST'])
@login_admin_required
def administratie():

    database_update_form = DatabaseForm()

    if database_update_form.validate_on_submit():
        VBL_login = database_update_form.VBL_login.data
        VBL_paswoord = database_update_form.VBL_paswoord.data
        importeerdata.importeernaardatabase(VBL_login, VBL_paswoord)
        flash('Update database succesvol', 'success')
        return redirect(url_for('administratie'))
    return render_template('administratie.html', title='Administratie', database_update_form=database_update_form)

@app.route('/over')
def over():
    return render_template('over.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/test')
def test():
    naam = { "voornaam": "Koen", "familienaam": "Vanhastel"}
    return json.dumps(naam)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        gebruiker = Gebruiker.query.filter_by(gebruikersnaam=form.username.data).first()
        if gebruiker is None or not gebruiker.check_password(form.password.data):
            flash('Verkeerde gebruikersnaam of paswoord', 'danger')
            return redirect(url_for('login'))
        login_user(gebruiker, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Log in', form=form)


# route voor log out website
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))