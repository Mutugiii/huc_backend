# huc_backend
Simple Flask API for the huc app.

## Setup
- Clone the repository
- Setup a venv in the cloned repo
  ```
  python3.6 -m venv --without-pip venv
  source venv/bin/activate
  curl https://bootstrap.pypa.io/get-pip.py | python
  ```
- Install the dependencies in the `requirements.txt` file
  ```
    pip install -r requirements.txt
  ```
- Run the application
  ```
    python3 manage.py server
  ```
  
 ## Database Commands
 run ```python3 manage.py db``` to view all db command options

 To Initialize db(create migrations folder) ```python3 manage.py db init```

 To run migrations use ```python3 manage.py db migrate```
