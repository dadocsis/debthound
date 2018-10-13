import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import AboutPage from "./AboutPage";

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

const Label = props => (<li className="list-group-item">{props.label.get('name')}</li>);

const AddLabelForm = props => (
                <form>
                        <div className="form-group">
                            <label htmlFor="inputLabelName">Label Name</label>
                            <input type="email" className="form-control" id="inputLabelName" aria-describedby="emailHelp"
                                   placeholder="Label Name"/>
                        </div>
                        <div className="form-group">
                            <label htmlFor="colorSelect">Select Color</label>
                            <select className="form-control form-control-sm" id="colorSelect">
                                <option>Yellow</option>
                            </select>
                        </div>
                        <button type="submit" className="btn btn-primary">Submit</button>
                </form>
        );

class AdminLabels extends React.Component{

    constructor(props){
        super(props);
        this.createLabel.bind(this);
    }

    createLabel(page){
        alert("Create Label")
        //his.props.handlePageClick(page);
    }

    render() {
        console.log(this.props.labels);
        if (this.props.labels.size > 0)
            return (
                <ul className="list-group">
                    {this.props.labels.toJS().map((l, idx) => (<Label key={idx} lable={l}/>))}
                </ul>
            );

        return <AddLabelForm/>

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