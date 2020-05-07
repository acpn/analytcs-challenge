# Django + Google Analytics API
This project it's useful to integrate with Google Analytics and retrieve informations from user with a friendly interface.

## Requirements

* Docker containers
    - Windows: https://docs.docker.com/docker-for-windows/install/
    - Ubuntu: https://docs.docker.com/engine/install/ubuntu/ 

* Credentials to use Google Analytics API, pay attention to the described steps.
    - https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py

* Besides credentials, it's necessary which the account has almost one property and one view.

## How to use

* In the root project directory run:
    - docker-compose up --build
    - After finish the build process open's your browser and type the url below:
        - http://localhost:8000/

## System functions

* The system has 5 mainly functions:
    - User signup
    - Login
    - Home page with data from accounts, properties and views
    - Google Analytics API request to retrieve data from account, properties and views
    - Log page which contains data from api request/response time, error logs and others

## User guide

* In user_guide directory has a file with explanations and images about how to use the system.

## Techonologies

* Main developments was in Python.
    - https://www.python.org/

* Frontend was made in Django framework
    - https://www.djangoproject.com/

* Database was postgres
    - https://www.postgresql.org/

* To UI was utilized bootstrap CDN
    - https://www.bootstrapcdn.com/

* To control DOM components was used JavaScript
    - https://www.javascript.com/

* To create and prepare the environment
    - https://www.docker.com/resources/what-container

* API development
    - https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py