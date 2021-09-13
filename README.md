# Task
# Django Rest Framework -UserRegistration-Authentication
Django app to register and authenticate user using Rest Framework

# how to use:
    --python manage.py
    --if port 8000 not connected try python manage.py runserver <port number>

# URLS to target
  ---to register a user
    --http://127.0.0.1:8080/api/session/register/
  --to login a user
    --http://127.0.0.1:8080/api/session/login/
  --to logout a user
    --http://127.0.0.1:8080/api/session/logout/
  --to get data
   --http://127.0.0.1:8080/api/session/data/
  
# token is generated using jwt package

#  Useful commands:
   --python manage.py makemigrations
   --python manage.py migrate
