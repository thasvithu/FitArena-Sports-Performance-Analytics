import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'

// Initialize auth state
store.dispatch('auth/initAuth')
store.dispatch('initDarkMode')

const app = createApp(App)

app.use(router)
app.use(store)
app.use(vuetify)

app.mount('#app')
