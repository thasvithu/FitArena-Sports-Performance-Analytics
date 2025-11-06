<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">
          <v-icon class="mr-2" size="large">mdi-account-group</v-icon>
          Team Management
        </h1>
      </v-col>
      <v-col cols="auto">
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="showCreateDialog = true"
        >
          Create Team
        </v-btn>
      </v-col>
    </v-row>

    <!-- Teams Grid -->
    <v-row>
      <v-col
        v-for="team in teams"
        :key="team.id"
        cols="12"
        md="6"
        lg="4"
      >
        <v-card class="elevation-2" hover @click="viewTeam(team.id)">
          <v-card-title class="d-flex align-center">
            <v-avatar color="primary" class="mr-3">
              <v-icon color="white">mdi-account-group</v-icon>
            </v-avatar>
            <span>{{ team.name }}</span>
          </v-card-title>

          <v-card-subtitle>
            <v-chip size="small" class="mr-2">
              <v-icon start size="small">mdi-account</v-icon>
              {{ team.members }} Members
            </v-chip>
            <v-chip size="small" color="success">
              {{ team.sport }}
            </v-chip>
          </v-card-subtitle>

          <v-card-text>
            <p class="text-body-2 mb-2">{{ team.description }}</p>
            
            <v-divider class="my-3" />

            <div class="d-flex justify-space-between">
              <div>
                <p class="text-caption text-medium-emphasis">Avg Performance</p>
                <p class="text-h6 font-weight-bold">{{ team.avgPerformance }}%</p>
              </div>
              <div>
                <p class="text-caption text-medium-emphasis">Active Athletes</p>
                <p class="text-h6 font-weight-bold">{{ team.activeAthletes }}</p>
              </div>
            </div>
          </v-card-text>

          <v-card-actions>
            <v-btn
              variant="text"
              color="primary"
              prepend-icon="mdi-eye"
              @click.stop="viewTeam(team.id)"
            >
              View
            </v-btn>
            <v-btn
              variant="text"
              color="warning"
              prepend-icon="mdi-pencil"
              @click.stop="editTeam(team)"
            >
              Edit
            </v-btn>
            <v-btn
              variant="text"
              color="error"
              prepend-icon="mdi-delete"
              @click.stop="deleteTeam(team.id)"
            >
              Delete
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Create/Edit Team Dialog -->
    <v-dialog v-model="showCreateDialog" max-width="600">
      <v-card>
        <v-card-title>
          <v-icon class="mr-2">mdi-account-group</v-icon>
          {{ editingTeam ? 'Edit Team' : 'Create New Team' }}
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="teamForm.name"
              label="Team Name"
              :rules="[rules.required]"
              prepend-icon="mdi-text"
              required
            />

            <v-textarea
              v-model="teamForm.description"
              label="Description"
              prepend-icon="mdi-text-box"
              rows="3"
            />

            <v-select
              v-model="teamForm.sport"
              :items="sports"
              label="Sport"
              prepend-icon="mdi-soccer"
              :rules="[rules.required]"
              required
            />

            <v-select
              v-model="teamForm.coach_id"
              :items="coaches"
              item-title="name"
              item-value="id"
              label="Coach"
              prepend-icon="mdi-whistle"
            />
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="closeDialog">Cancel</v-btn>
          <v-btn
            color="primary"
            :disabled="!valid"
            @click="saveTeam"
          >
            {{ editingTeam ? 'Update' : 'Create' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Teams',

  data() {
    return {
      showCreateDialog: false,
      editingTeam: null,
      valid: false,
      teamForm: {
        name: '',
        description: '',
        sport: '',
        coach_id: null
      },
      teams: [
        {
          id: 1,
          name: 'Elite Runners',
          description: 'Professional marathon training team',
          sport: 'Running',
          members: 12,
          avgPerformance: 87,
          activeAthletes: 10
        },
        {
          id: 2,
          name: 'Power Lifters',
          description: 'Strength and conditioning focus',
          sport: 'Weightlifting',
          members: 8,
          avgPerformance: 92,
          activeAthletes: 7
        },
        {
          id: 3,
          name: 'Cardio Warriors',
          description: 'High-intensity cardio training',
          sport: 'CrossFit',
          members: 15,
          avgPerformance: 84,
          activeAthletes: 13
        }
      ],
      sports: [
        'Running',
        'Cycling',
        'Swimming',
        'Weightlifting',
        'CrossFit',
        'Basketball',
        'Soccer',
        'Tennis',
        'Other'
      ],
      coaches: [
        { id: 1, name: 'Coach Smith' },
        { id: 2, name: 'Coach Johnson' },
        { id: 3, name: 'Coach Williams' }
      ],
      rules: {
        required: value => !!value || 'Required field'
      }
    }
  },

  methods: {
    ...mapActions({
      showSuccess: 'notifications/showSuccess',
      showError: 'notifications/showError'
    }),

    viewTeam(teamId) {
      this.$router.push(`/teams/${teamId}`)
    },

    editTeam(team) {
      this.editingTeam = team
      this.teamForm = { ...team }
      this.showCreateDialog = true
    },

    async deleteTeam(teamId) {
      if (confirm('Are you sure you want to delete this team?')) {
        try {
          // await authService.deleteTeam(teamId)
          this.teams = this.teams.filter(t => t.id !== teamId)
          this.showSuccess('Team deleted successfully!')
        } catch (error) {
          this.showError('Failed to delete team')
        }
      }
    },

    async saveTeam() {
      if (!this.$refs.form.validate()) return

      try {
        if (this.editingTeam) {
          // await authService.updateTeam(this.editingTeam.id, this.teamForm)
          this.showSuccess('Team updated successfully!')
        } else {
          // await authService.createTeam(this.teamForm)
          this.showSuccess('Team created successfully!')
        }
        this.closeDialog()
      } catch (error) {
        this.showError('Failed to save team')
      }
    },

    closeDialog() {
      this.showCreateDialog = false
      this.editingTeam = null
      this.teamForm = {
        name: '',
        description: '',
        sport: '',
        coach_id: null
      }
      this.$refs.form?.reset()
    }
  }
}
</script>
