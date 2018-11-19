import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import {COLORS, Label} from './Common'



const AdminHeader = (props) => (
    <ul className="nav nav-tabs" role="tablist">
        <li className="nav-item">
            <Link to='/Admin/Labels' className="nav-link">Labels</Link>
        </li>
        {/*<li className="nav-item">*/}
            {/*<a className="nav-link" href="#">Link</a>*/}
        {/*</li>*/}
        {/*<li className="nav-item">*/}
            {/*<a className="nav-link" href="#">Link</a>*/}
        {/*</li>*/}
        {/*<li className="nav-item">*/}
            {/*<a className="nav-link disabled" href="#">Disabled</a>*/}
        {/*</li>*/}
    </ul>);



const AddLabelForm = props => {
    let colorOptions = [(<option key='' value={''}>{"Select a color"}</option>)];
    for (let k in COLORS) colorOptions.push(<option key={k} value={COLORS[k]}>{COLORS[k]}</option>);
    return(
    <form ref={form => this.formEl = form} onSubmit={(e) => props.saveDraftLabel(e, this.formEl)}>
        <div className="form-group">
            <label htmlFor="inputLabelName">Label Name</label>
            <input name="name" type="text" className="form-control" id="inputLabelName" aria-describedby="emailHelp"
                   placeholder="Label Name" onChange={(e) => props.draftLabelChange(e.target.name, e.target.value)} required/>
        </div>
        <div className="form-group">
            <label htmlFor="colorSelect">Select Color</label>
            <select name="description" className="form-control form-control-sm" id="colorSelect" onChange={(e) => props.draftLabelChange(e.target.name, e.target.value)} required>
                {colorOptions}
            </select>
            <div className="invalid-feedback">
                Please choose a color.
            </div>
        </div>
        <button type="submit" className="btn btn-primary">Submit</button>
        <button type="button" className="btn btn-secondary" onClick={props.cancelLabel}>Cancel</button>
    </form>)
};

class AdminLabels extends React.Component{

    componentDidMount() {
      this.props.fetchLables(1)
    };

    render() {
        let {labels, cancelLabel, draftLabel, saveDraftLabel, draftLabelChange, deleteLabel} = this.props;
        if (!this.props.draftLabel.get('id'))
            return (
                <div>
                    <ul className="list-group">
                        {this.props.labels.get('results').map((l, idx) => (
                            <li className="list-group-item"><Label key={idx} label={l} deleteLabel={deleteLabel}/></li>)
                        )}
                    </ul>
                    <button onClick={this.props.createDraftLabel} type="button" className="btn btn-primary">New Label</button>
                </div>
            );

        return <AddLabelForm {...{labels, cancelLabel, draftLabel, saveDraftLabel, draftLabelChange}}/>

    }

}

const AdminPage = props => (
    <div className="container">
        <AdminHeader/>
        <Route path="/Admin/Labels"
               render={routeProps => (<AdminLabels {...routeProps} {...props}/>)}/>
    </div>
);

export default AdminPage;