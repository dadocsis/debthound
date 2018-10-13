from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload, defer, load_only, noload, defaultload

from data_api import models as m
from web_api.api import schemas as s
from web_api.extensions import ma, db

from web_api.commons.pagination import paginate


class Flags(Resource):
    def get(self):
        try:
            site = db.session.query(m.Site).options(joinedload(m.Site.doctypes)).get(site_id)
        except NoResultFound as nf:
            return 'Item not found', 404
        schema = s.SiteDocTypeSchema(many=True, exclude=('documents',))
        return schema.dump(site.doctypes).data