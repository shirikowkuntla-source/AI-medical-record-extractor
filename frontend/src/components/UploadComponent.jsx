import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { extractFromFile } from '../services/api';

const UploadComponent = ({ onExtractionComplete, onError }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setUploadedFile(file);
    setIsLoading(true);

    try {
      const result = await extractFromFile(file);
      onExtractionComplete(result);
    } catch (error) {
      console.error('Extraction error:', error);
      onError(error.response?.data?.detail || error.message || 'Extraction failed');
    } finally {
      setIsLoading(false);
    }
  }, [onExtractionComplete, onError]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'image/*': ['.png', '.jpg', '.jpeg', '.bmp', '.tiff'],
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: false,
  });

  return (
    <div className="card">
      <h2>Upload Medical Record</h2>
      
      <div
        {...getRootProps()}
        className={`upload-zone ${isDragActive ? 'active' : ''}`}
      >
        <input {...getInputProps()} />
        
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
          />
        </svg>
        
        {isDragActive ? (
          <p>Drop the file here...</p>
        ) : (
          <>
            <p>Drag and drop a medical record here, or click to select</p>
            <p className="file-types">
              Supported formats: PDF, TXT, PNG, JPG, JPEG, BMP, TIFF (Max 10MB)
            </p>
          </>
        )}
      </div>

      {uploadedFile && !isLoading && (
        <div className="file-info">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" />
            <polyline points="13 2 13 9 20 9" />
          </svg>
          <div>
            <strong>{uploadedFile.name}</strong>
            <br />
            <small>{(uploadedFile.size / 1024).toFixed(2)} KB</small>
          </div>
        </div>
      )}

      {isLoading && (
        <div className="loading">
          <div className="spinner"></div>
          <span style={{ marginLeft: '10px' }}>Processing document...</span>
        </div>
      )}
    </div>
  );
};

export default UploadComponent;