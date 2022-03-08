import { Route, Navigate } from 'react-router-dom';
import { useContext } from 'react';
import AuthContext from '../context/AuthContext';

const PrivateRoute = ({children, ...rest}) => {
    let {user} = useContext(AuthContext)
    return(
        <div>{!user ? <Navigate to="/login" /> :   children}</div>
    )
}

export default PrivateRoute;