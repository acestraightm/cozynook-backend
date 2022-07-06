from .settings import *

# Production
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pw)j7rv)pi&kp++l$&6eo;z9p3l209;z.20(^20=6032n)'  # Same as in base.py

# --- Password Validation ----
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

INSTALLED_APPS += [
]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'fdl_courier_database',
#         # 'USER': 'root',
#         'HOST': 'localhost',
#         'USER': 'admin',
#         'PASSWORD': '5j4jhfje3yQ8dDlXXoei24jk46',
#         'PORT': 3306,
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO'",
#             'charset': 'utf8'
#         },
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cozynook',
        'USER': 'postgres',
        'PASSWORD': 'owoak89fds9a9132~1832ds',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# --- LOGGING ---
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'mysite.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'FDL_RECRUITMENT': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'fdll.ro'
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = 'order@fdll.ro'
EMAIL_HOST_PASSWORD = '!@hnfkryJBGN78)(big'
