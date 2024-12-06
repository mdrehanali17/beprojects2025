import React, { useState, useContext } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import CustomDatePicker from '../Utils/CustomDatePicker'; // Ensure availability
import AuthContext from '../Context/AuthContext'; // Authentication context

const SportBooking = ({ sport_custom_id, sport_category, handleClose }) => {
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedStartTime, setSelectedStartTime] = useState('');
  const [selectedEndTime, setSelectedEndTime] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('esewa');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [message, setMessage] = useState('');
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  const handleBooking = async (e) => {
    e.preventDefault();

    if (!selectedDate || !selectedStartTime || !selectedEndTime) {
      setErrorMessage('Please select date and time.');
      return;
    }

    const formattedDate = formatDate(selectedDate);
    const availabilityCheckData = {
      sport_custom_id,
      date: formattedDate,
      start_time: selectedStartTime,
      end_time: selectedEndTime,
    };

    try {
      setLoading(true);
      setErrorMessage('');
      setMessage('');

      // Check availability
      const availabilityResponse = await axios.post('http://127.0.0.1:8000/api/availability/', availabilityCheckData);

      if (availabilityResponse.status === 200) {
        const bookingData = {
          user_id: user.id,
          phone_number: user.phone_number,
          sport_custom_id,
          sport_category,
          date: formattedDate,
          start_time: selectedStartTime,
          end_time: selectedEndTime,
          payment_method: paymentMethod,
        };

        if (paymentMethod === 'cash') {
          const cashPaymentResponse = await axios.post('http://127.0.0.1:8000/api/initiate-payment/',bookingData);

          if (cashPaymentResponse.status === 201) {
            setMessage('Booking successful with cash payment.');
            navigate(`/user/${user.id}/bookingHistory`);
          } else {
            setErrorMessage('Failed to book with cash payment. Please try again.');
          }
        } else if (paymentMethod === 'esewa') {
          const initiatePaymentResponse = await axios.post('http://127.0.0.1:8000/api/initiate-payment/',bookingData);

          if (initiatePaymentResponse.status === 200) {
            const esewaRedirectUrl = initiatePaymentResponse.data.redirectUrl;
            window.location.href = esewaRedirectUrl;
          } else {
            setErrorMessage('Failed to initiate payment with eSewa. Please try again.');
          }
        }
      } else {
        setErrorMessage('The selected slot is not available. Please choose a different time.');
      }
    } catch (error) {
      if (error.response && error.response.data.message) {
        setErrorMessage(error.response.data.message);
      } else {
        setErrorMessage('An error occurred. Please try again later.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <form onSubmit={handleBooking} className="container-without-background shadow-lg mt-2 p-3">
        <div className="form-group mb-2">
          <label>Select Date:</label>
          <CustomDatePicker selectedDate={selectedDate} onChange={(date) => setSelectedDate(date)} />
        </div>
        <div className="form-group mb-2">
          <label>From:</label>
          <input
            type="time"
            className="form-control"
            value={selectedStartTime}
            onChange={(e) => setSelectedStartTime(e.target.value)}
            disabled={loading}
          />
        </div>
        <div className="form-group mb-2">
          <label>To:</label>
          <input
            type="time"
            className="form-control"
            value={selectedEndTime}
            onChange={(e) => setSelectedEndTime(e.target.value)}
            disabled={loading}
          />
        </div>
        <div className="form-group mb-2">
          <label>Payment Method:</label>
          <select
            className="form-control"
            value={paymentMethod}
            onChange={(e) => setPaymentMethod(e.target.value)}
            disabled={loading}
          >
            <option value="esewa">eSewa</option>
            <option value="cash">Cash</option>
          </select>
        </div>

        {errorMessage && <div className="alert alert-danger mb-2">{errorMessage}</div>}
        {message && <div className="alert alert-success mb-2">{message}</div>}

        <div className="text-center">
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Booking...' : 'Book Now'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default SportBooking;
