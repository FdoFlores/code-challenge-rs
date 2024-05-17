# To run the api locally:
## Create venv
    python -m venv venv
## Activate the venv (windows)
    ./venv/Scripts/Activate.ps1
## install project requirements
    pip install -r requirements.txt
## go to the django project
    cd reservamos
## run the server
    python manage.py runserver

# test the endpoint:
    http://127.0.0.1:8000/api/{city_name}

# IMPORTANT
## The api that returns the coordinates fails randomly so it will return an error frequently all you have to do is test the endpoint again