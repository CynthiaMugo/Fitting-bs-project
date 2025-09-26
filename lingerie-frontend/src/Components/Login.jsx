import React, { useState } from "react";
import API from "../api";
import { useNavigate, Link } from "react-router-dom";

function Login() {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");
    setMessage("");

    API.post("/authentication/login", formData)
      .then((res) => {
        localStorage.setItem("token", res.data.access_token);

        setMessage("Login successful");
        navigate("/");
        setFormData({ email: "", password: "" });
      })
      .catch((err) => {
        if (err.response && err.response.data.error) {
          setError(err.response.data.error);
        } else {
          setError("Something went wrong. Try again.");
        }
      });
  };

  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h2>Login</h2>

        {error && <p className="error">{error}</p>}
        {message && <p className="success">{message}</p>}

        <input type="text" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
        <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} required />

        <button type="submit">Login</button>
         <p className="switch-auth">
          Don't  have an account? <Link to="/register">Register</Link>
        </p>
      </form>
    </div>
  );
}

export default Login;
