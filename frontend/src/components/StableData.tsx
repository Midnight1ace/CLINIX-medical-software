interface StableDataProps {
  bloodType?: string
  allergies?: string
  conditions?: string
}

export default function StableData({ bloodType, allergies, conditions }: StableDataProps) {
  return (
    <div className="stable-data">
      <h2>Stable Medical Data</h2>
      <div className="data-grid">
        <div className="data-item">
          <label>Blood Type</label>
          <p>{bloodType || 'Not documented'}</p>
        </div>
        
        <div className="data-item">
          <label>Allergies</label>
          <p>{allergies || 'None documented'}</p>
        </div>
        
        <div className="data-item">
          <label>Chronic Conditions</label>
          <p>{conditions || 'None documented'}</p>
        </div>
      </div>
    </div>
  )
}
