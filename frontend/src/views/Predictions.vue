<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">
          <v-icon class="mr-2" size="large">mdi-crystal-ball</v-icon>
          Performance Predictions
        </h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          AI-powered forecasts of your future performance
        </p>
      </v-col>
    </v-row>

    <!-- Metric Selector -->
    <v-card class="mb-4 elevation-2">
      <v-card-text>
        <v-row>
          <v-col cols="12" md="4">
            <v-select
              v-model="selectedMetric"
              :items="metrics"
              label="Select Metric"
              prepend-icon="mdi-chart-timeline-variant"
              @update:model-value="generatePrediction"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="predictionDays"
              :items="[7, 14, 30, 60, 90]"
              label="Prediction Period (Days)"
              prepend-icon="mdi-calendar-range"
              @update:model-value="generatePrediction"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-btn
              color="primary"
              block
              prepend-icon="mdi-chart-line"
              @click="generatePrediction"
              :loading="loading"
            >
              Generate Prediction
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Prediction Chart -->
    <v-row>
      <v-col cols="12">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-chart-line-variant</v-icon>
            {{ selectedMetric }} Prediction
          </v-card-title>
          <v-card-subtitle>
            Historical data vs. predicted values for next {{ predictionDays }} days
          </v-card-subtitle>
          <v-card-text>
            <apexchart
              type="line"
              height="400"
              :options="predictionChartOptions"
              :series="predictionChartSeries"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Prediction Insights -->
    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-information</v-icon>
            Prediction Insights
          </v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="insight in insights"
                :key="insight.id"
                :prepend-icon="insight.icon"
              >
                <v-list-item-title>{{ insight.title }}</v-list-item-title>
                <v-list-item-subtitle>{{ insight.description }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-target</v-icon>
            Predicted Goals
          </v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="goal in predictedGoals"
                :key="goal.id"
              >
                <template v-slot:prepend>
                  <v-avatar :color="goal.color">
                    <v-icon color="white">{{ goal.icon }}</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title class="font-weight-bold">
                  {{ goal.title }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  Target: {{ goal.target }} by {{ goal.date }}
                </v-list-item-subtitle>
                <template v-slot:append>
                  <v-chip :color="goal.probability > 70 ? 'success' : 'warning'" size="small">
                    {{ goal.probability }}% likely
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Model Confidence -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-gauge</v-icon>
            Model Confidence & Accuracy
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="4">
                <div class="text-center">
                  <h4 class="text-subtitle-1 mb-2">Prediction Confidence</h4>
                  <v-progress-circular
                    :model-value="modelConfidence"
                    :size="120"
                    :width="15"
                    color="primary"
                  >
                    <span class="text-h5 font-weight-bold">{{ modelConfidence }}%</span>
                  </v-progress-circular>
                </div>
              </v-col>
              <v-col cols="12" md="4">
                <div class="text-center">
                  <h4 class="text-subtitle-1 mb-2">Historical Accuracy</h4>
                  <v-progress-circular
                    :model-value="historicalAccuracy"
                    :size="120"
                    :width="15"
                    color="success"
                  >
                    <span class="text-h5 font-weight-bold">{{ historicalAccuracy }}%</span>
                  </v-progress-circular>
                </div>
              </v-col>
              <v-col cols="12" md="4">
                <div class="text-center">
                  <h4 class="text-subtitle-1 mb-2">Data Quality Score</h4>
                  <v-progress-circular
                    :model-value="dataQuality"
                    :size="120"
                    :width="15"
                    color="warning"
                  >
                    <span class="text-h5 font-weight-bold">{{ dataQuality }}%</span>
                  </v-progress-circular>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import VueApexCharts from 'vue3-apexcharts'

export default {
  name: 'Predictions',

  components: {
    apexchart: VueApexCharts
  },

  data() {
    return {
      loading: false,
      selectedMetric: 'Steps',
      predictionDays: 30,
      metrics: ['Steps', 'Calories', 'Heart Rate', 'Distance', 'Active Minutes'],
      modelConfidence: 87,
      historicalAccuracy: 92,
      dataQuality: 95,
      predictionChartOptions: {
        chart: {
          type: 'line',
          toolbar: { show: true }
        },
        colors: ['#1976D2', '#4CAF50', '#FF9800'],
        stroke: {
          curve: 'smooth',
          width: [3, 3, 0],
          dashArray: [0, 5, 0]
        },
        fill: {
          type: ['solid', 'solid', 'gradient'],
          gradient: {
            shade: 'light',
            type: 'vertical',
            opacityFrom: 0.4,
            opacityTo: 0.1
          }
        },
        xaxis: {
          categories: this.generateDates(60)
        },
        yaxis: {
          title: { text: 'Value' }
        },
        legend: {
          position: 'top'
        },
        annotations: {
          xaxis: [{
            x: 30,
            strokeDashArray: 0,
            borderColor: '#775DD0',
            label: {
              text: 'Today',
              style: {
                color: '#fff',
                background: '#775DD0'
              }
            }
          }]
        }
      },
      predictionChartSeries: [
        {
          name: 'Historical',
          data: this.generateHistoricalData(30),
          type: 'line'
        },
        {
          name: 'Predicted',
          data: [...Array(30).fill(null), ...this.generatePredictedData(30)],
          type: 'line'
        },
        {
          name: 'Confidence Interval',
          data: [...Array(30).fill(null), ...this.generateConfidenceData(30)],
          type: 'area'
        }
      ],
      insights: [
        {
          id: 1,
          icon: 'mdi-trending-up',
          title: 'Upward Trend Detected',
          description: 'Your performance shows a positive trajectory over the next month'
        },
        {
          id: 2,
          icon: 'mdi-alert-circle',
          title: 'Potential Plateau',
          description: 'Model predicts a plateau around day 45. Consider varying your routine'
        },
        {
          id: 3,
          icon: 'mdi-calendar-check',
          title: 'Optimal Training Days',
          description: 'Best results predicted on Mon, Wed, Fri based on patterns'
        }
      ],
      predictedGoals: [
        {
          id: 1,
          title: '10,000 Daily Steps',
          target: '10,000 steps/day',
          date: 'Dec 15, 2025',
          probability: 85,
          icon: 'mdi-walk',
          color: 'primary'
        },
        {
          id: 2,
          title: '5K Run Time',
          target: 'Sub-25 minutes',
          date: 'Jan 10, 2026',
          probability: 72,
          icon: 'mdi-run',
          color: 'success'
        },
        {
          id: 3,
          title: 'Weight Loss',
          target: 'Lose 10 lbs',
          date: 'Feb 1, 2026',
          probability: 68,
          icon: 'mdi-scale',
          color: 'warning'
        }
      ]
    }
  },

  methods: {
    ...mapActions({
      showSuccess: 'notifications/showSuccess',
      showError: 'notifications/showError'
    }),

    async generatePrediction() {
      this.loading = true
      try {
        // await authService.getPredictions(userId, this.selectedMetric, { days: this.predictionDays })
        await new Promise(resolve => setTimeout(resolve, 1500))
        this.showSuccess('Prediction generated successfully!')
      } catch (error) {
        this.showError('Failed to generate prediction')
      } finally {
        this.loading = false
      }
    },

    generateDates(days) {
      const dates = []
      for (let i = -30; i < days; i++) {
        const date = new Date()
        date.setDate(date.getDate() + i)
        dates.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }))
      }
      return dates
    },

    generateHistoricalData(days) {
      return Array.from({ length: days }, () => 
        Math.floor(Math.random() * 5000) + 6000
      )
    },

    generatePredictedData(days) {
      const data = []
      let base = 8000
      for (let i = 0; i < days; i++) {
        base += Math.random() * 200 - 50
        data.push(Math.floor(base))
      }
      return data
    },

    generateConfidenceData(days) {
      return Array.from({ length: days }, (_, i) => 
        Math.floor(8000 + Math.random() * 1000)
      )
    }
  }
}
</script>
