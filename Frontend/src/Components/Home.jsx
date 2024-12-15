import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../Context/AuthContext';
import Recommendations from './Recommendations'; // Import Recommendations component

const Home = () => {
  const [currentVideo, setCurrentVideo] = useState(0);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { user } = useAuth();

  const videos = [
    '/Images/football1.mp4',
    '/Images/football2.mp4',
    '/Images/basketball.mp4',
  ];

  const games = [
    { id: 1, name: 'Football', image: '/Images/boys.jpg' },
    { id: 2, name: 'Cricket', image: '/Images/cricket.jpg' },
    { id: 3, name: 'Kabaddi', image: '/Images/kabaddi.jpeg' },
    { id: 4, name: 'Basketball', image: '/Images/Basketball.jpg' },
  ];

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/latest-sports/');
        setCategories(response.data.sports || []);
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch sports by category:', error);
        setError('Failed to fetch sports');
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  const renderStaticContent = () => (
    <div className="static-content">
      <video
        key={currentVideo}
        src={videos[currentVideo]}
        autoPlay
        muted
        loop
        className="background-video"
      />
      <div className="content-overlay">
        <h1>Welcome to GearGo Sports</h1>
        <p>Your one-stop destination for sports bookings. Choose your game and get started!</p>
      </div>
    </div>
  );

  const renderGameSelection = () => (
    <div className="container mt-4">
      <h2>Choose a Game</h2>
      <div className="row">
        {games.map((game) => (
          <div key={game.id} className="col-md-3 mb-4">
            <div
              className="game-box"
              style={{ cursor: 'pointer' }}
              onClick={() => navigate(`/category/${game.name.toLowerCase()}`)}
            >
              <img
                src={game.image}
                alt={game.name}
                className="card-img-top"
                style={{ height: '200px', objectFit: 'cover' }}
              />
              <h4 className="text-center mt-2">{game.name}</h4>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderSportsByCategory = () => (
    <div className="container mt-5">
      <h2>Recently Added</h2>
      {categories.map((category) => (
        <div key={category.category} className="mb-5">
          <h3 className="text-capitalize" style={{ marginTop: '30px' }}>{category.category}</h3>
          <div className="row">
            {category.sports.map((sport) => (
              <div key={sport.id} className="col-md-4 mb-4">
                <div className="card h-100">
                  {sport.sport_images.length > 0 && (
                    <img
                      src={
                        sport.sport_images[0].image.startsWith('http')
                          ? sport.sport_images[0].image
                          : `http://127.0.0.1:8000${sport.sport_images[0].image}`
                      }
                      alt={sport.name}
                      className="card-img-top"
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
      ))}
    </div>
  );

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div style={{ marginTop: '80px' }}>
      {renderStaticContent()}
      {user && <Recommendations user={user} />} {/* Render Recommendations */}
      {renderGameSelection()}
      {renderSportsByCategory()}
    </div>
  );
};

export default Home;
