# Import every blueprint file
from inspire_api.views.general import general_bp
from inspire_api.views.inspire_llc_link import inspire_llc_link_bp


def register_blueprints(app):
    """Adds all blueprint objects into the app."""
    app.register_blueprint(general_bp)
    app.register_blueprint(inspire_llc_link_bp)

    # All done!
    app.logger.info("Blueprints registered")
