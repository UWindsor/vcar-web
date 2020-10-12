from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import PlainTextResponse
from models.auth_token import AuthToken
from models.vehicle_request import VehicleRequest
from services.function_helper import sendVIDEmail, sendTokenEmail, sendToVCar, logError
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

@vcar.post("/ap1/v1/vehicles", status_code=status.HTTP_201_CREATED)
async def createVehicles(gathered_information: VehicleRequest):
    if gathered_information.authenticateUser():
        sendToVCar(gathered_information, "embedded/v1/vehicle")
    
        cred_dict = decrypt_creds()
        sender_email = cred_dict["email"]
        sender_pass = cred_dict["password"]

        sendVIDEmail(gathered_information, sender_email, sender_pass) 
    else:
        logError("User does not exist!")

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
