import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import AuthContext from '../Context/AuthContext';
import Pagination from 'react-bootstrap/Pagination';
import "../App.css";

const BookingHistory = () => {
    const [bookings, setBookings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [bookingsPerPage] = useState(10);
    const { user } = useContext(AuthContext);
    const [selectedSportCategory, setSelectedSportCategory] = useState(''); // To filter by sport category

    console.log(bookings);
    

    useEffect(() => {
        const fetchBookingHistory = async () => {
            try {
                const sportFilter = selectedSportCategory ? `&sport_category=${selectedSportCategory}` : ''; 
                const response = await axios.get(`http://127.0.0.1:8000/api/booking-history/?user_id=${user.id}&ordering=-date${sportFilter}`);
                                
                if (Array.isArray(response.data)) {
                    setBookings(response.data);
                    
                } else {
                    setError('Unexpected response format');
                }
            } catch (error) {
                setError('Error fetching booking history');
            } finally {
                setLoading(false);
            }
        };

        fetchBookingHistory();
    }, [user.id, selectedSportCategory]); // Re-fetch when the sport category changes

    const indexOfLastBooking = currentPage * bookingsPerPage;
    const indexOfFirstBooking = indexOfLastBooking - bookingsPerPage;
    const currentBookings = bookings.slice(indexOfFirstBooking, indexOfLastBooking);

    const paginate = pageNumber => setCurrentPage(pageNumber);

    if (loading) {
        return <div className="text-center mt-5">Loading...</div>;
    }

    if (error) {
        return <div className="text-center mt-5" style={{ color: 'red' }}>{error}</div>;
    }

    if (!Array.isArray(bookings) || bookings.length === 0) {
        return <div className="text-center mt-5">No bookings available</div>;
    }

    return (
        <div className="booking-history-container mt-4">
            <h2 className="text-center mb-4">Booking History</h2>

            {/* Sport Category Filter Dropdown */}
            {/* <div className="text-center mb-3">
                <select 
                    value={selectedSportCategory} 
                    onChange={e => setSelectedSportCategory(e.target.value)} 
                    className="form-select w-auto">
                    <option value="">Select Sport Category</option>
                    <option value="Football">Football</option>
                    <option value="Basketball">Basketball</option>
                    <option value="Cricket">Cricket</option>
                </select>
            </div> */}

            <table className="booking-table">
                <thead>
                    <tr>
                        <th>Serial No.</th>
                        <th>Sport ID</th>
                        <th>Date</th>
                        <th>Start Time</th>
                        <th>End Time</th>
                        <th>Amount</th>
                        <th>Payment Status</th>
                        <th>Booking Date</th>
                    </tr>
                </thead>
                <tbody>
                    {currentBookings.map((booking, index) => (
                        <tr key={booking.booking_id}>
                            <td>{indexOfFirstBooking + index + 1}</td>
                            <td>{booking.sport_custom_id}</td> {/* Updated from turf to sport_id */}
                            <td>{booking.date}</td>
                            <td>{booking.start_time}</td>
                            <td>{booking.end_time}</td>
                            <td>{booking.amount}</td>
                            <td className={booking.payment_status === 'Paid' ? 'paid' : 'unpaid'}>
                                {booking.payment_status}
                            </td>
                            <td>
                                {`${new Date(booking.booking_date).getDate().toString().padStart(2, '0')}-${(new Date(booking.booking_date).getMonth() + 1).toString().padStart(2, '0')}-${new Date(booking.booking_date).getFullYear()} ${new Date(booking.booking_date).getHours().toString().padStart(2, '0')}:${new Date(booking.booking_date).getMinutes().toString().padStart(2, '0')}`}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <div className="pagination-container">
                <Pagination>
                    {Array.from({ length: Math.ceil(bookings.length / bookingsPerPage) }, (_, index) => (
                        <Pagination.Item key={index + 1} 
                        onClick={() => paginate(index + 1)} 
                        active={index + 1 === currentPage}>
                            {index + 1}
                        </Pagination.Item>
                    ))}
                </Pagination>
            </div>
        </div>
    );
};

export default BookingHistory;
