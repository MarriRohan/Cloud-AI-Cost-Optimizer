import { NavLink } from 'react-router-dom'

const tabs = [
  ['/', 'Cost Overview'],
  ['/recommendations', 'AI Recommendations'],
  ['/simulation', 'Optimization Simulation'],
  ['/forecast', 'Forecast'],
]

export default function NavBar() {
  return (
    <header className="top-nav">
      <h1>Cloud AI Cost Optimizer</h1>
      <nav>
        {tabs.map(([to, label]) => (
          <NavLink key={to} to={to} className={({ isActive }) => (isActive ? 'active' : '')}>
            {label}
          </NavLink>
        ))}
      </nav>
    </header>
  )
}
