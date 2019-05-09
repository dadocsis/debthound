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
            case ActionTypes.GET_DOC_IMAGE:
                return state.merge(Map({image: {isLoading: true, id: action.id}}));
            case ActionTypes.RCV_DOC_IMAGE:
                let _id = state.get('image').id;
                let _fname = _id + action.fileType;
                return state.merge(Map({image: {
                    isLoading: false, imageData: action.url, imageFileName: _fname, id:_id}}));
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
            case ActionTypes.SELECT_ALL_LEADS:
                if (state.get('selectedLeads').length > 0) {
                    return state.set('selectedLeads', [])
                }
                return state.set('selectedLeads', action.leads);


            default:
                return state;
        }
    }
}

export default new SelectedLeadStore();