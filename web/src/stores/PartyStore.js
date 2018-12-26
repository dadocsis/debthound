import Immutable from 'immutable';
import {ReduceStore} from 'flux/utils';
import {ActionTypes} from '../Actions';
import dispatcher from '../Dispatcher'

class PartyStore extends ReduceStore{
    constructor() {
        super(dispatcher)
    }

    getInitialState() {
        return Immutable.Map({
            results: Immutable.List(),
            showBlacklist: true,
            isLoading: false,
            searchString: undefined
        });
    }

    reduce(state, action) {
        switch (action.type) {
            case ActionTypes.GET_PARTIES:
                return state.set('isLoading', true);

            case ActionTypes.RCV_PARTIES:
                return state.merge(Immutable.fromJS(action.response)).set('isLoading', false)
                    .set('currentPage', action.currentPage).set('searchString', action.searchString);

            case ActionTypes.PARTY_UPDATED:
                let parties = state.get("results").toJS();
                let thisPartyIdx = parties.findIndex(l => l.id === action.party.id);
                parties[thisPartyIdx] = action.party;
                return state.set("results", Immutable.fromJS(parties)).delete("updateParty");

            case ActionTypes.SHOW_BLACKLIST_PARTIES:
                return state.set("showBlacklist", action.value);

            case ActionTypes.UPDATE_PARTY:
                return state.set("updateParty", action.party);

          default:
            return state;
        }
    }
}

export default new PartyStore();