# My Calendar
My Calendar is a simple calendar application. To review the project's front end code [my-calendar](https://github.com/selamet/my-calendar).

## Installation
My-Calendar requires Python 3.9.

Download project repository to your local directory:
```
git clone https://github.com/selamet/my-calendar-backend
```
Open your terminal in local project:
```
cd my-calendar-backend
``` 
Add `.env` file and configure :
```
nano .env
```
.env file looks like:
```
ENV=local
SECRET_KEY= 'If you don't have a Secret Key, it will be created automatically.'
DEBUG=True
```
With your virtual environment active, install required libraries with pip3:
```
pip3 install -r requirements.txt
```
Creation of virtual environments :
```
python3 -m venv venv
source venv/bin/activate
```

Create local_settings.py:
```
nano myCalender/local_settings.py  
```
local_settings.py looks like :
```python
from myCalender.default_settings import BASE_DIR

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ALLOWED_HOSTS = []

```


Now, we can migrate the initial database schema to our database using the management script:
```
python3 manage.py migrate
```
Finally to run the project:
```
python3 manage.py runserver
```