import React, { useState } from 'react';
import { extractFromText } from '../services/api';

const TextInputComponent = ({ onExtractionComplete, onError }) => {
  const [text, setText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!text.trim()) {
      onError('Please enter some text to extract information from');
      return;
    }

    setIsLoading(true);

    try {
      const result = await extractFromText(text);
      onExtractionComplete(result);
    } catch (error) {
      console.error('Extraction error:', error);
      onError(error.response?.data?.detail || error.message || 'Extraction failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setText('');
  };

  return (
    <div className="card">
      <h2>📝 Enter Medical Record Text</h2>
      
      <form onSubmit={handleSubmit}>
        <textarea
          className="text-input-area"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste or type the medical record text here...

Example:
Patient Name: John Doe
Age: 45
Gender: Male
Diagnosis: Type 2 Diabetes
Symptoms: Increased thirst, frequent urination, fatigue
Medications: Metformin 500mg twice daily
Medical History: Hypertension, High cholesterol
Doctor: Dr. Sarah Smith
Hospital: City General Hospital"
          disabled={isLoading}
        />

        <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={handleClear}
            disabled={isLoading || !text}
          >
            Clear
          </button>
          <button
            type="submit"
            className="btn"
            disabled={isLoading || !text.trim()}
          >
            {isLoading ? 'Extracting...' : 'Extract Information'}
          </button>
        </div>
      </form>

      {isLoading && (
        <div className="loading">
          <div className="spinner"></div>
          <span style={{ marginLeft: '10px' }}>Processing text with AI...</span>
        </div>
      )}

      <div style={{ marginTop: '20px', padding: '16px', background: '#f8f9fa', borderRadius: '8px', fontSize: '0.9rem', color: '#666' }}>
        <strong>💡 Tip:</strong> For best results, include as much detail as possible from the medical record, including patient information, diagnosis, symptoms, medications, and doctor details.
      </div>
    </div>
  );
};

export default TextInputComponent;