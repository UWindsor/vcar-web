import base64
import hashlib
import uuid

from services.function_helper import saveCredentialToDB
from .auth_token_db import AuthDB
from typing import Optional
from pydantic import BaseModel

class AuthToken(BaseModel):
    
    email: str
    password: str
    token: Optional[str] = None
    number_of_vehicles: Optional[int] = 0

    def generateToken(self):
        self.token = str(uuid.uuid4())
        return self.token

    def saveCredentials(self):
        
        self.generateToken()
        
        database_session = AuthDB(self.email, self.password, self.token, self.number_of_vehicles)
        saveCredentialToDB(database_session, self.email) 
