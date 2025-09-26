import React, { useState } from 'react';
import { Link } from "react-router-dom"; 
import API from '../api';

function Register() {
    const [form, setForm] = useState({ username: "", email: "", password: "" });
    const [message, setMessage] = useState("");
    const [user, setUser] = useState(null);


    const handleChange = (event) =>
        setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }));

    const handleSubmit = (event) => {
        event.preventDefault();
        API.post("/authentication/register", form)
        .then((res) => {
        setMessage(res.data.message);
        setUser(res.data.user); 
        })
        .catch((err) => {
        setMessage(err.response?.data.error || "Something went wrong");
        });
    }
    return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h2>Register</h2>

        <input name="username" placeholder="Username" onChange={handleChange} required />
        <input name="email" placeholder="Email" onChange={handleChange} required />
        <input name="password" type="password" placeholder="Password" onChange={handleChange} required/>
        <button type="submit">Register</button>

        {message && <p className="message">{message}</p>}
        {user && <p className="welcome">Welcome, {user.username}! </p>}

        <p className="switch-auth">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
    </div>
  );

}
export default Register;