import base64
import hashlib
import uuid
import requests
import json

from typing import Optional
from services.function_helper import checkIfCredentialsExist
from .auth_token_db import AuthDB
from pydantic import BaseModel

class CanMessage(BaseModel):
    email: str
    token: str
    vid: Optional[str] = None
    can_message: dict = {}
     
    def authenticateUser(self):
        new_email = str(hashlib.sha224(self.email.encode('utf-8')).hexdigest())
        
        database_session = AuthDB()
        database_session.secondaryConstructor(new_email, self.token)

        if checkIfCredentialsExist(new_email, database_session):
            return True
        else:
            return False

