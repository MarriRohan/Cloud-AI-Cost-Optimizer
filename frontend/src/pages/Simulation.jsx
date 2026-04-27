import { useEffect, useState } from 'react'
import { getSimulate } from '../services/api'

export default function Simulation() {
  const [sim, setSim] = useState({
    before_cost: 0,
    after_cost: 0,
    savings_percent: 0,
    utilization_improvement_percent: 0,
    monthly_projected_savings: 0,
  })

  useEffect(() => {
    getSimulate().then((res) => setSim(res.data))
  }, [])

  return (
    <section className="grid">
      <article className="card metric"><h3>Before Cost</h3><p>${sim.before_cost}</p></article>
      <article className="card metric"><h3>After Cost</h3><p>${sim.after_cost}</p></article>
      <article className="card metric"><h3>Savings %</h3><p>{sim.savings_percent}%</p></article>
      <article className="card metric"><h3>Utilization Improvement</h3><p>{sim.utilization_improvement_percent}%</p></article>
      <article className="card metric full"><h3>Monthly Projected Savings</h3><p>${sim.monthly_projected_savings}</p></article>
    </section>
  )
}
