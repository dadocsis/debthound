from flask import request
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload

from data_api import models as m
from web_api.api import schemas as s
from web_api.extensions import ma, db
from web_api.commons.pagination import paginate
from web_api.auth.helpers import jwt_or_local_only as jwt_required


class Sites(Resource):
    method_decorators = [jwt_required]

    def get(self):
        sites = db.session.query(m.Site).options(joinedload(m.Site.doctypes)).all()
        schema = s.SiteSchema(many=True, exclude=('scrape_logs', 'authtype', 'creds'))
        return schema.dump(sites).data


class SiteDoctypes(Resource):
    method_decorators = [jwt_required]

    def get(self, site_id):
        try:
            site = db.session.query(m.Site).options(joinedload(m.Site.doctypes)).get(site_id)
        except NoResultFound as nf:
            return 'Item not found', 404
        schema = s.SiteDocTypeSchema(many=True, exclude=('documents',))
        return schema.dump(site.doctypes).data


class SiteSchedules(Resource):
    method_decorators = [jwt_required]

    def get(self):
        sites = db.session.query(m.Schedule).options(joinedload(m.Schedule.site))
        schema = s.RunSpiderSchedule(many=True, exclude=('site.schedules',))
        return paginate(sites, schema)

    def post(self):
        schema = s.RunSpiderSchedule(partial=True)
        sched, errors = schema.load(request.json)
        if errors:
            return errors, 422
        db.session.add(sched)
        db.session.commit()
        sched.site
        return schema.dump(sched).data, 201


class SiteSchedule(Resource):
    method_decorators = [jwt_required]

    def delete(self, id):
        sched = db.session.query(m.Schedule).get_or_404(id)
        db.session.delete(sched)
        db.session.commit()

