from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import PlainTextResponse
from models.auth_token import AuthToken
from services.function_helper import sendEmail, pipeToVCar


vcar = FastAPI()
# TODO set up verification for jsons that do not match
# TODO set up logging
#TODO set up error when email that does not exists protection

@vcar.post("/api/v1/register", status_code=status.HTTP_201_CREATED)
async def register(gathered_information: AuthToken):
    #save the credentials in the sqlite database
    gathered_information.saveCredentials()
    
    pipeToVCar(gathered_information)

    #TODO temporary, TAKE FROM ENCRRYPTED FILE
    sender_email = "testingemailforschool@gmail.com"
    sender_pass = "12!3456Abcdef"

    #sends token to the embedded 
    sendEmail(gathered_information, sender_email, sender_pass)

#to validate the json being received
@vcar.exception_handler(RequestValidationError)
async def requestValidationExceptionHandler(request, exc):
    return PlainTextResponse("Does not match!", status_code=400)

#to check for http exceptions
@vcar.exception_handler(HTTPException)
async def httpExceptionHandler(request, exc):
    return PlainTextResponse("Error in HTTP", status_code=500)
