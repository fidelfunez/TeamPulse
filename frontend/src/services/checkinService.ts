const API_URL = import.meta.env.VITE_API_URL || 'https://teampulse-backend.onrender.com';

// Add CORS proxy for local development
const getApiUrl = (endpoint: string) => {
  const baseUrl = API_URL;
  // Use CORS proxy for local development
  if (window.location.hostname === 'localhost') {
    return `https://cors-anywhere.herokuapp.com/${baseUrl}${endpoint}`;
  }
  return `${baseUrl}${endpoint}`;
};

export interface CheckInData {
  mood_rating: number;
  work_load_rating?: number;
  stress_level?: number;
  comment?: string;
  project_id?: number;
}

export interface CheckInResponse {
  message: string;
  checkin: {
    id: number;
    user_id: number;
    user_name: string;
    project_id?: number;
    project_title?: string;
    check_in_date: string;
    mood_rating: number;
    comment?: string;
    work_load_rating?: number;
    stress_level?: number;
    created_at: string;
    updated_at: string;
  };
}

export interface DashboardStats {
  total_users: number;
  total_teams: number;
  total_projects: number;
  active_projects: number;
  total_checkins: number;
  recent_checkins: number;
}

class CheckInService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  async submitCheckIn(data: CheckInData): Promise<CheckInResponse> {
    try {
      const response = await fetch(getApiUrl('/api/checkins'), {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to submit check-in');
      }

      return await response.json();
    } catch (error) {
      console.error('Check-in submission error:', error);
      throw error;
    }
  }

  async getDashboardStats(): Promise<DashboardStats> {
    try {
      // Try the basic endpoint first
      console.log('Fetching dashboard stats from:', getApiUrl('/api/analytics/dashboard-basic'));
      const response = await fetch(getApiUrl('/api/analytics/dashboard-basic'), {
        method: 'GET',
        headers: this.getAuthHeaders(),
      });

      console.log('Response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Dashboard data received:', data);
        return {
          total_users: data.overview.total_users,
          total_teams: data.overview.total_teams,
          total_projects: data.overview.total_projects,
          active_projects: data.overview.active_projects,
          total_checkins: data.overview.total_checkins,
          recent_checkins: data.overview.recent_checkins,
        };
      }
      
      // If basic endpoint fails, try admin endpoint
      if (response.status === 401 || response.status === 403) {
        console.log('Basic endpoint requires admin, trying admin endpoint...');
        const adminResponse = await fetch(getApiUrl('/api/analytics/dashboard'), {
          method: 'GET',
          headers: this.getAuthHeaders(),
        });
        
        if (adminResponse.ok) {
          const data = await adminResponse.json();
          return {
            total_users: data.overview.total_users,
            total_teams: data.overview.total_teams,
            total_projects: data.overview.total_projects,
            active_projects: data.overview.active_projects,
            total_checkins: data.overview.total_checkins,
            recent_checkins: data.overview.recent_checkins,
          };
        }
      }
      
      // If both fail, provide fallback stats
      console.log('Both endpoints failed, providing fallback stats');
      return {
        total_users: 0,
        total_teams: 0,
        total_projects: 0,
        active_projects: 0,
        total_checkins: 0,
        recent_checkins: 0,
      };
      
    } catch (error) {
      console.error('Dashboard stats error:', error);
      // Return fallback stats on error
      return {
        total_users: 0,
        total_teams: 0,
        total_projects: 0,
        active_projects: 0,
        total_checkins: 0,
        recent_checkins: 0,
      };
    }
  }

  async getMyCheckIns(): Promise<any[]> {
    try {
      const response = await fetch(getApiUrl('/api/checkins/my-checkins'), {
        method: 'GET',
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to fetch check-ins');
      }

      const data = await response.json();
      return data.checkins;
    } catch (error) {
      console.error('Get check-ins error:', error);
      throw error;
    }
  }
}

export const checkinService = new CheckInService(); 