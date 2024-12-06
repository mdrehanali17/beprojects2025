import React, { useEffect, useState, useContext } from 'react';
import { useLocation, useNavigate} from 'react-router-dom';
import AuthContext from '../Context/AuthContext';

const PaymentSuccess = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [message, setMessage] = useState('');
    const [alertType, setAlertType] = useState('alert-info'); 
    const { user } = useContext(AuthContext);


    useEffect(() => {
        const queryParams = new URLSearchParams(location.search);
        const status = queryParams.get('status');
        
        switch (status) {
            case 'NOT_FOUND':
                setMessage('Payment not found. Please contact support.');
                setAlertType('alert-danger');
                break;
            case 'COMPLETE':
                setMessage('Payment was successful!');
                setAlertType('alert-success');
                break;
            default:
                setMessage('Unknown status. Please contact support.');
                setAlertType('alert-warning');
                break;
        }

        // Redirect to booking history page after 5 seconds
        const timer = setTimeout(() => {
            navigate(`/user/${user.id}/bookingHistory`);
        }, 5000);

        // Cleanup the timeout on component unmount
        return () => clearTimeout(timer);
    }, [location.search, navigate]);

    return (
        <div className="container mt-4 d-flex justify-content-center">
            <div className={`alert ${alertType}`} role="alert">
                {message}
            </div>
        </div>
    );
};

export default PaymentSuccess;
