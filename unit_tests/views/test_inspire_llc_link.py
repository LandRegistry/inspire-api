import json
from unittest.mock import MagicMock

from flask import url_for
from flask_testing import TestCase
from inspire_api import main
from mock import patch
from unit_tests.utilities_tests import super_test_context


class TestInspireLlcLink(TestCase):
    def create_app(self):
        main.app.testing = True
        return main.app

    @patch('inspire_api.app.validate')
    @patch('inspire_api.views.inspire_llc_link.InspireGeometry')
    @patch('inspire_api.views.inspire_llc_link.calc_display_id')
    def test_get_local_land_charge_id(self, mock_calc_display_id, mock_inspire_geometry, mock_validate):
        with super_test_context(main.app):
            mock_principle = MagicMock()
            mock_validate.return_value.principle = mock_principle

            mock_inspire = MagicMock()
            mock_inspire.local_land_charge = 1234
            mock_inspire_geometry.query.filter.return_value.first.return_value = mock_inspire

            mock_calc_display_id.return_value = "LLC-T3ST"

            response = self.client.get(url_for("inspire_llc_link.get_local_land_charge_id", inspire_id=1),
                                       headers={'Authorization': 'Fake JWT'})
            self.assertStatus(response, 200)
            self.assertEqual({"llc_id": "LLC-T3ST"}, json.loads(response.data.decode()))

    @patch('inspire_api.app.validate')
    @patch('inspire_api.views.inspire_llc_link.InspireGeometry')
    @patch('inspire_api.views.inspire_llc_link.calc_display_id')
    def test_get_local_land_charge_id_invalid_inspire(self, mock_calc_display_id, mock_inspire_geometry,
                                                      mock_validate):
        with super_test_context(main.app):
            mock_principle = MagicMock()
            mock_validate.return_value.principle = mock_principle

            mock_inspire = MagicMock()
            mock_inspire.local_land_charge = 1234
            mock_inspire_geometry.query.filter.return_value.first.return_value = mock_inspire

            mock_calc_display_id.return_value = "LLC-T3ST"

            response = self.client.get(url_for("inspire_llc_link.get_local_land_charge_id", inspire_id="abc"),
                                       headers={'Authorization': 'Fake JWT'})
            self.assertStatus(response, 400)
            self.assertEqual("Inspire ID must be an integer", json.loads(response.data.decode()).get("error_message"))

    @patch('inspire_api.app.validate')
    @patch('inspire_api.views.inspire_llc_link.InspireGeometry')
    @patch('inspire_api.views.inspire_llc_link.calc_display_id')
    def test_get_local_land_charge_id_no_results(self, mock_calc_display_id, mock_inspire_geometry, mock_validate):
        with super_test_context(main.app):
            mock_principle = MagicMock()
            mock_validate.return_value.principle = mock_principle

            mock_inspire = MagicMock()
            mock_inspire.local_land_charge = 1234
            mock_inspire_geometry.query.filter.return_value.first.return_value = None

            mock_calc_display_id.return_value = "LLC-T3ST"

            response = self.client.get(url_for("inspire_llc_link.get_local_land_charge_id", inspire_id=1),
                                       headers={'Authorization': 'Fake JWT'})
            self.assertStatus(response, 404)
            self.assertEqual("No land charge ID found for inspire ID 1",
                             json.loads(response.data.decode()).get("error_message"))
