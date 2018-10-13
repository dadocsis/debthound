import Actions from '../Actions'
import {getEntities, getDocumentsForLead} from "./api";

export const fetchLeads = (page=1) => {
    Actions.getEntities();
    getEntities(page, (rsp) => Actions.rcvEntities(rsp, page))
};

export const getDocsForLead = (l) => {
    Actions.getDocsForLead(l);
    getDocumentsForLead(l, Actions.rcvLeadDocs)
};