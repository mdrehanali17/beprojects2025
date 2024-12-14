import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';


const Signup = () => {
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        username: '',
        password: '',
        phone_number: ''
    });

    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();

    const handleChange = (event) => {
        setFormData({
            ...formData,
            [event.target.id]: event.target.value
        });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            await axios.post('http://127.0.0.1:8000/api/signup/', formData);
            setSuccessMessage('Signup successful! Redirecting to signin page...');
            setTimeout(() => {
                navigate('/signin');
            }, 3000);
        } catch (error) {
            if (error.response) {
                setErrorMessage(error.response.data.error || 'Error signing up. Please try again.');
            } else {
                setErrorMessage('Error signing up. Please try again.');
            }
        }
    };

    return (
        <div className="auth-containerUp">
            {successMessage && <div className="alert alert-success">{successMessage}</div>}
            <div className='auth-box'>
                <h2 className='text-center mb-4'>Sign Up</h2>
                {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}
                <form onSubmit={handleSubmit}>
                    <div className='form-group mb-3'>
                        <label>Full Name</label>
                        <input type='text' id='first_name' placeholder='Enter your first name' className='form-control' onChange={handleChange} required />
                    </div>
                    <div className='form-group mb-3'>
                        <label>Email</label>
                        <input type='email' id='email' placeholder='Enter your email' className='form-control' onChange={handleChange} required />
                    </div>
                    <div className='form-group mb-3'>
                        <label>Username</label>
                        <input type='text' id='username' placeholder='Enter your username' className='form-control' onChange={handleChange} required />
                    </div>
                    <div className='form-group mb-3'>
                        <label>Password</label>
                        <input type='password' id='password' placeholder='Enter your password' className='form-control' onChange={handleChange} required />
                    </div>
                    <div className='form-group mb-3'>
                        <label>Phone Number</label>
                        <input type='text' id='phone_number' placeholder='Enter your phone number' className='form-control' onChange={handleChange} required />
                    </div>
                    <button type='submit' className='btn btn-primary w-100'>Sign Up</button>
                    <div className='divider'>
                        <span>or</span>
                    </div>
                    <div className='text-center mt-3'>
                        <p>Already have an account? <Link to='/signin'>Sign in</Link></p>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Signup;