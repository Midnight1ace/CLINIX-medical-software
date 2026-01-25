/**
 * Demo Page - Judge Demonstration Flow
 * 
 * This page guides judges through the system showing:
 * 1. Patient search
 * 2. Snapshot view with alerts
 * 3. Emergency mode
 * 4. AI summary
 * 5. Full history
 */

export default function Demo() {
  return (
    <div className="demo-page">
      <h1>AI Patient Record Intelligence - Demo Flow</h1>
      <p>This system is designed for doctor-first, safety-critical patient records.</p>
      
      <section>
        <h2>Key Features:</h2>
        <ul>
          <li>⚡ Fast patient search (6 methods)</li>
          <li>🚨 Critical alerts always visible</li>
          <li>🏥 Emergency mode for crisis situations</li>
          <li>🤖 AI summaries with source links</li>
          <li>🔒 HIPAA/GDPR compliant</li>
        </ul>
      </section>
    </div>
  )
}
