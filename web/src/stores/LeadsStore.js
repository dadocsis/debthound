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
          default:
            return state;
        }
    }
}

export default new LeadsStore();