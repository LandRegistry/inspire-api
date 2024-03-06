from geoalchemy2 import Geometry
from inspire_api.extensions import db


class InspireGeometry(db.Model):
    __tablename__ = 'inspire_geometry'

    inspire_id = db.Column(db.BigInteger, primary_key=True)
    category = db.Column(db.String)
    sub_category = db.Column(db.String, nullable=True)
    geometry = db.Column(Geometry(srid=27700))
    create_timestamp = db.Column(db.DateTime)
    update_timestamp = db.Column(db.DateTime)
    cancellation_timestamp = db.Column(db.DateTime, nullable=True)
    deletion_timestamp = db.Column(db.DateTime, nullable=True)
    geometry_type = db.Column(db.Integer)
    local_land_charge = db.Column(db.BigInteger)
    inspire_theme = db.Column(db.String, nullable=True)
