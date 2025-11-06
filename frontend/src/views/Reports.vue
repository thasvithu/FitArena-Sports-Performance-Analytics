<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">
          <v-icon class="mr-2" size="large">mdi-file-document</v-icon>
          Reports
        </h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Generate and download performance reports
        </p>
      </v-col>
      <v-col cols="auto">
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="showGenerateDialog = true"
        >
          Generate Report
        </v-btn>
      </v-col>
    </v-row>

    <!-- Reports List -->
    <v-row>
      <v-col cols="12">
        <v-card class="elevation-2">
          <v-card-text>
            <v-data-table
              :headers="reportHeaders"
              :items="reports"
              class="elevation-0"
            >
              <template v-slot:item.type="{ item }">
                <v-chip :color="getTypeColor(item.type)" size="small">
                  {{ item.type }}
                </v-chip>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon
                  size="small"
                  variant="text"
                  color="primary"
                  @click="downloadReport(item.id)"
                >
                  <v-icon>mdi-download</v-icon>
                </v-btn>
                <v-btn
                  icon
                  size="small"
                  variant="text"
                  @click="viewReport(item.id)"
                >
                  <v-icon>mdi-eye</v-icon>
                </v-btn>
                <v-btn
                  icon
                  size="small"
                  variant="text"
                  color="error"
                  @click="deleteReport(item.id)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Generate Report Dialog -->
    <v-dialog v-model="showGenerateDialog" max-width="600">
      <v-card>
        <v-card-title>
          <v-icon class="mr-2">mdi-file-document-plus</v-icon>
          Generate New Report
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="reportForm.title"
              label="Report Title"
              :rules="[rules.required]"
              prepend-icon="mdi-text"
              required
            />

            <v-select
              v-model="reportForm.type"
              :items="reportTypes"
              label="Report Type"
              prepend-icon="mdi-file-chart"
              :rules="[rules.required]"
              required
            />

            <v-select
              v-model="reportForm.period"
              :items="periods"
              label="Time Period"
              prepend-icon="mdi-calendar"
              :rules="[rules.required]"
              required
            />

            <v-select
              v-model="reportForm.format"
              :items="formats"
              label="Export Format"
              prepend-icon="mdi-file-export"
              :rules="[rules.required]"
              required
            />

            <v-checkbox
              v-model="reportForm.includeCharts"
              label="Include Charts and Visualizations"
            />

            <v-checkbox
              v-model="reportForm.includeRecommendations"
              label="Include AI Recommendations"
            />
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="closeDialog">Cancel</v-btn>
          <v-btn
            color="primary"
            :disabled="!valid"
            :loading="generating"
            @click="generateReport"
          >
            Generate
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Reports',

  data() {
    return {
      showGenerateDialog: false,
      generating: false,
      valid: false,
      reportForm: {
        title: '',
        type: 'Performance Summary',
        period: 'Last 30 Days',
        format: 'PDF',
        includeCharts: true,
        includeRecommendations: true
      },
      reportTypes: [
        'Performance Summary',
        'Progress Report',
        'Team Analytics',
        'Training Analysis',
        'Health Metrics'
      ],
      periods: [
        'Last 7 Days',
        'Last 30 Days',
        'Last 90 Days',
        'This Year',
        'Custom Range'
      ],
      formats: ['PDF', 'Excel', 'CSV'],
      reportHeaders: [
        { title: 'Title', key: 'title' },
        { title: 'Type', key: 'type' },
        { title: 'Generated', key: 'generated' },
        { title: 'Period', key: 'period' },
        { title: 'Format', key: 'format' },
        { title: 'Actions', key: 'actions', sortable: false }
      ],
      reports: [
        {
          id: 1,
          title: 'October Performance Summary',
          type: 'Performance Summary',
          generated: '2025-11-01',
          period: 'October 2025',
          format: 'PDF'
        },
        {
          id: 2,
          title: 'Q3 Progress Report',
          type: 'Progress Report',
          generated: '2025-10-01',
          period: 'Q3 2025',
          format: 'Excel'
        },
        {
          id: 3,
          title: 'Team Analytics - Elite Runners',
          type: 'Team Analytics',
          generated: '2025-10-15',
          period: 'Last 90 Days',
          format: 'PDF'
        }
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

    async generateReport() {
      if (!this.$refs.form.validate()) return

      this.generating = true

      try {
        // await authService.generateReport(this.reportForm)
        await new Promise(resolve => setTimeout(resolve, 2000))
        this.showSuccess('Report generated successfully!')
        this.closeDialog()
      } catch (error) {
        this.showError('Failed to generate report')
      } finally {
        this.generating = false
      }
    },

    downloadReport(id) {
      this.showSuccess(`Downloading report ${id}...`)
    },

    viewReport(id) {
      this.showSuccess(`Viewing report ${id}`)
    },

    deleteReport(id) {
      if (confirm('Are you sure you want to delete this report?')) {
        this.reports = this.reports.filter(r => r.id !== id)
        this.showSuccess('Report deleted successfully!')
      }
    },

    closeDialog() {
      this.showGenerateDialog = false
      this.reportForm = {
        title: '',
        type: 'Performance Summary',
        period: 'Last 30 Days',
        format: 'PDF',
        includeCharts: true,
        includeRecommendations: true
      }
      this.$refs.form?.reset()
    },

    getTypeColor(type) {
      const colors = {
        'Performance Summary': 'primary',
        'Progress Report': 'success',
        'Team Analytics': 'warning',
        'Training Analysis': 'info',
        'Health Metrics': 'error'
      }
      return colors[type] || 'grey'
    }
  }
}
</script>
