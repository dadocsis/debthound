import Immutable from 'immutable';
import {ReduceStore} from 'flux/utils';
import {ActionTypes} from '../Actions';
import dispatcher from '../Dispatcher'
import {fromJS, Map} from "immutable/dist/immutable";


class SchedulesStore extends ReduceStore{
    constructor() {
        super(dispatcher)
    }

    getInitialState() {
        return Immutable.Map({results: Immutable.List(), sites: Immutable.List()});
    }

    reduce(state, action) {
        switch (action.type) {
            case ActionTypes.SCHEDULE_CREATED:
                let results = state.get('results').push(Map(action.rsp));
                return state.merge(Map({
                    isLoading: false,
                    results: results}));
            case ActionTypes.RCV_SCHEDULES:
                return state.merge(Immutable.fromJS(action.rsp)).set('isLoading', false)
                    .set('currentPage', action.currentPage);
            case ActionTypes.GET_SCHEDULES:
                return state.set('isLoading', true);
            case ActionTypes.SCHEDULE_DELETED:
                let _idx = state.get('results').findIndex((l, idx) => l.get('id') === action.id);
                let newResults = state.get('results').delete(_idx);
                return state.set('results', newResults);
            case ActionTypes.RCV_SITES:
                return state.set('sites', Immutable.fromJS(action.rsp));
            default:
                return state;
        }
    }
}

export default new SchedulesStore();