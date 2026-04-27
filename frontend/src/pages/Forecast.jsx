import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { getForecast } from '../services/api'

export default function Forecast() {
  const [forecast, setForecast] = useState({ points: [], baseline_total_30d: 0, optimized_total_30d: 0 })

  useEffect(() => {
    getForecast().then((res) => setForecast(res.data))
  }, [])

  return (
    <section className="card">
      <h2>30-Day Cost Forecast</h2>
      <p>Without Optimization: ${forecast.baseline_total_30d}</p>
      <p>With Optimization: ${forecast.optimized_total_30d}</p>
      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={forecast.points}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="baseline_cost" stroke="#FF4D4F" strokeWidth={2} />
          <Line type="monotone" dataKey="optimized_cost" stroke="#52C41A" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </section>
  )
}
