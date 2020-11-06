import smtplib
import os
import pydantic
import requests
import datetime

from models.auth_token_db import AuthDB
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

BASE_URL = "http://localhost:7998/"

def saveCredentialToDB(database_session, email):
    
    if checkIfCredentialsExist(email, database_session):
        database_session.updateDataEntry()
    else: 
        database_session.insertToDatabase()
    

def checkIfCredentialsExist(email, database_session):
    
    if database_session.searchByEmail(email):
        return True
    else:
        return False

# Sender email address must have 3rd party applications to send it 
def sendTokenEmail(gathered_information, sender_email, sender_pass):
        
    try:
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
    except Exception as e:
        logError(e)

def sendVIDEmail(gathered_information, sender_email, sender_pass):
        
    try:
        email_message = MIMEMultipart()
        email_message['Subject'] = f'Registered account token for VCAR'
        email_message['From'] = sender_email
        email_message['To'] = gathered_information.email

        mail_content = "Your vehicle ID is: " + str(gathered_information.vid)

        email_message.attach(MIMEText(mail_content, 'plain'))

        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_email, sender_pass)
        text = email_message.as_string()
        session.sendmail(sender_email, gathered_information.email, text)
        session.quit()
    except Exception as e:
        logError(e)

def getFromVCar(endpoint):
    try:
        response = requests.get(url=(BASE_URL+endpoint))
        return response
    
    except requests.exceptions.RequestException as e:
        logError(e)

    return 500


def sendToVCar(gathered_information, endpoint):

    try:
        response = requests.post(url=(BASE_URL+endpoint), json=gathered_information.json())
        
    except requests.exceptions.RequestException as e:
        logError(e)

def updateVCar(gathered_information, endpoint):

    try:
        response = requests.post(url=(BASE_URL+endpoint), json=gathered_information.json())
        
    except requests.exceptions.RequestException as e:
        logError(e)

def deleteUserFunction(endpoint):
    try:
        response = requests.delete(endpoint)
    except requests.exceptions.RequestExceptions as e:
        logError(e)

def logError(string_val):
    if not os.path.exists("logging"):
        os.system("mkdir logging")
    
    print("Error!: " + str(string_val))

    filename = "logging/" + str(datetime.datetime.now()) + ".txt"
    fd = open(filename, "w")
    fd.write(str(string_val))
