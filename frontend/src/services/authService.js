import apiClient from './api'

export default {
  // Authentication
  async login(credentials) {
    // Send as JSON (backend expects LoginRequest schema)
    const response = await apiClient.post('/auth/login', {
      username: credentials.username,
      password: credentials.password
    })
    return response.data
  },

  async register(userData) {
    const response = await apiClient.post('/auth/register', userData)
    return response.data
  },

  async getCurrentUser() {
    const response = await apiClient.get('/auth/me')
    return response.data
  },

  async logout() {
    // Clear local storage
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  },

  // Users
  async getUsers(params = {}) {
    const response = await apiClient.get('/users', { params })
    return response.data
  },

  async getUser(userId) {
    const response = await apiClient.get(`/users/${userId}`)
    return response.data
  },

  async updateUser(userId, userData) {
    const response = await apiClient.put(`/users/${userId}`, userData)
    return response.data
  },

  async deleteUser(userId) {
    const response = await apiClient.delete(`/users/${userId}`)
    return response.data
  },

  // Teams
  async getTeams(params = {}) {
    const response = await apiClient.get('/teams', { params })
    return response.data
  },

  async getTeam(teamId) {
    const response = await apiClient.get(`/teams/${teamId}`)
    return response.data
  },

  async createTeam(teamData) {
    const response = await apiClient.post('/teams', teamData)
    return response.data
  },

  async updateTeam(teamId, teamData) {
    const response = await apiClient.put(`/teams/${teamId}`, teamData)
    return response.data
  },

  async deleteTeam(teamId) {
    const response = await apiClient.delete(`/teams/${teamId}`)
    return response.data
  },

  // Analytics
  async getAnalyticsSummary(athleteId, params = {}) {
    const response = await apiClient.get('/analytics/summary', {
      params: { athlete_id: athleteId, ...params }
    })
    return response.data
  },

  async getTeamAnalytics(teamId, params = {}) {
    const response = await apiClient.get(`/analytics/team/${teamId}`, { params })
    return response.data
  },

  // Recommendations
  async getRecommendations(athleteId, params = {}) {
    const response = await apiClient.get(`/recommendations/${athleteId}`, { params })
    return response.data
  },

  async generateRecommendations(athleteId) {
    const response = await apiClient.post(`/recommendations/generate/${athleteId}`)
    return response.data
  },

  // Predictions
  async getPredictions(athleteId, metric, params = {}) {
    const response = await apiClient.get(`/predictions/${athleteId}/${metric}`, { params })
    return response.data
  },

  // Data Upload
  async uploadData(formData) {
    const response = await apiClient.post('/data/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  // Reports
  async generateReport(reportData) {
    const response = await apiClient.post('/reports/generate', reportData)
    return response.data
  },

  async getReports(params = {}) {
    const response = await apiClient.get('/reports', { params })
    return response.data
  },

  async downloadReport(reportId) {
    const response = await apiClient.get(`/reports/${reportId}/download`, {
      responseType: 'blob'
    })
    return response.data
  }
}
