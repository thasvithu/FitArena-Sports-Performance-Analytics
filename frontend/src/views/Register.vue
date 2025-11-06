<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="10" md="6">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>
              <v-icon class="mr-2">mdi-account-plus</v-icon>
              Create FitArena Account
            </v-toolbar-title>
          </v-toolbar>
          
          <v-card-text>
            <v-form ref="form" v-model="valid" @submit.prevent="handleRegister">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="userData.username"
                    :rules="[rules.required, rules.minLength(3)]"
                    label="Username"
                    prepend-icon="mdi-account"
                    required
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="userData.email"
                    :rules="[rules.required, rules.email]"
                    label="Email"
                    prepend-icon="mdi-email"
                    type="email"
                    required
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="userData.password"
                    :rules="[rules.required, rules.minLength(8)]"
                    label="Password"
                    prepend-icon="mdi-lock"
                    :type="showPassword ? 'text' : 'password'"
                    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    @click:append="showPassword = !showPassword"
                    required
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="confirmPassword"
                    :rules="[rules.required, rules.passwordMatch]"
                    label="Confirm Password"
                    prepend-icon="mdi-lock-check"
                    :type="showPassword ? 'text' : 'password'"
                    required
                  />
                </v-col>

                <v-col cols="12">
                  <v-select
                    v-model="userData.role"
                    :items="roles"
                    :rules="[rules.required]"
                    label="Role"
                    prepend-icon="mdi-account-badge"
                    required
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="userData.full_name"
                    label="Full Name (Optional)"
                    prepend-icon="mdi-card-account-details"
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="userData.phone"
                    label="Phone (Optional)"
                    prepend-icon="mdi-phone"
                  />
                </v-col>
              </v-row>

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
              variant="text"
              to="/login"
            >
              Back to Login
            </v-btn>
            <v-btn
              color="primary"
              :loading="loading"
              :disabled="!valid"
              @click="handleRegister"
            >
              Register
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Register',

  data() {
    return {
      valid: false,
      loading: false,
      showPassword: false,
      errorMessage: '',
      confirmPassword: '',
      userData: {
        username: '',
        email: '',
        password: '',
        role: 'athlete',
        full_name: '',
        phone: ''
      },
      roles: [
        { title: 'Athlete', value: 'athlete' },
        { title: 'Coach', value: 'coach' }
      ],
      rules: {
        required: value => !!value || 'Required field',
        minLength: (len) => (value) => 
          (value && value.length >= len) || `Minimum ${len} characters required`,
        email: value => {
          const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
          return pattern.test(value) || 'Invalid email address'
        },
        passwordMatch: value => 
          value === this.userData.password || 'Passwords do not match'
      }
    }
  },

  methods: {
    ...mapActions({
      register: 'auth/register',
      showSuccess: 'notifications/showSuccess',
      showError: 'notifications/showError'
    }),

    async handleRegister() {
      if (!this.$refs.form.validate()) return

      this.loading = true
      this.errorMessage = ''

      try {
        // Remove empty optional fields
        const registrationData = { ...this.userData }
        if (!registrationData.full_name) delete registrationData.full_name
        if (!registrationData.phone) delete registrationData.phone

        await this.register(registrationData)
        this.showSuccess('Registration successful! Welcome to FitArena!')
        this.$router.push('/dashboard')
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || 'Registration failed. Please try again.'
        this.showError(this.errorMessage)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
