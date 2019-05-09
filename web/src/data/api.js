import Actions from "../Actions";

let origin = '';

if (process.env.NODE_ENV !== 'production'){
    // we are in dev so
    origin = window.location.protocol + '//' + window.location.hostname + ':' +5000
}
else {
    origin = window.location.protocol + '//' + window.location.hostname
}


function getAuthHeader() {
    return 'Bearer ' + JSON.parse(localStorage.getItem("access_token"));
}

function getUrl(path, params={}){
    let url = new URL(origin + path);
    for (let k in params){
        if (Array.isArray(params[k])){
            for (let n in params[k]){
                url.searchParams.append(k, params[k][n])
            }
        }
        else {
            url.searchParams.append(k, params[k])
        }
    }
    return url;
}

export const getEntities = (page, args, func, ehandle=defaultEhandle) => {
     // todo fetch something
    let myUrl = getUrl('/api/v1/entities', {page, ...args});
     fetch(myUrl, {
          headers : {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': getAuthHeader()
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
            'Accept': 'application/json',
            'Authorization': getAuthHeader()
           }})
        .then(rsp => {
            if (!rsp.ok){
                ehandle(rsp);
                return;
            }
            rsp.json().then(json => func(json))
        }, ehandle)
};

export const saveLabel = (label, func, ehandle=defaultEhandle) => {
    fetch(getUrl('/api/v1/flags'), {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, same-origin, *omit
        headers: {
            'Authorization': getAuthHeader(),
            "Content-Type": "application/json; charset=utf-8",
            // "Content-Type": "application/x-www-form-urlencoded",
        },
        redirect: "follow", // manual, *follow, error
        referrer: "no-referrer", // no-referrer, *client
        body: JSON.stringify(label), // body data type must match "Content-Type" header
    })
    .then(rsp => {
            if (!rsp.ok) {
                ehandle(rsp);
                return;
            }
            rsp.json().then(json => func(json))
        }, ehandle)
};

export const getLables = (page, func, ehandle=defaultEhandle) => {
    fetch(getUrl('/api/v1/flags'), {
          headers : {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': getAuthHeader()
          }})
        .then(rsp => {
            if (!rsp.ok){
                ehandle(rsp);
                return;
            }
            rsp.json().then(json => func(json))
        }, ehandle)
};

export const deleteLabel = (id, func, ehandle=defaultEhandle) => {
    fetch(getUrl('/api/v1/flags/' + id), {
        method: "DELETE", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, same-origin, *omit
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            'Authorization': getAuthHeader()
        },
        redirect: "follow", // manual, *follow, error
        referrer: "no-referrer", // no-referrer, *client

    })
    .then(rsp => {
            if (!rsp.ok) {
                ehandle(rsp);
                return;
            }
            rsp.json().then(json => func(json))
        }, ehandle)
};

export const updateLeadLables = (data, func, ehandle=defaultEhandle) => {
    fetch(getUrl('/api/v1/updateLeadLables'), {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, same-origin, *omit
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            'Authorization': getAuthHeader()
        },
        redirect: "follow", // manual, *follow, error
        referrer: "no-referrer", // no-referrer, *client
        body: JSON.stringify(data), // body data type must match "Content-Type" header
    })
    .then(rsp => {
            if (!rsp.ok) {
                ehandle(rsp);
                return;
            }
            rsp.json().then(json => func(json))
        }, ehandle)
};

export const updateLead = (data, func, ehandle=defaultEhandle) => {
    fetch(getUrl('/api/v1/entities/' + data.id), {
        method: "PATCH", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, same-origin, *omit
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            'Authorization': getAuthHeader()
        },
        redirect: "follow", // manual, *follow, error
        referrer: "no-referrer", // no-referrer, *client
        body: JSON.stringify(data), // body data type must match "Content-Type" header
    })
    .then(rsp => {
            if (!rsp.ok) {
                ehandle(rsp);
                return;
            }
            rsp.json().then(json => func(json))
        }, ehandle)
};

export const loginUser = (data, func, ehandle=defaultEhandle) => {
    fetch(getUrl('/auth/login'), {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, same-origin, *omit
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            'Authorization': getAuthHeader()
        },
        redirect: "follow", // manual, *follow, error
        referrer: "no-referrer", // no-referrer, *client
        body: JSON.stringify(data), // body data type must match "Content-Type" header
    })
    .then(rsp => {
            if (!rsp.ok) {
                ehandle(rsp);
                return;
            }
            rsp.json().then(json => func(json))
        }, ehandle)
};

export const getSchedules = (page, func, ehandle=defaultEhandle) => {
    fetch(getUrl('/api/v1/siteSchedules'), {
          headers : {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': getAuthHeader()
          }})
        .then(rsp => {
            if (!rsp.ok){
                ehandle(rsp);
                return;
            }
            rsp.json().then(json => func(json))
        }, ehandle)
};

export const saveSchedule = (siteSchedule, func, ehandle=defaultEhandle) => {
    fetch(getUrl('/api/v1/siteSchedules'), {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, same-origin, *omit
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            'Authorization': getAuthHeader()
        },
        redirect: "follow", // manual, *follow, error
        referrer: "no-referrer", // no-referrer, *client
        body: JSON.stringify(siteSchedule), // body data type must match "Content-Type" header
    })
    .then(rsp => {
        if (!rsp.ok) {
            ehandle(rsp);
            return;
        }
        rsp.json().then(json => func(json))
    }, ehandle)
};

export const getSites = (func, ehandle=defaultEhandle) => {
    fetch(getUrl('/api/v1/sites'), {
          headers : {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': getAuthHeader()
          }})
        .then(rsp => {
            if (!rsp.ok){
                ehandle(rsp);
                return;
            }
            rsp.json().then(json => func(json))
        }, ehandle)
};

export const deleteSchedule= (id, func, ehandle=defaultEhandle) => {
    fetch(getUrl('/api/v1/siteSchedules/' + id), {
        method: "DELETE", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, same-origin, *omit
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            'Authorization': getAuthHeader()
        },
        redirect: "follow", // manual, *follow, error
        referrer: "no-referrer", // no-referrer, *client

    })
    .then(rsp => {
            if (!rsp.ok) {
                ehandle(rsp);
                return;
            }
            rsp.json().then(json => func(json))
        }, ehandle)
};

export const getParties = (page, args, func, ehandle=defaultEhandle) => {
     // todo fetch something
    let myUrl = getUrl('/api/v1/parties', {page, ...args});
    fetch(myUrl, {
          headers : {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': getAuthHeader()
           }})
    .then(rsp => {
        if (!rsp.ok){
            ehandle(rsp);
            return;
        }
        rsp.json().then(json => func(json))
    }, ehandle)
};

export const putParty = (party, func, ehandle=defaultEhandle) => {
    fetch(getUrl('/api/v1/parties/' + party.id), {
        method: "PUT", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, same-origin, *omit
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            'Authorization': getAuthHeader()
        },
        redirect: "follow", // manual, *follow, error
        referrer: "no-referrer", // no-referrer, *client
        body: JSON.stringify(party), // body data type must match "Content-Type" header
    })
    .then(rsp => {
        if (!rsp.ok) {
            ehandle(rsp);
            return;
        }
        rsp.json().then(json => func(json))
    }, ehandle)
};

export const getDocImage = (doc_id, func, ehandle=defaultEhandle) => {
  fetch(getUrl('/api/v1/images/' + doc_id), {
        headers : {
          'Authorization': getAuthHeader()
        }
  }).then(rsp => {
        if (!rsp.ok){
            ehandle(rsp);
            return;
        }
        rsp.blob().then(blob => func(blob, rsp.headers.get('content-type')))
    }, ehandle)
};