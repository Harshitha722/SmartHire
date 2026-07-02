import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import './index.css'

import Home from './pages/Home';
import CandidateDashboard from './pages/CandidateDashboard';
import RecruiterDashboard from './pages/RecruiterDashboard';

function App() {
  const [theme, setTheme] = useState('dark');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  return (
    <Router>
      <div className="gradient-bg"></div>
      
      <header className="glass-panel" style={{ borderRadius: 0, padding: '15px 20px', borderBottom: 'var(--glass-border)', position: 'sticky', top: 0, zIndex: 100 }}>
        <div className="container flex justify-between items-center">
          <Link to="/" style={{ textDecoration: 'none' }}>
            <h2 style={{ margin: 0, color: 'var(--primary)' }}>SmartHire AI</h2>
          </Link>
          <nav className="flex gap-6 items-center">
            <Link to="/" style={{ color: 'var(--text-primary)', textDecoration: 'none', fontWeight: 500 }}>Home</Link>
            <Link to="/candidate" style={{ color: 'var(--text-primary)', textDecoration: 'none', fontWeight: 500 }}>Candidate</Link>
            <Link to="/recruiter" style={{ color: 'var(--text-primary)', textDecoration: 'none', fontWeight: 500 }}>Recruiter</Link>
            <button onClick={toggleTheme} className="btn btn-secondary" style={{ padding: '0.5rem 1rem' }}>
              {theme === 'dark' ? '☀️ Light' : '🌙 Dark'}
            </button>
          </nav>
        </div>
      </header>

      <main style={{ paddingBottom: '3rem' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/candidate" element={<CandidateDashboard />} />
          <Route path="/recruiter" element={<RecruiterDashboard />} />
        </Routes>
      </main>
    </Router>
  )
}

export default App
