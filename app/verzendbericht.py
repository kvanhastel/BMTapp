from app import app
from flask_mail import Message, Mail


def verzend_bericht(name, email, message):

    mail = Mail()
    mail.init_app(app)
    mail = Mail()
      
    msg = Message(message, sender=email, recipients=['koen.vanhastel@gmail.com'])
    msg.body = """
    Van: %s 
    E-mail: %s
    Bericht: %s
    """ % (name, email, message)
    mail.send(msg)