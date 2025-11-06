export default {
  namespaced: true,
  
  state: {
    notifications: []
  },
  
  mutations: {
    ADD_NOTIFICATION(state, notification) {
      const id = Date.now()
      state.notifications.push({
        id,
        ...notification,
        timestamp: new Date()
      })
    },
    
    REMOVE_NOTIFICATION(state, id) {
      state.notifications = state.notifications.filter(n => n.id !== id)
    },
    
    CLEAR_NOTIFICATIONS(state) {
      state.notifications = []
    }
  },
  
  actions: {
    showSuccess({ commit }, message) {
      commit('ADD_NOTIFICATION', {
        type: 'success',
        message,
        timeout: 3000
      })
    },
    
    showError({ commit }, message) {
      commit('ADD_NOTIFICATION', {
        type: 'error',
        message,
        timeout: 5000
      })
    },
    
    showWarning({ commit }, message) {
      commit('ADD_NOTIFICATION', {
        type: 'warning',
        message,
        timeout: 4000
      })
    },
    
    showInfo({ commit }, message) {
      commit('ADD_NOTIFICATION', {
        type: 'info',
        message,
        timeout: 3000
      })
    },
    
    removeNotification({ commit }, id) {
      commit('REMOVE_NOTIFICATION', id)
    },
    
    clearAll({ commit }) {
      commit('CLEAR_NOTIFICATIONS')
    }
  },
  
  getters: {
    allNotifications: state => state.notifications
  }
}
