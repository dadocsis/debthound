import React from 'react';
import Loader from "react-loader-spinner";
//import isAuthenticated from '../auth'
const HomePage = (props) =>
{
    let isLoading = props.authenticatedUser.get('isLoading');
    const login = (e) => {
        e.preventDefault();
        let formData = new FormData(e.target);
        props.userLogin(formData.get('username'), formData.get('password'))
    };
    return (
        <div className='container'>
            {props.authenticatedUser.get("username") &&
            <div className="jumbotron">
                <h1>Home</h1>
                <p>logged in user: <i>{props.authenticatedUser.get("username")}</i> </p>
                <button type="submit" className="btn btn-primary" onClick={props.userLogout}>LogOut</button>
            </div>
            }
            {!props.authenticatedUser.get("username") &&
            <div>
                <div className="jumbotron">
                    <h1>Login</h1>
                    <p>please login to app =)</p>
                </div>
                <div>
                    <form onSubmit={login}>
                        <div className="form-group">
                            <label htmlFor="exampleInputUserName">User Name</label>
                            <input type="test" className="form-control" id="exampleInputUserName" name='username'
                                   aria-describedby="emailHelp" placeholder="User name" required/>
                        </div>
                        <div className="form-group">
                            <label htmlFor="exampleInputPassword1">Password</label>
                            <input type="password" className="form-control" id="exampleInputPassword1" name='password'
                                   placeholder="Password" required/>
                        </div>
                        <button type="submit" className="btn btn-primary" disabled={isLoading}>Login</button>
                        { isLoading &&
                            <Loader
                                type="Puff"
                                color="#00BFFF"
                                height="50"
                                width="50"/>
                        }
                        { props.authenticatedUser.get('loginFailureMessage') &&
                            <div className="text-danger">
                                {props.authenticatedUser.get('loginFailureMessage')}
                            </div>
                        }
                    </form>
                </div>
            </div>
            }
        </div>
    )
};

export default HomePage