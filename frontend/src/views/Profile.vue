<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">
          <v-icon class="mr-2" size="large">mdi-account</v-icon>
          User Profile
        </h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="4">
        <v-card class="elevation-2">
          <v-card-text class="text-center">
            <v-avatar size="120" color="primary" class="mb-4">
              <v-icon size="80" color="white">mdi-account</v-icon>
            </v-avatar>
            <h2 class="text-h5 mb-2">{{ currentUser?.username }}</h2>
            <v-chip :color="getRoleColor(currentUser?.role)" class="mb-4">
              {{ currentUser?.role }}
            </v-chip>
            <p class="text-body-2 text-medium-emphasis">{{ currentUser?.email }}</p>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="8">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-account-edit</v-icon>
            Profile Information
          </v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="profileForm.username"
                    label="Username"
                    prepend-icon="mdi-account"
                    readonly
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="profileForm.email"
                    label="Email"
                    prepend-icon="mdi-email"
                    :rules="[rules.email]"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="profileForm.full_name"
                    label="Full Name"
                    prepend-icon="mdi-card-account-details"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="profileForm.phone"
                    label="Phone"
                    prepend-icon="mdi-phone"
                  />
                </v-col>
              </v-row>

              <v-divider class="my-4" />

              <v-btn
                color="primary"
                prepend-icon="mdi-content-save"
                @click="saveProfile"
                :loading="saving"
              >
                Save Changes
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>

        <v-card class="elevation-2 mt-4">
          <v-card-title>
            <v-icon class="mr-2">mdi-lock-reset</v-icon>
            Change Password
          </v-card-title>
          <v-card-text>
            <v-form ref="passwordForm" v-model="passwordValid">
              <v-text-field
                v-model="passwordForm.current"
                label="Current Password"
                prepend-icon="mdi-lock"
                :type="showPassword ? 'text' : 'password'"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
                :rules="[rules.required]"
              />
              <v-text-field
                v-model="passwordForm.new"
                label="New Password"
                prepend-icon="mdi-lock-plus"
                :type="showPassword ? 'text' : 'password'"
                :rules="[rules.required, rules.minLength(8)]"
              />
              <v-text-field
                v-model="passwordForm.confirm"
                label="Confirm New Password"
                prepend-icon="mdi-lock-check"
                :type="showPassword ? 'text' : 'password'"
                :rules="[rules.required, rules.passwordMatch]"
              />

              <v-btn
                color="warning"
                prepend-icon="mdi-key-change"
                @click="changePassword"
                :disabled="!passwordValid"
                :loading="changingPassword"
              >
                Change Password
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Profile',

  data() {
    return {
      valid: false,
      passwordValid: false,
      saving: false,
      changingPassword: false,
      showPassword: false,
      profileForm: {
        username: '',
        email: '',
        full_name: '',
        phone: ''
      },
      passwordForm: {
        current: '',
        new: '',
        confirm: ''
      },
      rules: {
        required: value => !!value || 'Required field',
        email: value => {
          const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
          return pattern.test(value) || 'Invalid email address'
        },
        minLength: (len) => (value) => 
          (value && value.length >= len) || `Minimum ${len} characters required`,
        passwordMatch: value => 
          value === this.passwordForm.new || 'Passwords do not match'
      }
    }
  },

  computed: {
    ...mapGetters({
      currentUser: 'auth/currentUser'
    })
  },

  mounted() {
    if (this.currentUser) {
      this.profileForm = {
        username: this.currentUser.username,
        email: this.currentUser.email,
        full_name: this.currentUser.full_name || '',
        phone: this.currentUser.phone || ''
      }
    }
  },

  methods: {
    ...mapActions({
      showSuccess: 'notifications/showSuccess',
      showError: 'notifications/showError'
    }),

    async saveProfile() {
      if (!this.$refs.form.validate()) return

      this.saving = true

      try {
        // await authService.updateUser(this.currentUser.id, this.profileForm)
        await new Promise(resolve => setTimeout(resolve, 1000))
        this.showSuccess('Profile updated successfully!')
      } catch (error) {
        this.showError('Failed to update profile')
      } finally {
        this.saving = false
      }
    },

    async changePassword() {
      if (!this.$refs.passwordForm.validate()) return

      this.changingPassword = true

      try {
        // await authService.changePassword(this.passwordForm)
        await new Promise(resolve => setTimeout(resolve, 1000))
        this.showSuccess('Password changed successfully!')
        this.passwordForm = { current: '', new: '', confirm: '' }
        this.$refs.passwordForm.reset()
      } catch (error) {
        this.showError('Failed to change password')
      } finally {
        this.changingPassword = false
      }
    },

    getRoleColor(role) {
      const colors = {
        athlete: 'primary',
        coach: 'success',
        admin: 'error'
      }
      return colors[role] || 'grey'
    }
  }
}
</script>
