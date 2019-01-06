from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class Gebruiker (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(64), index=True, unique=True)
    gebruikersnaam = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    rechten = db.Column(db.String(64))

    def __repr__(self):
        return '<Gebruiker {}>',format(self.gebruikersnaam)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_rechten(self,rechten):
        if rechten is "administrator":
            self.rechten = "administrator"
        if rechten is "werkgroep":
            self.rechten = "werkgroep"
        if rechten is "ploegkapitein":
            self.rechten = "ploegkapitein"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        if self.rechten == 'administrator':
            return True


    @login.user_loader
    def load_user(id):
        return Gebruiker.query.get(int(id))


class Speler (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupcode = db.Column(db.String(128), index=True)
    groupname = db.Column(db.String(64), index=True)
    code = db.Column(db.String(128), index=True)
    memberid = db.Column(db.Integer, index=True)
    lastname = db.Column(db.String(64), index=True)
    lastname2 = db.Column(db.String(64), index=True)
    middlename = db.Column(db.String(64), index=True)
    firstname = db.Column(db.String(64), index=True)
    address = db.Column(db.String(128), index=True)
    address2 = db.Column(db.String(128), index=True)
    address3 = db.Column(db.String(128), index=True)
    postalcode = db.Column(db.String(16), index=True)
    city = db.Column(db.String(64), index=True)
    state = db.Column(db.String(64), index=True)
    country = db.Column(db.String(64), index=True)
    gender = db.Column(db.String(64), index=True)
    dob = db.Column(db.DateTime, index=True)
    phone = db.Column(db.String(64), index=True)
    phone2 = db.Column(db.String(64), index=True)
    mobile = db.Column(db.String(64), index=True)
    fax = db.Column(db.String(64), index=True)
    fax2 = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True)
    website = db.Column(db.String(128), index=True)
    categoryname = db.Column(db.String(64), index=True)
    startdate = db.Column(db.DateTime, index=True)
    endate = db.Column(db.DateTime, index=True)
    role = db.Column(db.String(64), index=True)
    playerlevelsingle = db.Column(db.String(2), index=True)
    playerleveldouble = db.Column(db.String(2), index=True)
    playerlevelmixed = db.Column(db.String(2), index=True)
    #playerlevelsinglebase = db.Column(db.String(2), index=True)
    #playerleveldoublebase = db.Column(db.String(2), index=True)
    #playerlevelmixedbase = db.Column(db.String(2), index=True)
    typename = db.Column(db.String(64), index=True)
    geen_badminton_magazine = db.Column(db.Boolean)
    handicap = db.Column(db.Boolean)
    nieuwsbrief = db.Column(db.Boolean)
    partners = db.Column(db.Boolean)
    betaald = db.Column(db.Boolean, index=True)
    betaald_bedrag = db.Column(db.Integer, index=True)
    datum_betaling = db.Column(db.DateTime)
    email_vader = db.Column(db.String(64))
    email_moeder = db.Column(db.String(64))
    gsm_vader = db.Column(db.String(64))
    gsm_moeder = db.Column(db.String(64))
    kyu = db.Column(db.String(64))
    kyu_gaat_in_op = db.Column(db.DateTime)
    verwittiging = db.Column(db.Boolean)
    po_id_votas = db.Column(db.String(128))

    kapitein = db.Column(db.Boolean, index=True)
    wedstrijdleider = db.Column(db.Boolean, index=True)

    def __repr__(self):
        return '<Speler {}>', format(self.firstname + ' ' + self.lastname)

    def speelt_interclub(self):
        if self.website == 'http://www.interclub.be':
            return 'Ja'
        else:
            return 'Nee'

    def naam(self):
        return self.firstname + ' ' + self.lastname


speler_ploeg = db.Table('speler_ploeg',
        db.Column('speler_id', db.Integer, db.ForeignKey('speler.id'), primary_key=True),
        db.Column('ploeg_id', db.Integer, db.ForeignKey('ploeg.id'), primary_key=True)
)

class Ploeg (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seizoen = db.Column(db.String(32), index=True)
    competitie = db.Column(db.String(32), index=True)
    ploegnaam = db.Column(db.String(64), index=True)
    afdeling = db.Column(db.String(64), index=True)

    #code voor many to many relationship

    spelers = db.relationship(
        'Speler', secondary=speler_ploeg,
        backref='ploegen', lazy='dynamic')


    def __repr__(self):
        return '<Ploeg {}>',format(self.ploegnaam)
