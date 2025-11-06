import { createStore } from 'vuex'
import auth from './modules/auth'
import analytics from './modules/analytics'
import teams from './modules/teams'
import notifications from './modules/notifications'

export default createStore({
  modules: {
    auth,
    analytics,
    teams,
    notifications
  },
  
  state: {
    loading: false,
    darkMode: false
  },
  
  mutations: {
    SET_LOADING(state, value) {
      state.loading = value
    },
    SET_DARK_MODE(state, value) {
      state.darkMode = value
      localStorage.setItem('darkMode', value)
    }
  },
  
  actions: {
    setLoading({ commit }, value) {
      commit('SET_LOADING', value)
    },
    toggleDarkMode({ commit, state }) {
      commit('SET_DARK_MODE', !state.darkMode)
    },
    initDarkMode({ commit }) {
      const darkMode = localStorage.getItem('darkMode') === 'true'
      commit('SET_DARK_MODE', darkMode)
    }
  },
  
  getters: {
    isLoading: state => state.loading,
    isDarkMode: state => state.darkMode
  }
})
