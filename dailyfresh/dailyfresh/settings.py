"""
Django settings for dailyfresh project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gl*wa(c$h@3436q)+^3326%yp^+$(1u9(s$tua^14+p$$q*ga0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'demo.ttfresh.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'tinymce',
    'goods',
    'haystack',
    'cart',
    'order',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'dailyfresh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
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

WSGI_APPLICATION = 'dailyfresh.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dailyfresh',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': '127.0.0.1',
        'POST': '3306',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

AUTH_USER_MODEL = 'user.User'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'static'),
    'static',
]
STATIC_ROOT = '/var/www/demo.ttfresh.com'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s [%(funcName)s] [%(lineno)d]: \n %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'normal': {
            'format': '%(levelname)s %(asctime)s %(module)s [%(funcName)s]: %(message)s'
        },
        'request': {
            'format': '%(levelname)s %(asctime)s status_code:[%(status_code)s] %(request)s: %(message)s'
        },
        'db': {
            'format': 'sql:[%(sql)s] 花费时间: [%(duration)s]'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'user/captcha.log'),
            'encoding': 'utf-8',
            'formatter': 'simple',
        },
        'file2': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
            'encoding': 'utf-8',
            'formatter': 'normal',
        },
        'file3': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.client_error.log'),
            'encoding': 'utf-8',
            'formatter': 'verbose',
        },
        'request': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.request.log'),
            'encoding': 'utf-8',
            'formatter': 'request',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'request',
            # 'filters': ['require_debug_false'],
        },
        'db': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'db.log'),
            'encoding': 'utf-8',
            'filters': ['require_debug_true'],
            'formatter': 'db',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['require_debug_true'],
        },
    },
    'loggers': {
        'captcha': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django': {
            'handlers': ['file2'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.client_error': {
            'handlers': ['file3'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'propagate': False,
            'level': 'WARNING',
        },
        'django.db.backends': {
            'handlers': ['db'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'myproject.debug': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    },
}
# USE_ETAGS = True
LOGIN_URL = 'user:login'
#  配置富文本初始化
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'width': 600,
    'height': 400,
}
# 配置全文索引引擎
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'goods.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 18
# 自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
ADMINS = (('chaiming', 'mail_cm@foxmail.com'),)  # email追踪5xx错误
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # 向标准输出打印邮件
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
#发送邮件的邮箱
EMAIL_HOST_USER = 'itcast88@163.com'
#在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'python808'
#收件人看到的发件人
EMAIL_FROM = 'dailyfresh错误邮件'
