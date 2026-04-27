import { useEffect, useState } from 'react'
import { getAnalyze, getRecommend } from '../services/api'

export default function Recommendations() {
  const [analysis, setAnalysis] = useState({ issues: [], estimated_savings: [] })
  const [recommend, setRecommend] = useState({ actions: [] })

  useEffect(() => {
    getAnalyze().then((res) => setAnalysis(res.data))
    getRecommend().then((res) => setRecommend(res.data))
  }, [])

  return (
    <section className="grid">
      <article className="card">
        <h2>Issues Detected</h2>
        <ul>{analysis.issues.map((i, idx) => <li key={idx}>{i}</li>)}</ul>
      </article>
      <article className="card">
        <h2>Suggested Actions</h2>
        <ul>{recommend.actions.map((a, idx) => <li key={idx}>{a.detail}</li>)}</ul>
      </article>
      <article className="card">
        <h2>Estimated Savings</h2>
        <ul>{analysis.estimated_savings.map((s, idx) => <li key={idx}>{s.resource_id}: ${s.amount}</li>)}</ul>
      </article>
    </section>
  )
}
