import {Map, fromJS} from 'immutable';
import {ReduceStore} from 'flux/utils';
import {ActionTypes} from '../Actions';
import dispatcher from '../Dispatcher'

class SelectedLeadStore extends ReduceStore{
    constructor() {
        super(dispatcher)
    }

    getInitialState() {
        return Map();
    }

    reduce(state, action) {
        switch (action.type) {
            case ActionTypes.VIEW_LEAD:
                return state.merge(Map({isLoading: true, id: action.id}));
            case ActionTypes.RCV_LEAD_DOCS:
                return state.merge(Map({
                    docs: fromJS(action.docs),
                    isLoading: false,
                    currentPage: action.currentPage
                }));

            default:
                return state;
        }
    }
}

export default new SelectedLeadStore();