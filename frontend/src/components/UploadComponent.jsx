import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { extractFromFile } from '../services/api';

const UploadComponent = ({ onExtractionComplete, onError }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setUploadedFile(file);
    setIsLoading(true);
    setUploadProgress(0);

    // Simulate progress
    const progressInterval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return 90;
        }
        return prev + 10;
      });
    }, 200);

    try {
      const result = await extractFromFile(file);
      clearInterval(progressInterval);
      setUploadProgress(100);
      setTimeout(() => {
        onExtractionComplete(result);
      }, 500);
    } catch (error) {
      clearInterval(progressInterval);
      console.error('Extraction error:', error);
      onError(error.response?.data?.detail || error.message || 'Extraction failed');
    } finally {
      setIsLoading(false);
      setUploadProgress(0);
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

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  const getFileIcon = (file) => {
    const type = file.type;
    if (type === 'application/pdf') return '📄';
    if (type.startsWith('image/')) return '🖼️';
    if (type === 'text/plain') return '📝';
    return '📎';
  };

  return (
    <div className="card">
      <h2>📤 Upload Medical Record</h2>
      
      <div
        {...getRootProps()}
        className={`upload-zone ${isDragActive ? 'active' : ''}`}
      >
        <input {...getInputProps()} />
        
        {!isDragActive && (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            style={{ marginBottom: '20px' }}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
        )}
        
        {isDragActive ? (
          <div>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="64"
              height="64"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              style={{ marginBottom: '20px' }}
            >
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="17 8 12 3 7 8" />
              <line x1="12" y1="3" x2="12" y2="15" />
            </svg>
            <p style={{ fontSize: '1.2rem', fontWeight: '600', color: '#667eea' }}>
              Drop the file here...
            </p>
          </div>
        ) : (
          <>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              style={{ marginBottom: '20px' }}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
            <p style={{ fontSize: '1.1rem', fontWeight: '500', marginBottom: '8px' }}>
              Drag and drop a medical record here, or click to select
            </p>
            <p className="file-types">
              Supported formats: PDF, TXT, PNG, JPG, JPEG, BMP, TIFF (Max 10MB)
            </p>
          </>
        )}
      </div>

      {uploadedFile && !isLoading && (
        <div className="file-info fade-in">
          <span style={{ fontSize: '2rem' }}>{getFileIcon(uploadedFile)}</span>
          <div style={{ flex: 1 }}>
            <strong>{uploadedFile.name}</strong>
            <br />
            <small>{formatFileSize(uploadedFile.size)}</small>
          </div>
          <span className="badge badge-success">Ready</span>
        </div>
      )}

      {isLoading && (
        <div className="loading fade-in">
          <div className="spinner"></div>
          <div style={{ flex: 1 }}>
            <div style={{ marginBottom: '8px', fontWeight: '500' }}>Processing document...</div>
            <div style={{ 
              width: '100%', 
              height: '6px', 
              background: '#e0e0e0', 
              borderRadius: '3px', 
              overflow: 'hidden' 
            }}>
              <div 
                style={{ 
                  width: `${uploadProgress}%`, 
                  height: '100%', 
                  background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
                  borderRadius: '3px',
                  transition: 'width 0.3s ease'
                }} 
              />
            </div>
            <div style={{ fontSize: '0.85rem', color: '#666', marginTop: '4px' }}>
              {uploadProgress < 100 ? `${uploadProgress}%` : 'Complete!'}
            </div>
          </div>
        </div>
      )}

      <div style={{ marginTop: '20px', padding: '16px', background: '#f8f9fa', borderRadius: '8px', fontSize: '0.9rem', color: '#666' }}>
        <strong>💡 Supported formats:</strong>
        <ul style={{ marginTop: '8px', marginLeft: '20px' }}>
          <li><strong>PDF:</strong> Portable Document Format</li>
          <li><strong>TXT:</strong> Plain text files</li>
          <li><strong>Images:</strong> PNG, JPG, JPEG, BMP, TIFF (OCR enabled)</li>
        </ul>
      </div>
    </div>
  );
};

export default UploadComponent;