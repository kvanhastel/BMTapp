from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField
from wtforms.validators import ValidationError, DataRequired, EqualTo, InputRequired
from app.models import Gebruiker, Ploeg, Speler
from app import Config, db


class LoginForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired(message="Geen gebruikersnaam opgegeven")])
    password = PasswordField('Paswoord', validators=[DataRequired(message="Geen paswoord opgegeven")])
    remember_me = BooleanField('Onthoud')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired(message="Geen gebruikersnaam opgegeven")])
    name = StringField('Naam', validators=[DataRequired(message="Geen naam opgegeven")])
    password = PasswordField('Paswoord', validators=[DataRequired(message="Geen paswoord opgegeven")])
    password2 = PasswordField(
        'Herhaal Paswoord', validators=[DataRequired(message="Geen paswoord controle opgegeven"),
                                        EqualTo('password', message="Wachtwoorden zijn niet hetzelfde")])
    rechten = RadioField('Rechten', choices=[('administrator','Administrator'),('werkgroep','Werkgroep'),('ploegkapitein','Ploegkapitein')],
                         validators=[InputRequired(message="Geen keuze gemaakt")])
    submit = SubmitField('Maak gebruiker aan')

    def validate_username(self, username):
        user = Gebruiker.query.filter_by(gebruikersnaam=username.data).first()
        if user is not None:
            raise ValidationError('Gebruikersnaam al in gebruik. Kies een andere gebruikersnaam.')


class DatabaseForm(FlaskForm):
    VBL_login = StringField('Gebruikersnaam', validators=[DataRequired(message="Geen gebruikersnaam opgegeven")])
    VBL_paswoord = PasswordField('Paswoord', validators=[DataRequired(message="Geen paswoord opgegeven")])
    submit = SubmitField('Update Database')


class TerugbetalingsForm(FlaskForm):
    lijst_ziekenfonds  = Config.ZIEKENFONDSEN
    speler_voornaam = StringField('Voornaam', validators=[DataRequired(message="Geen voornaam opgegeven")])
    speler_familienaam = StringField('Familienaam', validators=[DataRequired(message="Geen familienaam opgegeven")])
    ziekenfonds = SelectField('Ziekenfonds', choices=lijst_ziekenfonds,
                                  validators=[InputRequired(message="Geen ziekenfonds opgegeven")])
    submit = SubmitField('Download Formulier')

class BasisloegenForm(FlaskForm):

    # lijst samenstellen ploegen
    lijst_ploegen = []
    query_ploegen = Ploeg.query.all()
    i = 1
    for ploeg in query_ploegen:
        lijst_ploegen.append((str(i), ploeg.ploegnaam))
        i = i+1

    # lijst samenstellen seizoenen + extra seizoen toevoegen
    lijst_seizoenen = []
    query_seizoenen = db.session.query(Ploeg.seizoen).distinct().all()
    i = 1
    for seizoen in query_seizoenen:
        lijst_seizoenen.append((str(i), seizoen[0]))
        i = i+1

    lijst_spelers = []
    query_spelers = Speler.query.all()
    i = 1
    for speler in query_spelers:
        lijst_spelers.append((str(i), Speler.__repr__(speler)[1]))
        i = i+1

    nieuw_seizoen = '19-20'

    lijst_competities = Config.COMPETITIES

    keuze_seizoen = StringField('seizoen: ', validators=[InputRequired(message = "Geen seizoen opgegeven")], default=nieuw_seizoen)

    keuze_seizoenen = SelectField('seizoen', choices=lijst_seizoenen,
                                  validators=[InputRequired(message="Geen seizoen opgegeven")])
    keuze_competities = SelectField('competities', choices=lijst_competities,
                                    validators=[InputRequired(message="Geen competitie opgegeven")])
    keuze_ploegen = SelectField('ploegen', choices=lijst_ploegen,
                                validators=[InputRequired(message="Geen ploeg geselecteerd")])
    keuze_speler = SelectField('speler', choices=lijst_spelers,
                               validators=[InputRequired(message="Geen ploeg geselecteerd")])
    '''
    seizoenen = StringField('ploegnaam', validators=[DataRequired(message="Geen seizoen opgegeven")])
    ploegnaam = StringField('ploegnaam', validators=[DataRequired(message="Geen ploegnaam opgegeven")])
    basisspeler1 = StringField('speler1', validators=[DataRequired(message="Geen basisspeler opgegeven")])
    basisspeler2 = StringField('speler2', validators=[DataRequired(message="Geen basisspeler opgegeven")])
    basisspeler3 = StringField('speler3', validators=[DataRequired(message="Geen basisspeler opgegeven")])
    basisspeler4 = StringField('speler4', validators=[DataRequired(message="Geen basisspeler opgegeven")])
    '''
'''
class PloegopstellingForm(FlaskForm):

'''