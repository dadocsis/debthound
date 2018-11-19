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
        filters = request.args.getlist('labels')
        schema = s.EntitySchema(many=True)
        query = db.session.query(m.Entity)
        if filters:
            query = query.join(m.Entity.flags).filter(m.EntityFlag.name.in_(filters))

        query = query.options(joinedload(m.Entity.flags), joinedload(m.Entity.document_facts))
        return paginate(query, schema)


class EntityBatchUpdate(Resource):

    def post(self):
        schema = s.EntityBatchUpdateSchema(many=True)
        ents, errors = schema.load(request.json)
        if errors:
            return errors, 422
        query = db.session.query(m.Entity)
        results = []
        for ent in ents:
            from_db = query.get(ent['id'])
            for label_id in ent['flags']:
                if any(label_id == label.id for label in from_db.flags):
                    continue
                flag = db.session.query(m.EntityFlag).get(label_id)
                from_db.flags.append(flag)
                results.append(from_db)
        db.session.commit()
        schema = s.EntitySchema(many=True)
        return schema.dump(results).data, 201


class Entity(Resource):
    def patch(self, id):
        schema = s.EntitySchema()
        ent, error = schema.load(request.json, partial=True)
        from_db = db.session.query(m.Entity).get_or_404(ent.id)
        if hasattr(ent, 'flags'):
            flags_to_remove = []
            flags_to_add = []
            db_flag_ids = [flag.id for flag in from_db.flags]
            flag_ids = [flag.id for flag in ent.flags]

            for _id in flag_ids:
                if _id not in db_flag_ids:
                    new_flag = db.session.query(m.EntityFlag).get(_id)
                    flags_to_add.append(new_flag)

            for _id in db_flag_ids:
                if _id not in db_flag_ids:
                    remove_flag = db.session.query(m.EntityFlag).get(_id)
                    flags_to_remove.append(remove_flag)

            for add_me in flags_to_add:
                from_db.flags.append(add_me)

            for remove_me in flags_to_remove:
                from_db.flags.remove(remove_me)

        db.session.commit()
        return schema.dump(from_db).data
