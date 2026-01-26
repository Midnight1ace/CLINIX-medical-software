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
    // Return structured data instead of plain text
    return {
      patient: {
        name: data.patient_name || 'Unknown',
        age: data.age || 'N/A',
        gender: data.gender === 'M' ? 'Male' : data.gender === 'F' ? 'Female' : 'N/A'
      },
      chiefComplaint: data.chief_complaint || null,
      diagnoses: data.diagnoses && Array.isArray(data.diagnoses) ? data.diagnoses : [],
      vitalSigns: data.vital_signs || {},
      medications: data.medications && Array.isArray(data.medications) ? data.medications : [],
      conditions: data.conditions && Array.isArray(data.conditions) ? data.conditions : [],
      allergies: data.allergies && Array.isArray(data.allergies) ? data.allergies : []
    }
  }

  const renderStructuredSummary = (summaryData) => {
    if (typeof summaryData === 'string') {
      return <div>{summaryData}</div>
    }

    return (
      <div style={{ fontSize: '13px', lineHeight: '1.6' }}>
        {/* Patient Header */}
        <div style={{ 
          marginBottom: '15px', 
          paddingBottom: '10px', 
          borderBottom: '2px solid #3498db' 
        }}>
          <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#2c3e50', marginBottom: '5px' }}>
            {summaryData.patient.name}
          </div>
          <div style={{ color: '#7f8c8d', fontSize: '14px' }}>
            {summaryData.patient.age} year old {summaryData.patient.gender}
          </div>
        </div>

        {/* Chief Complaint */}
        {summaryData.chiefComplaint && (
          <div style={{ marginBottom: '15px' }}>
            <div style={{ 
              fontWeight: 'bold', 
              color: '#2c3e50', 
              marginBottom: '8px',
              fontSize: '14px',
              textTransform: 'uppercase',
              letterSpacing: '0.5px'
            }}>
              Chief Complaint
            </div>
            <div style={{ 
              padding: '12px 15px', 
              backgroundColor: '#e8f4f8', 
              borderLeft: '4px solid #3498db',
              borderRadius: '4px',
              color: '#2c3e50',
              fontSize: '14px',
              lineHeight: '1.6',
              fontStyle: 'italic'
            }}>
              "{summaryData.chiefComplaint}"
            </div>
          </div>
        )}

        {/* Vital Signs */}
        {Object.keys(summaryData.vitalSigns).length > 0 && (
          <div style={{ marginBottom: '15px' }}>
            <div style={{ 
              fontWeight: 'bold', 
              color: '#2c3e50', 
              marginBottom: '5px',
              fontSize: '13px'
            }}>
              Vital Signs:
            </div>
            <div style={{ 
              display: 'flex', 
              gap: '10px', 
              flexWrap: 'wrap',
              padding: '8px 12px',
              backgroundColor: '#fff3cd',
              borderRadius: '4px',
              border: '1px solid #ffc107'
            }}>
              {summaryData.vitalSigns.blood_pressure && (
                <span><strong>BP:</strong> {summaryData.vitalSigns.blood_pressure}</span>
              )}
              {summaryData.vitalSigns.pulse && (
                <span><strong>HR:</strong> {summaryData.vitalSigns.pulse} bpm</span>
              )}
              {summaryData.vitalSigns.temperature && (
                <span><strong>Temp:</strong> {summaryData.vitalSigns.temperature}°F</span>
              )}
            </div>
          </div>
        )}

        {/* Diagnoses */}
        {summaryData.diagnoses.length > 0 && (
          <div style={{ marginBottom: '15px' }}>
            <div style={{ 
              fontWeight: 'bold', 
              color: '#2c3e50', 
              marginBottom: '5px',
              fontSize: '13px'
            }}>
              Assessment/Diagnosis:
            </div>
            <div style={{ 
              padding: '8px 12px', 
              backgroundColor: '#e7f3ff', 
              borderRadius: '4px',
              border: '1px solid #3498db'
            }}>
              {summaryData.diagnoses.map((diag, i) => (
                <div key={i} style={{ 
                  marginBottom: i < summaryData.diagnoses.length - 1 ? '4px' : '0',
                  color: '#2c3e50'
                }}>
                  {i + 1}. {diag}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Conditions */}
        {summaryData.conditions.length > 0 && (
          <div style={{ marginBottom: '15px' }}>
            <div style={{ 
              fontWeight: 'bold', 
              color: '#2c3e50', 
              marginBottom: '5px',
              fontSize: '13px'
            }}>
              Conditions:
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
              {summaryData.conditions.map((cond, i) => (
                <span key={i} style={{
                  backgroundColor: '#9b59b6',
                  color: 'white',
                  padding: '4px 10px',
                  borderRadius: '12px',
                  fontSize: '11px',
                  fontWeight: '500'
                }}>
                  {cond.condition || cond.name}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Allergies */}
        {summaryData.allergies.length > 0 && (
          <div style={{ marginBottom: '15px' }}>
            <div style={{ 
              fontWeight: 'bold', 
              color: '#c0392b', 
              marginBottom: '5px',
              fontSize: '13px',
              display: 'flex',
              alignItems: 'center',
              gap: '5px'
            }}>
              ⚠️ Allergies:
            </div>
            <div style={{ 
              padding: '8px 12px', 
              backgroundColor: '#ffe6e6', 
              borderRadius: '4px',
              border: '2px solid #e74c3c'
            }}>
              {summaryData.allergies.map((allergy, i) => (
                <div key={i} style={{ 
                  marginBottom: i < summaryData.allergies.length - 1 ? '6px' : '0',
                  paddingBottom: i < summaryData.allergies.length - 1 ? '6px' : '0',
                  borderBottom: i < summaryData.allergies.length - 1 ? '1px solid #ffcccc' : 'none'
                }}>
                  <span style={{ fontWeight: 'bold', color: '#c0392b' }}>
                    {allergy.substance}
                  </span>
                  <span style={{ 
                    marginLeft: '6px',
                    padding: '2px 6px',
                    backgroundColor: allergy.severity === 'CRITICAL' ? '#c0392b' : '#e74c3c',
                    color: 'white',
                    borderRadius: '4px',
                    fontSize: '10px',
                    fontWeight: 'bold'
                  }}>
                    {allergy.severity}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Medications */}
        {summaryData.medications.length > 0 && (
          <div>
            <div style={{ 
              fontWeight: 'bold', 
              color: '#2c3e50', 
              marginBottom: '5px',
              fontSize: '13px'
            }}>
              Medications:
            </div>
            <div style={{ 
              padding: '8px 12px', 
              backgroundColor: '#fff3e0', 
              borderRadius: '4px',
              border: '1px solid #ff9800'
            }}>
              {summaryData.medications.map((med, i) => (
                <div key={i} style={{ 
                  marginBottom: i < summaryData.medications.length - 1 ? '4px' : '0',
                  color: '#555'
                }}>
                  • <strong>{med.name}</strong> - {med.dose}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    )
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

  const getFieldConfidence = (value, defaultValue = 'Unknown') => {
    if (!value || value === defaultValue || value === 'Not specified') return 0
    if (value.includes('See record') || value.includes('Pending')) return 50
    return 100
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 90) return '#28a745'
    if (confidence >= 70) return '#3498db'
    if (confidence >= 40) return '#f39c12'
    return '#e74c3c'
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
              {analysis.rawContent}
            </div>
          </div>
        </div>

        {/* Right side - Clinical Summary */}
        <div className="analysis-data-side">
          <div className="analysis-header-top">
            <h2>Clinical Summary</h2>
            <button onClick={onClose} className="btn-close">✕</button>
          </div>

          <div className="encounters-container">
            {analysis.encounters && analysis.encounters.map((encounter, idx) => (
              <div key={idx} style={{ 
                padding: '20px',
                backgroundColor: '#ffffff',
                borderRadius: '8px',
                border: '1px solid #dee2e6'
              }}>
                {/* Encounter Metadata - Compact Header */}
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '12px 15px',
                  backgroundColor: '#f8f9fa',
                  borderRadius: '6px',
                  marginBottom: '20px',
                  border: '1px solid #dee2e6'
                }}>
                  <div style={{ display: 'flex', gap: '20px', fontSize: '13px', flexWrap: 'wrap' }}>
                    {encounter.date && encounter.date !== 'Unknown' && (
                      <div>
                        <strong style={{ color: '#6c757d' }}>Date:</strong>{' '}
                        <span style={{ color: '#2c3e50' }}>{encounter.date}</span>
                      </div>
                    )}
                    {encounter.type && (
                      <div>
                        <strong style={{ color: '#6c757d' }}>Type:</strong>{' '}
                        <span style={{ color: '#2c3e50' }}>{encounter.type}</span>
                      </div>
                    )}
                    {encounter.provider && encounter.provider !== 'Not specified' && (
                      <div>
                        <strong style={{ color: '#6c757d' }}>Provider:</strong>{' '}
                        <span style={{ color: '#2c3e50' }}>{encounter.provider}</span>
                      </div>
                    )}
                    {encounter.facility && encounter.facility !== 'Not specified' && (
                      <div>
                        <strong style={{ color: '#6c757d' }}>Facility:</strong>{' '}
                        <span style={{ color: '#2c3e50' }}>{encounter.facility}</span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Main Summary - Full Focus */}
                <div style={{ 
                  width: '100%', 
                  padding: '20px',
                  borderRadius: '8px',
                  border: '2px solid #3498db',
                  backgroundColor: '#ffffff',
                  maxHeight: '600px',
                  overflowY: 'auto'
                }}>
                  {renderStructuredSummary(encounter.summary)}
                </div>

                {/* Action Button */}
                <div style={{ marginTop: '20px', textAlign: 'center' }}>
                  <button 
                    className="btn-approve-record"
                    style={{
                      backgroundColor: '#28a745',
                      color: 'white',
                      border: 'none',
                      padding: '12px 30px',
                      borderRadius: '6px',
                      fontSize: '14px',
                      fontWeight: 'bold',
                      cursor: 'pointer',
                      transition: 'background-color 0.2s'
                    }}
                    onMouseOver={(e) => e.target.style.backgroundColor = '#218838'}
                    onMouseOut={(e) => e.target.style.backgroundColor = '#28a745'}
                  >
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
