import React from 'react';

const ResultsComponent = ({ data }) => {
  if (!data) return null;

  const renderList = (items, emptyMessage = 'None detected') => {
    if (!items || items.length === 0) {
      return (
        <p style={{ color: '#999', fontStyle: 'italic', fontSize: '0.9rem' }}>
          {emptyMessage}
        </p>
      );
    }
    return (
      <ul>
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    );
  };

  const InfoRow = ({ label, value }) => (
    <div style={{ marginBottom: '8px' }}>
      <strong style={{ color: '#667eea', fontSize: '0.9rem' }}>{label}:</strong>
      <span style={{ marginLeft: '8px', color: '#2c3e50' }}>{value || 'Not detected'}</span>
    </div>
  );

  return (
    <div className="card fade-in">
      <h2>
        <span style={{ fontSize: '1.5rem' }}>✨</span>
        Extracted Medical Information
      </h2>

      <div className="results-grid">
        <div className="result-item">
          <h3>
            <span>👤</span>
            Patient Details
          </h3>
          <InfoRow label="Name" value={data.patient_name} />
          <InfoRow label="Age" value={data.age} />
          <InfoRow label="Gender" value={data.gender} />
        </div>

        <div className="result-item">
          <h3>
            <span>🩺</span>
            Diagnosis
          </h3>
          <p style={{ lineHeight: '1.6' }}>{data.diagnosis || 'Not detected'}</p>
        </div>

        <div className="result-item">
          <h3>
            <span>🤒</span>
            Symptoms
          </h3>
          {renderList(data.symptoms, 'No symptoms detected')}
        </div>

        <div className="result-item">
          <h3>
            <span>💊</span>
            Medications
          </h3>
          {renderList(data.medications, 'No medications detected')}
        </div>

        <div className="result-item">
          <h3>
            <span>📋</span>
            Medical History
          </h3>
          {renderList(data.medical_history, 'No medical history detected')}
        </div>

        <div className="result-item">
          <h3>
            <span>👨‍⚕️</span>
            Doctor Information
          </h3>
          <InfoRow label="Doctor" value={data.doctor_name} />
          <InfoRow label="Hospital" value={data.hospital_name} />
        </div>
      </div>

      {data.summary && (
        <div className="summary-box">
          <h3>
            <span>📝</span>
            Medical Summary
          </h3>
          <p>{data.summary}</p>
        </div>
      )}

      {data.confidence_score && (
        <div style={{ marginTop: '20px', padding: '16px', background: '#f8f9fa', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <strong style={{ color: '#667eea' }}>Confidence Score:</strong>
            <span style={{ marginLeft: '8px', fontSize: '1.1rem', fontWeight: '600' }}>
              {(data.confidence_score * 100).toFixed(1)}%
            </span>
          </div>
          <div style={{ 
            width: '200px', 
            height: '8px', 
            background: '#e0e0e0', 
            borderRadius: '4px', 
            overflow: 'hidden' 
          }}>
            <div 
              style={{ 
                width: `${data.confidence_score * 100}%`, 
                height: '100%', 
                background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
                borderRadius: '4px',
                transition: 'width 0.5s ease'
              }} 
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsComponent;