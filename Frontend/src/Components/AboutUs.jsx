import React from 'react';
import '../App.css';


const AboutUs = () => {
    return (
        <div style={{ background: 'none' }}>
            <section className="px-4 pt-5 my-5 text-center border-bottom">
                <h1 className="display-4 fw-bold">Know About Us</h1>
                <div className="col-lg-6 mx-auto">
                    <p className="lead mb-4">
                        Welcome to our platform, dedicated to revolutionizing how you book and enjoy Turf experiences
                        across Nepal. As innovators in the industry, we believe that finding and booking Turf shouldn't be
                        complicated or stressful. Our mission is to make the process seamless and enjoyable for every user.
                        Get started today!
                    </p>
                    <div className="d-grid gap-2 d-sm-flex justify-content-sm-center mb-5">
                        <button
                            type="button"
                            className="btn btn-primary btn-lg px-4 me-sm-3"
                            onClick={() => document.getElementById('footer').scrollIntoView()}
                        >
                            Contact Us
                        </button>
                    </div>
                </div>
                <div className="overflow-hidden" style={{ maxHeight: '40vh' }}>
                    <div className="container px-5">
                        <img src="Images/team.jpg" className="img-fluid border rounded-3 shadow-lg" alt="Team" width="550" height="200" loading="lazy" />
                    </div>
                </div>
            </section>

            <section className="container px-4 py-5" id="featured-3">
                <h2 className="pb-2 border-bottom">Why Choose Us?</h2>
                <div className="row g-4 py-5 row-cols-1 row-cols-lg-3">
                    {[
                        { src: 'Images/calendar-check.svg', alt: 'calendar', title: 'Convenient Scheduling', text: 'Our Turf Booking System allows you to easily schedule your playtime with just a few clicks. We prioritize your convenience, ensuring that you can book your preferred slots without any hassle. Our user-friendly interface makes the booking process smooth and efficient.' },
                        { src: 'Images/globe.svg', alt: 'globe', title: 'Accessible Locations', text: 'We offer a range of accessible turf locations across the city to meet your needs. Whether you\'re looking for a spot close to home or near your workplace, our system provides you with a variety of options. Enjoy the flexibility of choosing a location that suits you best.' },
                        { src: 'Images/star.svg', alt: 'star', title: 'Quality Experience', text: 'We are dedicated to providing an exceptional experience every time you book with us. Our turfs are well maintained and equipped with the best facilities to ensure your game is as enjoyable as possible. Book with confidence knowing you’re getting top-notch service and quality.' },
                    ].map((feature, idx) => (
                        <div className="feature col" key={idx}>
                            <div className="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3">
                                <img src={feature.src} alt={feature.alt} height="30" />
                            </div>
                            <h3 className="fs-2">{feature.title}</h3>
                            <p>{feature.text}</p>
                        </div>
                    ))}
                </div>
            </section>

            <section className="container">
                <div id="carouselExampleIndicators" className="carousel slide">
                    <div className="carousel-indicators">
                        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" className="active" aria-current="true" aria-label="Slide 1"></button>
                        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
                        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
                    </div>
                    <div className="carousel-inner">
                        {['Images/boys.jpg', 'Images/ball.jpg'].map((src, idx) => (
                            <div className={`carousel-item ${idx === 0 ? 'active' : ''}`} key={idx}>
                                <img src={src} className="d-block w-100" alt="Slide" />
                            </div>
                        ))}
                    </div>
                    <button className="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
                        <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span className="visually-hidden">Previous</span>
                    </button>
                    <button className="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
                        <span className="carousel-control-next-icon" aria-hidden="true"></span>
                        <span className="visually-hidden">Next</span>
                    </button>
                </div>
            </section>

            <footer className="container py-5 border-top" id="footer">
                <div className="row row-cols-1 row-cols-sm-2 row-cols-md-5">
                    <div className="col mb-3">
                        <a href="/" className="d-flex align-items-center mb-3 text-body-emphasis text-decoration-none">
                            <svg className="bi me-2" width="40" height="32">
                                <use xlinkHref="#bootstrap"></use>
                            </svg>
                        </a>
                        <p className="text-body-secondary">© 2024 All rights reserved</p>
                    </div>
                    <div className="col mb-3"></div>
                    <div className="col mb-3"></div>
                    <div className="col mb-3"></div>
                    <div className="col mb-3">
                        <h5>Contact Information</h5>
                        <ul className="nav flex-column">
                            <li className="nav-item mb-2">
                                <a href="tel:9876543210" className="nav-link p-0 text-body-secondary">
                                    <img src="Images/phone-icon.svg" alt="Phone" width="20" height="20" className="me-2" />
                                    +91 9876543210
                                </a>
                            </li>
                            <li className="nav-item mb-2">
                                <a href="mailto:AOneTurf@gmail.com" className="nav-link p-0 text-body-secondary">
                                    <img src="Images/email-icon.svg" alt="Email" width="20" height="20" className="me-2" />
                                    AOneTurf@gmail.com
                                </a>
                            </li>
                            <li className="nav-item mb-2">
                                <a href="https://www.instagram.com/example" className="nav-link p-0 text-body-secondary">
                                    <img src="Images/instagram-icon.svg" alt="Instagram" width="20" height="20" className="me-2" />
                                    AOneTurfs
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default AboutUs;
