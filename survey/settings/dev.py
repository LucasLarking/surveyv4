from .common import *


DEBUG = True
SECRET_KEY = 'django-insecure-_1q5lapu+aomuwczgq5h#%lhr_des8qn!!lqd$)_dj7i@wyz13'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}