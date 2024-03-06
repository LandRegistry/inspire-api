# This file is the entry point.
# First we import the app object, which will get initialised as we do it. Then import methods we're about to use.
from inspire_api.app import app
from inspire_api.blueprints import register_blueprints
from inspire_api.exceptions import register_exception_handlers
from inspire_api.extensions import register_extensions

# Now we register any extensions we use into the app
register_extensions(app)
# Register the exception handlers
register_exception_handlers(app)
# Finally we register our blueprints to get our routes up and running.
register_blueprints(app)
