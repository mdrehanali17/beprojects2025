import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { Button, Modal, Carousel } from 'react-bootstrap';
import SportBooking from './SportBooking'; 
import { useAuth } from '../Context/AuthContext'; 

const SportDetails = () => {
  const { id } = useParams();
  const { user } = useAuth(); // Get the user from context (if authenticated)
  
  const [sportDetails, setSportDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);

  // Ref to track if view count has been increased
  const viewCountIncreased = useRef(false);

  useEffect(() => {
    const fetchSportDetails = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/sportDetails/${id}/`);
        setSportDetails(response.data);
        setLoading(false);
        
        // Only increase view count if user exists and view count has not been increased yet
        if (user && !viewCountIncreased.current) {
          console.log("Increasing view count");
          await axios.post(`http://127.0.0.1:8000/api/increase_view_count/${id}/`, { user_id: user.id });
          
          // Set the ref to true after the view count is incremented
          viewCountIncreased.current = true;
        }
      } catch (err) {
        setError('Failed to fetch sport details.');
        setLoading(false);
      }
    };

    fetchSportDetails();
  }, [id, user]); // Only trigger when id or user changes

  const handleShowModal = () => setShowModal(true);
  const handleCloseModal = () => setShowModal(false);

  if (loading) {
    return <div className="text-center">Loading...</div>;
  }

  if (error) {
    return <div className="text-center text-danger">{error}</div>;
  }

  if (!sportDetails) {
    return <div className="text-center">No sport details available.</div>;
  }

  return (
    <div className="container text-center mt-5">
      <div className="carousel-container" style={{ maxWidth: '850px', margin: '0 auto' }}>
        <Carousel fade>
          {sportDetails.sport_images.map((imageObj, index) => (
            <Carousel.Item key={index}>
              <div className="d-flex justify-content-center align-items-center" style={{ height: '500px' }}>
                <img
                  src={imageObj.image.startsWith('http') ? imageObj.image : `http://127.0.0.1:8000${imageObj.image}`}
                  className="d-block w-100"
                  alt={`Slide ${index}`}
                  style={{ height: '100%', objectFit: 'cover' }}
                />
              </div>
            </Carousel.Item>
          ))}
        </Carousel>
      </div>

      <div className="container-without-background mb-4" style={{ maxWidth: '850px', margin: '0 auto' }}>
        <h2>{sportDetails.name}</h2>
        <p>{sportDetails.description}</p>
        <p>Price: Rs.{sportDetails.price}/hour</p>
        <Button variant="primary" onClick={handleShowModal}>
          Select Slot
        </Button>
      </div>

      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>Book Your Slot</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <SportBooking handleClose={handleCloseModal} sport_custom_id={sportDetails.sport_custom_id} sport_category={sportDetails.category} />
        </Modal.Body>
      </Modal>
    </div>
  );
};

export default SportDetails;
