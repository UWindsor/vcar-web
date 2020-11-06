import json

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import PlainTextResponse
from models.auth_token import AuthToken
from models.delete_token import DeleteToken
from models.vehicle_request import VehicleRequest
from models.can_message import CanMessage
from services.function_helper import sendVIDEmail, sendTokenEmail, getFromVCar, sendToVCar, updateVCar, logError
from services.encrypt_helper import decrypt_creds


vcar = FastAPI()

@vcar.post("/api/v1/register", status_code=status.HTTP_201_CREATED)
async def register(gathered_information: AuthToken):
    #save the credentials in the sqlite database
    gathered_information.saveCredentials()
    sendToVCar(gathered_information, "embedded/v1/register")
   
    cred_dict = decrypt_creds()
    sender_email = cred_dict["email"]
    sender_pass = cred_dict["password"]

    #sends token to the embedded 
    sendTokenEmail(gathered_information, sender_email, sender_pass)

@vcar.post("/api/v1/vehicles", status_code=status.HTTP_201_CREATED)
async def createVehicles(gathered_information: VehicleRequest):
    if gathered_information.authenticateUser():
        sendToVCar(gathered_information, "embedded/v1/vehicles")
    
        cred_dict = decrypt_creds()
        sender_email = cred_dict["email"]
        sender_pass = cred_dict["password"]

        sendVIDEmail(gathered_information, sender_email, sender_pass) 
    else:
        logError("User does not exist!")

@vcar.get("/api/v1/vehicles/{vid}", status_code=200)
async def getVehicleStatus(vid: str):
    return getFromVCar("/embedded/v1/vehicles/"+str(vid))

@vcar.put("/api/v1/vehicles/{vid}", status_code=200)
async def updateVehicleStatus(vid:str, message: CanMessage):
        
    if message.authenticateUser():
        updateVCar(gathered_information=message, endpoint="/embedded/v1/vehicles/"+str(vid))   
    else:
        logError("User does not exist!")

@vcar.delete("/api/v1/vehicles/{vid}")
async def deleteVehicle(vid: str, credential: DeleteToken):
    if credential.authenticateUser():
       return 200
    else:
        return 400

#to validate the json being received
@vcar.exception_handler(RequestValidationError)
async def requestValidationExceptionHandler(request, exc):
    logError("Request JSON does not match endpoint!")
    return PlainTextResponse("Does not match!", status_code=400)

#to check for http exceptions
@vcar.exception_handler(HTTPException)
async def httpExceptionHandler(request, exc):
    logError("Error in HTTP or connections!")
    return PlainTextResponse("Error in HTTP", status_code=500)
