from flask import request
from flask_restful import Resource
from web_api.api import schemas as s
from web_api.extensions import db
from web_api.auth.helpers import jwt_or_local_only as jwt_required

from web_api.commons.pagination import paginate


class Flags(Resource):
    method_decorators = [jwt_required]

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
    method_decorators = [jwt_required]

    def delete(self, id):
        flag = s.FlagSchema.Meta.model.query.get_or_404(id)
        db.session.delete(flag)
        db.session.commit()

        return {"msg": "user deleted"}, 201
