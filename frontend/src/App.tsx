

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            TeamPulse
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
            A comprehensive internal tool for small teams and companies to track employee check-ins, morale, and project status.
          </p>
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 max-w-2xl mx-auto">
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
              🚀 Coming Soon!
            </h2>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              Your TeamPulse application is being set up. This will be a powerful dashboard for:
            </p>
            <ul className="text-left text-gray-600 dark:text-gray-300 space-y-2 mb-6">
              <li>✅ Employee check-ins and mood tracking</li>
              <li>✅ Team management and analytics</li>
              <li>✅ Project status monitoring</li>
              <li>✅ Role-based access control</li>
              <li>✅ Real-time insights and reports</li>
            </ul>
            <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
              <p className="text-sm text-blue-800 dark:text-blue-200">
                <strong>Tech Stack:</strong> Flask (Python) + React (TypeScript) + PostgreSQL + Netlify
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App 