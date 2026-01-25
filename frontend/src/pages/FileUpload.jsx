import { useState } from 'react'
import DocumentViewer from './DocumentViewer'

function FileUpload({ token, patientId, onUploadComplete }) {
  const [isDragging, setIsDragging] = useState(false)
  const [uploadProgress, setUploadProgress] = useState({})
  const [uploadedFiles, setUploadedFiles] = useState([])
  const [error, setError] = useState(null)
  const [viewingDocument, setViewingDocument] = useState(null)
  const [extractedRecords, setExtractedRecords] = useState([])

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

  return (
    <>
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
            <label className="btn-file-select">
              Browse Files
              <input
                type="file"
                multiple
                onChange={handleFileSelect}
                style={{ display: 'none' }}
                accept=".pdf,.doc,.docx,.txt,.jpg,.png,.jpeg"
              />
            </label>
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
                  <button
                    onClick={() => viewFile(file)}
                    className="btn-view-file"
                    title="View and search document"
                  >
                    🔍
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {extractedRecords.length > 0 && (
          <div className="extracted-records">
            <h4>Extracted Patient Records</h4>
            {extractedRecords.map((record, idx) => (
              <div key={idx} className="extracted-record-card">
                <div className="record-header">
                  <h5>{record.patient_name || 'Unknown Patient'}</h5>
                  {record.patient_id && (
                    <span className="patient-id-badge">ID: {record.patient_id}</span>
                  )}
                </div>
                
                <div className="record-grid">
                  <div className="record-section">
                    <h6>Demographics</h6>
                    <p><strong>Age:</strong> {record.age || 'N/A'}</p>
                    <p><strong>Gender:</strong> {record.gender || 'N/A'}</p>
                    <p><strong>DOB:</strong> {record.date_of_birth || 'N/A'}</p>
                    <p><strong>Blood Type:</strong> {record.blood_type || 'N/A'}</p>
                  </div>

                  {record.allergies && record.allergies.length > 0 && (
                    <div className="record-section allergies-section">
                      <h6>Allergies</h6>
                      {record.allergies.map((allergy, aIdx) => (
                        <div key={aIdx} className={`allergy-tag ${allergy.severity?.toLowerCase()}`}>
                          {allergy.substance} ({allergy.severity})
                        </div>
                      ))}
                    </div>
                  )}

                  {record.medications && record.medications.length > 0 && (
                    <div className="record-section">
                      <h6>Medications</h6>
                      {record.medications.map((med, mIdx) => (
                        <p key={mIdx}>{med.name} - {med.dose}</p>
                      ))}
                    </div>
                  )}

                  {record.conditions && record.conditions.length > 0 && (
                    <div className="record-section">
                      <h6>Conditions</h6>
                      {record.conditions.map((cond, cIdx) => (
                        <p key={cIdx}>{cond.condition} ({cond.status})</p>
                      ))}
                    </div>
                  )}

                  {record.vital_signs && Object.keys(record.vital_signs).length > 0 && (
                    <div className="record-section">
                      <h6>Vital Signs</h6>
                      {record.vital_signs.blood_pressure && (
                        <p><strong>BP:</strong> {record.vital_signs.blood_pressure}</p>
                      )}
                      {record.vital_signs.pulse && (
                        <p><strong>Pulse:</strong> {record.vital_signs.pulse}</p>
                      )}
                      {record.vital_signs.temperature && (
                        <p><strong>Temp:</strong> {record.vital_signs.temperature}</p>
                      )}
                    </div>
                  )}
                </div>

                <div className="record-actions">
                  <p className="success-message">Patient added to system. You can now search for them.</p>
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
