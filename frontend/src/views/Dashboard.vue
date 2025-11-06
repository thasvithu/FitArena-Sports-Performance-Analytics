<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">
          <v-icon class="mr-2" size="large">mdi-view-dashboard</v-icon>
          Performance Dashboard
        </h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Welcome back, {{ currentUser?.username }}!
        </p>
      </v-col>
      <v-col cols="auto">
        <v-btn
          color="primary"
          prepend-icon="mdi-refresh"
          @click="refreshData"
          :loading="loading"
        >
          Refresh
        </v-btn>
      </v-col>
    </v-row>

    <!-- Date Range Selector -->
    <v-row class="mb-4">
      <v-col cols="12" md="3">
        <v-select
          v-model="dateRange"
          :items="dateRangeOptions"
          label="Time Period"
          prepend-icon="mdi-calendar"
          density="comfortable"
          @update:model-value="fetchAnalytics"
        />
      </v-col>
    </v-row>

    <!-- KPI Cards -->
    <v-row>
      <v-col v-for="kpi in kpiCards" :key="kpi.title" cols="12" sm="6" md="3">
        <v-card class="elevation-2">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <p class="text-subtitle-2 text-medium-emphasis mb-1">
                  {{ kpi.title }}
                </p>
                <h2 class="text-h4 font-weight-bold">
                  {{ kpi.value }}
                </h2>
                <v-chip
                  :color="kpi.trend > 0 ? 'success' : 'error'"
                  size="small"
                  class="mt-2"
                >
                  <v-icon start size="small">
                    {{ kpi.trend > 0 ? 'mdi-arrow-up' : 'mdi-arrow-down' }}
                  </v-icon>
                  {{ Math.abs(kpi.trend) }}%
                </v-chip>
              </div>
              <v-avatar :color="kpi.color" size="56">
                <v-icon size="32" color="white">{{ kpi.icon }}</v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Charts Row 1 -->
    <v-row class="mt-4">
      <v-col cols="12" md="8">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-chart-line</v-icon>
            Activity Trends (Last 30 Days)
          </v-card-title>
          <v-card-text>
            <apexchart
              type="line"
              height="350"
              :options="activityChartOptions"
              :series="activityChartSeries"
            />
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-chart-donut</v-icon>
            Activity Distribution
          </v-card-title>
          <v-card-text>
            <apexchart
              type="donut"
              height="350"
              :options="donutChartOptions"
              :series="donutChartSeries"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Charts Row 2 -->
    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-heart-pulse</v-icon>
            Weekly Performance Score
          </v-card-title>
          <v-card-text>
            <apexchart
              type="bar"
              height="300"
              :options="weeklyChartOptions"
              :series="weeklyChartSeries"
            />
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-fire</v-icon>
            Calories Burned
          </v-card-title>
          <v-card-text>
            <apexchart
              type="area"
              height="300"
              :options="caloriesChartOptions"
              :series="caloriesChartSeries"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Recent Activity -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-history</v-icon>
            Recent Activity
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="activityHeaders"
              :items="recentActivities"
              :items-per-page="5"
              class="elevation-0"
            >
              <template v-slot:item.intensity="{ item }">
                <v-chip :color="getIntensityColor(item.intensity)" size="small">
                  {{ item.intensity }}
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
import { mapGetters, mapActions } from 'vuex'
import VueApexCharts from 'vue3-apexcharts'

export default {
  name: 'Dashboard',
  
  components: {
    apexchart: VueApexCharts
  },

  data() {
    return {
      loading: false,
      dateRange: '30days',
      dateRangeOptions: [
        { title: 'Last 7 Days', value: '7days' },
        { title: 'Last 30 Days', value: '30days' },
        { title: 'Last 90 Days', value: '90days' },
        { title: 'This Year', value: 'year' }
      ],
      kpiCards: [
        {
          title: 'Total Steps',
          value: '142,584',
          trend: 12.5,
          icon: 'mdi-walk',
          color: 'primary'
        },
        {
          title: 'Calories Burned',
          value: '24,512',
          trend: 8.2,
          icon: 'mdi-fire',
          color: 'error'
        },
        {
          title: 'Active Minutes',
          value: '1,847',
          trend: -3.1,
          icon: 'mdi-timer',
          color: 'success'
        },
        {
          title: 'Performance Score',
          value: '87',
          trend: 5.4,
          icon: 'mdi-chart-line',
          color: 'warning'
        }
      ],
      activityChartOptions: {
        chart: {
          type: 'line',
          toolbar: { show: false }
        },
        colors: ['#1976D2', '#4CAF50', '#FFC107'],
        stroke: { curve: 'smooth', width: 2 },
        xaxis: {
          categories: this.generateDates(30)
        },
        yaxis: {
          title: { text: 'Count' }
        },
        legend: {
          position: 'top'
        }
      },
      activityChartSeries: [
        {
          name: 'Steps',
          data: this.generateRandomData(30, 5000, 15000)
        },
        {
          name: 'Calories',
          data: this.generateRandomData(30, 500, 1500)
        },
        {
          name: 'Active Minutes',
          data: this.generateRandomData(30, 30, 120)
        }
      ],
      donutChartOptions: {
        chart: {
          type: 'donut'
        },
        labels: ['Cardio', 'Strength', 'Flexibility', 'Rest'],
        colors: ['#1976D2', '#4CAF50', '#FFC107', '#9E9E9E'],
        legend: {
          position: 'bottom'
        }
      },
      donutChartSeries: [35, 28, 20, 17],
      weeklyChartOptions: {
        chart: {
          type: 'bar',
          toolbar: { show: false }
        },
        colors: ['#1976D2'],
        plotOptions: {
          bar: {
            borderRadius: 4,
            dataLabels: { position: 'top' }
          }
        },
        xaxis: {
          categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yaxis: {
          title: { text: 'Performance Score' },
          max: 100
        }
      },
      weeklyChartSeries: [
        {
          name: 'Score',
          data: [78, 85, 82, 90, 88, 75, 80]
        }
      ],
      caloriesChartOptions: {
        chart: {
          type: 'area',
          toolbar: { show: false }
        },
        colors: ['#FF5252'],
        fill: {
          type: 'gradient',
          gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.7,
            opacityTo: 0.3
          }
        },
        xaxis: {
          categories: this.generateDates(14)
        },
        yaxis: {
          title: { text: 'Calories' }
        }
      },
      caloriesChartSeries: [
        {
          name: 'Calories',
          data: this.generateRandomData(14, 1200, 2500)
        }
      ],
      activityHeaders: [
        { title: 'Date', key: 'date' },
        { title: 'Activity', key: 'activity' },
        { title: 'Duration', key: 'duration' },
        { title: 'Intensity', key: 'intensity' },
        { title: 'Performance', key: 'performance' }
      ],
      recentActivities: [
        {
          date: '2025-11-06',
          activity: 'Morning Run',
          duration: '45 min',
          intensity: 'High',
          performance: 92
        },
        {
          date: '2025-11-05',
          activity: 'Strength Training',
          duration: '60 min',
          intensity: 'Medium',
          performance: 85
        },
        {
          date: '2025-11-04',
          activity: 'Cycling',
          duration: '30 min',
          intensity: 'Medium',
          performance: 78
        },
        {
          date: '2025-11-03',
          activity: 'Yoga',
          duration: '40 min',
          intensity: 'Low',
          performance: 88
        },
        {
          date: '2025-11-02',
          activity: 'HIIT Workout',
          duration: '25 min',
          intensity: 'High',
          performance: 95
        }
      ]
    }
  },

  computed: {
    ...mapGetters({
      currentUser: 'auth/currentUser'
    })
  },

  mounted() {
    this.fetchAnalytics()
  },

  methods: {
    ...mapActions({
      showSuccess: 'notifications/showSuccess',
      showError: 'notifications/showError'
    }),

    async fetchAnalytics() {
      this.loading = true
      try {
        // In real implementation, fetch from API
        // const data = await authService.getAnalyticsSummary(this.currentUser.id, {
        //   period: this.dateRange
        // })
        await new Promise(resolve => setTimeout(resolve, 1000))
        this.showSuccess('Dashboard updated successfully!')
      } catch (error) {
        this.showError('Failed to load analytics')
      } finally {
        this.loading = false
      }
    },

    refreshData() {
      this.fetchAnalytics()
    },

    generateDates(days) {
      const dates = []
      for (let i = days - 1; i >= 0; i--) {
        const date = new Date()
        date.setDate(date.getDate() - i)
        dates.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }))
      }
      return dates
    },

    generateRandomData(count, min, max) {
      return Array.from({ length: count }, () => 
        Math.floor(Math.random() * (max - min + 1)) + min
      )
    },

    getIntensityColor(intensity) {
      const colors = {
        'High': 'error',
        'Medium': 'warning',
        'Low': 'success'
      }
      return colors[intensity] || 'grey'
    },

    getPerformanceColor(performance) {
      if (performance >= 90) return 'success'
      if (performance >= 75) return 'primary'
      if (performance >= 60) return 'warning'
      return 'error'
    }
  }
}
</script>

<style scoped>
.v-card {
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-2px);
}
</style>
