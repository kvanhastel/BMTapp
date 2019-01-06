from datetime import datetime
from app import db,Config
from app.models import Speler
import requests
from bs4 import BeautifulSoup


def importeernaardatabase(VBL_login, VBL_paswoord):

    def data_naar_datum(data):
        if data != '':
            return datetime.strptime(data, '%d-%m-%Y')
    def data_naar_bool(data):
        if data == ('False' or ''):
            return 0
        if data == 'True':
            return 1

    def find_between(s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    with requests.Session() as sessie:
        login_url = "https://www.badmintonvlaanderen.be/member/login.aspx"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

        sessie.headers.update(headers)
        login_sessie = sessie.get(login_url)
        soup = BeautifulSoup(login_sessie.content, "lxml")

        EVENTTARGET = ""
        EVENTARGUMENT = ""
        VIEWSTATE = soup.find(id="__VIEWSTATE")['value']
        VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value']
        EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")['value']

        login_data = {
            "__EVENTTARGET": EVENTTARGET,
            "__EVENTARGUMENT": EVENTARGUMENT,
            "__VIEWSTATE": VIEWSTATE,
            "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
            "__EVENTVALIDATION": EVENTVALIDATION,
            "ctl01$ctl01$container$content$ctl00$cphPage$cphPage$pnlLogin$UserName": VBL_login,
            "ctl01$ctl01$container$content$ctl00$cphPage$cphPage$pnlLogin$Password": VBL_paswoord,
            "ctl01$ctl01$container$content$ctl00$cphPage$cphPage$pnlLogin$LoginButton": "Inloggen"}

        login_site = sessie.post(login_url, data=login_data)
        login_site_data = BeautifulSoup(login_site.content, "lxml")
        id = find_between(str(login_site_data), r'group.aspx?id=', r'&amp;gid')
        gid = find_between(str(login_site_data), r'&amp;gid=', r'&amp;p=3')
    xlsx_param = 'glid=0'
    csv_param = 'ft=1'
    leden = 'export_memberperrolepergroup.aspx'
    data_url = "https://badmintonvlaanderen.toernooi.nl/organization/export/" + leden + "?id=" + id + "&gid=" + gid + '&' + csv_param + "&" + xlsx_param
    data_site = sessie.get(data_url, data=login_data)
    spelersgegevens = [line.decode('utf-8') for line in data_site.iter_lines()]
    # eerste en laatste regel weghalen
    spelersgegevens.pop(0)

    # oude gegevens verwijderen
    Speler.query.delete()
    #database vullen met nieuwe gegevens
    for rij in spelersgegevens:
        spelerinfo = [x.strip() for x in rij.split(';')]
        if spelerinfo[0] != "":
            speler = Speler(
                groupcode=spelerinfo[0],
                groupname=spelerinfo[1],
                code=spelerinfo[2],
                memberid=spelerinfo[3],
                lastname=spelerinfo[4],
                lastname2=spelerinfo[5],
                middlename=spelerinfo[6],
                firstname=spelerinfo[7],
                address=spelerinfo[8],
                address2=spelerinfo[9],
                address3=spelerinfo[10],
                postalcode=spelerinfo[11],
                city=spelerinfo[12],
                state=spelerinfo[13],
                country=spelerinfo[14],
                gender=spelerinfo[15],
                dob=data_naar_datum(spelerinfo[16]),
                phone=spelerinfo[17],
                phone2=spelerinfo[18],
                mobile=spelerinfo[19],
                fax=spelerinfo[20],
                fax2=spelerinfo[21],
                email=spelerinfo[22],
                website=spelerinfo[23],
                categoryname=spelerinfo[24],
                startdate=data_naar_datum(spelerinfo[25]),
                endate=data_naar_datum(spelerinfo[26]),
                role=spelerinfo[27],
                playerlevelsingle=spelerinfo[28],
                playerleveldouble=spelerinfo[29],
                playerlevelmixed=spelerinfo[30],
                typename=spelerinfo[31],
                geen_badminton_magazine=data_naar_bool(spelerinfo[32]),
                handicap=data_naar_bool(spelerinfo[33]),
                nieuwsbrief=data_naar_bool(spelerinfo[34]),
                partners=data_naar_bool(spelerinfo[35]),
                betaald=data_naar_bool(spelerinfo[36]),
                betaald_bedrag=spelerinfo[37],
                datum_betaling=data_naar_datum(spelerinfo[38]),
                email_vader=spelerinfo[39],
                email_moeder=spelerinfo[40],
                gsm_vader=spelerinfo[41],
                gsm_moeder=spelerinfo[42],
                kyu=spelerinfo[43],
                kyu_gaat_in_op=data_naar_datum(spelerinfo[44]),
                verwittiging=data_naar_bool(spelerinfo[45]),
                po_id_votas=spelerinfo[46]
            )
        db.session.add(speler) #record in database plaatsen
    db.session.commit() #database schrijven