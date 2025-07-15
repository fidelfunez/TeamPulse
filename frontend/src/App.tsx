import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { ProtectedRoute } from './components/ProtectedRoute'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import CheckIn from './pages/CheckIn'
import AdminDashboard from './pages/AdminDashboard'
import Users from './pages/Users'
import Teams from './pages/Teams'
import Projects from './pages/Projects'
import Analytics from './pages/Analytics'
import Layout from './components/Layout'

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
          <Route index element={<Dashboard />} />
          <Route path="checkin" element={<CheckIn />} />
          <Route path="admin" element={<ProtectedRoute adminOnly><AdminDashboard /></ProtectedRoute>} />
          <Route path="users" element={<ProtectedRoute adminOnly><Users /></ProtectedRoute>} />
          <Route path="teams" element={<ProtectedRoute adminOnly><Teams /></ProtectedRoute>} />
          <Route path="projects" element={<ProtectedRoute adminOnly><Projects /></ProtectedRoute>} />
          <Route path="analytics" element={<ProtectedRoute adminOnly><Analytics /></ProtectedRoute>} />
        </Route>
      </Routes>
    </AuthProvider>
  )
}

export default App 