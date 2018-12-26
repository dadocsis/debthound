import Actions from '../Actions'
import {getEntities, getDocumentsForLead, saveLabel, getLables, deleteLabel as _deleteLabel,
        deleteSchedule as _deleteSchedule, updateLeadLables, updateLead as _updateLead, loginUser, getSchedules,
        saveSchedule, getSites, getParties, putParty} from "./api";

export const fetchLeads = (page=1, args={}) => {
    Actions.getEntities();
    getEntities(page, args, (rsp) => Actions.rcvEntities(rsp, page, args.searchString))
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

export const fetchSchedules = (page=1) => {
    Actions.getSchedules();
    getSchedules(page, (rsp) => Actions.rcvSchedules(rsp, page))
    getSites(rsp => Actions.rcvSites(rsp))
};

export const saveDraftSchedule = (schedules) => {
    for (let schedule of schedules) {
        saveSchedule(schedule, Actions.scheduleCreated)
    }
};

export const deleteSchedule = (id) => {
    _deleteSchedule(id, rsp => Actions.scheduleDeleted(id))
};

export const fetchParties = (page=1, args={}) => {
    Actions.getParties();
    getParties(page, args, (rsp) => Actions.rcvParties(rsp, page, args.searchString))
};

export const updateParty = (party) => {
    Actions.updateParty(party);
    putParty(party, Actions.partyUpdated)
};