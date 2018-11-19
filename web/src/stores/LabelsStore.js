import Immutable from 'immutable';
import {ReduceStore} from 'flux/utils';
import {ActionTypes} from '../Actions';
import dispatcher from '../Dispatcher'
import {fromJS, Map} from "immutable/dist/immutable";


class LabelsStore extends ReduceStore{
    constructor() {
        super(dispatcher)
    }

    getInitialState() {
        return Immutable.Map({results: Immutable.List()});
    }

    reduce(state, action) {
        switch (action.type) {
            case ActionTypes.LABEL_CREATED:
                let results = state.get('results').push(Map(action.rsp.flag));
                return state.merge(Map({
                    isLoading: false,
                    results: results}));
            case ActionTypes.RCV_LABELS:
                return state.merge(Immutable.fromJS(action.rsp)).set('isLoading', false)
                    .set('currentPage', action.currentPage);
            case ActionTypes.GET_LABELS:
                return state.set('isLoading', true);
            case ActionTypes.LABEL_DELETED:
                let idx = state.get('results').findIndex((l, idx) => l.id === action.id);
                let newResults = state.get('results').delete(idx);
                return state.set('results', newResults);
            default:
                return state;
        }
    }
}

export default new LabelsStore();