import { Navigate } from 'react-router-dom'
import React, { useContext } from 'react'
import AuthContext from '../context/AuthContext'

const AnonRoute = ({ children }) => {
    let { user } = useContext(AuthContext)
    return (
        <div>{user ? <Navigate to="/in_search" /> : children}</div>
    )
}

export default AnonRoute;