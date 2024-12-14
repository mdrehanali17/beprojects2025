import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [authTokens, setAuthTokens] = useState(() =>
        localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null
    );
    const [user, setUser] = useState(() =>
        localStorage.getItem('authTokens') ? jwtDecode(localStorage.getItem('authTokens')) : null
    );
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    const signinUser = async (email, password) => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/signin/', {
                email: email,
                password: password,
            });

            const data = response.data;

            if (response.status === 200) {
                setAuthTokens(data);
                const decodedToken = jwtDecode(data.access);

                // Fetch additional user details from backend after successful login
                const userDetailsResponse = await axios.get(`http://127.0.0.1:8000/api/users/${decodedToken.user_id}/`);
                const userDetails = userDetailsResponse.data;

                // Update user object with additional details (phone_number, id, etc.)
                setUser(prevUser => ({
                    ...prevUser,
                    id: userDetails.id,
                    username: userDetails.username,
                    phone_number: userDetails.phone_number,
                }));

                localStorage.setItem('authTokens', JSON.stringify(data));
                navigate('/');
            } else {
                alert('Something went wrong!');
            }
        } catch (error) {
            console.error('Login error:', error);
        }
    };

    const logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
        navigate('/signin');
    };

    useEffect(() => {
        if (authTokens) {
            const decodedToken = jwtDecode(authTokens.access);

            if (decodedToken.exp * 1000 < Date.now()) {
                // Token is expired, log out user
                logoutUser();
            } else {
                // Fetch additional user details after token refresh or initial load
                const fetchUserDetails = async () => {
                    try {
                        const userDetailsResponse = await axios.get(`http://127.0.0.1:8000/api/users/${decodedToken.user_id}/`);
                        const userDetails = userDetailsResponse.data;

                        setUser(prevUser => ({
                            ...prevUser,
                            id: userDetails.id,
                            username: userDetails.username,
                            phone_number: userDetails.phone_number,
                        }));
                    } catch (error) {
                        console.error('Error fetching user details:', error);
                    } finally {
                        setLoading(false);
                    }
                };

                fetchUserDetails();
            }
        } else {
            setLoading(false);
        }
    }, [authTokens]);

    const contextData = {
        user,
        authTokens,
        signinUser,
        logoutUser,
    };

    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return React.useContext(AuthContext);
};

export default AuthContext;
