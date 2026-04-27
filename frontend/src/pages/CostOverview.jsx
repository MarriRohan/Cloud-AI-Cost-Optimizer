import { useEffect, useState } from 'react'
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts'
import { getOverview } from '../services/api'

const colors = ['#6C63FF', '#00C49F', '#FF8042', '#FFBB28']

export default function CostOverview() {
  const [data, setData] = useState({ total_cost: 0, breakdown: {} })

  useEffect(() => {
    getOverview().then((res) => setData(res.data))
  }, [])

  const chartData = Object.entries(data.breakdown).map(([service, cost]) => ({ service, cost }))

  return (
    <section className="card">
      <h2>Total Monthly Cost: ${data.total_cost?.toFixed(2)}</h2>
      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie data={chartData} dataKey="cost" nameKey="service" outerRadius={120}>
              {chartData.map((_, index) => (
                <Cell key={index} fill={colors[index % colors.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}
