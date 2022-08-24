# Web blog for board and video games 


### How to setup

- Python 3.10.4 should be pre-installed.
- Download repository
- Create virtual environment with you favourite method or just use command: `python -m venv venv`
- Activate virtual environment with `source venv/bin/activate` for mac/linux or `venv\scripts\activate`
- Install requirements with the command `pip install -r requirements.txt`
- Create database with `python3 manage.py migrate`
- Create admin-user with `python3 manage.py createsuperuser`
- Run `python manage.py collectstatic` command
- Run test-server `python3 manage.py runserver`


### How to use

- Site will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Admin will be available at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
