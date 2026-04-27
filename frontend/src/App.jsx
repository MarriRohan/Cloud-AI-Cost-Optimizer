import { Routes, Route } from 'react-router-dom'
import NavBar from './components/NavBar'
import CostOverview from './pages/CostOverview'
import Recommendations from './pages/Recommendations'
import Simulation from './pages/Simulation'
import Forecast from './pages/Forecast'

export default function App() {
  return (
    <div className="container">
      <NavBar />
      <main>
        <Routes>
          <Route path="/" element={<CostOverview />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/simulation" element={<Simulation />} />
          <Route path="/forecast" element={<Forecast />} />
        </Routes>
      </main>
    </div>
  )
}
