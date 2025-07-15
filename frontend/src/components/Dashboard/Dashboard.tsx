import React, { useState, useEffect } from 'react';
import { User } from '../../services/authService';
import { checkinService, CheckInData, DashboardStats } from '../../services/checkinService';

interface DashboardProps {
  user: User;
  onLogout: () => void;
}

const Dashboard: React.FC<DashboardProps> = ({ user, onLogout }) => {
  // Check-in form state
  const [moodRating, setMoodRating] = useState<number>(0);
  const [workloadRating, setWorkloadRating] = useState<number>(0);
  const [stressLevel, setStressLevel] = useState<number>(0);
  const [comment, setComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [checkInError, setCheckInError] = useState('');
  const [checkInSuccess, setCheckInSuccess] = useState('');

  // Dashboard stats state
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loadingStats, setLoadingStats] = useState(true);
  const [statsError, setStatsError] = useState('');

  // Load dashboard stats on component mount
  useEffect(() => {
    loadDashboardStats();
  }, []);

  const loadDashboardStats = async () => {
    try {
      setLoadingStats(true);
      setStatsError('');
      const dashboardStats = await checkinService.getDashboardStats();
      setStats(dashboardStats);
    } catch (error) {
      console.error('Failed to load dashboard stats:', error);
      setStatsError('Failed to load dashboard statistics');
    } finally {
      setLoadingStats(false);
    }
  };

  const handleCheckInSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!moodRating) {
      setCheckInError('Please select a mood rating');
      return;
    }

    try {
      setIsSubmitting(true);
      setCheckInError('');
      setCheckInSuccess('');

      const checkInData: CheckInData = {
        mood_rating: moodRating,
        work_load_rating: workloadRating || undefined,
        stress_level: stressLevel || undefined,
        comment: comment.trim() || undefined,
      };

      await checkinService.submitCheckIn(checkInData);
      
      // Reset form
      setMoodRating(0);
      setWorkloadRating(0);
      setStressLevel(0);
      setComment('');
      
      setCheckInSuccess('Check-in submitted successfully!');
      
      // Reload dashboard stats to update the numbers
      await loadDashboardStats();
      
    } catch (error) {
      console.error('Check-in submission failed:', error);
      setCheckInError(error instanceof Error ? error.message : 'Failed to submit check-in');
    } finally {
      setIsSubmitting(false);
    }
  };

  const getMoodText = (rating: number): string => {
    switch (rating) {
      case 1: return '😢 Terrible';
      case 2: return '😔 Bad';
      case 3: return '😐 Okay';
      case 4: return '🙂 Good';
      case 5: return '😊 Great';
      default: return 'Select mood...';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-b border-white/30 dark:border-gray-700/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                TeamPulse
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-800 dark:text-gray-200">
                Welcome, {user.name}
              </span>
              <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                {user.role}
              </span>
              <button
                onClick={onLogout}
                className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg border border-red-600 hover:border-red-700 focus:ring-2 focus:ring-red-500 focus:outline-none transition-all duration-200"
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
          <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/30 dark:border-gray-700/30 p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Quick Check-in
            </h3>
            
            {checkInSuccess && (
              <div className="mb-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
                <p className="text-green-600 dark:text-green-400 text-sm">{checkInSuccess}</p>
              </div>
            )}
            
            {checkInError && (
              <div className="mb-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                <p className="text-red-600 dark:text-red-400 text-sm">{checkInError}</p>
              </div>
            )}

            <form onSubmit={handleCheckInSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-800 dark:text-gray-200 mb-2">
                  How are you feeling today?
                </label>
                <select 
                  value={moodRating}
                  onChange={(e) => setMoodRating(Number(e.target.value))}
                  className="w-full px-4 py-3 bg-white/90 dark:bg-gray-700/90 backdrop-blur-sm border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-gray-900 dark:text-white"
                  required
                >
                  <option value={0}>Select mood...</option>
                  <option value={5}>😊 Great</option>
                  <option value={4}>🙂 Good</option>
                  <option value={3}>😐 Okay</option>
                  <option value={2}>😔 Bad</option>
                  <option value={1}>😢 Terrible</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-800 dark:text-gray-200 mb-2">
                  Workload (optional)
                </label>
                <select 
                  value={workloadRating}
                  onChange={(e) => setWorkloadRating(Number(e.target.value))}
                  className="w-full px-4 py-3 bg-white/90 dark:bg-gray-700/90 backdrop-blur-sm border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-gray-900 dark:text-white"
                >
                  <option value={0}>Select workload...</option>
                  <option value={1}>Very Light</option>
                  <option value={2}>Light</option>
                  <option value={3}>Moderate</option>
                  <option value={4}>Heavy</option>
                  <option value={5}>Very Heavy</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-800 dark:text-gray-200 mb-2">
                  Stress Level (optional)
                </label>
                <select 
                  value={stressLevel}
                  onChange={(e) => setStressLevel(Number(e.target.value))}
                  className="w-full px-4 py-3 bg-white/90 dark:bg-gray-700/90 backdrop-blur-sm border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-gray-900 dark:text-white"
                >
                  <option value={0}>Select stress level...</option>
                  <option value={1}>Very Low</option>
                  <option value={2}>Low</option>
                  <option value={3}>Moderate</option>
                  <option value={4}>High</option>
                  <option value={5}>Very High</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-800 dark:text-gray-200 mb-2">
                  What are you working on? (optional)
                </label>
                <textarea
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  className="w-full px-4 py-3 bg-white/90 dark:bg-gray-700/90 backdrop-blur-sm border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-gray-900 dark:text-white placeholder-gray-600 dark:placeholder-gray-300"
                  rows={3}
                  placeholder="Describe what you're working on..."
                />
              </div>
              
              <button 
                type="submit"
                disabled={isSubmitting}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg border border-blue-600 hover:border-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? 'Submitting...' : 'Submit Check-in'}
              </button>
            </form>
          </div>

          {/* Team Overview Card */}
          <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/30 dark:border-gray-700/30 p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Team Overview
            </h3>
            
            {loadingStats ? (
              <div className="space-y-4">
                <div className="animate-pulse">
                  <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded"></div>
                </div>
                <div className="animate-pulse">
                  <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded"></div>
                </div>
                <div className="animate-pulse">
                  <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded"></div>
                </div>
              </div>
            ) : statsError ? (
              <div className="text-red-600 dark:text-red-400 text-sm">{statsError}</div>
            ) : stats ? (
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-700 dark:text-gray-200">Team Members</span>
                  <span className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total_users}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-700 dark:text-gray-200">Active Projects</span>
                  <span className="text-2xl font-bold text-gray-900 dark:text-white">{stats.active_projects}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-700 dark:text-gray-200">Today's Check-ins</span>
                  <span className="text-2xl font-bold text-gray-900 dark:text-white">{stats.recent_checkins}</span>
                </div>
                {stats.total_users === 0 && stats.active_projects === 0 && stats.recent_checkins === 0 && (
                  <div className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                    Stats will appear as data is added to the system
                  </div>
                )}
              </div>
            ) : (
              <div className="text-gray-500 dark:text-gray-400 text-sm">No data available</div>
            )}
          </div>

          {/* Recent Activity Card */}
          <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/30 dark:border-gray-700/30 p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Recent Activity
            </h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                <span className="text-sm text-gray-700 dark:text-gray-200">
                  Sarah checked in - feeling great
                </span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                <span className="text-sm text-gray-700 dark:text-gray-200">
                  New project "Mobile App" created
                </span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-yellow-400 rounded-full"></div>
                <span className="text-sm text-gray-700 dark:text-gray-200">
                  Mike updated project status
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Admin Section (only for admins) */}
        {user.role === 'admin' && (
          <div className="mt-8">
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/30 dark:border-gray-700/30 p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Admin Panel
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg border border-blue-600 hover:border-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all duration-200">
                  Manage Users
                </button>
                <button className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg border border-green-600 hover:border-green-700 focus:ring-2 focus:ring-green-500 focus:outline-none transition-all duration-200">
                  View Analytics
                </button>
                <button className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-lg border border-purple-600 hover:border-purple-700 focus:ring-2 focus:ring-purple-500 focus:outline-none transition-all duration-200">
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