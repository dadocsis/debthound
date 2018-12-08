import Immutable from 'immutable';
import {ReduceStore} from 'flux/utils';
import {ActionTypes} from '../Actions';
import dispatcher from '../Dispatcher'
import {fromJS, Map} from "immutable/dist/immutable";
import {saveDraftSchedule} from '../data/DataManager';
import {ordinal_suffix_of} from '../components/Common'


class DraftScheduleStore extends ReduceStore{
    constructor() {
        super(dispatcher)
    }

    getInitialState() {
        return Map();
    }

    reduce(state, action) {
        switch (action.type) {
            case ActionTypes.CREATE_DRAFT_SCHEDULE:
                const now = new Date();
                const timeStr = now.getHours().toString() + ':' +
                    ('0' + now.getMinutes().toString()).substring(('0' + now.getMinutes().toString()).length - 2);
                const dateStr = now.getFullYear().toString() + '-' + (now.getMonth() + 1).toString() + '-' + now.getDate().toString();
                return fromJS({
                    id: -1,
                    frequency: 'once',
                    site_id: action.site,
                    start: dateStr,
                    end: dateStr,
                    time: timeStr,
                    endChoice: "never",
                    day: ordinal_suffix_of(now.getDate())
                });
            case ActionTypes.CANCEL_SCHEDULE:
                return state.set('id', null);
            case ActionTypes.DRAFT_SCHEDULE_CHANGE:
                return state.merge(action.data);
            case ActionTypes.CREATE_SCHEDULE:
                let sched = state.toJS();
                delete sched['id'];
                const ts = "T01:00";
                let data = {};

                sched.end = sched.endChoice === "never" ? "9999-12-31" : sched.end + ts;
                data.exact = "once month".includes(sched.frequency);
                data.site_id = sched.site_id;
                data.start = new Date(sched.start + ts).toISOString().substring(0,10);
                data.end = new Date(sched.end + ts).toISOString().substring(0, 10);
                data.time = new Date("2018-01-01T" + sched.time + ":00").toISOString().substring(11,19);
                data.day = data.exact ?  parseInt(sched.day.substring(0,2)) : sched.days;
                console.log(data)
                // todo: break out multiple scheds if exact is false (data.day will be an array)
                let schedules = [];
                if (Array.isArray(data.day)){
                    for (let d of data.day){
                        schedules.push({
                            exact: data.exact,
                            site_id: data.site_id,
                            start: data.start,
                            end: data.end,
                            time: data.time,
                            day: ++d //I believe the server expects date from 1(mon) - 7(sun)
                        })
                    }
                }else  {
                    schedules.push(data)
                }
                saveDraftSchedule(schedules);
                return Map();
            default:
                return state;
        }
        return state;
    }
}

export default new DraftScheduleStore();