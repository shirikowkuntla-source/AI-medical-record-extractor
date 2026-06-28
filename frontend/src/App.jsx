import React, { useState, useEffect } from 'react';
import UploadComponent from './components/UploadComponent';
import TextInputComponent from './components/TextInputComponent';
import ResultsComponent from './components/ResultsComponent';
import HistoryComponent from './components/HistoryComponent';
import { healthCheck, getRecord } from './services/api';

function App() {
  const [extractedData, setExtractedData] = useState(null);
  const [error, setError] = useState(null);
  const [isHealthy, setIsHealthy] = useState(null);
  const [activeTab, setActiveTab] = useState('upload');
  const [selectedRecord, setSelectedRecord] = useState(null);

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      await healthCheck();
      setIsHealthy(true);
    } catch (error) {
      setIsHealthy(false);
      console.error('Health check failed:', error);
    }
  };

  const handleExtractionComplete = (data) => {
    setExtractedData(data);
    setError(null);
    setSelectedRecord(null);
  };

  const handleError = (errorMessage) => {
    setError(errorMessage);
    setExtractedData(null);
  };

  const handleReset = () => {
    setExtractedData(null);
    setError(null);
    setSelectedRecord(null);
    setActiveTab('upload');
  };

  const handleSelectRecord = async (record) => {
    try {
      const fullRecord = await getRecord(record.id);
      setSelectedRecord(fullRecord);
      setExtractedData(fullRecord);
      setError(null);
    } catch (error) {
      setError('Failed to load record details');
      console.error('Error loading record:', error);
    }
  };

  const handleDeleteRecord = (recordId) => {
    if (selectedRecord && selectedRecord.id === recordId) {
      setSelectedRecord(null);
      setExtractedData(null);
    }
  };

  const tabs = [
    { id: 'upload', label: '📤 Upload File', icon: '📤' },
    { id: 'text', label: '📝 Text Input', icon: '📝' },
    { id: 'history', label: '📜 History', icon: '📜' },
  ];

  return (
    <div className="min-h-screen">
      <nav className="nav">
        <div className="nav-content">
          <h1>
            <span style={{ fontSize: '1.8rem' }}>🏥</span>
            AI Medical Record Extractor
          </h1>
          <div className="nav-links">
            <div className={`health-indicator ${isHealthy === true ? 'connected' : isHealthy === false ? 'disconnected' : 'checking'}`}>
              <span className="health-dot"></span>
              {isHealthy === true ? 'Backend Connected' : isHealthy === false ? 'Backend Disconnected' : 'Checking...'}
            </div>
          </div>
        </div>
      </nav>

      <div className="container">
        <div className="header">
          <h1>AI Medical Record Extractor</h1>
          <p>
            Upload medical records or enter text directly to extract structured information using offline AI.
            <br />
            Works completely offline with CPU-only inference for maximum privacy.
          </p>
        </div>

        {error && (
          <div className="error">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            <div>
              <strong>Error:</strong> {error}
            </div>
          </div>
        )}

        {!extractedData && !error && (
          <>
            <div className="tabs">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  className={`tab ${activeTab === tab.id ? 'active' : ''}`}
                  onClick={() => setActiveTab(tab.id)}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {activeTab === 'upload' && (
              <UploadComponent
                onExtractionComplete={handleExtractionComplete}
                onError={handleError}
              />
            )}

            {activeTab === 'text' && (
              <TextInputComponent
                onExtractionComplete={handleExtractionComplete}
                onError={handleError}
              />
            )}

            {activeTab === 'history' && (
              <HistoryComponent
                onSelectRecord={handleSelectRecord}
                onDeleteRecord={handleDeleteRecord}
              />
            )}
          </>
        )}

        {extractedData && (
          <>
            <ResultsComponent data={extractedData} />
            <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', marginTop: '24px' }}>
              <button className="btn btn-secondary" onClick={handleReset}>
                ← Back to Upload
              </button>
              <button 
                className="btn" 
                onClick={() => {
                  navigator.clipboard.writeText(JSON.stringify(extractedData, null, 2));
                  alert('Results copied to clipboard!');
                }}
              >
                📋 Copy Results
              </button>
            </div>
          </>
        )}

        <div className="footer">
          <p>© 2024 AI Medical Record Extractor | Offline-First | CPU-Only Inference | Privacy-Focused</p>
        </div>
      </div>
    </div>
  );
}

export default App;