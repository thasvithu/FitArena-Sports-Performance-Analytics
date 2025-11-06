<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>
              <v-icon class="mr-2">mdi-chart-line</v-icon>
              FitArena Login
            </v-toolbar-title>
          </v-toolbar>
          
          <v-card-text>
            <v-form ref="form" v-model="valid" @submit.prevent="handleLogin">
              <v-text-field
                v-model="credentials.username"
                :rules="[rules.required]"
                label="Username"
                prepend-icon="mdi-account"
                type="text"
                required
              />

              <v-text-field
                v-model="credentials.password"
                :rules="[rules.required]"
                label="Password"
                prepend-icon="mdi-lock"
                :type="showPassword ? 'text' : 'password'"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
                required
              />

              <v-alert
                v-if="errorMessage"
                type="error"
                variant="tonal"
                closable
                class="mt-2"
                @click:close="errorMessage = ''"
              >
                {{ errorMessage }}
              </v-alert>
            </v-form>
          </v-card-text>

          <v-card-actions>
            <v-spacer />
            <v-btn
              color="primary"
              :loading="loading"
              :disabled="!valid"
              @click="handleLogin"
            >
              Login
            </v-btn>
          </v-card-actions>

          <v-divider class="mx-4 mb-4" />

          <v-card-text class="text-center">
            <p class="mb-2">Don't have an account?</p>
            <v-btn
              variant="text"
              color="primary"
              to="/register"
            >
              Register Now
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Login',

  data() {
    return {
      valid: false,
      loading: false,
      showPassword: false,
      errorMessage: '',
      credentials: {
        username: '',
        password: ''
      },
      rules: {
        required: value => !!value || 'Required field'
      }
    }
  },

  methods: {
    ...mapActions({
      login: 'auth/login',
      showSuccess: 'notifications/showSuccess',
      showError: 'notifications/showError'
    }),

    async handleLogin() {
      if (!this.$refs.form.validate()) return

      this.loading = true
      this.errorMessage = ''

      try {
        await this.login(this.credentials)
        this.showSuccess('Login successful!')
        
        // Redirect to intended page or dashboard
        const redirect = this.$route.query.redirect || '/dashboard'
        this.$router.push(redirect)
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || 'Invalid username or password'
        this.showError(this.errorMessage)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
