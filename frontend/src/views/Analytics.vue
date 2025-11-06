<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">
          <v-icon class="mr-2" size="large">mdi-chart-box</v-icon>
          Advanced Analytics
        </h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Deep dive into your performance metrics
        </p>
      </v-col>
    </v-row>

    <!-- Filters -->
    <v-card class="mb-4 elevation-2">
      <v-card-text>
        <v-row>
          <v-col cols="12" md="3">
            <v-select
              v-model="selectedMetric"
              :items="metrics"
              label="Metric"
              prepend-icon="mdi-chart-line"
              density="comfortable"
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="selectedPeriod"
              :items="periods"
              label="Time Period"
              prepend-icon="mdi-calendar"
              density="comfortable"
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="selectedComparison"
              :items="comparisons"
              label="Compare With"
              prepend-icon="mdi-compare"
              density="comfortable"
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-btn
              color="primary"
              block
              prepend-icon="mdi-refresh"
              @click="updateAnalytics"
            >
              Update
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Performance Comparison -->
    <v-row>
      <v-col cols="12">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-compare-arrows</v-icon>
            Performance Comparison
          </v-card-title>
          <v-card-text>
            <apexchart
              type="line"
              height="400"
              :options="comparisonChartOptions"
              :series="comparisonChartSeries"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Detailed Metrics -->
    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-chart-scatter-plot</v-icon>
            Correlation Analysis
          </v-card-title>
          <v-card-text>
            <apexchart
              type="heatmap"
              height="350"
              :options="heatmapOptions"
              :series="heatmapSeries"
            />
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-chart-box-outline</v-icon>
            Distribution Analysis
          </v-card-title>
          <v-card-text>
            <apexchart
              type="boxPlot"
              height="350"
              :options="boxPlotOptions"
              :series="boxPlotSeries"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Statistics Table -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-table</v-icon>
            Statistical Summary
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="statsHeaders"
              :items="statsData"
              class="elevation-0"
            >
              <template v-slot:item.trend="{ item }">
                <v-chip
                  :color="item.trend > 0 ? 'success' : 'error'"
                  size="small"
                >
                  <v-icon start size="small">
                    {{ item.trend > 0 ? 'mdi-trending-up' : 'mdi-trending-down' }}
                  </v-icon>
                  {{ item.trend }}%
                </v-chip>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Export Options -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-download</v-icon>
            Export Analytics
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-btn
                  color="primary"
                  block
                  prepend-icon="mdi-file-pdf"
                  @click="exportPDF"
                >
                  Export as PDF
                </v-btn>
              </v-col>
              <v-col cols="12" md="6">
                <v-btn
                  color="success"
                  block
                  prepend-icon="mdi-file-excel"
                  @click="exportExcel"
                >
                  Export as Excel
                </v-btn>
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
  name: 'Analytics',
  
  components: {
    apexchart: VueApexCharts
  },

  data() {
    return {
      selectedMetric: 'steps',
      selectedPeriod: '30days',
      selectedComparison: 'previous',
      metrics: [
        { title: 'Steps', value: 'steps' },
        { title: 'Calories', value: 'calories' },
        { title: 'Heart Rate', value: 'heartrate' },
        { title: 'Distance', value: 'distance' }
      ],
      periods: [
        { title: 'Last 7 Days', value: '7days' },
        { title: 'Last 30 Days', value: '30days' },
        { title: 'Last 90 Days', value: '90days' }
      ],
      comparisons: [
        { title: 'Previous Period', value: 'previous' },
        { title: 'Team Average', value: 'team' },
        { title: 'Personal Best', value: 'best' }
      ],
      comparisonChartOptions: {
        chart: {
          type: 'line',
          toolbar: { show: true }
        },
        colors: ['#1976D2', '#4CAF50'],
        stroke: { curve: 'smooth', width: 3 },
        xaxis: {
          categories: this.generateDates(30)
        },
        legend: {
          position: 'top'
        }
      },
      comparisonChartSeries: [
        {
          name: 'Current Period',
          data: this.generateRandomData(30, 6000, 12000)
        },
        {
          name: 'Previous Period',
          data: this.generateRandomData(30, 5000, 11000)
        }
      ],
      heatmapOptions: {
        chart: {
          type: 'heatmap'
        },
        plotOptions: {
          heatmap: {
            colorScale: {
              ranges: [
                { from: 0, to: 0.3, color: '#00A100', name: 'low' },
                { from: 0.3, to: 0.6, color: '#FEB019', name: 'medium' },
                { from: 0.6, to: 1, color: '#FF4560', name: 'high' }
              ]
            }
          }
        }
      },
      heatmapSeries: [
        { name: 'Steps', data: [{ x: 'Calories', y: 0.8 }, { x: 'Distance', y: 0.9 }, { x: 'Heart Rate', y: 0.4 }] },
        { name: 'Calories', data: [{ x: 'Steps', y: 0.8 }, { x: 'Distance', y: 0.7 }, { x: 'Heart Rate', y: 0.5 }] },
        { name: 'Distance', data: [{ x: 'Steps', y: 0.9 }, { x: 'Calories', y: 0.7 }, { x: 'Heart Rate', y: 0.3 }] }
      ],
      boxPlotOptions: {
        chart: {
          type: 'boxPlot'
        },
        colors: ['#1976D2']
      },
      boxPlotSeries: [
        {
          name: 'Performance',
          data: [
            { x: 'Week 1', y: [54, 66, 69, 75, 88] },
            { x: 'Week 2', y: [43, 65, 69, 76, 81] },
            { x: 'Week 3', y: [31, 39, 45, 51, 59] },
            { x: 'Week 4', y: [39, 46, 55, 65, 71] }
          ]
        }
      ],
      statsHeaders: [
        { title: 'Metric', key: 'metric' },
        { title: 'Average', key: 'average' },
        { title: 'Min', key: 'min' },
        { title: 'Max', key: 'max' },
        { title: 'Std Dev', key: 'stdDev' },
        { title: 'Trend', key: 'trend' }
      ],
      statsData: [
        { metric: 'Steps', average: '8,542', min: '3,245', max: '15,234', stdDev: '2,341', trend: 12.5 },
        { metric: 'Calories', average: '2,145', min: '1,234', max: '3,567', stdDev: '456', trend: 8.3 },
        { metric: 'Active Minutes', average: '58', min: '25', max: '120', stdDev: '18', trend: -3.2 },
        { metric: 'Heart Rate', average: '72', min: '58', max: '165', stdDev: '12', trend: 2.1 }
      ]
    }
  },

  methods: {
    ...mapActions({
      showSuccess: 'notifications/showSuccess',
      showError: 'notifications/showError'
    }),

    updateAnalytics() {
      this.showSuccess('Analytics updated!')
    },

    exportPDF() {
      this.showSuccess('Exporting to PDF...')
    },

    exportExcel() {
      this.showSuccess('Exporting to Excel...')
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
    }
  }
}
</script>
