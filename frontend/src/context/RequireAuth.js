import { useLocation, Navigate } from 'react-router-dom';
import React, { useContext } from 'react'
import AuthContext from '../context/AuthContext';

const RequireAuth = ({ children }) => {
  const location = useLocation();
  let { user } = useContext(AuthContext)

  if (!user) {
    return <Navigate to='/login' state={{ from: location }} />
  }

  return children;
}

export { RequireAuth };