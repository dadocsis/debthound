import Actions from "../Actions";

let origin = '';

if (process != undefined){
    // we are in dev so
    origin = window.location.protocol + '//' + window.location.hostname + ':' +5000

}

function getUrl(path, params={}){
    let url = new URL(origin + path);
    for (let k in params){
        url.searchParams.append(k, params[k])
    }
    return url;
}

export const getEntities = (page, func, ehandle=defaultEhandle) => {
     // todo fetch something
      fetch(getUrl('/api/v1/entities', {page}), {
          headers : {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
           }})
        .then(rsp => {
            if (!rsp.ok){
                ehandle(rsp);
                return;
            }
            rsp.json().then(json => func(json))
        }, ehandle)
        //.then(json => func(json))
};

const defaultEhandle = (rsp) => {
    alert("Error in response: " + rsp.message);
    // todo: implement Actions.errorReceiving
};

export const getDocumentsForLead = (id, func, ehandle=defaultEhandle) => {
          fetch(getUrl('/api/v1/entities/' + id + '/documents'), {
          headers : {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
           }})
        .then(rsp => {
            if (!rsp.ok){
                ehandle(rsp);
                return;
            }
            rsp.json().then(json => func(json))
        }, ehandle)
}
