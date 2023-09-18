import { useLocation, Navigate } from 'react-router-dom';
import React, { useContext } from 'react'
import AuthContext from '../context/AuthContext';

const RequireAnon = ({ children }) => {
  const location = useLocation();
  let { user } = useContext(AuthContext)

  if (user) {
    return <Navigate to='/in_search' state={{ from: location }} />
  }

  return children;
}

export { RequireAnon };