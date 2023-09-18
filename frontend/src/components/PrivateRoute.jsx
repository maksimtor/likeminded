import {  Navigate } from 'react-router-dom';
import React, { useContext } from 'react';
import AuthContext from '../context/AuthContext';

const PrivateRoute = ({ children }) => {
    let { user } = useContext(AuthContext)
    return (
        <div>{!user ? <Navigate to="/login" /> : children}</div>
    )
}

export default PrivateRoute;