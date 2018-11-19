import Immutable from 'immutable';
import {ReduceStore} from 'flux/utils';
import {ActionTypes} from '../Actions';
import dispatcher from '../Dispatcher'

class AuthenticatedUserStore extends ReduceStore{
    constructor() {
        super(dispatcher)
    }

    getInitialState() {
        const access_token = localStorage.getItem("access_token") ? JSON.parse(localStorage.getItem("access_token")) : null;
        const refresh_token = localStorage.getItem("refresh_token") ? JSON.parse(localStorage.getItem("refresh_token")) : null;
        const userName = localStorage.getItem("username") ? JSON.parse(localStorage.getItem("username")) : null;
        const userId = localStorage.getItem("userid") ? JSON.parse(localStorage.getItem("userid")) : null;
        return Immutable.Map({
            accessToken: access_token,
            refreshToken: refresh_token,
            username: userName,
            userid: userId
        });
    }

    reduce(state, action) {
        switch (action.type) {
            case ActionTypes.USER_LOGGED_IN:
                if (action.loginFailureMessage) {
                    return state.set('isLoading', false).set('loginFailureMessage', action.loginFailureMessage);
                }else {
                    localStorage.setItem('access_token', JSON.stringify(action.userData.access_token));
                    localStorage.setItem('refresh_token', JSON.stringify(action.userData.refresh_token));
                    localStorage.setItem('username', JSON.stringify(action.userData.username));
                    localStorage.setItem('userid', JSON.stringify(action.userData.userid));
                    return state.merge(Immutable.Map(action.userData)).set('isLoading', false).set('loginFailureMessage', null);
                }
            case ActionTypes.USER_LOGGING_IN:
                return state.set('isLoading', true);
            case ActionTypes.USER_LOGGED_OUT:
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('username');
                localStorage.removeItem('userid');
                return this.getInitialState();

          default:
            return state;
        }
    }
}

export default new AuthenticatedUserStore();