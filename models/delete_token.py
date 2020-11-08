import base64
import hashlib
import uuid
import requests

from services.function_helper import checkIfCredentialsExist,  deleteUserFunction
from .auth_token_db import AuthDB
from typing import Optional
from pydantic import BaseModel

class DeleteToken(BaseModel):
    
    email: str
    token: str
    vid: str
    number_of_vehicles: Optional[int] = 0

    def authenticateUser(self):
        hashed_email = str(hashlib.sha224(self.email.encode('utf-8')).hexdigest())

        database_session = AuthDB()
        database_session.secondaryConstructor(hashed_email, database_session)

        if checkIfCredentialsExist(hashed_email, database_session):
            if self.deleteUser(database_session):
                return True
            else:
                return False
        else:
            return False

    def deleteUser(self, database_session):
        if deleteUserFunction("/embedded/v1/vehicles/"+self.vid):                
            for x in vnum:
                num = x[0] - 1

                if num < 0:
                    print("Error! No vehicle to delete!")
                    return False
                else:
                    database_session.updateVehicleNumber(int(num))
                    return True
            else:
                return False

