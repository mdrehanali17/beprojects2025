import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Carousel, Spinner } from 'react-bootstrap';
import { useAuth } from '../Context/AuthContext';

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    const fetchRecommendations = async () => {
      if (!user?.id) {
        setError('User not found. Please log in again.');
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/recommendations/${user.id}`);
        setRecommendations(response.data.recommendations || []);
      } catch (err) {
        console.error('Error fetching recommendations:', err);
        setError('Failed to fetch recommendations.');
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [user?.id]);

  const handleNavigate = (id) => {
    navigate(`/sports/${id}`);
  };

  if (loading) {
    return (
      <div className="text-center mt-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </div>
    );
  }

  if (error) {
    return <div className="text-center text-danger mt-5">{error}</div>;
  }

  if (recommendations.length === 0) {
    return <div className="text-center mt-5">No recommendations available.</div>;
  }

  return (
    <div className="container mt-3">
      <h2 className="text-center mb-4">Recommended for You</h2>
      <Carousel
        interval={3000} // Auto-slide every 3 seconds
        controls={true} // Enable left and right arrows
        indicators={true} // Show indicators
        className="carousel-container"
        nextLabel=""
        prevLabel=""
      >
        {recommendations.map((sport, index) => (
          <Carousel.Item key={index}>
            {/* Image container */}
            <div
              className="d-flex flex-column align-items-center"
              style={{
                height: "600px",
                width: "800px",
                margin: "0 auto",
                borderRadius: "8px",
                overflow: "hidden",
              }}
            >
              <img
                src={`http://127.0.0.1:8000${sport.sport_images[0]?.image}`}
                alt={`${sport.name}`}
                style={{
                  height: "400px",
                  width: "100%",
                  objectFit: "cover",
                }}
              />
              {/* Text content below the image */}
              <div className="mt-3 text-center">
                <h3>{sport.name}</h3>
                <p>
                  {sport.description.length > 100
                    ? `${sport.description.substring(0, 100)}...`
                    : sport.description}
                </p>
                <button
                  onClick={() => handleNavigate(sport.id)}
                  className="btn btn-primary"
                  aria-label={`View details of ${sport.name}`}
                >
                  View Details
                </button>
              </div>
            </div>
          </Carousel.Item>
        ))}
      </Carousel>
    </div>
  );
  
};

export default Recommendations;
