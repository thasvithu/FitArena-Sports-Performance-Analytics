import authService from '@/services/authService'

export default {
  namespaced: true,
  
  state: {
    user: null,
    token: localStorage.getItem('access_token') || null,
    isAuthenticated: false
  },
  
  mutations: {
    SET_USER(state, user) {
      state.user = user
      state.isAuthenticated = !!user
      if (user) {
        localStorage.setItem('user', JSON.stringify(user))
      } else {
        localStorage.removeItem('user')
      }
    },
    
    SET_TOKEN(state, token) {
      state.token = token
      if (token) {
        localStorage.setItem('access_token', token)
      } else {
        localStorage.removeItem('access_token')
      }
    },
    
    CLEAR_AUTH(state) {
      state.user = null
      state.token = null
      state.isAuthenticated = false
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
    }
  },
  
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await authService.login(credentials)
        commit('SET_TOKEN', response.access_token)
        
        // Fetch user data
        const user = await authService.getCurrentUser()
        commit('SET_USER', user)
        
        return { success: true, user }
      } catch (error) {
        commit('CLEAR_AUTH')
        throw error
      }
    },
    
    async register({ commit }, userData) {
      try {
        const user = await authService.register(userData)
        // After registration, automatically login
        const loginResponse = await authService.login({
          username: userData.username,
          password: userData.password
        })
        commit('SET_TOKEN', loginResponse.access_token)
        commit('SET_USER', user)
        
        return { success: true, user }
      } catch (error) {
        throw error
      }
    },
    
    async logout({ commit }) {
      await authService.logout()
      commit('CLEAR_AUTH')
    },
    
    async fetchCurrentUser({ commit, state }) {
      if (state.token) {
        try {
          const user = await authService.getCurrentUser()
          commit('SET_USER', user)
          return user
        } catch (error) {
          commit('CLEAR_AUTH')
          throw error
        }
      }
    },
    
    initAuth({ commit }) {
      const token = localStorage.getItem('access_token')
      const userStr = localStorage.getItem('user')
      
      if (token && userStr) {
        commit('SET_TOKEN', token)
        commit('SET_USER', JSON.parse(userStr))
      }
    }
  },
  
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    currentUser: state => state.user,
    userRole: state => state.user?.role,
    isCoach: state => state.user?.role === 'coach',
    isAthlete: state => state.user?.role === 'athlete',
    isAdmin: state => state.user?.role === 'admin'
  }
}
