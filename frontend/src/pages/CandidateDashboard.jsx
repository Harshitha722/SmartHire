import React, { useState } from 'react';
import axios from 'axios';
import { FiUploadCloud, FiBriefcase, FiTarget, FiAlertCircle } from 'react-icons/fi';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

const CandidateDashboard = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      // 1. Upload Resume
      const uploadRes = await axios.post('http://127.0.0.1:8000/resume/upload', formData);
      const resumeId = uploadRes.data.resumeId;
      
      // 2. Run ML Analysis in parallel
      const [roleRes, scoreRes, jobsRes, gapRes] = await Promise.all([
        axios.post('http://127.0.0.1:8000/ml/predict-role', { resume_id: resumeId }),
        axios.post('http://127.0.0.1:8000/ml/resume-score', { resume_id: resumeId }),
        axios.post('http://127.0.0.1:8000/ml/recommend-jobs', { resume_id: resumeId }),
        axios.post('http://127.0.0.1:8000/ml/skill-gap', { resume_id: resumeId, job_id: "dummy" })
      ]);
      
      setAnalysis({
        role: roleRes.data.predicted_role,
        confidence: roleRes.data.confidence,
        score: scoreRes.data.score,
        jobs: jobsRes.data.recommendations,
        skills: gapRes.data
      });
      
    } catch (err) {
      console.error(err);
      alert("Error analyzing resume. Make sure backend is running.");
    }
    setLoading(false);
  };

  const scoreData = analysis ? {
    labels: ['Score', 'Room for Improvement'],
    datasets: [{
      data: [analysis.score, 100 - analysis.score],
      backgroundColor: ['#6366f1', 'rgba(255, 255, 255, 0.1)'],
      borderWidth: 0,
    }]
  } : null;

  return (
    <div className="container animate-fade-in" style={{ padding: '2rem 0' }}>
      <h2 style={{ fontSize: '2.5rem', marginBottom: '2rem' }}>Candidate Workspace</h2>
      
      {!analysis ? (
        <div className="glass-panel text-center" style={{ padding: '4rem 2rem' }}>
          <FiUploadCloud size={64} color="var(--primary)" style={{ marginBottom: '1rem' }} />
          <h3>Upload Your Resume</h3>
          <p>We accept PDF and DOCX formats up to 5MB.</p>
          
          <form onSubmit={handleFileUpload} className="mt-4 flex-col items-center gap-4">
            <input 
              type="file" 
              accept=".pdf,.docx" 
              onChange={(e) => setFile(e.target.files[0])}
              style={{ padding: '1rem', background: 'rgba(0,0,0,0.1)', borderRadius: '8px' }}
            />
            <button type="submit" className="btn btn-primary" disabled={!file || loading}>
              {loading ? 'Analyzing with AI...' : 'Analyze Resume'}
            </button>
          </form>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}>
          
          {/* Left Column - Stats */}
          <div className="flex-col gap-6">
            <div className="glass-panel text-center">
              <h3>Resume Score</h3>
              <div style={{ width: '200px', margin: '2rem auto' }}>
                <Doughnut data={scoreData} options={{ cutout: '80%' }} />
                <div style={{ position: 'relative', top: '-120px', fontSize: '2.5rem', fontWeight: 'bold', color: 'var(--primary)' }}>
                  {analysis.score}
                </div>
              </div>
            </div>
            
            <div className="glass-panel">
              <div className="flex items-center gap-4 mb-4">
                <FiTarget size={24} color="var(--secondary)" />
                <h3 style={{ margin: 0 }}>Predicted Role</h3>
              </div>
              <p style={{ fontSize: '1.2rem', fontWeight: 600 }}>{analysis.role}</p>
              <p style={{ opacity: 0.7 }}>AI Confidence: {analysis.confidence}%</p>
            </div>

            <div className="glass-panel" style={{ borderLeft: '4px solid var(--secondary)' }}>
              <div className="flex items-center gap-4 mb-4">
                <FiAlertCircle size={24} color="var(--secondary)" />
                <h3 style={{ margin: 0 }}>Skill Gap Analysis</h3>
              </div>
              <div>
                <strong>Missing Skills:</strong>
                <div className="flex mt-2" style={{ flexWrap: 'wrap', gap: '0.5rem' }}>
                  {analysis.skills.missing_skills.map(s => (
                    <span key={s} style={{ background: 'rgba(236, 72, 153, 0.2)', padding: '4px 10px', borderRadius: '20px', fontSize: '0.8rem', color: 'var(--secondary)' }}>{s}</span>
                  ))}
                </div>
              </div>
            </div>
          </div>
          
          {/* Right Column - Recommendations */}
          <div className="glass-panel">
            <div className="flex items-center gap-4 mb-6">
              <FiBriefcase size={28} color="var(--primary)" />
              <h2 style={{ margin: 0 }}>Top Matched Jobs</h2>
            </div>
            
            <div className="flex-col gap-4">
              {analysis.jobs.map((job, idx) => (
                <div key={idx} style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.05)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
                  <div className="flex justify-between items-center mb-2">
                    <h3 style={{ margin: 0 }}>{job.title}</h3>
                    <span style={{ fontWeight: 'bold', color: 'var(--primary)' }}>{job.matchPercentage}% Match</span>
                  </div>
                  <p style={{ margin: '0 0 10px 0', opacity: 0.8 }}>{job.company} • {job.location}</p>
                  <p style={{ margin: 0, fontWeight: 500, color: '#10b981' }}>{job.salary}</p>
                  
                  <div className="mt-4 flex justify-between items-center">
                    <div className="flex" style={{ flexWrap: 'wrap', gap: '0.5rem' }}>
                      {job.requiredSkills.slice(0, 3).map(skill => (
                        <span key={skill} style={{ background: 'rgba(99, 102, 241, 0.2)', padding: '2px 8px', borderRadius: '4px', fontSize: '0.8rem' }}>{skill}</span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
        </div>
      )}
    </div>
  );
};

export default CandidateDashboard;
