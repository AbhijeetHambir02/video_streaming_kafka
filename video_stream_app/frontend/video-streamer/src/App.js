import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import VideoCard from './components/VideoCard';

const API_URL = 'http://localhost:8000/video-streamer/v1';

function App() {
  const [file, setFile] = useState(null);
  const [uploadedVideo, setUploadedVideo] = useState(null);

  // Load saved video from localStorage on page load
  useEffect(() => {
    const savedVideo = localStorage.getItem('uploadedVideo');
    if (savedVideo) {
      setUploadedVideo(JSON.parse(savedVideo));
    }
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a video file first!");

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(`${API_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setUploadedVideo(res.data);

      // Save uploaded video info to localStorage
      localStorage.setItem('uploadedVideo', JSON.stringify(res.data));
    } catch (err) {
      console.error('Upload failed:', err);
    }
  };

  return (
    <div className="app-container">
      <h2 className="title">Video Streaming Portal</h2>

      {/* Upload section */}
      <div className="upload-section">
        <input type="file" className="file-input" onChange={handleFileChange} />
        <button className="upload-btn" onClick={handleUpload}>
          Upload
        </button>
      </div>

      {/* Show video */}
      {uploadedVideo && (
        <div className="video-center">
          <VideoCard
            video={uploadedVideo}
            streamUrl={`${API_URL}/stream/${uploadedVideo.id}`}
          />
        </div>
      )}
    </div>
  );
}

export default App;
