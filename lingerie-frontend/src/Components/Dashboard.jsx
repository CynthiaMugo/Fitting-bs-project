import React from "react";
import { useNavigate, Link } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const username = localStorage.getItem("username");

  if (!token) {
    navigate("/login");
    return null;
  }

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    navigate("/login");
  };

  return (
    <div className="home-container">
      {/* Navbar */}
      <nav className="navbar">
        <h1 className="logo">Fit & Fabulous</h1>
        <ul className="nav-links">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/measurements">My Measurements</Link></li>
          <li><Link to="/products">Products</Link></li>
          <li><button className="logout-btn" onClick={handleLogout}>Logout</button></li>
        </ul>
      </nav>

      {/* Hero Section */}
      <section className="hero">
        <h2 className="welcome">Welcome back, {username || "Lovely"} 💕</h2>
        <p className="info">
          Discover bras tailored to your unique fit and style. 
          Update your measurements, browse our curated collection, and place your next order.
        </p>
        <div className="hero-buttons">
          <Link to="/measurements"><button className="cta-btn">Update Measurements</button></Link>
          <Link to="/products"><button className="cta-btn secondary">Shop Bras</button></Link>
        </div>
      </section>
    </div>
  );
}

export default Dashboard;
