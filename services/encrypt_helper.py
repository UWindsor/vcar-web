import os

from cryptography.fernet import Fernet

FILE_PATH = os.path.dirname(os.path.abspath(__file__))

def load_key():
    return open(os.path.join(FILE_PATH, "credentials/secret.key"), "rb").read()

def load_email(): 
    return open(os.path.join(FILE_PATH, "credentials/email.txt"), "rb").read()

def load_pass():
    return open(os.path.join(FILE_PATH, "credentials/pass.txt"), "rb").read()

def decrypt_creds():
    key = load_key()
    f = Fernet(key)
    
    email = f.decrypt(load_email())
    password = f.decrypt(load_pass())

    decrypt_message = dict({"email": email.decode() , "password": password.decode()})

    return decrypt_message
