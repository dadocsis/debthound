import Immutable from 'immutable';
import {ReduceStore} from 'flux/utils';
import {ActionTypes} from '../Actions';
import dispatcher from '../Dispatcher'
import {fromJS, Map} from "immutable/dist/immutable";
import {saveDraftlabel} from '../data/DataManager'


class DraftLabelStore extends ReduceStore{
    constructor() {
        super(dispatcher)
    }

    getInitialState() {
        return Map();
    }

    reduce(state, action) {
        switch (action.type) {
            case ActionTypes.DRAFT_LABEL:
                return state.set('id', -1);
            case ActionTypes.CANCEL_LABEL:
                return state.set('id', null);
            case ActionTypes.DRAFT_LABEL_CHANGE:
                return state.merge(action.data);
            case ActionTypes.CREATE_LABEL:
                let label = state.toJS();
                delete label['id'];
                saveDraftlabel(label);
                return Map();
            default:
                return state;
        }
        return state;
    }
}

export default new DraftLabelStore();