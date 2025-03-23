import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import UploadImage from "./pages/UploadImage";
import UploadVideo from "./pages/UploadVideo";
import About from "./components/About";
import "./App.css";


function App() {
    return (
        <Router>
            <Navbar />
            <Routes>
                {/* Redirect "/" to "/upload/image" */}
                <Route path="/" element={<Navigate to="/upload/image" />} />
                <Route path="/upload/image" element={<UploadImage />} />
                <Route path="/upload/video" element={<UploadVideo />} />
                <Route path="/about" element={<About />} />  
            </Routes>
        </Router>
    );
}

export default App;
