import React, { useState, useEffect } from 'react';

const PaymentFailure = () => {
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        setErrorMessage("Error in Esewa Server. Please try again after sometime!");
    }, []);

    return (
        <div className="container mt-4">
            <div className="alert alert-danger" role="alert">
                {errorMessage}
            </div>
        </div>
    );
};

export default PaymentFailure;
