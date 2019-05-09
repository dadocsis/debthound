from flask import request, make_response
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload, contains_eager

from data_api import models as m
from web_api.extensions import db
from web_api.api import schemas as s

from web_api.commons.pagination import paginate
from web_api.auth.helpers import jwt_or_local_only as jwt_required
from web_api.commons.images import handler_factory


class DocumentResource(Resource):
    method_decorators = [jwt_required]

    def get(self, id):
        doc = db.session.query(m.Document).get(id)
        schema = s.DocumentSchema()
        return schema.dump(doc).data


class DocumentByCFNResource(Resource):
    method_decorators = [jwt_required]

    def get(self, cfn):
        try:
            doc = db.session.query(m.Document).filter_by(cfn=cfn).one()
        except NoResultFound as nr:
            return 'Item not found', 404
        schema = s.DocumentSchema()
        return schema.dump(doc).data


class DocumentsCollection(Resource):
    method_decorators = [jwt_required]

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
    method_decorators = [jwt_required]

    def get(self, id):
        edocs = db.session.query(m.Entity).\
            options(
                joinedload(m.Entity.document_facts).
                joinedload(m.DocumentFact.document).
                joinedload(m.Document.doc_type).
                joinedload('sites')).\
            options(
                joinedload(m.Entity.document_facts).
                joinedload(m.DocumentFact.document).
                joinedload(m.Document.site)).\
            options(
                joinedload(m.Entity.document_facts).
                joinedload(m.DocumentFact.document).
                joinedload(m.Document.flags)). \
            get(id)
        docs = [d.document for d in edocs.document_facts]
        schema = s.DocumentSchema(many=True)
        return schema.dump(docs).data


class EntityCollection(Resource):
    method_decorators = [jwt_required]

    def get(self):
        filters = request.args.getlist('labels')
        searchStr = request.args.get('searchString')
        schema = s.EntitySchema(many=True)
        query = db.session.query(m.Entity).filter(m.Entity.document_facts.any())
        query = query.options(joinedload(m.Entity.document_facts, innerjoin=True), joinedload(m.Entity.flags))

        if searchStr:
            query = query.filter(m.Entity.name.like(F'%{searchStr}%'))
        if filters:
            query = query.join(m.Entity.flags).filter(m.EntityFlag.name.in_(filters))

        return paginate(query, schema)


class PartyCollection(Resource):
    method_decorators = [jwt_required]

    def get(self):
        searchStr = request.args.get('searchString')
        show_blacklist = request.args.get('showBlacklist')
        schema = s.EntitySchema(many=True, only=('id', 'name', 'black_listed'))
        query = db.session.query(m.Entity)

        if searchStr:
            query = query.filter(m.Entity.name.like(F'%{searchStr}%'))
        if show_blacklist:
            query = query.filter(m.Entity.black_listed == False)

        return paginate(query, schema)


class Party(Resource):
    method_decorators = [jwt_required]

    def put(self, id):
        schema = s.EntitySchema(only=('id', 'name', 'black_listed'))
        from_db = db.session.query(m.Entity).get_or_404(id)
        ent, error = schema.load(request.json, instance=from_db)
        if error:
            return error, 422

        if ent.black_listed:
            # remove all docs for the entity if defendant
            if len(ent.document_facts) > 0:
                ent.flags.clear()
                db.session.query(m.DocumentFact).filter(m.DocumentFact.entity_id == ent.id).delete()

            jud_id = db.session.query(m.SiteDocType).filter(
                m.SiteDocType.description == 'Certified Judgment',).first().id
            deed_id = db.session.query(m.SiteDocType).filter(
                m.SiteDocType.description == 'Deed', ).first().id
            jud_ents = db.session.query(m.Entity).\
                join(m.Entity.document_facts).\
                join(m.DocumentFact.document).options(
                    contains_eager(m.Entity.document_facts).contains_eager(m.DocumentFact.document)
                ).filter_by(
                        party1=ent.name,
                        doctype_id=jud_id,
                ).all()

            # remove all judgment docs for the entity if plantiff
            jud_ents_ids = []
            leads_to_remove = []
            docs_to_remove = []
            for jud_ent in jud_ents:
                jud_ents_ids.append(jud_ent.id)
                for docf in jud_ent.document_facts:
                    if docf.document.doctype_id == jud_id and docf.document.party1 == ent.name:
                        docs_to_remove.append(docf)

            for docf in docs_to_remove:
                db.session.delete(docf)

            db.session.commit()

            # now check if the lead is still valid
            for id in jud_ents_ids:
                # reload the enities so we can get all the docs
                jud_ent = db.session.query(m.Entity).options(
                    joinedload(m.Entity.document_facts).
                    joinedload(m.DocumentFact.document)).\
                    filter(m.Entity.id == id).first()
                sites = {df.document.site_id for df in jud_ent.document_facts}

                def comp(d):
                    return d.date

                for site in sites:
                    judments = sorted([df.document for df in jud_ent.document_facts if
                                       df.document.site_id == site and df.document.doctype_id == jud_id],
                                      key=comp, reverse=False)

                    jud = next(iter(judments), None)
                    deeds = sorted([df.document for df in jud_ent.document_facts if
                                    df.document.site_id == site and df.document.doctype_id == deed_id],
                                   key=comp, reverse=True)
                    deed = next(iter(deeds), None)

                    if jud is not None and deed is not None and jud.date < deed.date:
                        break
                else:
                    leads_to_remove.append(jud_ent)

            for lead in leads_to_remove:
                lead.flags.clear()
                for df in lead.document_facts:
                    db.session.delete(df)

        db.session.commit()

        return schema.dump(ent).data


class EntityBatchUpdate(Resource):
    method_decorators = [jwt_required]

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
    method_decorators = [jwt_required]

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


class Images(Resource):
    method_decorators = [jwt_required]

    def get(self, id):
        doc = db.session.query(m.Document).get_or_404(id)
        resp = handler_factory(doc.site).handle(doc)
        f_rsp = make_response(resp.content)
        f_rsp.headers['content-type'] = resp.headers['content-type']
        return f_rsp
