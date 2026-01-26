import { useState, useRef } from 'react'
import DocumentViewer from './DocumentViewer'
import FileAnalysisSummary from './FileAnalysisSummary'

function FileUpload({ token, patientId, onUploadComplete, onAnalyzeFile }) {
  const fileInputRef = useRef(null)
  const [isDragging, setIsDragging] = useState(false)
  const [uploadProgress, setUploadProgress] = useState({})
  const [uploadedFiles, setUploadedFiles] = useState([])
  const [error, setError] = useState(null)
  const [viewingDocument, setViewingDocument] = useState(null)
  const [extractedRecords, setExtractedRecords] = useState([])
  const [analyzingFile, setAnalyzingFile] = useState(null)

  const handleDragEnter = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const uploadFile = async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    try {
      setUploadProgress(prev => ({ ...prev, [file.name]: 0 }))

      const xhr = new XMLHttpRequest()

      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
          const percentComplete = (e.loaded / e.total) * 100
          setUploadProgress(prev => ({ ...prev, [file.name]: percentComplete }))
        }
      })

      xhr.addEventListener('load', () => {
        if (xhr.status === 200) {
          const response = JSON.parse(xhr.responseText)
          
          const fileData = {
            name: file.name,
            type: file.type,
            size: file.size,
            timestamp: new Date().toLocaleString(),
            status: 'success',
            extractedData: response.extracted_data,
            rawText: response.extracted_data?.raw_text || ''
          }
          
          setUploadedFiles(prev => [...prev, fileData])
          
          if (response.extracted_data?.patient_id) {
            setExtractedRecords(prev => [...prev, response.extracted_data])
          }
          
          setUploadProgress(prev => {
            const newProgress = { ...prev }
            delete newProgress[file.name]
            return newProgress
          })
          
          if (onUploadComplete) {
            onUploadComplete(response)
          }
        } else {
          setError(`Upload failed with status ${xhr.status}`)
        }
      })

      xhr.addEventListener('error', () => {
        setError(`Failed to upload ${file.name}`)
        setUploadProgress(prev => {
          const newProgress = { ...prev }
          delete newProgress[file.name]
          return newProgress
        })
      })

      xhr.open('POST', 'http://localhost:8000/api/v1/patients/upload', true)
      xhr.setRequestHeader('Authorization', `Bearer ${token}`)
      xhr.send(formData)
    } catch (err) {
      setError(err.message)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)

    const files = Array.from(e.dataTransfer.files)
    processFiles(files)
  }

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files)
    processFiles(files)
  }

  const handleBrowseClick = () => {
    fileInputRef.current?.click()
  }

  const processFiles = (files) => {
    setError(null)
    files.forEach(file => {
      uploadFile(file)
    })
  }

  const viewFile = (file) => {
    setViewingDocument({
      name: file.name,
      type: file.type?.includes('pdf') ? 'pdf' : 'text',
      size: file.size,
      timestamp: file.timestamp,
      preview: file.rawText || file.extractedData?.raw_text || 'No content available',
      previewUrl: null
    })
  }

  const handleAnalyzeFile = (file) => {
    setAnalyzingFile(file)
    if (onAnalyzeFile) {
      onAnalyzeFile(file)
    }
  }

  return (
    <>
      {analyzingFile && (
        <FileAnalysisSummary
          file={analyzingFile}
          token={token}
          onClose={() => setAnalyzingFile(null)}
          onViewSource={(data) => {
            setViewingDocument({
              name: data.file.name,
              type: data.file.type?.includes('pdf') ? 'pdf' : 'text',
              size: data.file.size,
              timestamp: data.file.timestamp,
              preview: data.file.rawText || data.file.extractedData?.raw_text || 'No content available',
              previewUrl: null,
              searchTerm: data.searchTerm,
              highlightData: data.highlightData
            })
            setAnalyzingFile(null)
          }}
        />
      )}
      {viewingDocument && (
        <DocumentViewer
          document={viewingDocument}
          onClose={() => setViewingDocument(null)}
        />
      )}
      <div className="file-upload-container">
        <div
          className={`drag-drop-zone ${isDragging ? 'dragging' : ''}`}
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          <div className="drag-drop-content">
            <div className="upload-icon">📁</div>
            <h4>Drag and drop files here</h4>
            <p>or</p>
            <button 
              type="button"
              onClick={handleBrowseClick}
              className="btn-file-select"
              style={{ pointerEvents: 'auto' }}
            >
              Browse Files
            </button>
            <input
              ref={fileInputRef}
              type="file"
              multiple
              onChange={handleFileSelect}
              accept=".pdf,.doc,.docx,.txt,.jpg,.png,.jpeg"
              style={{ 
                position: 'absolute',
                left: '-9999px',
                top: '-9999px'
              }}
            />
            <p className="file-types">Supported: PDF, DOC, DOCX, TXT, JPG, PNG</p>
          </div>
        </div>

        {error && (
          <div className="upload-error">
            {error}
          </div>
        )}

        {Object.entries(uploadProgress).length > 0 && (
          <div className="upload-progress">
            {Object.entries(uploadProgress).map(([fileName, progress]) => (
              <div key={fileName} className="progress-item">
                <p>{fileName}</p>
                <div className="progress-bar">
                  <div className="progress-fill" style={{ width: `${progress}%` }} />
                </div>
                <span>{Math.round(progress)}%</span>
              </div>
            ))}
          </div>
        )}

        {uploadedFiles.length > 0 && (
          <div className="uploaded-files">
            <h4>Uploaded Files</h4>
            <div className="file-list">
              {uploadedFiles.map((file, idx) => (
                <div key={idx} className="file-item">
                  <span className="file-icon">✓</span>
                  <div className="file-details">
                    <p className="file-name">{file.name}</p>
                    <p className="file-meta">
                      {(file.size / 1024).toFixed(2)} KB | {file.timestamp}
                    </p>
                  </div>
                  <div className="file-actions">
                    <button
                      onClick={() => handleAnalyzeFile(file)}
                      className="btn-analyze-file"
                      title="Analyze with AI and view summary"
                    >
                      🔍
                    </button>
                    <button
                      onClick={() => viewFile(file)}
                      className="btn-view-file"
                      title="View and search document"
                    >
                      📄
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {extractedRecords.length > 0 && (
          <div className="extracted-records">
            <h4>✅ Extracted Patient Records</h4>
            {extractedRecords.map((record, idx) => (
              <div key={idx} className="extracted-record-card" style={{
                backgroundColor: '#f8f9fa',
                border: '2px solid #28a745',
                borderRadius: '8px',
                padding: '20px',
                marginBottom: '15px'
              }}>
                <div className="record-header" style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: '15px',
                  paddingBottom: '10px',
                  borderBottom: '2px solid #28a745'
                }}>
                  <h5 style={{ margin: 0, fontSize: '18px', color: '#2c3e50' }}>
                    {record.patient_name || 'Unknown Patient'}
                  </h5>
                  {record.patient_id && (
                    <span style={{
                      backgroundColor: '#28a745',
                      color: 'white',
                      padding: '4px 12px',
                      borderRadius: '20px',
                      fontSize: '12px',
                      fontWeight: 'bold'
                    }}>
                      ID: {record.patient_id}
                    </span>
                  )}
                </div>
                
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '15px' }}>
                  {/* Demographics */}
                  <div style={{
                    backgroundColor: 'white',
                    padding: '15px',
                    borderRadius: '6px',
                    border: '1px solid #dee2e6'
                  }}>
                    <h6 style={{ 
                      fontSize: '14px', 
                      fontWeight: 'bold', 
                      marginBottom: '10px',
                      color: '#495057',
                      borderBottom: '2px solid #3498db',
                      paddingBottom: '5px'
                    }}>
                      👤 Demographics
                    </h6>
                    <div style={{ fontSize: '13px', lineHeight: '1.8' }}>
                      <p style={{ margin: '0 0 5px 0' }}>
                        <strong>Age:</strong> <span style={{ color: '#555' }}>{record.age || 'N/A'}</span>
                      </p>
                      <p style={{ margin: '0 0 5px 0' }}>
                        <strong>Gender:</strong> <span style={{ color: '#555' }}>{record.gender || 'N/A'}</span>
                      </p>
                      <p style={{ margin: '0 0 5px 0' }}>
                        <strong>DOB:</strong> <span style={{ color: '#555' }}>{record.date_of_birth || 'N/A'}</span>
                      </p>
                      <p style={{ margin: 0 }}>
                        <strong>Blood Type:</strong> <span style={{ color: '#555' }}>{record.blood_type || 'N/A'}</span>
                      </p>
                    </div>
                  </div>

                  {/* Vital Signs */}
                  {record.vital_signs && Object.keys(record.vital_signs).length > 0 && (
                    <div style={{
                      backgroundColor: 'white',
                      padding: '15px',
                      borderRadius: '6px',
                      border: '1px solid #dee2e6'
                    }}>
                      <h6 style={{ 
                        fontSize: '14px', 
                        fontWeight: 'bold', 
                        marginBottom: '10px',
                        color: '#495057',
                        borderBottom: '2px solid #e74c3c',
                        paddingBottom: '5px'
                      }}>
                        💓 Vital Signs
                      </h6>
                      <div style={{ fontSize: '13px', lineHeight: '1.8' }}>
                        {record.vital_signs.blood_pressure && (
                          <p style={{ margin: '0 0 5px 0' }}>
                            <strong>BP:</strong> <span style={{ color: '#555' }}>{record.vital_signs.blood_pressure}</span>
                          </p>
                        )}
                        {record.vital_signs.pulse && (
                          <p style={{ margin: '0 0 5px 0' }}>
                            <strong>Pulse:</strong> <span style={{ color: '#555' }}>{record.vital_signs.pulse} bpm</span>
                          </p>
                        )}
                        {record.vital_signs.temperature && (
                          <p style={{ margin: 0 }}>
                            <strong>Temp:</strong> <span style={{ color: '#555' }}>{record.vital_signs.temperature}°F</span>
                          </p>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Allergies */}
                  {record.allergies && record.allergies.length > 0 && (
                    <div style={{
                      backgroundColor: '#ffe6e6',
                      padding: '15px',
                      borderRadius: '6px',
                      border: '2px solid #e74c3c'
                    }}>
                      <h6 style={{ 
                        fontSize: '14px', 
                        fontWeight: 'bold', 
                        marginBottom: '10px',
                        color: '#c0392b',
                        borderBottom: '2px solid #e74c3c',
                        paddingBottom: '5px'
                      }}>
                        ⚠️ Allergies
                      </h6>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {record.allergies.map((allergy, aIdx) => (
                          <div key={aIdx} style={{
                            backgroundColor: allergy.severity === 'CRITICAL' ? '#c0392b' : '#e74c3c',
                            color: 'white',
                            padding: '8px 12px',
                            borderRadius: '6px',
                            fontSize: '12px',
                            fontWeight: 'bold'
                          }}>
                            {allergy.substance} ({allergy.severity})
                            <div style={{ fontSize: '11px', fontWeight: 'normal', marginTop: '4px', opacity: 0.9 }}>
                              {allergy.reaction}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Conditions */}
                  {record.conditions && record.conditions.length > 0 && (
                    <div style={{
                      backgroundColor: 'white',
                      padding: '15px',
                      borderRadius: '6px',
                      border: '1px solid #dee2e6'
                    }}>
                      <h6 style={{ 
                        fontSize: '14px', 
                        fontWeight: 'bold', 
                        marginBottom: '10px',
                        color: '#495057',
                        borderBottom: '2px solid #9b59b6',
                        paddingBottom: '5px'
                      }}>
                        🏥 Conditions
                      </h6>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                        {record.conditions.map((cond, cIdx) => (
                          <div key={cIdx} style={{
                            backgroundColor: '#f0f0f0',
                            padding: '6px 10px',
                            borderRadius: '4px',
                            fontSize: '12px',
                            color: '#2c3e50'
                          }}>
                            <strong>{cond.condition}</strong>
                            <span style={{ marginLeft: '6px', color: '#7f8c8d' }}>({cond.status})</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Medications */}
                  {record.medications && record.medications.length > 0 && (
                    <div style={{
                      backgroundColor: 'white',
                      padding: '15px',
                      borderRadius: '6px',
                      border: '1px solid #dee2e6'
                    }}>
                      <h6 style={{ 
                        fontSize: '14px', 
                        fontWeight: 'bold', 
                        marginBottom: '10px',
                        color: '#495057',
                        borderBottom: '2px solid #f39c12',
                        paddingBottom: '5px'
                      }}>
                        💊 Medications
                      </h6>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                        {record.medications.map((med, mIdx) => (
                          <div key={mIdx} style={{
                            fontSize: '12px',
                            padding: '4px 0',
                            borderBottom: mIdx < record.medications.length - 1 ? '1px solid #f0f0f0' : 'none'
                          }}>
                            <strong style={{ color: '#2c3e50' }}>{med.name}</strong>
                            <span style={{ marginLeft: '6px', color: '#7f8c8d' }}>{med.dose}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <div style={{
                  marginTop: '15px',
                  padding: '12px',
                  backgroundColor: '#d4edda',
                  border: '1px solid #c3e6cb',
                  borderRadius: '6px',
                  textAlign: 'center'
                }}>
                  <p style={{ 
                    margin: 0, 
                    fontSize: '13px', 
                    color: '#155724',
                    fontWeight: 'bold'
                  }}>
                    ✓ Patient record successfully created and added to system. You can now search for this patient.
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  )
}

export default FileUpload