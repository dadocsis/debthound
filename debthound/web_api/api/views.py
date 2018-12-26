from flask import Blueprint
from flask_restful import Api

from web_api.api.resources import (UserResource, UserList, DocumentResource, DocumentByCFNResource, Sites, SiteDoctypes,
                                   DocumentsCollection, EntityCollection, DocumentsByEntityId, Flags, Flag,
                                   EntityBatchUpdate, Entity, RunSpiderRequests, RunSpiderSchedules, RunSpiderSchedule,
                                   SiteSchedules, SiteSchedule, RunSiteEtl, PartyCollection, Party)

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(DocumentResource, '/documents/<int:id>')
api.add_resource(DocumentByCFNResource, '/documents/cfn/<string:cfn>')

api.add_resource(Sites, '/sites')
api.add_resource(SiteDoctypes, '/site_doc_type/<int:site_id>')
api.add_resource(DocumentsCollection, '/documents')
api.add_resource(EntityCollection, '/entities')
api.add_resource(DocumentsByEntityId, '/entities/<int:id>/documents')
api.add_resource(Flags, '/flags')
api.add_resource(Flag, '/flags/<int:id>')
api.add_resource(EntityBatchUpdate, '/updateLeadLables')
api.add_resource(Entity, '/entities/<int:id>')
api.add_resource(RunSpiderRequests, '/runspiderrequests')
api.add_resource(RunSpiderSchedules, '/runspiderschedules')
api.add_resource(RunSpiderSchedule, '/runspiderschedules/<int:id>')
api.add_resource(SiteSchedules, '/siteSchedules')
api.add_resource(SiteSchedule, '/siteSchedules/<int:id>')
api.add_resource(RunSiteEtl, '/runSiteETLs')
api.add_resource(PartyCollection, '/parties')
api.add_resource(Party, '/parties/<int:id>')
