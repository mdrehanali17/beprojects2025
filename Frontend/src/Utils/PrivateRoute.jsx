import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import AuthContext from '../Context/AuthContext';

const PrivateRoute = ({ element }) => {
    const { authTokens } = useContext(AuthContext);

    if (!authTokens) {
        return <Navigate to='/signin' />;
    }

    return element;
}

export default PrivateRoute;
