import React from 'react';
import { BrowserRouter as Router, Route, NavLink } from "react-router-dom";
import Home from './components/HomePage'
import About from './components/AboutPage'
import Leads from './components/LeadsPage'
import AdminPage  from './components/AdminPage'
import LeadsStore from './stores/LeadsStore'
import SelectedLeadStore from './stores/SelectedLeadStore'
import LablesStore from './stores/LabelsStore'
import {Container} from 'flux/utils';
import './App.css';
import {fetchLeads, getDocsForLead} from './data/DataManager'

const Header = (props) => (
    <nav className="navbar navbar-expand-md navbar-dark bg-dark mb-4">

        <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav mr-auto">
                <li className="nav-item">
                    <NavLink className="nav-link" to="/home">Home </NavLink>
                </li>
                <li className="nav-item">
                    <NavLink className="nav-link" to="/about">About</NavLink>
                </li>
                <li className="nav-item">
                    <NavLink className="nav-link" to="/Leads">Leads</NavLink>
                </li>
                <li className="nav-item">
                    <NavLink className="nav-link" to="/Admin">Admin</NavLink>
                </li>

            </ul>
            <form className="form-inline my-2 my-lg-0">
                <input className="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search"/>
                    <button className="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
            </form>
        </div>
    </nav>
);


const routes = [
  {
    path: "/about",
    component: About,
    name: "About"
  },
  {
    path: "/Home",
    component: Home,
    name: "Home",
  },
  {
    path: "/Leads",
    component: Leads,
    name: "Leads",
  },
  {
    path: "/Admin",
    component: AdminPage,
    name: "Admin",
  }
];

const AppView = (props) => (
    <Router>
        <div>
            <Header/>
        {
         routes.map((r, i) => {
         let state = props;
         return (
         <Route key={i}
                path={r.path}
                render={props => { return <r.component {...props} {...state}/>}}
         />)})}
        </div>
    </Router>
);

function getStores() {
  return [
    LeadsStore,
    SelectedLeadStore,
    LablesStore
  ];
}


function getState() {

  return {
    entities: LeadsStore.getState(),
    selectedLead: SelectedLeadStore.getState(),
    fetchLeads: (page) => fetchLeads(page),
    getDocsForLead: getDocsForLead,
    handlePageClick: (page) => fetchLeads(page),
    labels: LablesStore.getState()
  };
}

const AppContainer = Container.createFunctional(AppView, getStores, getState);

export default AppContainer;
