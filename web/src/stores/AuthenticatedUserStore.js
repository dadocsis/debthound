import Immutable from 'immutable';
import {ReduceStore} from 'flux/utils';
import {ActionTypes} from '../Actions';
import dispatcher from '../Dispatcher'

class LeadsStore extends ReduceStore{
    constructor() {
        super(dispatcher)
    }

    getInitialState() {
        return Immutable.Map({results: Immutable.List()});
    }

    reduce(state, action) {
        switch (action.type) {
            case ActionTypes.GET_LEADS:
                return state.set('isLoading', true);

            case ActionTypes.RCV_LEADS:
                return state.merge(Immutable.fromJS(action.response)).set('isLoading', false)
                    .set('currentPage', action.currentPage);

            case ActionTypes.LEAD_UPDATED:
                let leads = state.get("results").toJS();
                let thisLeadIdx = leads.findIndex(l => l.id === action.lead.id);
                leads[thisLeadIdx] = action.lead;
                return state.set("results", Immutable.fromJS(leads));

          default:
            return state;
        }
    }
}

export default new LeadsStore();