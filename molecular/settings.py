import os
import raven
from cryptography.fernet import Fernet

TESTING = os.environ.get('TRAVIS', 'False')
DOCKER = os.environ.get('DOCKER_CONTAINER', 'False')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'fv($0e1to(r8ddlr4e802nl7i#42sm0k8b(mc-4oor8el%^z-p'
DEBUG = True

PRODUCTION = False

if TESTING == 'True':
    # Travis 테스트 작동 중이면, 시크릿 키가 없기 때문에 비밀 환경변수 사용
    KEY = os.environ['KEY']
else:
    from molecular.crypt_key import KEY

KEY = KEY.encode() # 스트링값 바이트로 변경
cipher_suite = Fernet(KEY)

ciphered_ip = b'gAAAAABbdl0msVTv0ZCE22f7PGl8eOizLrbgydyEIGrWtRFI6uITqMbYny7nV6KqRiIoav6pGoCNihqeXzB6imO_ns0BuJUT8Q=='
IP_ADDRESS = cipher_suite.decrypt(ciphered_ip).decode()

ciphered_db = b'gAAAAABbcPVvHqEYN9va0lVAKxbx4di8fY8d3rTpeFh3rgnk1zvlGpmKEIsiIHCktNVD7iFS-x9qVfd49Jz9wqX_GtFH4SlrYA=='
DB_ADDRESS = cipher_suite.decrypt(ciphered_db).decode()

ALLOWED_HOSTS = ['127.0.0.1', '127.0.1.1', IP_ADDRESS]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # corsheaders
    'corsheaders',

    # Sentry: 에러 로깅
    'raven.contrib.django.raven_compat',

    # Django Restframework (API Template)
    'rest_framework',

    # celery + celerybeat
    'django_celery_beat',
    'django_celery_results',

    # 몰레큘러 앱 정의내리는 곳
    'algorithms',
    'contents',
    'gobble',
]

### Sentry 새팅 ###
RAVEN_CONFIG = {
    'dsn': 'https://d10494d8c8c74652a24a93bb716e51f9:ec401ad52f6149ed961705143832de67@sentry.io/1263993',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(BASE_DIR),
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'molecular.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'molecular.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    ### contents 디비를 사용하고 싶으면, Model.objects.using('contents').all(), data.save(using='contents')
    'contents': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'avocado',
        'USER': 'avocado',
        'PASSWORD': 'veggieavocado2018',
        'HOST': DB_ADDRESS,
        'PORT': 5432,
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# https://github.com/ottoyiu/django-cors-headers
CORS_ORIGIN_ALLOW_ALL = True # 외부에서 API 요청 가능하도록 새팅

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

if TESTING == 'True' or DOCKER == 'False':
    cache_location = 'redis://localhost:6379/'
else:
    cache_location = 'redis://redis:6379/'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": cache_location,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'PASSWORD': 'molecularredispassword'
        }
    }
}

amqp_user = 'molecularuser'
amqp_pass = 'molecularrabbitmqpassword'
if TESTING == 'True' or DOCKER == 'False':
    amqp_location = 'localhost'
else:
    amqp_location = 'rabbit'
amqp_url = 'amqp://{}:{}@{}:5672//'.format(amqp_user, amqp_pass, amqp_location)

CELERY_BROKER_URL = amqp_url
CELERY_RESULT_BACKEND = 'django-db' # https://github.com/celery/django-celery-results/issues/19
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
