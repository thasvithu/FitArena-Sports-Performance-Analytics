<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <v-btn variant="text" prepend-icon="mdi-arrow-left" @click="$router.back()">
          Back to Teams
        </v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card class="elevation-2">
          <v-card-title class="text-h4">
            <v-icon class="mr-2" size="large">mdi-account-group</v-icon>
            {{ team.name }}
          </v-card-title>
          <v-card-subtitle>
            {{ team.sport }} • {{ team.members }} Members
          </v-card-subtitle>
          <v-card-text>
            <p>{{ team.description }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Team Statistics -->
    <v-row class="mt-4">
      <v-col v-for="stat in teamStats" :key="stat.title" cols="12" sm="6" md="3">
        <v-card class="elevation-2">
          <v-card-text>
            <div class="text-center">
              <v-icon :color="stat.color" size="48">{{ stat.icon }}</v-icon>
              <h2 class="text-h4 mt-2">{{ stat.value }}</h2>
              <p class="text-subtitle-2 text-medium-emphasis">{{ stat.title }}</p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Team Members -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-account-multiple</v-icon>
            Team Members
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="memberHeaders"
              :items="members"
              class="elevation-0"
            >
              <template v-slot:item.status="{ item }">
                <v-chip :color="item.status === 'Active' ? 'success' : 'warning'" size="small">
                  {{ item.status }}
                </v-chip>
              </template>
              <template v-slot:item.performance="{ item }">
                <v-progress-linear
                  :model-value="item.performance"
                  :color="getPerformanceColor(item.performance)"
                  height="20"
                >
                  <strong>{{ item.performance }}%</strong>
                </v-progress-linear>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: 'TeamDetail',

  data() {
    return {
      team: {
        id: 1,
        name: 'Elite Runners',
        description: 'Professional marathon training team',
        sport: 'Running',
        members: 12
      },
      teamStats: [
        { title: 'Avg Performance', value: '87%', icon: 'mdi-chart-line', color: 'primary' },
        { title: 'Active Members', value: '10', icon: 'mdi-account-check', color: 'success' },
        { title: 'Total Workouts', value: '342', icon: 'mdi-dumbbell', color: 'warning' },
        { title: 'Team Rank', value: '#3', icon: 'mdi-trophy', color: 'error' }
      ],
      memberHeaders: [
        { title: 'Name', key: 'name' },
        { title: 'Role', key: 'role' },
        { title: 'Status', key: 'status' },
        { title: 'Performance', key: 'performance' },
        { title: 'Last Active', key: 'lastActive' }
      ],
      members: [
        { name: 'John Doe', role: 'Athlete', status: 'Active', performance: 92, lastActive: '2 hours ago' },
        { name: 'Jane Smith', role: 'Athlete', status: 'Active', performance: 88, lastActive: '1 day ago' },
        { name: 'Mike Johnson', role: 'Athlete', status: 'Inactive', performance: 75, lastActive: '5 days ago' }
      ]
    }
  },

  methods: {
    getPerformanceColor(performance) {
      if (performance >= 90) return 'success'
      if (performance >= 75) return 'primary'
      if (performance >= 60) return 'warning'
      return 'error'
    }
  }
}
</script>
