import { useState } from 'react'

function DocumentViewer({ document, onClose }) {
  const [searchTerm, setSearchTerm] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [currentResultIndex, setCurrentResultIndex] = useState(0)
  const [highlightedText, setHighlightedText] = useState('')

  const handleSearch = (value) => {
    setSearchTerm(value)
    
    if (!value.trim()) {
      setSearchResults([])
      setCurrentResultIndex(0)
      return
    }

    const content = document.preview || ''
    const regex = new RegExp(`(${value})`, 'gi')
    const matches = []
    let match

    while ((match = regex.exec(content)) !== null) {
      matches.push({
        index: match.index,
        text: match[0],
        context: content.substring(
          Math.max(0, match.index - 50),
          Math.min(content.length, match.index + value.length + 50)
        )
      })
    }

    setSearchResults(matches)
    setCurrentResultIndex(0)
    if (matches.length > 0) {
      setHighlightedText(matches[0].text)
    }
  }

  const goToNextResult = () => {
    if (searchResults.length === 0) return
    const nextIndex = (currentResultIndex + 1) % searchResults.length
    setCurrentResultIndex(nextIndex)
    setHighlightedText(searchResults[nextIndex].text)
  }

  const goToPreviousResult = () => {
    if (searchResults.length === 0) return
    const prevIndex = (currentResultIndex - 1 + searchResults.length) % searchResults.length
    setCurrentResultIndex(prevIndex)
    setHighlightedText(searchResults[prevIndex].text)
  }

  const getHighlightedContent = () => {
    if (!searchTerm || searchResults.length === 0) {
      return document.preview || ''
    }

    const content = document.preview || ''
    const regex = new RegExp(`(${searchTerm})`, 'gi')
    const parts = content.split(regex)

    return parts.map((part, idx) => {
      if (part && part.toLowerCase() === searchTerm.toLowerCase()) {
        return (
          <span
            key={idx}
            className={`highlight ${idx === searchResults[currentResultIndex]?.index ? 'active' : ''}`}
            style={{
              backgroundColor:
                idx === searchResults[currentResultIndex]?.index ? '#FFD700' : '#FFFF99',
              padding: '2px 4px',
              borderRadius: '3px'
            }}
          >
            {part}
          </span>
        )
      }
      return part
    })
  }

  return (
    <div className="document-viewer-modal">
      <div className="document-viewer-container">
        <div className="document-header">
          <div className="document-info">
            <h2>📄 {document.name}</h2>
            <p className="file-meta">{(document.size / 1024).toFixed(2)} KB • {document.timestamp}</p>
          </div>
          <button onClick={onClose} className="btn-close">✕</button>
        </div>

        <div className="search-box">
          <div className="search-input-wrapper">
            <input
              type="text"
              placeholder="🔍 Search for medications, allergies, conditions..."
              value={searchTerm}
              onChange={(e) => handleSearch(e.target.value)}
              className="search-input"
            />
            {searchTerm && searchResults.length > 0 && (
              <div className="search-nav">
                <button onClick={goToPreviousResult} className="btn-nav">←</button>
                <span className="result-count">
                  {currentResultIndex + 1} of {searchResults.length}
                </span>
                <button onClick={goToNextResult} className="btn-nav">→</button>
              </div>
            )}
          </div>
          {searchTerm && searchResults.length === 0 && (
            <p className="no-results">No matches found</p>
          )}
        </div>

        <div className="document-content">
          {document.type === 'pdf' ? (
            <div className="pdf-placeholder">
              <p>📑 PDF Preview</p>
              <p style={{ fontSize: '12px', color: '#7f8c8d', marginTop: '10px' }}>
                PDF files can be viewed in your default PDF reader
              </p>
              <a
                href={document.previewUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary"
                style={{ marginTop: '15px', display: 'inline-block' }}
              >
                Open PDF
              </a>
            </div>
          ) : (
            <div className="text-content">
              {getHighlightedContent()}
            </div>
          )}
        </div>

        {searchResults.length > 0 && (
          <div className="search-results-panel">
            <h4>Found {searchResults.length} match{searchResults.length !== 1 ? 'es' : ''}</h4>
            <div className="result-list">
              {searchResults.slice(0, 5).map((result, idx) => (
                <div
                  key={idx}
                  className={`result-item ${idx === currentResultIndex ? 'active' : ''}`}
                  onClick={() => {
                    setCurrentResultIndex(idx)
                    setHighlightedText(result.text)
                  }}
                >
                  <span className="result-preview">
                    ...{result.context.substring(Math.max(0, result.context.length - 60))}...
                  </span>
                </div>
              ))}
              {searchResults.length > 5 && (
                <p style={{ fontSize: '12px', color: '#7f8c8d', padding: '10px' }}>
                  +{searchResults.length - 5} more results
                </p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default DocumentViewer
