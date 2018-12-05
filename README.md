[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.com/kirega/ireporter-ch3.svg?branch=develop)](https://travis-ci.com/kirega/ireporter-ch3)
[![Maintainability](https://api.codeclimate.com/v1/badges/bdcb7758901f1a806bb1/maintainability)](https://codeclimate.com/github/kirega/ireporter-ch3/maintainability)

# iReporter
## Project Overview
Corruption is a huge bane to Africa’s development. African countries must develop novel and
localised solutions that will curb this menace, hence the birth of iReporter. iReporter enables any/every citizen to bring any form of corruption to the notice of appropriate authorities and the general public. Users can also report on things that needs government intervention

To view this site : https://kirega.github.io/iReporter/


## Technologies used.

* Python 3
* flask
* flask-restful
* flask-jwt
* Postgres

## [Pivotal Tacker Stories](https://www.pivotaltracker.com/n/projects/2227132)

## Current endpoints

| Method  | Endpoint  | Usage  |
|---|---|---|
| POST | api/v1/signup | Register a user.  |   
| POST | api/v1/login | Login a new user  |  
| POST | api/v1/incidents  | Create a new incident  |   
| GET | api/v1/incidents| Get all the created incidents|
| GET | api/v1/incident/ (incidentId) | Get a single incident|
| PUT |	api/v1/incident/ (incidentId)/location |	Update a single incident location. |
| PUT |	api/v1/incident/(incidentId)/comment |	Update a single incident comment. |
| DELETE | api/v1/incident/(incidentId)/comment	| Delete a single incident. |
## Installation guide and usage

#### **Clone the repo.**
  ```
   $ git clone https://github.com/kirega/iReporter.git
  ```

#### **Create virtual environment & Activate.**
  ```
   $ virtualenv env -p python3
   $ source env/bin/activate
   ```
#### **Install Dependancies.**
  ```
    (env)$ pip install -r requirements.txt
  ```

#### **Run the app**
```
(env)$ cd iReporter/
```

On Linux set the enviroment variables for the project
```
(env)$ export FLASK_APP=run.py
(env)$ export FLASK_DEBUG=1
(env)$ export FLASK_ENV=development
(env)$ flask run
```

#### **Run Tests**

  ```
    (env)$ pytest --cov=tests
  ```
