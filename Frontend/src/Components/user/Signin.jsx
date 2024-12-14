import React, { useState, useContext } from 'react';
import '../../App.css';
import { Link } from 'react-router-dom';
import AuthContext from '../../Context/AuthContext';


const Signin = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    const { signinUser } = useContext(AuthContext);

    const submitHandler = async (event) => {
        event.preventDefault();

        try {
            await signinUser(username, password);
        } catch (error) {
            console.error("Signin error:", error);
            if (error.response && error.response.status === 401) {
                setErrorMessage("Invalid credentials. Please enter correct username/email and password.");
            } else {
                setErrorMessage("Something went wrong. Please try again later.");
            }
        }
    };

    return (
        <div className="auth-container">
            <div className='auth-box'>
                <h2 className='text-center mb-4'>Sign In</h2>
                {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}
                <form onSubmit={submitHandler}>
                    <div className='mb-3'>
                        <label><strong>Email</strong></label>
                        <input
                            type='text'
                            placeholder='Enter your email'
                            className='form-control'
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div className='mb-3'>
                        <label><strong>Password</strong></label>
                        <input
                            type='password'
                            placeholder='Enter your password'
                            className='form-control'
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button type='submit' className='btn btn-primary w-100'>Sign In</button>
                    <div className='divider'>
                        <span>or</span>
                    </div>
                    <div className='text-center mt-3'>
                        <p>Do not have an account? <Link to='/signup'>Sign up</Link></p>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default Signin;