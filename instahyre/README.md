
Steps to run the API
## Install dependencies

pip3 install requirements.txt


## Runserver

python3 manage.py runserver

## Test the API

Route: http://localhost:8000/register/
Request Type: POST
Data:
{
    "username": "example_user",
    "password": "secure_password",
    "email": "user@example.com",
    "phone_number": "1234567890"
}



Route: http://localhost:8000/login/
Request Type: POST
Data: 

  {
    "username": "example_user",
    "password": "secure_password",
    
}


### To view all the contacts

Route: http://localhost:8000/contacts/
Request Type: GET


### To mark a contact as SPAM

Private Route: http://localhost:8000/spam/
Request Type: POST
Data:
    {
        "phone": "9988689856"
    }


### To search a contact by name

Private Route: http://localhost:8000/search_name?name=Somasree
Request Type: GET


### To search a contact by phone

Private Route: http://localhost:8000/search_phone?phone=8887655645
Request Type: GET
