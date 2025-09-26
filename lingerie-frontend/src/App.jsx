// App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./Components/Login";
import Register from "./Components/Register";
import Dashboard from "./Components/Dashboard";
import "./index.css";

function App() {
  return (
    <Router>
      <Routes>
        {/* Register route */}
        <Route path="/register" element={<Register />} />

        {/* Login route */}
        <Route path="/login" element={<Login />} />

        {/* Default route */}
        <Route path="/" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
