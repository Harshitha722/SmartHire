import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FiUsers, FiFileText, FiDownload, FiX } from 'react-icons/fi';

const RecruiterDashboard = () => {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showJobForm, setShowJobForm] = useState(false);
  const [jobForm, setJobForm] = useState({ title: '', description: '', required_skills: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    const fetchCandidates = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:8000/recruiter/candidates');
        setCandidates(res.data.candidates);
      } catch (err) {
        console.error("Error fetching candidates", err);
      }
      setLoading(false);
    };
    fetchCandidates();
  }, []);

  const handleJobSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Parse skills from comma-separated string to array
    const skillsArray = jobForm.required_skills.split(',').map(s => s.trim()).filter(s => s);
    
    try {
      await axios.post('http://127.0.0.1:8000/recruiter/job', {
        title: jobForm.title,
        description: jobForm.description,
        required_skills: skillsArray
      });
      alert('Job posted successfully!');
      setShowJobForm(false);
      setJobForm({ title: '', description: '', required_skills: '' });
    } catch (err) {
      console.error(err);
      alert('Failed to post job. Make sure the backend is running.');
    }
    setIsSubmitting(false);
  };

  return (
    <div className="container animate-fade-in" style={{ padding: '2rem 0' }}>
      <h2 style={{ fontSize: '2.5rem', marginBottom: '2rem' }}>Recruiter Workspace</h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 3fr', gap: '2rem' }}>
        
        {/* Sidebar */}
        <div className="flex-col gap-6">
          <div className="glass-panel text-center">
            <FiFileText size={48} color="var(--primary)" style={{ marginBottom: '1rem' }} />
            <h3>Post a New Job</h3>
            <p>Upload a job description to automatically rank candidates.</p>
            <button 
              className="btn btn-primary w-full mt-4" 
              onClick={() => setShowJobForm(!showJobForm)}
            >
              {showJobForm ? 'Cancel' : 'Upload JD'}
            </button>
            
            {showJobForm && (
              <form onSubmit={handleJobSubmit} className="mt-4 text-left flex-col gap-4 animate-fade-in">
                <div>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem' }}>Job Title</label>
                  <input 
                    type="text" 
                    required
                    style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'rgba(0,0,0,0.1)', color: 'var(--text-primary)' }}
                    value={jobForm.title}
                    onChange={e => setJobForm({...jobForm, title: e.target.value})}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem' }}>Description</label>
                  <textarea 
                    required
                    rows="3"
                    style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'rgba(0,0,0,0.1)', color: 'var(--text-primary)' }}
                    value={jobForm.description}
                    onChange={e => setJobForm({...jobForm, description: e.target.value})}
                  ></textarea>
                </div>
                <div>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem' }}>Required Skills (comma separated)</label>
                  <input 
                    type="text" 
                    required
                    placeholder="Python, SQL, React"
                    style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'rgba(0,0,0,0.1)', color: 'var(--text-primary)' }}
                    value={jobForm.required_skills}
                    onChange={e => setJobForm({...jobForm, required_skills: e.target.value})}
                  />
                </div>
                <button type="submit" className="btn btn-secondary w-full" disabled={isSubmitting}>
                  {isSubmitting ? 'Posting...' : 'Submit Job'}
                </button>
              </form>
            )}
          </div>
          
          <div className="glass-panel text-center">
            <FiUsers size={48} color="var(--secondary)" style={{ marginBottom: '1rem' }} />
            <h3>Total Talent Pool</h3>
            <h2 style={{ fontSize: '3rem', color: 'var(--text-primary)', margin: 0 }}>{candidates.length}</h2>
          </div>
        </div>
        
        {/* Main Content - Candidates Table */}
        <div className="glass-panel" style={{ padding: '0' }}>
          <div style={{ padding: '24px', borderBottom: 'var(--glass-border)', display: 'flex', justifyContent: 'space-between' }}>
            <h3 style={{ margin: 0 }}>Ranked Candidates</h3>
            <button className="btn btn-secondary" style={{ padding: '0.5rem 1rem' }}>
              <FiDownload /> Export CSV
            </button>
          </div>
          
          {loading ? (
            <div style={{ padding: '2rem' }}>
              <div className="skeleton" style={{ height: '50px', marginBottom: '1rem' }}></div>
              <div className="skeleton" style={{ height: '50px', marginBottom: '1rem' }}></div>
              <div className="skeleton" style={{ height: '50px' }}></div>
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ background: 'rgba(0,0,0,0.2)', textAlign: 'left' }}>
                    <th style={{ padding: '1rem 1.5rem' }}>Filename</th>
                    <th style={{ padding: '1rem 1.5rem' }}>Predicted Role</th>
                    <th style={{ padding: '1rem 1.5rem' }}>AI Score</th>
                    <th style={{ padding: '1rem 1.5rem' }}>Uploaded Date</th>
                  </tr>
                </thead>
                <tbody>
                  {candidates.map(candidate => (
                    <tr key={candidate.id} style={{ borderBottom: 'var(--glass-border)' }}>
                      <td style={{ padding: '1rem 1.5rem', fontWeight: 500 }}>{candidate.filename}</td>
                      <td style={{ padding: '1rem 1.5rem', color: 'var(--primary)' }}>{candidate.predictedRole || 'Pending'}</td>
                      <td style={{ padding: '1rem 1.5rem' }}>
                        {candidate.resumeScore ? (
                          <span style={{ background: candidate.resumeScore > 75 ? 'rgba(16, 185, 129, 0.2)' : 'rgba(245, 158, 11, 0.2)', color: candidate.resumeScore > 75 ? '#10b981' : '#f59e0b', padding: '4px 12px', borderRadius: '20px', fontWeight: 'bold' }}>
                            {candidate.resumeScore}/100
                          </span>
                        ) : 'N/A'}
                      </td>
                      <td style={{ padding: '1rem 1.5rem', opacity: 0.7 }}>
                        {new Date(candidate.createdAt).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                  {candidates.length === 0 && (
                    <tr>
                      <td colSpan="5" style={{ padding: '3rem', textAlign: 'center', opacity: 0.6 }}>
                        No candidates found in the database.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
        
      </div>
    </div>
  );
};

export default RecruiterDashboard;
