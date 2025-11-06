import authService from '@/services/authService'

export default {
  namespaced: true,
  
  state: {
    teams: [],
    currentTeam: null,
    loading: false,
    error: null
  },
  
  mutations: {
    SET_TEAMS(state, teams) {
      state.teams = teams
    },
    
    SET_CURRENT_TEAM(state, team) {
      state.currentTeam = team
    },
    
    ADD_TEAM(state, team) {
      state.teams.push(team)
    },
    
    UPDATE_TEAM(state, updatedTeam) {
      const index = state.teams.findIndex(t => t.id === updatedTeam.id)
      if (index !== -1) {
        state.teams.splice(index, 1, updatedTeam)
      }
    },
    
    REMOVE_TEAM(state, teamId) {
      state.teams = state.teams.filter(t => t.id !== teamId)
    },
    
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  
  actions: {
    async fetchTeams({ commit }, params = {}) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      
      try {
        const teams = await authService.getTeams(params)
        commit('SET_TEAMS', teams)
        return teams
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchTeam({ commit }, teamId) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      
      try {
        const team = await authService.getTeam(teamId)
        commit('SET_CURRENT_TEAM', team)
        return team
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async createTeam({ commit }, teamData) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      
      try {
        const team = await authService.createTeam(teamData)
        commit('ADD_TEAM', team)
        return team
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async updateTeam({ commit }, { teamId, teamData }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      
      try {
        const team = await authService.updateTeam(teamId, teamData)
        commit('UPDATE_TEAM', team)
        return team
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async deleteTeam({ commit }, teamId) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      
      try {
        await authService.deleteTeam(teamId)
        commit('REMOVE_TEAM', teamId)
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    }
  },
  
  getters: {
    allTeams: state => state.teams,
    currentTeam: state => state.currentTeam,
    isLoading: state => state.loading,
    error: state => state.error
  }
}
