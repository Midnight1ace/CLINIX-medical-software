import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { patientService } from '@/services/api'
import AISummaryCard from '@/components/AISummaryCard'
import LoadingState from '@/components/LoadingState'

export default function AISummary() {
  const { id } = useParams<{ id: string }>()
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!id) return

    const fetchSummary = async () => {
      try {
        const data = await patientService.getAISummary(id)
        setSummary(data.summary)
      } catch (err) {
        setError('Failed to load AI summary')
      } finally {
        setLoading(false)
      }
    }

    fetchSummary()
  }, [id])

  if (loading) return <LoadingState />
  if (error) return <div className="error-message">{error}</div>

  return (
    <div className="ai-summary-page">
      <h1>AI-Generated Summary</h1>
      <div className="disclaimer">
        <p>
          ⚠️ This is an AI-generated summary for clinical support only. Always verify against
          original documents.
        </p>
      </div>
      {summary && <AISummaryCard summary={summary} />}
    </div>
  )
}
