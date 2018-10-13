import dispatcher from './Dispatcher'


export const ActionTypes = {
    GET_LEADS: 'GET_LEADS',
    RCV_LEADS: 'RCV_LEADS',
    VIEW_LEAD: 'VIEW_LEAD',
    RCV_LEAD_DOCS: 'RCV_LEAD_DOCS'
};

 const Actions = {
    getEntities(){
        dispatcher.dispatch({
            type: ActionTypes.GET_LEADS
        });
    },
    rcvEntities(rsp, page){
        dispatcher.dispatch({
            type: ActionTypes.RCV_LEADS,
            response: rsp,
            currentPage: page
        });
    },
    getDocsForLead(id){
        dispatcher.dispatch({
            type: ActionTypes.VIEW_LEAD,
            id: id
        });
    },
    rcvLeadDocs(docs){
        dispatcher.dispatch({
            type: ActionTypes.RCV_LEAD_DOCS,
            docs: docs
        })
    }
};

 export default Actions;