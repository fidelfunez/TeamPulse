import React from 'react';
import { User } from '../../services/authService';

interface DashboardProps {
  user: User;
  onLogout: () => void;
}

const Dashboard: React.FC<DashboardProps> = ({ user, onLogout }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="bg-white/20 backdrop-blur-sm border-b border-white/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                TeamPulse
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700 dark:text-gray-300">
                Welcome, {user.name}
              </span>
              <span className="bg-white/20 backdrop-blur-sm text-white px-3 py-1 rounded-full text-sm font-medium border border-white/30">
                {user.role}
              </span>
              <button
                onClick={onLogout}
                className="bg-white/20 backdrop-blur-sm text-white font-bold py-2 px-4 rounded-lg border border-white/30 hover:bg-white/30 focus:ring-2 focus:ring-white/50 focus:outline-none transition-all duration-200"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Quick Check-in Card */}
          <div className="bg-white/20 backdrop-blur-sm rounded-2xl shadow-xl border border-white/30 p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Quick Check-in
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  How are you feeling today?
                </label>
                <select className="w-full px-4 py-3 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-gray-900 dark:text-white">
                  <option value="">Select mood...</option>
                  <option value="great">😊 Great</option>
                  <option value="good">🙂 Good</option>
                  <option value="okay">😐 Okay</option>
                  <option value="bad">😔 Bad</option>
                  <option value="terrible">😢 Terrible</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  What are you working on?
                </label>
                <textarea
                  className="w-full px-4 py-3 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
                  rows={3}
                  placeholder="Describe what you're working on..."
                />
              </div>
              <button className="w-full bg-white/20 backdrop-blur-sm text-white font-bold py-3 px-6 rounded-lg border border-white/30 hover:bg-white/30 focus:ring-2 focus:ring-white/50 focus:outline-none transition-all duration-200">
                Submit Check-in
              </button>
            </div>
          </div>

          {/* Team Overview Card */}
          <div className="bg-white/20 backdrop-blur-sm rounded-2xl shadow-xl border border-white/30 p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Team Overview
            </h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600 dark:text-gray-300">Team Members</span>
                <span className="text-2xl font-bold text-gray-900 dark:text-white">12</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600 dark:text-gray-300">Active Projects</span>
                <span className="text-2xl font-bold text-gray-900 dark:text-white">5</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600 dark:text-gray-300">Today's Check-ins</span>
                <span className="text-2xl font-bold text-gray-900 dark:text-white">8</span>
              </div>
            </div>
          </div>

          {/* Recent Activity Card */}
          <div className="bg-white/20 backdrop-blur-sm rounded-2xl shadow-xl border border-white/30 p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Recent Activity
            </h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                <span className="text-sm text-gray-600 dark:text-gray-300">
                  Sarah checked in - feeling great
                </span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                <span className="text-sm text-gray-600 dark:text-gray-300">
                  New project "Mobile App" created
                </span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-yellow-400 rounded-full"></div>
                <span className="text-sm text-gray-600 dark:text-gray-300">
                  Mike updated project status
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Admin Section (only for admins) */}
        {user.role === 'admin' && (
          <div className="mt-8">
            <div className="bg-white/20 backdrop-blur-sm rounded-2xl shadow-xl border border-white/30 p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Admin Panel
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button className="bg-white/20 backdrop-blur-sm text-white font-bold py-3 px-6 rounded-lg border border-white/30 hover:bg-white/30 focus:ring-2 focus:ring-white/50 focus:outline-none transition-all duration-200">
                  Manage Users
                </button>
                <button className="bg-white/20 backdrop-blur-sm text-white font-bold py-3 px-6 rounded-lg border border-white/30 hover:bg-white/30 focus:ring-2 focus:ring-white/50 focus:outline-none transition-all duration-200">
                  View Analytics
                </button>
                <button className="bg-white/20 backdrop-blur-sm text-white font-bold py-3 px-6 rounded-lg border border-white/30 hover:bg-white/30 focus:ring-2 focus:ring-white/50 focus:outline-none transition-all duration-200">
                  Team Settings
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard; 