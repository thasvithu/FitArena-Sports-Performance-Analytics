import authService from '@/services/authService'

export default {
  namespaced: true,
  
  state: {
    summary: null,
    trends: [],
    teamAnalytics: null,
    loading: false,
    error: null
  },
  
  mutations: {
    SET_SUMMARY(state, summary) {
      state.summary = summary
    },
    
    SET_TRENDS(state, trends) {
      state.trends = trends
    },
    
    SET_TEAM_ANALYTICS(state, analytics) {
      state.teamAnalytics = analytics
    },
    
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  
  actions: {
    async fetchSummary({ commit }, { athleteId, params }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      
      try {
        const summary = await authService.getAnalyticsSummary(athleteId, params)
        commit('SET_SUMMARY', summary)
        return summary
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchTeamAnalytics({ commit }, { teamId, params }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      
      try {
        const analytics = await authService.getTeamAnalytics(teamId, params)
        commit('SET_TEAM_ANALYTICS', analytics)
        return analytics
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    }
  },
  
  getters: {
    summary: state => state.summary,
    trends: state => state.trends,
    teamAnalytics: state => state.teamAnalytics,
    isLoading: state => state.loading,
    error: state => state.error
  }
}
