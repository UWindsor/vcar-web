import smtplib
import os

from models.auth_token_db import AuthDB
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def saveCredentialToDB(database_session, email):
    
    if __checkIfCredentialsExist(email, database_session):
        database_session.updateDataEntry()
    else: 
        database_session.insertToDatabase()
    

def __checkIfCredentialsExist(email, database_session):
    
    if database_session.searchByEmail(email):
        return True
    else:
        return False

# Sender email address must have 3rd party applications to send it 
def sendEmail(gathered_information, sender_email, sender_pass):
    
    email_message = MIMEMultipart()
    email_message['Subject'] = f'Registered account token for VCAR'
    email_message['From'] = sender_email
    email_message['To'] = gathered_information.email

    mail_content = "Your token is: " + str(gathered_information.token)

    email_message.attach(MIMEText(mail_content, 'plain'))

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_email, sender_pass)
    text = email_message.as_string()
    session.sendmail(sender_email, gathered_information.email, text)
    session.quit()

def pipeToVCar(gathered_information):
    
    to_emb_fifo = "/tmp/rest-emp"
    from_emb_fifo = "/tmp/emb-rest"

