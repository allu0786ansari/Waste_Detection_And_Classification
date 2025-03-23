import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="navbar-brand">NLQ-AI</div>
            <div className="navbar-links">
                <Link to="/upload/image" className="nav-link">Image Upload</Link>
                <Link to="/upload/video" className="nav-link">Video Upload</Link>
                <Link to="/about" className="nav-link">About Us</Link>
            </div>
        </nav>
    );
};

export default Navbar;