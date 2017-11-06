# tweet-django
Simple microblog platform

## Instalation
### Creating virtualenv
- `virtualenv --python=python3 .env`
- `source .env/bin/activate`
### Deploymenting
- `git clone https://github.com/elektro-NIK/tweet-django.git`
- `cd tweet-django/`
- `pip3 install -r requirements.txt`
- `./manage.py migrate`
- `./manage.py compilemessages`
### Runing
- `./manage.py runserver 0.0.0.0:8000`
- open `http://localhost:8000/` in web browser
