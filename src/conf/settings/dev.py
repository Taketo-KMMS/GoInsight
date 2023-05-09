from .base import *  # noqa
from .base import INSTALLED_APPS, MIDDLEWARE

DEBUG = True

INTERNAL_IPS = ["127.0.0.1"]
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

ROOT_URLCONF = "conf.urls.dev"
