import React from "react";
import Loader from 'react-loader-spinner'
import Pager from './Pager'


const LeadDocs = (props) => {
    let staged = {};
    props.docs.forEach((d, idx) =>{
        if (!staged[d.getIn(['doc_type','id'])]) {
            staged[d.getIn(['doc_type','id'])] = {docype: d.get('doc_type'), docs: []};
        }
        let docgroup = staged[d.getIn(['doc_type','id'])];
        docgroup.docs.push(d)
    });
    let markup = [];
    for (let k in staged){
        let t = (
        <table className="table table-sm" key={k}>
            <thead>
            <caption>{staged[k].docype.get('description')}</caption>
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
            {staged[k].docs.map((d =>
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
        markup.push(t);
    }
    return markup;
};

const Lead = (props) => {
    let selectedLead = props.lead.get('id') === props.selectedLead.get('id');
    let isLoading = selectedLead && props.selectedLead.get('isLoading') === true;
    let loader = isLoading && <Loader
                                type="Puff"
                                color="#00BFFF"
                                height="50"
                                width="50"
                              />;
    if (loader) return loader;


    let li = (<li className="list-group-item list-group-item-action"
                onClick={(e) => props.getDocsForLead(props.lead.get('id'))}
                 id={props.lead.get('id')}> {props.lead.get('name')}
            <span className="badge badge-primary badge-pill">{props.lead.get('document_facts').size}</span>
        { selectedLead &&
            <LeadDocs docs={props.selectedLead.get('docs')} />
        }
             </li>);

    if (props.lead.get('id') === props.selectedLead.get('id')) {
        if (props.selectedLead.get('isLoading') === true)
            return (<Loader
                type="Puff"
                color="#00BFFF"
                height="50"
                width="50"/>);
        //return (li)
    }
    return li
};

class Leads extends React.Component {
    // state = {entities: []}
    constructor(props) {
        super(props);
    }

    render() {
        if (this.props.entities.get('isLoading')){
            return <Loader
                 type="Puff"
                 color="#00BFFF"
                 height="100"
                 width="100"/>
        }
        return this.props.entities.get('results').size > 0 && (
            <div>
                <ul className="list-group">
                    {
                        this.props.entities.get('results').map((lead, i)=>
                            <Lead key={i} lead={lead} {...this.props} handleclick={this.handleclick}/>)
                    }
                </ul>
                <Pager currentPage={this.props.entities.get('currentPage')}
                       totalPages={this.props.entities.get('pages')}
                       handlePageClick={this.props.handlePageClick} />
            </div>
        )
    }
    componentDidMount() {
      this.props.fetchLeads(1)
    };

}

export default Leads