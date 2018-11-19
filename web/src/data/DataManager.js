import Actions from '../Actions'
import {getEntities, getDocumentsForLead, saveLabel, getLables, deleteLabel as _deleteLabel,
        updateLeadLables, updateLead as _updateLead, loginUser} from "./api";

export const fetchLeads = (page=1, args={}) => {
    Actions.getEntities();
    getEntities(page, args, (rsp) => Actions.rcvEntities(rsp, page))
};

export const getDocsForLead = (l) => {
    Actions.getDocsForLead(l);
    if (l === -1) return;
    getDocumentsForLead(l, Actions.rcvLeadDocs)
};

export const saveDraftlabel = (label) => {
    saveLabel(label, Actions.labelCreated)
};

export const fetchLables = (page=1) => {
    Actions.getLabels();
    getLables(page, (rsp) => Actions.rcvLabels(rsp, page))
};

export const deleteLabel = (id) => {
    _deleteLabel(id, rsp => Actions.labelDeleted(id))
};

export const batchUpdateLeadLabels = (labels, leads) => {
    let dataForUpdate = [];
    for (let lead of leads){
        let out = {id: lead.id, flags:[]};
        for (let label of labels){
            if (lead.flags.includes(label)){
                continue;
            }
            out.flags.push(label)
        }
        dataForUpdate.push(out)
    }
    updateLeadLables(dataForUpdate,
        (resp)=>{
            for (let lead of resp){
                Actions.leadUpdated(lead)
            }
        })
};

export const updateLead = (lead) => {
    _updateLead(lead, rsp => Actions.leadUpdated(rsp))
};

export const userLogin = (userName, pw) => {
    Actions.userLoggingIn();
    loginUser({username: userName, password: pw},
        (rsp) => Actions.userLoggedIn(rsp),
        (rsp) => {
            if (rsp.status === 400){
                rsp.json().then(data => Actions.userLoggedIn(null, data.msg))
            } else {
                alert('unhandled error while logging in user')
            }
        })
};
