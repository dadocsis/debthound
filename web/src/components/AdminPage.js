import React from "react";
import { BrowserRouter as Router, Route, NavLink} from "react-router-dom";
import {COLORS, Label, MyMultiSelect, ordinal_suffix_of, WEEKDAYS, getDayOfWeek} from './Common'
import Loader from "react-loader-spinner";
import Pager from "./Pager";



const AdminHeader = (props) => (
    <ul className="nav nav-tabs" role="tablist">
        <li className="nav-item">
            <NavLink to='/Admin' exact activeClassName="active" className="nav-link">Labels</NavLink>
        </li>
        <li className="nav-item">
            <NavLink className="nav-link" activeClassName="active" to="/Admin/Schedules">Schedules</NavLink>
        </li>
        <li className="nav-item">
            <NavLink className="nav-link" activeClassName="active" to="/Admin/Parties">Party Administration</NavLink>
        </li>
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

const AddScheduleForm = props => {
    const siteOptions = props.sites.map((s, idx) => (<option key={idx} value={s.id}>{s.spider_name}</option>));
    const handleDaySelectChange = (selected) => (props.draftScheduleChange('days', selected));
    let dayOptions = WEEKDAYS.map((d, idx) => ({value: idx, label: d}));
    const handleFormSubmit = e => {
        e.preventDefault();
        props.saveDraftSchedule()


    };
    return(
    <form ref={form => this.formEl = form} onSubmit={(e) => handleFormSubmit(e, this.formEl)}
        className="mt-3">
        <div className="form-group row">
            <label className="col-form-label col-sm-1">Site</label>
            <div className="col-sm-3">
                <select name="site_id" className="form-control" defaultValue={props.draftSchedule.get("site_id")}
                        onChange={(e) => props.draftScheduleChange(e.target.name, e.target.value)} required>
                    {siteOptions}
                </select>
            </div>
        </div>
        <div className="form-group row">
            <label name="repeatFrequency" htmlFor="repeatSelect" className="col-form-label col-sm-1">Repeat Every:</label>
            <div className="col-sm-3">
                <select className="form-control" id="repeatSelect" defaultValue={props.draftSchedule.get("frequency")} name="frequency"
                        onChange={(e) => props.draftScheduleChange(e.target.name, e.target.value)}>
                    <option value="once">Run Once</option>
                    <option value="week">Weekly</option>
                    <option value="month">Monthly</option>
                </select>
            </div>
        </div>
        <div className="form-group row" >
            <label name="at" htmlFor="timeInput" className="col-form-label col-sm-1">On:</label>
            <div className="col-sm-2">
                {props.draftSchedule.get('frequency') !== 'week' && <input type="text" className="form-control" name="day" readOnly
                       value={props.draftSchedule.get("day")}
                       onChange={(e) => props.draftScheduleChange(e.target.name, e.target.value)} required/>}
            </div>
            <div className="col-sm-3">
                <input type="time" className="form-control" id="timeInput" name="time"
                       value={props.draftSchedule.get("time")}
                       onChange={(e) => props.draftScheduleChange(e.target.name, e.target.value)} required/>
            </div>
        </div>
        {props.draftSchedule.get('frequency') === 'week' &&
        <div className="form-group col">
            <MyMultiSelect className="form-control" name="days" overrideOptions={{showSubmitChangeButton: false}} options={dayOptions}
                           myChangeHandler={handleDaySelectChange}
                           overrideStrings={{selectSomeItems: "Select Day(s)"}}/>
            <div className="invalid-feedback">
                Please choose at least one day.
            </div>
        </div>}
        <div className="form-group row">
            <label className="col-form-label col-sm-1">Start Date:</label>
            <div className="col-sm-3">
                <input type="date" className="form-control" name="start"
                       value={props.draftSchedule.get("start")}
                       onChange={(e) => props.draftScheduleChange(e.target.name, e.target.value)} required/>
            </div>
        </div>
        <label className="col-form-label">End Date:</label>
        <div className="form-row">
            <div className="form-group col-md-6">
                <div className="form-check">
                    <input className="form-check-input" type="radio" name="endChoice" value="never"
                           checked={props.draftSchedule.get('endChoice') === "never"}
                           onChange={(e) => props.draftScheduleChange(e.target.name, e.target.value)}/>
                    <label className="form-check-label" htmlFor="exampleRadios1">
                        Never
                    </label>
                </div>
            </div>

        </div>
        <div className="form-row">
            <div className="form-group col-md-1">
                <div className="form-check">
                    <input className="form-check-input" type="radio" name="endChoice" value="on"
                        checked={props.draftSchedule.get('endChoice') === "on"}
                           onChange={(e) => props.draftScheduleChange(e.target.name, e.target.value)}/>
                    <label className="form-check-label" htmlFor="exampleRadios2">
                        On:
                    </label>
                </div>
            </div>
            <div className="form-group col-md-2">
                <input type="date" className="form-control ml-3" name="end"
                   value={props.draftSchedule.get("end")}
                   onChange={(e) => props.draftScheduleChange(e.target.name, e.target.value)} required/>
            </div>
        </div>
        <div className="btn-group">
            <button type="submit" className="btn btn-primary">Submit</button>
            <button type="button" className="btn btn-secondary" onClick={props.cancelDraftSchedule}>Cancel</button>
        </div>
    </form>)
};

class AdminLabels extends React.Component {

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
                            <li className="list-group-item" key={idx} ><Label label={l} deleteLabel={deleteLabel}/></li>)
                        )}
                    </ul>
                    <button onClick={this.props.createDraftLabel} type="button" className="btn btn-primary">New Label
                    </button>
                </div>
            );

        return <AddLabelForm {...{labels, cancelLabel, draftLabel, saveDraftLabel, draftLabelChange}}/>

    }
}

class AdminSchedules extends React.Component{

    componentDidMount() {
      this.props.fetchSchedules(1);
      this.deleteSchedule.bind(this)
    };

    deleteSchedule(e) {
        alert("todo: delete schedule")
    }

    getLocalTime(timeStr) {
        let utcdate = new Date('Feb 16, 1982 ' + timeStr + ' GMT+00:00');
        return utcdate.toLocaleTimeString();
        // let newDate = new Date(utcdate.getTime()+utcdate.getTimezoneOffset()*60*1000);
        // let offset = date.getTimezoneOffset() / 60;
        // let hours = date.getHours();
        //
        // newDate.setHours(hours - offset);
        //
        // return newDate;
    }

    render() {
        let {schedules, cancelDraftSchedule, draftSchedule, saveDraftSchedule,
            draftScheduleChange, deleteSchedule, fetchSchedules, createDraftSchedule} = this.props;
        let sites = schedules.get('sites').toJS();
        let isLoading = schedules.get('isLoading') === true;
        if (!draftSchedule.get('id'))
            return (

                <div>
                    { isLoading &&
            <Loader
                type="Puff"
                color="#00BFFF"
                height="50"
                width="50"/>
                }
                    {!isLoading &&
                    <table className="table table-sm">
                        <thead>
                        <tr>
                            <th>Site</th>
                            <th>Frequency</th>
                            <th>On</th>
                            <th>Start Date</th>
                            <th>End Date</th>
                            <th></th>
                        </tr>
                        </thead>
                        <tbody>
                        {schedules.get("results").toJS().map((s, idx) => (
                            <tr key={idx}>
                                <td>{s.site.spider_name}</td>
                                <td>{s.exact && "Monthly" || "Weekly"}</td>
                                <td>{s.exact && ordinal_suffix_of(s.day) + this.getLocalTime(s.time) || getDayOfWeek(s.day-1) +' '+ this.getLocalTime(s.time)}</td>
                                <td>{s.start}</td>
                                <td>{s.end}</td>
                                <td><i className="fas fa-times" onClick={e => deleteSchedule(s.id)}></i></td>
                            </tr>))}
                        </tbody>
                    </table>
                    }
                    <button onClick={e => createDraftSchedule(sites)} type="button" className="btn btn-primary">New Schedule</button>
                </div>
            );

        return <AddScheduleForm {...{cancelDraftSchedule, draftSchedule, saveDraftSchedule, draftScheduleChange,
            fetchSchedules, createDraftSchedule, sites}}/>

    }


}

class PartyAdmin extends React.Component {

    componentDidMount() {
        this.props.fetchParties(1);
        this.handleSearch = this.handleSearch.bind(this);
        this.handleShowBlackListToggle = this.handleShowBlackListToggle.bind(this);
        this.handleBlackListToggle = this.handleBlackListToggle.bind(this);
        this.handlePager = this.handlePager.bind(this);
        this.enterKey = this.enterKey.bind(this);
    };

    handleSearch(searchStr) {
        let args = {};
        if (this.props.parties.get('showBlacklist') === false){
            args.showBlacklist = false;
        }
        if (searchStr.length > 2) {
            args.searchString = searchStr;
            this.props.fetchParties(1, {...args});
        }
        else if (searchStr.length === 0){
            delete args.searchString;
            this.props.fetchParties(1, {...args});
        }
    }

    handleShowBlackListToggle(e){
        this.props.toggleBlackList(e.target.checked);
        let that = this;
        setTimeout(function () {
            that.handleSearch(that.props.parties.get('searchString') || '')
        }, 300);
        //this.handleSearch(this.props.parties.get('searchString') || '');
    }

    handleBlackListToggle(party, on){
        party.black_listed = on;
        this.props.updateParty(party);
    }

    enterKey(e){
        if (e.key === 'Enter') {
            let args = {};
            args.searchString = e.target.value;
            if (this.props.parties.get('showBlacklist') === false){
                args.showBlacklist = false;
            }
            if (args.searchString.length > 0) {
                this.props.fetchParties(1, {...args});
            }
            else if (args.searchString.length === 0){
                delete args.searchString;
                this.props.fetchParties(1, {...args});
            }
        }
    }

    handlePager(page) {
        let args = {};
        let searchStr = this.props.parties.get('searchString');

        if (this.props.parties.get('showBlacklist') === false){
            args.showBlacklist = false;
        }
        if (searchStr && searchStr.length > 0) {
            args.searchString = searchStr;
        }

        this.props.fetchParties(page, {...args})
    }

    render() {
        let isLoading = this.props.parties.get('isLoading') === true;
        let loadingParty = this.props.parties.get('updateParty');
        return (
            <div>
                <div>
                    <div className="mt-2 col-lg-12">
                        <input type="text" placeholder="Search" className="w-50"
                               onChange={e => this.handleSearch(e.target.value)} onKeyPress={this.enterKey}/>
                        <input type="checkbox" checked={this.props.parties.get('showBlacklist') === true}
                               onChange={this.handleShowBlackListToggle}/> <label>Show Black Listed Parties</label>
                    </div>
                {
                isLoading &&
                    <Loader
                        type="Puff"
                        color="#00BFFF"
                        height="50"
                        width="50"/>
                }
                    {
                        !isLoading &&
                         <div>
                            <table className="table table-sm">
                                <thead>
                                <tr>
                                    <th>Party Name</th>
                                    <th>BlackList</th>
                                </tr>
                                </thead>
                                <tbody>
                                {this.props.parties.get("results").toJS().map((s, idx) => {
                                    let partyid = loadingParty ? loadingParty.id : undefined
                                    let isUpdating = s.id === partyid;
                                    return (
                                    <tr key={idx}>
                                        <td>{s.name}</td>
                                        <td>
                                            {!isUpdating &&
                                            <input type="checkbox" name="black_listed"
                                                   checked={s.black_listed}
                                                   onChange={(e) => this.handleBlackListToggle(s, e.target.checked)}/>
                                            }
                                            { isUpdating &&
                                                <Loader
                                                    type="Puff"
                                                    color="#00BFFF"
                                                    height="15"
                                                    width="15"/>
                                            }
                                        </td>
                                    </tr>)})

                                }
                                </tbody>
                            </table>

                            {this.props.parties.get('pages') > 1 &&
                                <Pager currentPage={this.props.parties.get('currentPage')}
                                       totalPages={this.props.parties.get('pages')}
                                       handlePageClick={this.handlePager} />}
                       </div>
                    }
                </div>

            </div>
        )
    }
}

const AdminPage = props => (
    <div className="container">
        <AdminHeader/>
        <Route path="/Admin" exact={true}
               render={routeProps => (<AdminLabels {...routeProps} {...props}/>)}/>
        <Route path="/Admin/Schedules"
               render={routeProps => (<AdminSchedules {...routeProps} {...props}/>)}/>
        <Route path="/Admin/Parties"
               render={routeProps => (<PartyAdmin {...routeProps} {...props}/>)}/>
    </div>
);

export default AdminPage;