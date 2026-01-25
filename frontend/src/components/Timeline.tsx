import { MedicalRecord } from '@/types'

interface TimelineProps {
  records: MedicalRecord[]
}

export default function Timeline({ records }: TimelineProps) {
  const sortedRecords = [...records].sort((a, b) => 
    new Date(b.record_date).getTime() - new Date(a.record_date).getTime()
  )

  return (
    <div className="timeline">
      {sortedRecords.map((record, index) => (
        <div key={record.id} className="timeline-item">
          <div className="timeline-marker">
            {index === 0 ? '●' : '○'}
          </div>
          <div className="timeline-content">
            <div className="timeline-header">
              <h3>{record.title}</h3>
              <span className="timeline-date">
                {new Date(record.record_date).toLocaleDateString()}
              </span>
            </div>
            <p className="timeline-type">{record.record_type}</p>
            {record.description && <p className="timeline-description">{record.description}</p>}
            <div className="timeline-meta">
              <span>Source: {record.source}</span>
              {record.verified && <span className="badge-verified">Verified</span>}
              {record.is_critical && <span className="badge-critical">Critical</span>}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
