import { Route, Navigate } from 'react-router-dom'
import { useContext } from 'react'
import AuthContext from '../context/AuthContext'

const AnonRoute = ({children, ...rest}) => {
    let {user} = useContext(AuthContext)
    return(
        <div>{user ? <Navigate to="/in_search" /> :   children}</div>
    )
}

export default AnonRoute;