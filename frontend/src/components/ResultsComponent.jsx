import React from 'react';

const ResultsComponent = ({ data }) => {
  if (!data) return null;

  const renderList = (items, emptyMessage = 'None detected') => {
    if (!items || items.length === 0) {
      return <p style={{ color: '#999', fontStyle: 'italic' }}>{emptyMessage}</p>;
    }
    return (
      <ul>
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    );
  };

  return (
    <div className="card">
      <h2>Extracted Medical Information</h2>
      
      <div className="results-grid">
        <div className="result-item">
          <h3>Patient Details</h3>
          <p><strong>Name:</strong> {data.patient_name || 'Not detected'}</p>
          <p><strong>Age:</strong> {data.age || 'Not detected'}</p>
          <p><strong>Gender:</strong> {data.gender || 'Not detected'}</p>
        </div>

        <div className="result-item">
          <h3>Diagnosis</h3>
          <p>{data.diagnosis || 'Not detected'}</p>
        </div>

        <div className="result-item">
          <h3>Symptoms</h3>
          {renderList(data.symptoms, 'No symptoms detected')}
        </div>

        <div className="result-item">
          <h3>Medications</h3>
          {renderList(data.medications, 'No medications detected')}
        </div>

        <div className="result-item">
          <h3>Medical History</h3>
          {renderList(data.medical_history, 'No medical history detected')}
        </div>

        <div className="result-item">
          <h3>Doctor Information</h3>
          <p><strong>Doctor:</strong> {data.doctor_name || 'Not detected'}</p>
          <p><strong>Hospital:</strong> {data.hospital_name || 'Not detected'}</p>
        </div>
      </div>

      {data.summary && (
        <div className="summary-box">
          <h3>Medical Summary</h3>
          <p>{data.summary}</p>
        </div>
      )}
    </div>
  );
};

export default ResultsComponent;