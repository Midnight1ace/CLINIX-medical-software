import { MedicalRecord } from '@/types'

interface DynamicDataProps {
  records: MedicalRecord[]
}

export default function DynamicData({ records }: DynamicDataProps) {
  return (
    <div className="dynamic-data">
      <h2>Recent Clinical Data</h2>
      <div className="records-list">
        {records && records.length > 0 ? (
          records.map((record) => (
            <div key={record.id} className="record-item">
              <div className="record-header">
                <h3>{record.title}</h3>
                <span className="record-date">{new Date(record.record_date).toLocaleDateString()}</span>
              </div>
              <p className="record-type">{record.record_type}</p>
              {record.description && <p>{record.description}</p>}
              <span className="record-source">Source: {record.source}</span>
            </div>
          ))
        ) : (
          <p>No recent records</p>
        )}
      </div>
    </div>
  )
}
