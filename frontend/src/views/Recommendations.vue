<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">
          <v-icon class="mr-2" size="large">mdi-lightbulb</v-icon>
          AI Recommendations
        </h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Personalized insights to improve your performance
        </p>
      </v-col>
      <v-col cols="auto">
        <v-btn
          color="primary"
          prepend-icon="mdi-refresh"
          @click="generateRecommendations"
          :loading="loading"
        >
          Generate New
        </v-btn>
      </v-col>
    </v-row>

    <!-- Priority Filter -->
    <v-card class="mb-4 elevation-2">
      <v-card-text>
        <v-chip-group v-model="selectedPriority" mandatory>
          <v-chip value="all" color="primary">All</v-chip>
          <v-chip value="high" color="error">High Priority</v-chip>
          <v-chip value="medium" color="warning">Medium Priority</v-chip>
          <v-chip value="low" color="success">Low Priority</v-chip>
        </v-chip-group>
      </v-card-text>
    </v-card>

    <!-- Recommendations List -->
    <v-row>
      <v-col
        v-for="recommendation in filteredRecommendations"
        :key="recommendation.id"
        cols="12"
      >
        <v-card class="elevation-2" :class="`border-l-${getPriorityColor(recommendation.priority)}`">
          <v-card-title class="d-flex align-center">
            <v-icon :color="getCategoryColor(recommendation.category)" class="mr-3" size="large">
              {{ getCategoryIcon(recommendation.category) }}
            </v-icon>
            <span>{{ recommendation.title }}</span>
            <v-spacer />
            <v-chip :color="getPriorityColor(recommendation.priority)" size="small">
              {{ recommendation.priority }}
            </v-chip>
          </v-card-title>

          <v-card-text>
            <p class="text-body-1 mb-3">{{ recommendation.description }}</p>

            <v-divider class="my-3" />

            <div class="mb-3">
              <h4 class="text-subtitle-1 font-weight-bold mb-2">
                <v-icon size="small" class="mr-1">mdi-format-list-checks</v-icon>
                Action Items:
              </h4>
              <v-list density="compact" class="bg-transparent">
                <v-list-item
                  v-for="(action, index) in recommendation.actions"
                  :key="index"
                >
                  <template v-slot:prepend>
                    <v-icon size="small">mdi-checkbox-marked-circle</v-icon>
                  </template>
                  <v-list-item-title>{{ action }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </div>

            <v-alert
              type="info"
              variant="tonal"
              density="compact"
              icon="mdi-chart-line"
            >
              <strong>Expected Impact:</strong> {{ recommendation.expectedImpact }}
            </v-alert>

            <div class="mt-3">
              <v-row>
                <v-col cols="6">
                  <p class="text-caption text-medium-emphasis mb-1">Confidence Score</p>
                  <v-progress-linear
                    :model-value="recommendation.confidence"
                    color="primary"
                    height="20"
                  >
                    <strong>{{ recommendation.confidence }}%</strong>
                  </v-progress-linear>
                </v-col>
                <v-col cols="6">
                  <p class="text-caption text-medium-emphasis mb-1">Implementation Time</p>
                  <v-chip size="small" prepend-icon="mdi-clock-outline">
                    {{ recommendation.timeframe }}
                  </v-chip>
                </v-col>
              </v-row>
            </div>
          </v-card-text>

          <v-card-actions>
            <v-btn
              variant="text"
              color="success"
              prepend-icon="mdi-check"
              @click="markCompleted(recommendation.id)"
            >
              Mark Complete
            </v-btn>
            <v-btn
              variant="text"
              color="primary"
              prepend-icon="mdi-calendar"
              @click="scheduleAction(recommendation.id)"
            >
              Schedule
            </v-btn>
            <v-btn
              variant="text"
              prepend-icon="mdi-share"
              @click="shareRecommendation(recommendation.id)"
            >
              Share
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Empty State -->
    <v-row v-if="filteredRecommendations.length === 0">
      <v-col cols="12">
        <v-card class="elevation-2 text-center pa-8">
          <v-icon size="80" color="grey">mdi-lightbulb-outline</v-icon>
          <h3 class="text-h5 mt-4 mb-2">No Recommendations</h3>
          <p class="text-body-1 text-medium-emphasis">
            Click "Generate New" to get personalized recommendations
          </p>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Recommendations',

  data() {
    return {
      loading: false,
      selectedPriority: 'all',
      recommendations: [
        {
          id: 1,
          title: 'Increase Weekly Mileage Gradually',
          description: 'Based on your current performance data, gradually increasing your weekly running distance by 10% could improve endurance without risk of injury.',
          category: 'training',
          priority: 'high',
          confidence: 92,
          timeframe: '4-6 weeks',
          actions: [
            'Add 1-2 miles to your weekly long run',
            'Include one additional easy-pace run per week',
            'Monitor fatigue levels and adjust accordingly'
          ],
          expectedImpact: 'Expected 15% improvement in endurance metrics within 6 weeks'
        },
        {
          id: 2,
          title: 'Improve Recovery Time',
          description: 'Your heart rate recovery data suggests room for improvement. Better recovery practices could enhance overall performance.',
          category: 'recovery',
          priority: 'high',
          confidence: 88,
          timeframe: '2-3 weeks',
          actions: [
            'Include 7-8 hours of sleep per night',
            'Add active recovery days with light stretching',
            'Consider foam rolling or massage therapy'
          ],
          expectedImpact: 'Improved recovery rate by 20% and reduced injury risk'
        },
        {
          id: 3,
          title: 'Optimize Nutrition Timing',
          description: 'Your calorie burn patterns suggest that pre-workout nutrition could be optimized for better performance.',
          category: 'nutrition',
          priority: 'medium',
          confidence: 75,
          timeframe: '1-2 weeks',
          actions: [
            'Eat a light meal 2-3 hours before workouts',
            'Include complex carbohydrates for sustained energy',
            'Hydrate adequately before and during exercise'
          ],
          expectedImpact: 'Increased workout intensity and reduced mid-session fatigue'
        },
        {
          id: 4,
          title: 'Add Strength Training',
          description: 'Incorporating strength training could balance your fitness profile and reduce injury risk.',
          category: 'training',
          priority: 'medium',
          confidence: 82,
          timeframe: '6-8 weeks',
          actions: [
            'Add 2 strength sessions per week',
            'Focus on core and lower body exercises',
            'Start with bodyweight exercises before adding weights'
          ],
          expectedImpact: 'Enhanced overall strength and 10% reduction in injury risk'
        },
        {
          id: 5,
          title: 'Maintain Consistency',
          description: 'Your activity patterns show excellent consistency. Keep maintaining this schedule for continued progress.',
          category: 'general',
          priority: 'low',
          confidence: 95,
          timeframe: 'Ongoing',
          actions: [
            'Continue your current training schedule',
            'Track progress weekly',
            'Celebrate small wins to maintain motivation'
          ],
          expectedImpact: 'Sustained performance improvement and long-term habit formation'
        }
      ]
    }
  },

  computed: {
    filteredRecommendations() {
      if (this.selectedPriority === 'all') {
        return this.recommendations
      }
      return this.recommendations.filter(r => r.priority === this.selectedPriority)
    }
  },

  methods: {
    ...mapActions({
      showSuccess: 'notifications/showSuccess',
      showError: 'notifications/showError'
    }),

    async generateRecommendations() {
      this.loading = true
      try {
        // await authService.generateRecommendations(currentUser.id)
        await new Promise(resolve => setTimeout(resolve, 1500))
        this.showSuccess('New recommendations generated!')
      } catch (error) {
        this.showError('Failed to generate recommendations')
      } finally {
        this.loading = false
      }
    },

    markCompleted(id) {
      this.recommendations = this.recommendations.filter(r => r.id !== id)
      this.showSuccess('Recommendation marked as complete!')
    },

    scheduleAction(id) {
      this.showSuccess('Action scheduled successfully!')
    },

    shareRecommendation(id) {
      this.showSuccess('Recommendation shared!')
    },

    getPriorityColor(priority) {
      const colors = {
        high: 'error',
        medium: 'warning',
        low: 'success'
      }
      return colors[priority] || 'grey'
    },

    getCategoryColor(category) {
      const colors = {
        training: 'primary',
        recovery: 'success',
        nutrition: 'warning',
        general: 'info'
      }
      return colors[category] || 'grey'
    },

    getCategoryIcon(category) {
      const icons = {
        training: 'mdi-dumbbell',
        recovery: 'mdi-sleep',
        nutrition: 'mdi-food-apple',
        general: 'mdi-information'
      }
      return icons[category] || 'mdi-lightbulb'
    }
  }
}
</script>

<style scoped>
.border-l-error {
  border-left: 4px solid rgb(var(--v-theme-error));
}

.border-l-warning {
  border-left: 4px solid rgb(var(--v-theme-warning));
}

.border-l-success {
  border-left: 4px solid rgb(var(--v-theme-success));
}
</style>
