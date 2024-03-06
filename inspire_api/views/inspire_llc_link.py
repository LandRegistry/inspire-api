import json

from flask import Blueprint, current_app
from inspire_api.exceptions import ApplicationError
from inspire_api.models import InspireGeometry
from inspire_api.utilities.charge_id_utilities import calc_display_id

inspire_llc_link_bp = Blueprint('inspire_llc_link', __name__, url_prefix='/local-land-charge-id')


@inspire_llc_link_bp.route('/<inspire_id>', methods=['GET'])
def get_local_land_charge_id(inspire_id):
    """Get local land charge ID for a specified inspire ID"""
    current_app.logger.info("Get local land charge ID by inspire ID {}".format(inspire_id))

    try:
        int(inspire_id)
    except ValueError:
        raise ApplicationError("Inspire ID must be an integer", 400, 400)

    inspire_geometry = InspireGeometry.query\
        .filter(InspireGeometry.inspire_id == inspire_id)\
        .first()

    if not inspire_geometry:
        raise ApplicationError("No land charge ID found for inspire ID {}".format(inspire_id), 404, 404)
        # return "No land charge ID found for inspire ID {}".format(inspire_id), 404
    internal_llc_id = inspire_geometry.local_land_charge
    external_llc_id = calc_display_id(internal_llc_id)

    current_app.logger.info("Returning local land charge ID {}".format(external_llc_id))

    return json.dumps({"llc_id": external_llc_id}), 200, {'Content-Type': 'application/json'}
