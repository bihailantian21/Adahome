"""
Django settings for opsweb project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print('------os.path.abspath: %s ' % (os.path.abspath(__file__)))
print('------os.path.dirname: %s' % (os.path.dirname(os.path.abspath(__file__))))
print('------BASE_DIR: %s ' % (BASE_DIR))

'''
os.path.abspath: /root/opswed/opsweb/settings.py
os.path.dirname: /root/opswed/opsweb
BASE_DIR: /root/opswed
'''

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!bw93ck6flds-7%2r5++8yz7l^meh4s0og4vlh7gyx5u%bmhvo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Ada开发步骤:
    'dashboard',  # 1 控制面板
    'accounts',  # 2 用户管理
    'resources',  # 3 资产管理
    'monitor',  # 4 监控告警
    'code_update',  # 5 发布系统
    'djcelery',
    'django_crontab',
    'workorder'  # 工单系统
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'opsweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'opsweb.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'zyl',
        'PASSWORD': '888888',
        'HOST': '172.16.18.88',
        'PORT': '9036',
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#################### 自定义配置: 必须大写 ####################

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

## 180905 session 设置
SESSION_COOKIE_AGE = 60 * 10  # 10分钟
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 关闭浏览器，则COOKIE失效

## 180908 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
            'datefmt': '%Y%m%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '%s/access.log' % os.path.join(BASE_DIR, 'logs')
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', ],
            'level': 'DEBUG',
            'propagate': True,  # 是否向上传递
        },
    },
    'root': {
        'handlers': ['file', ],
        'level': 'DEBUG',
    },
}

## 180908 Zabbix Api
ZABBIX_API = 'http://172.16.18.88:99/zabbix/'
ZABBIX_USER = 'Admin'
ZABBIX_USERPASS = '888888'

## 180913 SaltStack API
SALT_API_URL = 'http://172.16.18.130:8000/'
SALT_API_USER = 'admin'
SALT_API_PASSWD = 'admin'
SALT_API_LOCATION = 'slq'

## 180922 Celery + redis
import djcelery
from celery import Celery, platforms

platforms.C_FORCE_ROOT = True  # 解决:
"""https://www.jianshu.com/p/9e422d9f1ce2
If you really want to continue then you have to set the C_FORCE_ROOT"""

djcelery.setup_loader()  # 初始化所有的task
BROKER_URL = 'redis://127.0.0.1:6379/6'  # 有redis 6数据库，默认是0
CELERY_IMPORTS = ('core.tasks')

## 180922 Djando_crontab
# https://github.com/kraiz/django-crontab
CRONJOBS = (
    # ('*/1 * * * *', 'core.crons.test_django_crontab', '>>/tmp/django_cron.log'),
    ('*/1 * * * *', 'core.crons.test_django_crontab'),
)

## Email settings smtp/pop3
# EMAIL_HOST = "smtp.163.com"
# EMAIL_HOST_USER = "xxx@email.com"
# EMAIL_HOST_PASSWORD = "123456"
# EMAIL_USE_TLS = False
# EMAIL_SUBJECT_PREFIX = u"[邮件]"

## Mongo DB
# MONGO_HOST = '172.16.18.88'
# MONGO_PORT = '27017'

## Redis
# REDSI_KWARGS_LPUSH = {"host": '172.16.18.88', 'port': 6379, 'db': 3}
# REDSI_LPUSH_POOL = None
