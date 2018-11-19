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
        schema = s.FlagSchema(many=True)
        query = s.FlagSchema.Meta.model.query
        return paginate(query, schema)

    def post(self):
        schema = s.FlagSchema()
        flag, errors = schema.load(request.json)
        if errors:
            return errors, 422

        db.session.add(flag)
        db.session.commit()
        return {"msg": "flag created", "flag": schema.dump(flag).data}, 201


class Flag(Resource):
    def delete(self, id):
        flag = s.FlagSchema.Meta.model.query.get_or_404(id)
        db.session.delete(flag)
        db.session.commit()

        return {"msg": "user deleted"}, 201
