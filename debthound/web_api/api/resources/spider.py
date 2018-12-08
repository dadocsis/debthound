from os.path import join

from flask import request
from flask_restful import Resource
import requests

from web_api.api import schemas as s
from web_api.auth.helpers import local_only
from web_api.extensions import db
from data_api import models as m
from sqlalchemy.orm import joinedload
from sqlalchemy import func

SCRAPYD_URL = 'http://127.0.0.1:6800'


class RunSpiderRequests(Resource):
    method_decorators = [local_only]

    def post(self):
        schema = s.RunSpiderRequest()
        run_spider, errors = schema.load(request.json)
        if errors:
            return errors, 422
        data = {
            'project': run_spider['project'],
            'spider': run_spider['spider']
        }
        for k in run_spider['params']:
            data[k] = run_spider['params'][k]

        rsp = requests.post('{0}/schedule.json'.format(SCRAPYD_URL), data=data)
        rspd = rsp.json()

        return rspd


class RunSpiderSchedule(Resource):
    method_decorators = [local_only]

    def get(self, id):
        sched = db.session.query(m.Schedule).get_or_404(id)
        schema = s.RunSpiderSchedule()
        return schema.dump(sched).data

    def put(self, id):
        schema = s.RunSpiderSchedule()
        sched = db.session.query(m.Schedule).get_or_404(id)
        sched, errors = schema.load(request.json, instance=sched)
        if errors:
            return errors, 422
        db.session.commit()
        return schema.dump(sched).data


class RunSpiderSchedules(Resource):
    method_decorators = [local_only]

    def post(self):
        schema = s.RunSpiderSchedule()
        sched, errors = schema.load(request.json)

        if errors:
            return errors, 422

        db.session.add(sched)
        db.session.commit()

        return schema.dump(sched).data, 201

    def get(self):
        sched = db.session.query(m.Schedule).options(joinedload(m.Schedule.site)).all()
        schema = s.RunSpiderSchedule(many=True, exclude=('site.schedules',))
        return schema.dump(sched).data


class RunSiteEtl(Resource):
    method_decorators = [local_only]

    def post(self):
        schema = s.SiteSchema(partial=True)
        site, errors = schema.load(request.json)
        if errors:
            return errors, 422
        db.session.execute('call document_etl({0})'.format(site.id))