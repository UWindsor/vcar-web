import base64
import hashlib
import uuid

from typing import Optional
from services.function_helper import checkIfCredentialsExist
from .auth_token_db import AuthDB
from pydantic import BaseModel

class VehicleRequest(BaseModel):
    email: str
    token: str
    vtype: str
    vid: Optional[str] = None
     
    def generateVID(self):
        self.vid = str(uuid.uuid4())
        return self.vid

    def authenticateUser(self):
        new_email = str(hashlib.sha224(self.email.encode('utf-8')).hexdigest())
        
        database_session = AuthDB()
        database_session.secondaryConstructor(new_email, self.token)

        if checkIfCredentialsExist(new_email, database_session):
            self.generateVID()
            vnum = database_session.getVehicleNumber()
            for x in vnum:
                num = x[0] + 1
            
            if num <= 5:
                database_session.updateVehicleNumber(int(num))
            else:
                self.vid = "Error! Too many vehicles registered! Please delete one before you make another! >:( "

            return True
        else:
            return False
