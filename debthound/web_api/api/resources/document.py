from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload

from data_api import models as m
from web_api.extensions import db
from web_api.api import schemas as s

from web_api.commons.pagination import paginate


class DocumentResource(Resource):

    def get(self, id):
        doc = db.session.query(m.Document).get(id)
        schema = s.DocumentSchema()
        return schema.dump(doc).data


class DocumentByCFNResource(Resource):
    def get(self, cfn):
        try:
            doc = db.session.query(m.Document).filter_by(cfn=cfn).one()
        except NoResultFound as nr:
            return 'Item not found', 404
        schema = s.DocumentSchema()
        return schema.dump(doc).data


class DocumentsCollection(Resource):
    def post(self):
        schema = s.DocumentSchema()
        doc, errors = schema.load(request.json)
        if errors:
            return errors, 422
        doc.doctype_id = request.json['doctype_id']
        doc.site_id = request.json['site_id']
        db.session.add(doc)
        db.session.commit()
        return {"msg": " created", 'id': doc.id}, 201


class DocumentsByEntityId(Resource):
    def get(self, id):
        edocs = db.session.query(m.Entity).options(
            joinedload(m.Entity.document_facts).joinedload(m.DocumentFact.document).
            joinedload(m.Document.doc_type).joinedload('sites')).options(
            joinedload(m.Entity.document_facts).joinedload(m.DocumentFact.document).joinedload(m.Document.site)).get(id)
        docs = [d.document for d in edocs.document_facts]
        schema = s.DocumentSchema(many=True)
        return schema.dump(docs).data


class EntityCollection(Resource):
    def get(self):
        schema = s.EntitySchema(many=True)
        query = schema.model.query
        return paginate(query, schema)
