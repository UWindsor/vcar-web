# VCAR REST API 

Rest API that will be used as a means of authentication and communication between the user and the embedded system

## How to run it

Either run the file given in vcar-web/

> ./run

or run the following command with any port number you want

> uvicorn vcar:main --reload --port 7999

For quality of life, the default port on the file "run" is 7999 

## Endpoints and what they do
### /api/v1/register

    This endpoint accept POST requests with a JSON that includes the email, password, and option token and number of vehicles. 
  
Note: The optional fields are not being sent in, the request looks like:

{
    "email":"",
    "password": 
}

This endpoint will send an email to the email in the request with a token that is used to gain access to vcars.

### /api/v1/vehicles

    This endpoint will accept a POST request and be used to register a new vehicle on the server. Each email is limited to 5 vcars.

### /api/v1/vehicles/{id}
    
    This endpoint will accept a GET request and fetch the state of the vehicle

### /api/v1/vehicles/{vid}
    
    This endpoint will send a message to the vehicle.

NOTE::

Credential file must be placed in services for the program to function
