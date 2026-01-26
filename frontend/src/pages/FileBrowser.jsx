import { useState, useEffect } from 'react'
import './FileBrowser.css'

function FileBrowser({ token, onFileSelect, onClose }) {
  const [files, setFiles] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedFile, setSelectedFile] = useState(null)
  const [fileContent, setFileContent] = useState(null)
  const [contentLoading, setContentLoading] = useState(false)

  useEffect(() => {
    loadFiles()
  }, [])

  const loadFiles = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch('http://localhost:8000/api/v1/files/browse', {
        headers: { 'Authorization': `Bearer ${token}` }
      })

      if (!response.ok) {
        throw new Error('Failed to load files')
      }

      const data = await response.json()
      setFiles(data.files || [])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleFileClick = async (file) => {
    setSelectedFile(file)
    setContentLoading(true)
    try {
      const response = await fetch(`http://localhost:8000/api/v1/files/${file.name}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })

      if (!response.ok) {
        throw new Error('Failed to load file content')
      }

      const data = await response.json()
      setFileContent(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setContentLoading(false)
    }
  }

  const handleSelectFile = () => {
    if (fileContent && onFileSelect) {
      onFileSelect({
        name: fileContent.filename,
        content: fileContent.content,
        size: fileContent.size,
        modified: fileContent.modified
      })
    }
  }

  return (
    <div className="file-browser-overlay">
      <div className="file-browser-modal">
        <div className="file-browser-header">
          <h2>📁 File Browser</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="file-browser-container">
          {/* Files List */}
          <div className="files-list-section">
            <h3>Available Files</h3>
            {loading ? (
              <div className="loading">Loading files...</div>
            ) : error ? (
              <div className="error-message">Error: {error}</div>
            ) : files.length === 0 ? (
              <div className="no-files">No files found in uploads directory</div>
            ) : (
              <div className="files-list">
                {files.map((file) => (
                  <div
                    key={file.name}
                    className={`file-item ${selectedFile?.name === file.name ? 'selected' : ''}`}
                    onClick={() => handleFileClick(file)}
                  >
                    <div className="file-icon">📄</div>
                    <div className="file-info">
                      <div className="file-name">{file.name}</div>
                      <div className="file-meta">
                        <span className="file-size">{file.size_readable}</span>
                        <span className="file-date">
                          {new Date(file.modified).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* File Content Preview */}
          <div className="file-content-section">
            <h3>Preview</h3>
            {selectedFile ? (
              contentLoading ? (
                <div className="loading">Loading content...</div>
              ) : fileContent ? (
                <div className="file-content">
                  <div className="content-header">
                    <span className="filename">{fileContent.filename}</span>
                    <span className="filesize">{(fileContent.size / 1024).toFixed(2)} KB</span>
                  </div>
                  <div className="content-preview">
                    {fileContent.content}
                  </div>
                  <button className="select-file-btn" onClick={handleSelectFile}>
                    ✓ Select This File
                  </button>
                </div>
              ) : (
                <div className="no-content">Unable to load file content</div>
              )
            ) : (
              <div className="no-selection">Select a file to preview</div>
            )}
          </div>
        </div>

        <div className="file-browser-footer">
          <button className="refresh-btn" onClick={loadFiles}>🔄 Refresh</button>
          <button className="close-modal-btn" onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  )
}

export default FileBrowser
