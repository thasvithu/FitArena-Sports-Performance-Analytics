<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">
          <v-icon class="mr-2" size="large">mdi-upload</v-icon>
          Data Upload
        </h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Upload performance data for analysis
        </p>
      </v-col>
    </v-row>

    <!-- Upload Area -->
    <v-row>
      <v-col cols="12">
        <v-card class="elevation-2">
          <v-card-text>
            <v-file-input
              v-model="files"
              multiple
              chips
              show-size
              accept=".csv,.xlsx,.xls"
              label="Select Files"
              prepend-icon="mdi-paperclip"
              @update:model-value="onFilesSelected"
            >
              <template v-slot:selection="{ fileNames }">
                <template v-for="fileName in fileNames" :key="fileName">
                  <v-chip
                    size="small"
                    label
                    color="primary"
                    class="me-2"
                  >
                    {{ fileName }}
                  </v-chip>
                </template>
              </template>
            </v-file-input>

            <v-alert
              v-if="uploadError"
              type="error"
              variant="tonal"
              class="mt-3"
              closable
              @click:close="uploadError = ''"
            >
              {{ uploadError }}
            </v-alert>

            <v-alert
              v-if="uploadSuccess"
              type="success"
              variant="tonal"
              class="mt-3"
              closable
              @click:close="uploadSuccess = ''"
            >
              {{ uploadSuccess }}
            </v-alert>

            <div class="d-flex justify-end mt-4">
              <v-btn
                color="primary"
                prepend-icon="mdi-upload"
                :disabled="files.length === 0"
                :loading="uploading"
                @click="uploadFiles"
              >
                Upload Files
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Upload Instructions -->
    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-information</v-icon>
            Supported File Formats
          </v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item prepend-icon="mdi-file-delimited">
                <v-list-item-title>CSV Files (.csv)</v-list-item-title>
                <v-list-item-subtitle>Comma-separated values</v-list-item-subtitle>
              </v-list-item>
              <v-list-item prepend-icon="mdi-file-excel">
                <v-list-item-title>Excel Files (.xlsx, .xls)</v-list-item-title>
                <v-list-item-subtitle>Microsoft Excel spreadsheets</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-format-list-checks</v-icon>
            Data Requirements
          </v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item prepend-icon="mdi-check-circle">
                <v-list-item-title>Include date/time columns</v-list-item-title>
              </v-list-item>
              <v-list-item prepend-icon="mdi-check-circle">
                <v-list-item-title>Numeric values for metrics</v-list-item-title>
              </v-list-item>
              <v-list-item prepend-icon="mdi-check-circle">
                <v-list-item-title>User ID or identifier</v-list-item-title>
              </v-list-item>
              <v-list-item prepend-icon="mdi-check-circle">
                <v-list-item-title>Max file size: 10MB</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Upload History -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card class="elevation-2">
          <v-card-title>
            <v-icon class="mr-2">mdi-history</v-icon>
            Recent Uploads
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="uploadHeaders"
              :items="uploadHistory"
              class="elevation-0"
            >
              <template v-slot:item.status="{ item }">
                <v-chip
                  :color="getStatusColor(item.status)"
                  size="small"
                >
                  {{ item.status }}
                </v-chip>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon
                  size="small"
                  variant="text"
                  @click="viewUpload(item.id)"
                >
                  <v-icon>mdi-eye</v-icon>
                </v-btn>
                <v-btn
                  icon
                  size="small"
                  variant="text"
                  color="error"
                  @click="deleteUpload(item.id)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import authService from '@/services/authService'

export default {
  name: 'DataUpload',

  data() {
    return {
      files: [],
      uploading: false,
      uploadError: '',
      uploadSuccess: '',
      uploadHeaders: [
        { title: 'Filename', key: 'filename' },
        { title: 'Upload Date', key: 'uploadDate' },
        { title: 'Records', key: 'records' },
        { title: 'Status', key: 'status' },
        { title: 'Actions', key: 'actions', sortable: false }
      ],
      uploadHistory: [
        {
          id: 1,
          filename: 'daily_activity.csv',
          uploadDate: '2025-11-05',
          records: 1250,
          status: 'Completed'
        },
        {
          id: 2,
          filename: 'heart_rate_data.xlsx',
          uploadDate: '2025-11-04',
          records: 3420,
          status: 'Completed'
        },
        {
          id: 3,
          filename: 'workout_log.csv',
          uploadDate: '2025-11-03',
          records: 567,
          status: 'Processing'
        }
      ]
    }
  },

  methods: {
    ...mapActions({
      showSuccess: 'notifications/showSuccess',
      showError: 'notifications/showError'
    }),

    onFilesSelected() {
      this.uploadError = ''
      this.uploadSuccess = ''
    },

    async uploadFiles() {
      if (this.files.length === 0) return

      this.uploading = true
      this.uploadError = ''
      this.uploadSuccess = ''

      try {
        const formData = new FormData()
        this.files.forEach(file => {
          formData.append('files', file)
        })

        await authService.uploadData(formData)
        this.uploadSuccess = `Successfully uploaded ${this.files.length} file(s)!`
        this.showSuccess(this.uploadSuccess)
        this.files = []
        
        // Refresh upload history
        // await this.fetchUploadHistory()
      } catch (error) {
        this.uploadError = error.response?.data?.detail || 'Upload failed. Please try again.'
        this.showError(this.uploadError)
      } finally {
        this.uploading = false
      }
    },

    viewUpload(id) {
      this.showSuccess(`Viewing upload ${id}`)
    },

    deleteUpload(id) {
      if (confirm('Are you sure you want to delete this upload?')) {
        this.uploadHistory = this.uploadHistory.filter(u => u.id !== id)
        this.showSuccess('Upload deleted successfully!')
      }
    },

    getStatusColor(status) {
      const colors = {
        'Completed': 'success',
        'Processing': 'warning',
        'Failed': 'error'
      }
      return colors[status] || 'grey'
    }
  }
}
</script>
