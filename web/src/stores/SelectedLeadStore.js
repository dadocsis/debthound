import {Map, fromJS} from 'immutable';
import {ReduceStore} from 'flux/utils';
import {ActionTypes} from '../Actions';
import dispatcher from '../Dispatcher'

class SelectedLeadStore extends ReduceStore{
    constructor() {
        super(dispatcher)
    }

    getInitialState() {
        return Map({selectedLeads: []});
    }

    reduce(state, action) {
        switch (action.type) {
            case ActionTypes.VIEW_LEAD:
                return state.merge(Map({isLoading: action.id !== -1, id: action.id}));
            case ActionTypes.RCV_LEAD_DOCS:
                return state.merge(Map({
                    docs: fromJS(action.docs),
                    isLoading: false,
                    currentPage: action.currentPage
                }));
            case ActionTypes.TOGGLE_LEAD:
                let selectedLeads = state.get('selectedLeads');
                let newSelected = [];
                newSelected.push(action.lead);
                if (selectedLeads) {
                    let found = selectedLeads.find(l => l.id === action.lead.id);
                    if (found){
                        newSelected = selectedLeads.filter(l => l.id !== found.id);
                    } else {
                        newSelected = selectedLeads.concat(newSelected);
                    }
                }
                return state.merge(Map({selectedLeads: newSelected}));
            default:
                return state;
        }
    }
}

export default new SelectedLeadStore();