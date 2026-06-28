import React, { useState, useEffect } from 'react';
import { getRecords, deleteRecord } from '../services/api';

const HistoryComponent = ({ onSelectRecord, onDeleteRecord }) => {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadRecords();
  }, []);

  const loadRecords = async () => {
    try {
      setLoading(true);
      const data = await getRecords(50, 0);
      setRecords(data.records || []);
      setError(null);
    } catch (error) {
      setError('Failed to load records');
      console.error('Error loading records:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (recordId, event) => {
    event.stopPropagation();
    if (!window.confirm('Are you sure you want to delete this record?')) {
      return;
    }

    try {
      await deleteRecord(recordId);
      setRecords(records.filter(record => record.id !== recordId));
      if (onDeleteRecord) {
        onDeleteRecord(recordId);
      }
    } catch (error) {
      setError('Failed to delete record');
      console.error('Error deleting record:', error);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="card">
        <h2>📜 Extraction History</h2>
        <div className="loading">
          <div className="spinner"></div>
          <span>Loading history...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <h2>📜 Extraction History</h2>
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
        <button className="btn" onClick={loadRecords}>
          Retry
        </button>
      </div>
    );
  }

  if (records.length === 0) {
    return (
      <div className="card">
        <h2>📜 Extraction History</h2>
        <div className="empty-state">
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
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <h3>No Records Yet</h3>
          <p>Start by uploading a medical record to see it here</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>📜 Extraction History</h2>
        <button className="btn btn-secondary" onClick={loadRecords}>
          Refresh
        </button>
      </div>
      
      <div className="history-list">
        {records.map((record) => (
          <div
            key={record.id}
            className="history-item"
            onClick={() => onSelectRecord && onSelectRecord(record)}
          >
            <div className="history-item-info">
              <div className="history-item-title">
                {record.patient_name || 'Unknown Patient'}
              </div>
              <div className="history-item-meta">
                {formatDate(record.created_at)} • {record.file_name || 'Text Input'}
              </div>
              {record.diagnosis && (
                <div style={{ fontSize: '0.875rem', color: '#667eea', marginTop: '4px' }}>
                  {record.diagnosis.substring(0, 100)}
                  {record.diagnosis.length > 100 && '...'}
                </div>
              )}
            </div>
            <div className="history-item-actions">
              <button
                className="btn btn-danger"
                onClick={(e) => handleDelete(record.id, e)}
                title="Delete record"
              >
                🗑️
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HistoryComponent;