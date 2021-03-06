import React from 'react';
import { BrowserRouter as Router, Route, NavLink, Redirect } from "react-router-dom";
import Home from './components/HomePage'
import About from './components/AboutPage'
import Leads from './components/LeadsPage'
import AdminPage  from './components/AdminPage'
import LeadsStore from './stores/LeadsStore'
import SelectedLeadStore from './stores/SelectedLeadStore'
import LablesStore from './stores/LabelsStore'
import {Container} from 'flux/utils';
import './App.css';
import {fetchLeads, getDocsForLead, fetchLables, deleteLabel, deleteSchedule, updateParty,
        batchUpdateLeadLabels, updateLead, userLogin, fetchSchedules, fetchParties} from './data/DataManager';
import Actions from './Actions'
import DraftLabelStore from "./stores/DraftLabelStore";
import AuthenticatedUserStore from './stores/AuthenticatedUserStore'
import SchedulesStore from './stores/SchedulesStore'
import DraftScheduleStore from './stores/DraftScheduleStore'
import PartyStore from './stores/PartyStore'

const Header = (props) => {
    let isAuthed = !!props.isAuthed;
    let loggin_out = isAuthed ? 'Log Out' : 'Log In';
    let showNav = isAuthed ? 'nav-item' : 'nav-item invisible';
        return (
            <nav className="navbar navbar-expand-md navbar-dark bg-dark mb-1 navbar-expand-lg">
              <button className="navbar-toggler" type="button"
                      data-toggle="collapse"
                      data-target="#navbarSupportedContent"
                      aria-controls="navbarSupportedContent"
                      aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
              </button>
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav mr-auto">
                        <li className="nav-item">
                            <NavLink className="nav-link" to="/home">{loggin_out} </NavLink>
                        </li>
                        <li className="nav-item">
                            <NavLink className="nav-link" to="/about">About</NavLink>
                        </li>
                        <li className={showNav}>
                            <NavLink className="nav-link" to="/Leads">Leads</NavLink>
                        </li>
                        <li className={showNav}>
                            <NavLink className="nav-link" to="/Admin">Admin</NavLink>
                        </li>

                    </ul>

                </div>
            </nav>)
};


const routes = [
  {
    path: "/about",
    component: About,
    name: "About"
  },
  {
    path: "/",
    component: Home,
    name: "Home",
    exact: true
  },
    {
    path: "/Home",
    component: Home,
    name: "Home"
  },
  {
    path: "/Leads",
    component: Leads,
    name: "Leads",
    secure: true
  },
  {
    path: "/Admin",
    component: AdminPage,
    name: "Admin",
    secure: true
  }
];

const AppView = (props) => (
    <Router>
        <div>
            <Header isAuthed={props.authenticatedUser.get("username")}/>
        {
         routes.map((r, i) => {
             let state = props;
             return (
                 <Route key={i}
                        exact={r.exact}
                        path={r.path}
                        render={props => {
                            if (r.secure && !state.authenticatedUser.get("username")){
                                return <Redirect to='/Home'/>
                            }
                            return <r.component {...props} {...state}/>
                        }}
                 />
             )})
        }
        </div>
    </Router>
);

function getStores() {
  return [
    LeadsStore,
    SelectedLeadStore,
    LablesStore,
    DraftLabelStore,
    AuthenticatedUserStore,
    SchedulesStore,
    DraftScheduleStore,
    PartyStore
  ];
}


function getState() {

  return {
    entities: LeadsStore.getState(),
    selectedLead: SelectedLeadStore.getState(),
    fetchLeads,
    getDocsForLead: getDocsForLead,
    handlePageClick: (page, args) => fetchLeads(page, args),
    labels: LablesStore.getState(),
    createDraftLabel: Actions.createDraftLabel,
    draftLabel: DraftLabelStore.getState(),
    cancelLabel: Actions.cancelDraftLabel,
    draftLabelChange: Actions.draftLabelChange,
    saveDraftLabel: Actions.saveDraftLabel,
    fetchLables,
    deleteLabel,
    updateLeadLabels: batchUpdateLeadLabels,
    toggleLead: Actions.toggleLead,
    updateLead,
    authenticatedUser: AuthenticatedUserStore.getState(),
    userLogin,
    userLogout: Actions.userLoggedOut,
    createDraftSchedule: Actions.createDraftSchedule,
    saveDraftSchedule: Actions.saveDraftSchedule,
    cancelDraftSchedule: Actions.cancelDraftSchedule,
    fetchSchedules,
    schedules: SchedulesStore.getState(),
    draftSchedule: DraftScheduleStore.getState(),
    draftScheduleChange: Actions.draftScheduleChange,
    deleteSchedule,
    searchLeads: Actions.searchLeads,
    userApplyLables: Actions.userApplyLables,
    selectAllLeads: Actions.selectAllLeads,
    fetchParties,
    parties: PartyStore.getState(),
    updateParty,
    toggleBlackList: Actions.partyBlackListToggle
  };
}


const AppContainer = Container.createFunctional(AppView, getStores, getState);

export default AppContainer;
