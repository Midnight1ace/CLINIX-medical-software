import { useState, useEffect } from 'react'

function FileAnalysisSummary({ file, token, onClose, onViewSource }) {
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedHighlight, setSelectedHighlight] = useState(null)

  useEffect(() => {
    const analyzeFile = async () => {
      try {
        setLoading(true)
        // Extract and analyze the file content
        const fileContent = file.rawText || file.extractedData?.raw_text || ''
        
        // Create analysis from extracted data
        const fileAnalysis = {
          fileName: file.name,
          fileType: file.type,
          timestamp: file.timestamp,
          rawContent: fileContent,
          extractedData: file.extractedData || {},
          sections: parseContentSections(fileContent),
          highlights: extractHighlights(fileContent, file.extractedData),
          encounters: buildEncounters(file.extractedData)
        }
        
        setAnalysis(fileAnalysis)
      } catch (err) {
        console.error('Error analyzing file:', err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    analyzeFile()
  }, [file, token])

  const buildEncounters = (extractedData) => {
    const encounters = []
    
    // Create encounter from extracted data
    if (extractedData && Object.keys(extractedData).length > 0) {
      encounters.push({
        id: 1,
        date: extractedData.encounter_date || extractedData.date || 'Unknown',
        type: extractedData.encounter_type || 'Medical Encounter',
        provider: extractedData.provider || 'Not specified',
        facility: extractedData.facility || extractedData.source || 'Not specified',
        summary: extractedData.summary || buildSummaryFromData(extractedData),
        reason: extractedData.chief_complaint || extractedData.reason_for_visit || 'Not specified',
        allergies: extractedData.allergies || [],
        medications: extractedData.medications || [],
        conditions: extractedData.conditions || [],
        vitals: extractedData.vital_signs || {},
        diagnosis: extractedData.diagnosis || 'Not specified'
      })
    }
    
    return encounters
  }

  const buildSummaryFromData = (data) => {
    const parts = []
    if (data.chief_complaint) parts.push(data.chief_complaint)
    if (data.diagnosis) parts.push(`Diagnosis: ${data.diagnosis}`)
    if (data.assessment) parts.push(data.assessment)
    return parts.join('. ') || 'Medical record information'
  }

  const parseContentSections = (content) => {
    const sections = []
    
    // Split content into paragraphs
    const paragraphs = content.split('\n\n').filter(p => p.trim())
    
    paragraphs.forEach((para, idx) => {
      if (para.trim().length > 20) {
        sections.push({
          id: idx,
          type: detectSectionType(para),
          content: para.trim(),
          startIndex: content.indexOf(para)
        })
      }
    })
    
    return sections
  }

  const detectSectionType = (text) => {
    const lower = text.toLowerCase()
    if (lower.includes('allerg') || lower.includes('reaction')) return 'allergies'
    if (lower.includes('medic') || lower.includes('drug') || lower.includes('dose')) return 'medications'
    if (lower.includes('condition') || lower.includes('diagnos') || lower.includes('disease')) return 'conditions'
    if (lower.includes('vital') || lower.includes('bp') || lower.includes('temp') || lower.includes('pulse')) return 'vitals'
    if (lower.includes('history') || lower.includes('past')) return 'history'
    return 'general'
  }

  const extractHighlights = (content, extractedData) => {
    const highlights = []
    
    // Extract allergies
    if (extractedData?.allergies && Array.isArray(extractedData.allergies)) {
      extractedData.allergies.forEach(allergy => {
        const searchText = allergy.substance || allergy.name || ''
        if (searchText) {
          const idx = content.toLowerCase().indexOf(searchText.toLowerCase())
          if (idx !== -1) {
            highlights.push({
              type: 'allergy',
              text: searchText,
              index: idx,
              data: allergy,
              severity: allergy.severity
            })
          }
        }
      })
    }
    
    // Extract medications
    if (extractedData?.medications && Array.isArray(extractedData.medications)) {
      extractedData.medications.forEach(med => {
        const searchText = med.name || ''
        if (searchText) {
          const idx = content.toLowerCase().indexOf(searchText.toLowerCase())
          if (idx !== -1) {
            highlights.push({
              type: 'medication',
              text: searchText,
              index: idx,
              data: med
            })
          }
        }
      })
    }
    
    // Extract conditions
    if (extractedData?.conditions && Array.isArray(extractedData.conditions)) {
      extractedData.conditions.forEach(cond => {
        const searchText = cond.condition || cond.name || ''
        if (searchText) {
          const idx = content.toLowerCase().indexOf(searchText.toLowerCase())
          if (idx !== -1) {
            highlights.push({
              type: 'condition',
              text: searchText,
              index: idx,
              data: cond
            })
          }
        }
      })
    }
    
    return highlights.sort((a, b) => a.index - b.index)
  }

  const handleHighlightClick = (highlight) => {
    // Navigate to document viewer with highlight
    if (onViewSource) {
      onViewSource({
        file,
        searchTerm: highlight.text,
        highlightData: highlight
      })
    }
  }

  const getConfidenceColor = (value) => {
    const num = parseInt(value) || 0
    if (num >= 90) return '#27ae60'
    if (num >= 75) return '#f39c12'
    return '#e74c3c'
  }

  const getConfidencePercentage = (data) => {
    if (typeof data === 'object' && data.confidence) {
      return parseInt(data.confidence) || 100
    }
    return 100
  }

  if (loading) {
    return (
      <div className="analysis-modal">
        <div className="analysis-container">
          <div className="analysis-header">
            <h2>Analyzing File...</h2>
            <button onClick={onClose} className="btn-close">✕</button>
          </div>
          <div className="analysis-loading">
            <p>Processing file content...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="analysis-modal">
        <div className="analysis-container">
          <div className="analysis-header">
            <h2>Analysis Error</h2>
            <button onClick={onClose} className="btn-close">✕</button>
          </div>
          <div className="analysis-error">
            <p>{error}</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="analysis-modal">
      <div className="analysis-split-container">
        {/* Left side - Document Preview */}
        <div className="analysis-document-side">
          <div className="document-preview-panel">
            <h3>📄 Document Content</h3>
            <div className="document-preview-content">
              {analysis.rawContent.substring(0, 2000)}
              {analysis.rawContent.length > 2000 && '...'}
            </div>
          </div>
        </div>

        {/* Right side - Structured Data */}
        <div className="analysis-data-side">
          <div className="analysis-header-top">
            <h2>Encounters</h2>
            <button onClick={onClose} className="btn-close">✕</button>
          </div>

          <div className="encounters-container">
            {analysis.encounters && analysis.encounters.map((encounter, idx) => (
              <div key={idx} className="encounter-card">
                <div className="encounter-title">
                  <h4>Encounter #{idx + 1}</h4>
                </div>

                {/* Date Field */}
                <div className="encounter-field">
                  <label>Date</label>
                  <div className="field-content">
                    <span className="field-value">{encounter.date}</span>
                    <span className="confidence-badge" style={{ backgroundColor: '#28a745' }}>100%</span>
                  </div>
                  {encounter.date && (
                    <button 
                      className="btn-field-search"
                      onClick={() => handleHighlightClick({ text: encounter.date })}
                      title="Find in document"
                    >
                      🔍
                    </button>
                  )}
                </div>

                {/* Type Field */}
                <div className="encounter-field">
                  <label>Type</label>
                  <div className="field-content">
                    <span className="field-value">{encounter.type}</span>
                    <span className="confidence-badge" style={{ backgroundColor: '#3498db' }}>90%</span>
                  </div>
                  {encounter.type && (
                    <button 
                      className="btn-field-search"
                      onClick={() => handleHighlightClick({ text: encounter.type })}
                      title="Find in document"
                    >
                      🔍
                    </button>
                  )}
                </div>

                {/* Provider Field */}
                <div className="encounter-field">
                  <label>Provider</label>
                  <div className="field-content">
                    <input 
                      type="text" 
                      className="field-input" 
                      value={encounter.provider}
                      readOnly
                    />
                    <span className="confidence-badge" style={{ backgroundColor: '#e74c3c' }}>0%</span>
                  </div>
                  {encounter.provider && encounter.provider !== 'Not specified' && (
                    <button 
                      className="btn-field-search"
                      onClick={() => handleHighlightClick({ text: encounter.provider })}
                      title="Find in document"
                    >
                      🔍
                    </button>
                  )}
                </div>

                {/* Facility Field */}
                <div className="encounter-field">
                  <label>Facility</label>
                  <div className="field-content">
                    <span className="field-value">{encounter.facility}</span>
                    <span className="confidence-badge" style={{ backgroundColor: '#28a745' }}>100%</span>
                  </div>
                  {encounter.facility && (
                    <button 
                      className="btn-field-search"
                      onClick={() => handleHighlightClick({ text: encounter.facility })}
                      title="Find in document"
                    >
                      🔍
                    </button>
                  )}
                </div>

                {/* Summary Field */}
                <div className="encounter-field full-width">
                  <label>Summary</label>
                  <div className="field-content">
                    <span className="field-value">{encounter.summary}</span>
                    <span className="confidence-badge" style={{ backgroundColor: '#28a745' }}>100%</span>
                  </div>
                </div>

                {/* Action Button */}
                <div className="encounter-actions">
                  <button className="btn-approve-record">
                    ✓ Approve & Save Record
                  </button>
                </div>
              </div>
            ))}

            {(!analysis.encounters || analysis.encounters.length === 0) && (
              <p className="no-encounters">No encounters found in this document.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default FileAnalysisSummary
