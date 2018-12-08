from data_api import models as m
from web_api.extensions import ma, db
from marshmallow.fields import Float, Nested, Int, List, Str, Dict
from marshmallow_sqlalchemy import field_for


class EntityModelWrapped(db.Model, m.Entity):
    pass


class SmartNested(Nested):

    def serialize(self, attr, obj, accessor=None):
        if attr not in obj.__dict__:
            return None
        return super(SmartNested, self).serialize(attr, obj, accessor)


class SiteDocTypeSchema(ma.ModelSchema):
    class Meta:
        model = m.SiteDocType
        sqla_session = db.session


class SiteSchema(ma.ModelSchema):
    class Meta:
        model = m.Site
        sqla_session = db.session


class DocumentSchema(ma.ModelSchema):
    consideration = Float()
    doc_type = SmartNested(SiteDocTypeSchema, exclude=('documents',))
    site = SmartNested(SiteSchema, exclude=('doctypes','scrape_logs'))

    class Meta:
        model = m.Document
        sqla_session = db.session


class FlagModelWrapped(db.Model, m.EntityFlag):
    pass


class FlagSchema(ma.ModelSchema):
    class Meta:
        model = FlagModelWrapped
        sqla_session = db.session


class EntitySchema(ma.ModelSchema):
    class Meta:
        model = EntityModelWrapped
        sqla_session = db.session
    flags = Nested(FlagSchema, many=True)


class EntityBatchUpdateSchema(ma.Schema):
    id = Int()
    flags = List(Int())


class RunSpiderRequest(ma.Schema):
    spider = Str()
    project = Str()
    params = Dict()


class RunSpiderSchedule(ma.ModelSchema):
    class Meta:
        model = m.Schedule
        sqla_session = db.session

    site_id = field_for(m.Schedule, 'site_id', dump_only=False)
    site = SmartNested(SiteSchema, exclude=('doctypes', 'scrape_logs'))
