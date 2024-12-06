import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

const SportByCategory = () => {
  const { category } = useParams(); // Access the category from the URL
  const [sports, setSports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  

  useEffect(() => {
    const fetchSportsByCategory = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/sports/category/${category}/`);
        setSports(response.data || []);
        setLoading(false);
      } catch (err) {
        console.error('Failed to fetch sports for category:', err);
        setError('Failed to load sports data');
        setLoading(false);
      }
    };

    fetchSportsByCategory();
  }, [category]);

  if (loading) {
    return <div style={{paddingTop: '80px', marginTop: '20px', textAlign: 'center'}}>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  if (!loading && sports.length === 0) {
    console.log("No sports found for the selected category."); // Debugging statement
    return <div style={{paddingTop: '80px', marginTop: '20px', textAlign: 'center'}}>No sports found for this category.....</div>;
  }
  
  return (
    <div className="container mt-5" style={{paddingTop : '40px'}}>
      <h2 className="text-center my-4">Available Facilities for {category.charAt(0).toUpperCase() + category.slice(1)}</h2>
      
      <div className="row">
        {sports.map((sport) => (
          <div key={sport.id} className="col-md-4 mb-4">
            <div className="card h-100 sport-card">
              {sport.sport_images.length > 0 && (
                <img
                  src={
                    sport.sport_images[0].image.startsWith('http')
                      ? sport.sport_images[0].image
                      : `http://127.0.0.1:8000${sport.sport_images[0].image}`
                  }
                  alt={sport.name}
                  className="card-img-top sport-card-img"
                />
              )}
              <div className="card-body">
                <h4 className="card-title text-center">{sport.name}</h4>
                <p className="card-text">{sport.description}</p>
                <p className="card-text text-center">
                  <strong>Price:</strong> Rs. {sport.price}
                </p>
                <Link to={`/sports/${sport.id}`} className="btn btn-primary w-100">
                  See Details
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SportByCategory;
