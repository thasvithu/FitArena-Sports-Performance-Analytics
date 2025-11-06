<template>
  <v-app :theme="isDarkMode ? 'darkTheme' : 'customTheme'">
    <v-navigation-drawer
      v-if="isAuthenticated"
      v-model="drawer"
      app
      :permanent="$vuetify.display.mdAndUp"
      :temporary="$vuetify.display.smAndDown"
    >
      <v-list>
        <v-list-item
          prepend-avatar="https://via.placeholder.com/40"
          :title="currentUser?.username || 'User'"
          :subtitle="currentUser?.email || ''"
        />
      </v-list>

      <v-divider />

      <v-list density="compact" nav>
        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          :to="item.to"
          :prepend-icon="item.icon"
          :title="item.title"
          :value="item.title"
        />
      </v-list>
    </v-navigation-drawer>

    <v-app-bar v-if="isAuthenticated" app color="primary" dark>
      <v-app-bar-nav-icon
        v-if="$vuetify.display.smAndDown"
        @click="drawer = !drawer"
      />
      
      <v-toolbar-title>
        <v-icon class="mr-2">mdi-chart-line</v-icon>
        FitArena
      </v-toolbar-title>

      <v-spacer />

      <v-btn icon @click="toggleDarkMode">
        <v-icon>{{ isDarkMode ? 'mdi-brightness-7' : 'mdi-brightness-4' }}</v-icon>
      </v-btn>

      <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props">
            <v-icon>mdi-account-circle</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item to="/profile">
            <v-list-item-title>
              <v-icon class="mr-2">mdi-account</v-icon>
              Profile
            </v-list-item-title>
          </v-list-item>
          <v-list-item @click="handleLogout">
            <v-list-item-title>
              <v-icon class="mr-2">mdi-logout</v-icon>
              Logout
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

    <!-- Notifications -->
    <v-snackbar
      v-for="notification in notifications"
      :key="notification.id"
      v-model="notification.visible"
      :color="notification.type"
      :timeout="notification.timeout"
      location="top right"
      multi-line
    >
      {{ notification.message }}
      <template v-slot:actions>
        <v-btn
          variant="text"
          @click="removeNotification(notification.id)"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>

    <!-- Loading overlay -->
    <v-overlay
      v-model="isLoading"
      class="align-center justify-center"
      persistent
    >
      <v-progress-circular
        indeterminate
        size="64"
        color="primary"
      />
    </v-overlay>
  </v-app>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'App',

  data() {
    return {
      drawer: true
    }
  },

  computed: {
    ...mapGetters({
      isAuthenticated: 'auth/isAuthenticated',
      currentUser: 'auth/currentUser',
      userRole: 'auth/userRole',
      isLoading: 'isLoading',
      isDarkMode: 'isDarkMode',
      notifications: 'notifications/allNotifications'
    }),

    menuItems() {
      const items = [
        { title: 'Dashboard', icon: 'mdi-view-dashboard', to: '/dashboard' },
        { title: 'Analytics', icon: 'mdi-chart-box', to: '/analytics' },
        { title: 'Recommendations', icon: 'mdi-lightbulb', to: '/recommendations' },
        { title: 'Predictions', icon: 'mdi-crystal-ball', to: '/predictions' },
        { title: 'Reports', icon: 'mdi-file-document', to: '/reports' }
      ]

      // Add coach/admin only items
      if (this.userRole === 'coach' || this.userRole === 'admin') {
        items.splice(2, 0, { 
          title: 'Teams', 
          icon: 'mdi-account-group', 
          to: '/teams' 
        })
        items.push({ 
          title: 'Data Upload', 
          icon: 'mdi-upload', 
          to: '/data-upload' 
        })
      }

      return items
    }
  },

  methods: {
    ...mapActions({
      logout: 'auth/logout',
      toggleDarkMode: 'toggleDarkMode',
      removeNotification: 'notifications/removeNotification'
    }),

    async handleLogout() {
      try {
        await this.logout()
        this.$router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
  }
}
</script>

<style>
#app {
  font-family: 'Roboto', sans-serif;
}
</style>
