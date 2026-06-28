import React, { useState } from 'react';
import UploadComponent from './components/UploadComponent';
import ResultsComponent from './components/ResultsComponent';
import { healthCheck } from './services/api';

function App() {
  const [extractedData, setExtractedData] = useState(null);
  const [error, setError] = useState(null);
  const [isHealthy, setIsHealthy] = useState(null);

  React.useEffect(() => {
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
  };

  const handleError = (errorMessage) => {
    setError(errorMessage);
    setExtractedData(null);
  };

  const handleReset = () => {
    setExtractedData(null);
    setError(null);
  };

  return (
    <div className="min-h-screen">
      <nav className="nav">
        <div className="nav-content">
          <h1>🏥 AI Medical Record Extractor</h1>
          <div className="nav-links">
            <span style={{ color: isHealthy === true ? '#28a745' : isHealthy === false ? '#dc3545' : '#666' }}>
              {isHealthy === true ? '● Backend Connected' : isHealthy === false ? '● Backend Disconnected' : '● Checking...'}
            </span>
          </div>
        </div>
      </nav>

      <div className="container">
        <div className="header">
          <h1>AI Medical Record Extractor</h1>
          <p>
            Upload medical records and extract structured information using offline AI.
            <br />
            Works completely offline with CPU-only inference.
          </p>
        </div>

        {error && (
          <div className="error">
            <strong>Error:</strong> {error}
          </div>
        )}

        {!extractedData && !error && (
          <UploadComponent
            onExtractionComplete={handleExtractionComplete}
            onError={handleError}
          />
        )}

        {extractedData && (
          <>
            <ResultsComponent data={extractedData} />
            <div style={{ textAlign: 'center', marginTop: '20px' }}>
              <button className="btn" onClick={handleReset}>
                Upload Another File
              </button>
            </div>
          </>
        )}

        <div className="footer">
          <p>© 2024 AI Medical Record Extractor | Offline-First | CPU-Only Inference</p>
        </div>
      </div>
    </div>
  );
}

export default App;