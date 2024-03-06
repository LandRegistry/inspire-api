import os
from urllib.parse import quote_plus

# RULES OF CONFIG:
# 1. No region specific code. Regions are defined by setting the OS environment variables appropriately to build up the
# desired behaviour.
# 2. No use of defaults when getting OS environment variables. They must all be set to the required values prior to the
# app starting.
# 3. This is the only file in the app where os.environ should be used.

# For logging
LOG_LEVEL = os.environ['LOG_LEVEL']

# For health route
COMMIT = os.environ['COMMIT']

# This APP_NAME variable is to allow changing the app name when the app is running in a cluster. So that
# each app in the cluster will have a unique name.
APP_NAME = os.environ['APP_NAME']

# --- Database variables start
# These must all be set in the OS environment.
# The password must be the correct one for either the app user or alembic user,
# depending on which will be used (which is controlled by the
# SQL_USE_ALEMBIC_USER variable)
SQL_HOST = os.environ['SQL_HOST']
SQL_DATABASE = os.environ['SQL_DATABASE']
SQL_PASSWORD = os.environ['SQL_PASSWORD']
APP_SQL_USERNAME = os.environ['APP_SQL_USERNAME']
ALEMBIC_SQL_USERNAME = os.environ['ALEMBIC_SQL_USERNAME']
if os.environ['SQL_USE_ALEMBIC_USER'] == 'yes':
    FINAL_SQL_USERNAME = ALEMBIC_SQL_USERNAME
else:
    FINAL_SQL_USERNAME = APP_SQL_USERNAME
SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}/{3}'.format(
    FINAL_SQL_USERNAME, quote_plus(SQL_PASSWORD), SQL_HOST, SQL_DATABASE)
# Explicitly set this in order to remove warning on run
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle': int(os.environ['SQLALCHEMY_POOL_RECYCLE'])}

AUTHENTICATION_API_URL = os.environ['AUTHENTICATION_API_URL']
AUTHENTICATION_API_ROOT = os.environ['AUTHENTICATION_API_ROOT']

# --- Database variables end

MAX_HEALTH_CASCADE = os.environ['MAX_HEALTH_CASCADE']
DEPENDENCIES = {
    "postgres": SQLALCHEMY_DATABASE_URI,
    'authentication-api': AUTHENTICATION_API_ROOT
}

# Using SQLAlchemy/Postgres?
# The required variables (and required usage) can be found here:
# http://internal-git-host/gadgets/gadget-api/blob/master/gadget_api/config.py

LOGCONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            '()': 'inspire_api.extensions.JsonFormatter'
        },
        'audit': {
            '()': 'inspire_api.extensions.JsonAuditFormatter'
        }
    },
    'filters': {
        'contextual': {
            '()': 'inspire_api.extensions.ContextualFilter'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['contextual'],
            'stream': 'ext://sys.stdout'
        },
        'audit_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'audit',
            'filters': ['contextual'],
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'inspire_api': {
            'handlers': ['console'],
            'level': LOG_LEVEL
        },
        'audit': {
            'handlers': ['audit_console'],
            'level': 'INFO'
        }
    }
}
