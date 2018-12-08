import React from "react";
import Loader from 'react-loader-spinner'
import Pager from './Pager'
import {MyMultiSelect, Label} from "./Common";

const $ = window.$;

const LeadToolbar = (props) => {
    let menu = React.createRef();
    let rInput = React.createRef();
    let labels = props.labels.toJS().map((label, i)=>({value: label, label: label.name}));
    let selectedFiltersRaw = localStorage.getItem("selectedFilters");
    let selectedFilters = selectedFiltersRaw ? JSON.parse(selectedFiltersRaw) : [];
    let selectedFiltersFromLabels = [];


    for (let f of selectedFilters){
        let item = labels.find(l => l.value.id === f.id)
        if (item) {
            selectedFiltersFromLabels.push(item.value)
        }
    }

    props.registerResizeCallBack(toggle);

    function toggle(e) {
        menu.current.style.width = rInput.current.offsetWidth.toString() + 'px';
        if (e.type === "resize") return;
        if (menu.current.classList.contains("show")) {
            menu.current.classList.remove("show")
        }
        else {
            if (labels.length === 0){
                props.fetchLables()
            }
            menu.current.classList.add("show")
        }
    }

    function applyFilter(selection) {
        let args = selection.map((s) => (s.name));
        props.fetchLeads(1, {labels: args});
        localStorage.setItem('selectedFilters', JSON.stringify(selection))
    }

    function applyLabelAssignment(e) {
        e.preventDefault();
        let labels = [];
        let leads = props.selectedLeads;
        let formData = new FormData(e.target);
        for (let id of formData.values()) {
            labels.push(id)
        }
        if (labels.length) {
            props.updateLeadLabels(labels, leads);
            let chkboxes = $(e.target).find('input:checkbox:checked')
            chkboxes.prop( "checked", false )
        }
    }

    return(
    <div className='container-fluid'>

            <div className="btn-toolbar mb-1" role="toolbar" aria-label="Lead Toolbar">
                <div className="btn-group mr-2" role="group">
                    <button type="button" className="btn btn-sm">
                        <i className="far fa-check-square"></i>
                    </button>
                </div>
                <div className="btn-group mr-2 dropright" role="group" >
                    <button disabled={props.selectedLeads.length === 0} className="btn btn-sm dropdown-toggle" data-toggle="dropdown"><i className="fas fa-tags"></i></button>
                    <div className="dropdown-menu" id="filterAssignment">
                        <h6 className="dropdown-header">Label as:</h6>
                        <div className="dropdown-divider"></div>
                        <form className="px-4 py-3" onSubmit={applyLabelAssignment}>
                            {labels.map((l)=>(
                                <div className="form-group" key={l.value.id}>
                                    <div className="form-check">
                                        <input type="checkbox" className="form-check-input" name={l.label} value={l.value.id}/>
                                            <label className="form-check-label" htmlFor="dropdownCheck">
                                                {l.value.name}
                                            </label>
                                    </div>
                                </div>
                            ))}

                        <div className="dropdown-divider"></div>
                        <button className="dropdown-item" type="submit">Apply Labels</button>
                        <button className="dropdown-item" type="button">Cancel</button>
                             </form>
                    </div>

                </div>
                <div className="btn-group mr-2 d-flex flex-fill justify-content-center" role="group" >

                   <button onClick={toggle}  className="btn btn-sm" data-toggle="collapse" data-target="#filterMenu"  aria-controls="filterMenu" aria-expanded="false">
                       <i className="fas fa-search"></i>
                   </button>

                    <div className="w-50">

                       <input style={{width: "100%"}} ref={rInput} type='text'/>

                        <div ref={menu} className="border FilterMenu collapse">
                            <form className="px-2">
                                <div className="form-group">
                                    <label htmlFor="lead-filter" className="font-weight-bold">Lead Filter</label>
                                    <MyMultiSelect overrideOptions={{showSubmitChangeButton: true}} options={labels} myApplyHandler={applyFilter} selected={selectedFiltersFromLabels}/>

                                </div>
                            </form>
                            <span className='sticky-top position-absolute' style={{right: 0}}>
                                <i className="fas fa-times" onClick={toggle}></i></span>
                        </div>
                    </div>
                    <div className="float-right" style={{right: 0}} >
                            <button onClick={toggle} className="btn btn-sm" data-toggle="collapse" data-target="#filterMenu"  aria-controls="filterMenu"
                                    aria-expanded="false">
                                <i className="fas fa-angle-down"></i>
                            </button>
                    </div>
                    <span className="float-left">{props.leads.size}</span>
                </div>

            </div>
    </div>)};

const LeadDocs = (props) => {
    let staged = {};
    props.docs.forEach((d, idx) =>{
        if (!staged[d.getIn(['site','id'])]) {
            let dtg = {};
            dtg[d.getIn(['doc_type', 'id'])] = {
                doc_type: d.get('doc_type'),
                docs: [d]
            };
            staged[d.getIn(['site','id'])] = {
                site: d.get('site'), doc_type_grouped: dtg
            }
        } else if (!staged[d.getIn(['site','id'])]['doc_type_grouped'][d.getIn(['doc_type', 'id'])]){
            let dtg = staged[d.getIn(['site','id'])]['doc_type_grouped'];
            dtg[d.getIn(['doc_type', 'id'])] = {
                doc_type: d.get('doc_type'),
                docs: [d]
            };
        } else {
            let dtg = staged[d.getIn(['site','id'])]['doc_type_grouped'][d.getIn(['doc_type', 'id'])];
            dtg.docs.push(d)
        }
    });
    let markup = [];
    for (let k in staged){
        let t = (
         <div key={k} className="rounded border border-light bg-light p-2">
             <p className="text-center">
                <h5 className="m-2">{staged[k].site.get('base_url')}</h5>
             </p>
             {Object.keys(staged[k].doc_type_grouped).map(dtg_k => {
                 let dtg = staged[k].doc_type_grouped[dtg_k];
                 return (
                     <table className="table table-sm" key={dtg_k}>
                        <thead>
                        <caption>{dtg.doc_type.get('description')}</caption>
                        <tr>
                            <th scope="col">date</th>
                            <th scope="col">party1</th>
                            <th scope="col">party2</th>
                            <th scope="col">document image</th>
                            <th scope="col">cross name</th>
                            <th scope="col">legal</th>
                            <th scope="col">cfn</th>
                        </tr>
                        </thead>
                        <tbody>
                        {dtg.docs.map((d =>
                            <tr key={d.get('id')}>
                                <td className='text-nowrap'>{d.get('date')}</td>
                                <td>{d.get('party1')}</td>
                                <td>{d.get('party2')}</td>
                                <td className='text-truncate d-inline-block' style={{maxWidth: '150px'}}><a target='_blank' href={d.get('image_uri')}>{d.get('image_uri')} </a> </td>
                                <td>{d.get('cross_name')}</td>
                                <td>{d.get('legal')}</td>
                                <td>{d.get('cfn')}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                 );
             })
         }
         </div>
        );
        markup.push(t);
    }
    return markup;
};

const Lead = (props) => {
    let selectedLead = props.lead.get('id') === props.selectedLead.get('id');
    let isLoading = selectedLead && props.selectedLead.get('isLoading') === true;
    let flags = props.lead.get('flags');

    function toggleDocs(id){
        if (selectedLead){
            props.getDocsForLead(-1)
        } else {
            props.getDocsForLead(id)
        }
    }

    function deleteLabel(label){
        let lead = props.lead.toJS();
        lead.flags = lead.flags.filter(f => f.id !== label.id);
        props.updateLead(lead);
    }

    let _li = (<li className="list-group-item list-group-item-action" id={props.lead.get('id')}>
        <div className={'d-inline-flex'}>
                <input type='checkbox' className='mr-2' onChange={(e) => props.toggleLead(props.lead.toJS())}/>
                <span className="font-weight-normal mr-2" onClick={(e) => toggleDocs(props.lead.get('id'))} style={{cursor: 'crosshair'}}>
                    {props.lead.get('name')}</span>
        { flags.size > 0 && flags.map((f, idx) => (<Label key={idx} label={f} deleteLabel={deleteLabel} options={{deleteStyle: 'compact'}}/>))}

                <span className="badge badge-primary badge-pill d-table">{props.lead.get('document_facts').size}</span>
             </div>
                { !isLoading && selectedLead &&
                    <LeadDocs docs={props.selectedLead.get('docs')} />
                }
        { isLoading && selectedLead &&
            <Loader
                type="Puff"
                color="#00BFFF"
                height="50"
                width="50"/>
        }
             </li>);
    return _li
};

class Leads extends React.Component {
    constructor(props) {
        super(props);
        this.resizeCallback = null;
        this.registerResizeCallBack = this.registerResizeCallBack.bind(this);
        this.handleResize = this.handleResize.bind(this);
    }
    render() {
        if (this.props.entities.get('isLoading')){
            return <Loader
                 type="Puff"
                 color="#00BFFF"
                 height="100"
                 width="100"/>
        }
        return (
            <div>
                <LeadToolbar registerResizeCallBack={this.registerResizeCallBack} leads={this.props.entities.get('results')}
                             labels={this.props.labels.get('results')} fetchLables={this.props.fetchLables} fetchLeads={this.props.fetchLeads}
                             updateLeadLabels={this.props.updateLeadLabels} selectedLeads={this.props.selectedLead.get('selectedLeads')}/>
                <ul className="list-group">
                    {
                        this.props.entities.get('results').map((lead, i)=>
                            <Lead key={i} lead={lead} {...this.props} handleclick={this.handleclick}/>)
                    }
                </ul>
                {this.props.entities.get('pages') > 1 &&
                <Pager currentPage={this.props.entities.get('currentPage')}
                       totalPages={this.props.entities.get('pages')}
                       handlePageClick={this.props.handlePageClick} />}
            </div>
        )
    }
    componentDidMount() {
      let filters = localStorage.getItem("selectedFilters");
      filters = filters ? JSON.parse(filters) : [];

      if (filters.length){
          const args = filters.map((s) => (s.name));
          this.props.fetchLeads(1, {labels: args});
      } else {
          this.props.fetchLeads(1);
      }

      this.props.fetchLables();
      window.addEventListener("resize", this.handleResize);
    };

    componentWillUnmount() {
        window.removeEventListener("resize", this.handleResize);
        this.resizeCallback = null;
    }

    handleResize(e) {
        if (this.resizeCallback) this.resizeCallback(e);
    }

    registerResizeCallBack(f){
        this.resizeCallback = f
    }

}

export default Leads
