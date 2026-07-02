import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => (
  <div className="container flex-col items-center justify-center animate-fade-in" style={{ minHeight: '80vh', display: 'flex' }}>
    <div style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '4rem', marginBottom: '1.5rem', background: 'linear-gradient(135deg, var(--primary), var(--secondary))', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
        Hire Smarter with AI
      </h1>
      <p style={{ fontSize: '1.3rem', color: 'var(--text-secondary)', marginBottom: '3rem', lineHeight: '1.8' }}>
        SmartHire AI is the premium platform for modern recruitment. Upload your resume to get instant AI analysis, skill gap tracking, and matched job opportunities powered by state-of-the-art NLP models.
      </p>
      
      <div className="flex justify-center gap-6">
        <Link to="/candidate" className="btn btn-primary" style={{ fontSize: '1.1rem', padding: '1rem 2rem' }}>
          I am a Candidate
        </Link>
        <Link to="/recruiter" className="btn btn-secondary" style={{ fontSize: '1.1rem', padding: '1rem 2rem' }}>
          I am a Recruiter
        </Link>
      </div>
      
      <div className="mt-8 flex justify-center gap-8" style={{ opacity: 0.7, marginTop: '4rem' }}>
        <div className="text-center">
          <h3 style={{ fontSize: '2rem', color: 'var(--primary)' }}>99%</h3>
          <p>Accuracy</p>
        </div>
        <div className="text-center">
          <h3 style={{ fontSize: '2rem', color: 'var(--secondary)' }}>10k+</h3>
          <p>Resumes Parsed</p>
        </div>
        <div className="text-center">
          <h3 style={{ fontSize: '2rem', color: 'var(--accent)' }}>500+</h3>
          <p>Top Companies</p>
        </div>
      </div>
    </div>
  </div>
);

export default Home;
