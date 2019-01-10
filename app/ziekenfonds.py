from app import db,Config
from app.models import Speler
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import os
import time, datetime
import webbrowser
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from flask import flash, send_file


def maak_document_ziekenfonds(speler, ziekenfonds):

    basedir = os.path.abspath(os.path.dirname(__file__))
    packet = io.BytesIO()
    can = canvas.Canvas(packet)

    #pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    #can.setFont('Arial', 10)
    speler_straat = speler.address
    if "bus " in speler.address:
        speler_bus = speler.address.split(" bus ", 1)[1]
        speler_huisnummer = speler.address.split(" bus ", 1)[0].rsplit(' ', 1)[1]
        speler_straat = speler.address.split(" bus ", 1)[0].rsplit(' ', 1)[0]
    else:
        speler_bus = ""
        speler_huisnummer = speler.address.rsplit(' ', 1)[1]
        speler_straat = speler.address.rsplit(' ', 1)[0]

    vandaag_dag = time.strftime("%d")
    vandaag_maand = time.strftime("%m")
    vandaag_jaar = time.strftime("%Y")

    if int(vandaag_maand) > 8:
        seizoen_jaar = vandaag_jaar
    else:
        seizoen_jaar = str(int(vandaag_jaar) - 1)


# formulier invullen
# Als ziekenfonds is CM
    if ziekenfonds == 'CM':
        existing_pdf = PdfFileReader(open(basedir + "/templates/formulieren/Form_CM.pdf", "rb"))
        can.drawString(90, 681, speler.lastname)
        can.drawString(350, 681, speler.firstname)
        can.drawString(90, 663, speler_straat)
        can.drawString(320, 663, speler_huisnummer)
        can.drawString(408, 663, speler_bus)
        can.drawString(97, 645, speler.postalcode)
        can.drawString(195, 645, speler.city)
        can.drawString(380, 645, speler.country)
        can.drawString(85, 627, speler.mobile)
        can.drawString(250, 627, speler.email)
        can.drawString(160, 562, "Badmintonclub Tielt")
        can.drawString(90, 544, "Sneppe 44, 8540 Deerlijk")
        can.drawString(185, 526, "koen.vanhastel@gmail.com")
        can.drawString(240, 508, "01/09/" + seizoen_jaar + " - 31/08/" + str(int(seizoen_jaar)+1))
        can.drawString(130, 491, "€ " + str(speler.betaald_bedrag))
        can.drawString(130, 473, speler.datum_betaling.strftime("%d/%m/%Y"))
        can.drawString(56, 430, "X")
        can.drawString(250, 395, "Badminton")
        can.drawString(205, 378, "Badminton Vlaanderen")
        can.drawString(90, 319, vandaag_dag[0])
        can.drawString(104, 319, vandaag_dag[1])
        can.drawString(128, 319, vandaag_maand[0])
        can.drawString(141, 319, vandaag_maand[1])
        can.drawString(165, 319, vandaag_jaar[0])
        can.drawString(179, 319, vandaag_jaar[1])
        can.drawString(192, 319, vandaag_jaar[2])
        can.drawString(206, 319, vandaag_jaar[3])
        can.save()

    # Als ziekenfonds is LM
    if ziekenfonds == 'LM':
        existing_pdf = PdfFileReader(open(basedir + "/templates/formulieren/Form_LM.pdf", "rb"))
        can.drawString(132, 653, speler.lastname)
        can.drawString(160, 622, speler.firstname)
        can.drawString(160, 591, speler.address)
        can.drawString(160, 565, speler.postalcode + ' ' + speler.city)
        can.drawString(180, 512, speler.email)
        can.drawString(123, 424, "X")
        can.drawString(410, 421, seizoen_jaar + " - " + str(int(seizoen_jaar)+1))
        can.drawString(160, 399, "Badminton")
        can.drawString(195, 197, speler.datum_betaling.strftime("%d/%m/%Y"))
        can.drawString(395, 197, "€ " + str(speler.betaald_bedrag))
        can.drawString(160, 120, time.strftime("%d/%m/%Y"))
        can.save()

    # Als ziekenfonds is VNZ
    if ziekenfonds == 'VNZ':
        existing_pdf = PdfFileReader(open(basedir + "/templates/formulieren/Form_VNZ.pdf", "rb"))
        can.drawString(260, 286, "Koen Vanhastel")
        can.drawString(260, 262, speler.lastname + ' ' + speler.firstname)
        can.drawString(137, 236, "X")
        can.drawString(300, 157, "Badminton")
        can.drawString(141, 135, speler.datum_betaling.strftime("%d")[0])
        can.drawString(155, 135, speler.datum_betaling.strftime("%d")[1])
        can.drawString(169, 135, speler.datum_betaling.strftime("%m")[0])
        can.drawString(183, 135, speler.datum_betaling.strftime("%m")[1])
        can.drawString(240, 135, speler.datum_betaling.strftime("%Y")[3])
        can.drawString(141, 118, "{:06.2f}".format(speler.betaald_bedrag)[0])
        can.drawString(155, 118, "{:06.2f}".format(speler.betaald_bedrag)[1])
        can.drawString(169, 118, "{:06.2f}".format(speler.betaald_bedrag)[2])
        can.drawString(204, 118, "{:06.2f}".format(speler.betaald_bedrag)[4])
        can.drawString(218, 118, "{:06.2f}".format(speler.betaald_bedrag)[5])
        can.drawString(102, 87, vandaag_dag[0])
        can.drawString(116, 87, vandaag_dag[1])
        can.drawString(130, 87, vandaag_maand[0])
        can.drawString(144, 87, vandaag_maand[1])
        can.drawString(201, 87, vandaag_jaar[3])
        can.save()

    # Als ziekenfonds is BM
    if ziekenfonds == 'BM':
        existing_pdf = PdfFileReader(open(basedir + "/templates/formulieren/Form_BM.pdf", "rb"))
        can.drawString(330, 610, speler.lastname + ' ' + speler.firstname)
        can.drawString(59, 464, "X")
        can.drawString(248, 465, "Badminton")
        can.drawString(205, 452, str(speler.betaald_bedrag))
        can.drawString(295, 452, speler.datum_betaling.strftime("%d"))
        can.drawString(315, 452, speler.datum_betaling.strftime("%m"))
        can.drawString(339, 452, speler.datum_betaling.strftime("%Y")[1:])
        can.drawString(82, 424, "X")
        can.drawString(198, 425, "01")
        can.drawString(216, 425, "09")
        can.drawString(240, 425, seizoen_jaar[1:])
        can.drawString(341, 425, "31")
        can.drawString(361, 425, "08")
        can.drawString(383, 425, str(int(seizoen_jaar) + 1)[1:])
        can.drawString(119, 320, time.strftime("%d"))
        can.drawString(139, 320, time.strftime("%m"))
        can.drawString(162, 320, time.strftime("%Y")[1:])
        can.drawString(225, 305, "X")
        can.drawString(230, 260, "Koen Vanhastel")
        can.save()


    # Als ziekenfonds is OZ
    if ziekenfonds == 'OZ':
        existing_pdf = PdfFileReader(open(basedir + "/templates/formulieren/Form_OZ.pdf", "rb"))
        can.drawString(73, 509, "X")
        can.drawString(208, 461, "Badmintonclub Tielt")
        can.drawString(230, 435, "Koen Vanhastel")
        can.drawString(120, 410, "01/09/" + seizoen_jaar + " - 31/08/" + str(int(seizoen_jaar) + 1))
        can.drawString(163, 384, str(speler.betaald_bedrag))
        can.drawString(157, 359, speler.datum_betaling.strftime("%d"))
        can.drawString(174, 359, speler.datum_betaling.strftime("%m"))
        can.drawString(192, 359, speler.datum_betaling.strftime("%Y"))
        can.save()

    # Als ziekenfonds is PAR
    if ziekenfonds == 'PAR':
        existing_pdf = PdfFileReader(open(basedir + "/templates/formulieren/Form_PAR.pdf", "rb"))
        can.drawString(181, 338, "Badmintonclub Tielt")
        can.drawString(195, 313, speler.lastname + ' ' + speler.firstname)
        can.drawString(112, 288, "01/09/" + seizoen_jaar + " - 31/08/" + str(int(seizoen_jaar) + 1))
        can.drawString(135, 263, "Badminton")
        can.drawString(160, 239, "€ " + str(speler.betaald_bedrag))
        can.save()

#move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
# read your existing PDF

    output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
# finally, write "output" to a real file

    outputstream = open(basedir + "/templates/formulieren/Form_filled.pdf", "w+b")
    os.chmod(basedir + "/templates/formulieren/Form_filled.pdf", 0o777)
    output.write(outputstream)
    outputstream.close()

    send_file(basedir + "/templates/formulieren/Form_filled.pdf", as_attachment='pdf', attachment_filename='terugbetalingsformulier.pdf')