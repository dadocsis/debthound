import dispatcher from './Dispatcher'


export const ActionTypes = {
    GET_LEADS: 'GET_LEADS',
    RCV_LEADS: 'RCV_LEADS',
    VIEW_LEAD: 'VIEW_LEAD',
    RCV_LEAD_DOCS: 'RCV_LEAD_DOCS',
    DRAFT_LABEL: 'DRAFT_LABEL',
    DRAFT_LABEL_CHANGE: 'DRAFT_LABEL_CHANGE',
    CREATE_LABEL: 'CREATE_LABEL',
    LABEL_CREATED: 'LABEL_CREATED',
    CANCEL_LABEL: 'CANCEL_DRAFTFLAG',
    GET_LABELS: 'GET_LABELS',
    RCV_LABELS: 'RCV_LABELS',
    LABEL_DELETED: 'LABEL_DELETED',
    TOGGLE_LEAD: 'TOGGLE_LEAD',
    APPLY_LABELS: 'APPLY_LABELS',
    LEAD_UPDATED: 'LEAD_UPDATED',
    USER_LOGGED_IN: 'USER_LOGGED_IN',
    USER_LOGGING_IN: 'USER_LOGGING_IN',
    USER_LOGGED_OUT: 'USER_LOGGED_OUT',
    CREATE_DRAFT_SCHEDULE: 'CREATE_DRAFT_SCHEDULE',
    DRAFT_SCHEDULE_CHANGE: 'DRAFT_SCHEDULE_CHANGE',
    CREATE_SCHEDULE: 'CREATE_SCHEDULE',
    SCHEDULE_CREATED: 'SCHEDULE_CREATED',
    CANCEL_SCHEDULE: 'CANCEL_DRAFTSCHEDULE',
    GET_SCHEDULES: 'GET_SCHEDULES',
    RCV_SCHEDULES: 'RCV_SCHEDULES',
    SCHEDULE_DELETED: 'SCHEDULE_DELETED',
    RCV_SITES: 'RCV_SITES',

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
    },
    createDraftLabel() {
        dispatcher.dispatch({
            type: ActionTypes.DRAFT_LABEL
        })
    },
    cancelDraftLabel() {
        dispatcher.dispatch({
            type: ActionTypes.CANCEL_LABEL
        })
    },
    draftLabelChange(fieldName, value) {
        let data = {};
        data[fieldName] = value;
        dispatcher.dispatch({
            type: ActionTypes.DRAFT_LABEL_CHANGE,
            data
        })
    },
    saveDraftLabel(e, form) {
        e.preventDefault();
        if (form.checkValidity())
        dispatcher.dispatch({
            type: ActionTypes.CREATE_LABEL,
        })
    },
    labelCreated(rsp) {
        dispatcher.dispatch({
            type: ActionTypes.LABEL_CREATED,
            rsp: rsp
        })
    },
    getLabels() {
        dispatcher.dispatch({
            type: ActionTypes.GET_LABELS
        });
    },
    rcvLabels(rsp, page) {
        dispatcher.dispatch({
            type: ActionTypes.RCV_LABELS,
            rsp: rsp,
            currentPage: page
        });
    },
    labelDeleted(id) {
        dispatcher.dispatch({
            type: ActionTypes.LABEL_DELETED,
            id
        })
    },
    toggleLead(lead) {
        dispatcher.dispatch({
            type: ActionTypes.TOGGLE_LEAD,
            lead
        })
    },
    leadUpdated(lead) {
        dispatcher.dispatch({
            type: ActionTypes.LEAD_UPDATED,
            lead
        })
    },
    userLoggedIn(userData, loginFailureMessage=null) {
        dispatcher.dispatch({
            type: ActionTypes.USER_LOGGED_IN,
            userData,
            loginFailureMessage
        })
    },
     userLoggingIn() {
        dispatcher.dispatch({
            type: ActionTypes.USER_LOGGING_IN
        })
    },
     userLoggedOut() {
        dispatcher.dispatch({
            type: ActionTypes.USER_LOGGED_OUT
        })
     },
     saveDraftSchedule() {
        dispatcher.dispatch({
            type: ActionTypes.CREATE_SCHEDULE,
        })
    },
     cancelDraftSchedule() {
        dispatcher.dispatch({
            type: ActionTypes.CANCEL_SCHEDULE,

        })
    },
    getSchedules() {
        dispatcher.dispatch({
            type: ActionTypes.GET_SCHEDULES
        })
    },
    rcvSchedules(rsp, page) {
        dispatcher.dispatch({
            type: ActionTypes.RCV_SCHEDULES,
            rsp: rsp,
            currentPage: page
        })
    },
    createDraftSchedule(sites) {
        dispatcher.dispatch({
            type: ActionTypes.CREATE_DRAFT_SCHEDULE,
            site: sites[0].id
        })
    },
    draftScheduleChange(fieldName, value) {
        let data = {};
        data[fieldName] = value;
        dispatcher.dispatch({
            type: ActionTypes.DRAFT_SCHEDULE_CHANGE,
            data
        })
    },
    scheduleCreated(rsp) {
        dispatcher.dispatch({
            type: ActionTypes.SCHEDULE_CREATED,
            rsp: rsp
        })
    },
    rcvSites(rsp) {
        dispatcher.dispatch({
            type: ActionTypes.RCV_SITES,
            rsp: rsp
        });
    },
     scheduleDeleted(id) {
        dispatcher.dispatch({
            type: ActionTypes.SCHEDULE_DELETED,
            id
        })
    },
};

 export default Actions;